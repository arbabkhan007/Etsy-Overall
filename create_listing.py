"""
create_listing.py — Create a digital Etsy listing from the command line.

Setup (one time):
  1. Create an Etsy app at https://www.etsy.com/developers/register
       - Set "Redirect URIs" to: http://localhost:3003/callback
  2. Create etsy_config.json in this folder:
       {"client_id": "your_keystring_here"}
  3. python create_listing.py --auth

Usage:
  python create_listing.py --spec listing.json [--draft]

  python create_listing.py \\
      --title "8-Week Trail Running Plan | Printable PDF" \\
      --description "A week-by-week..." \\
      --tags "trail running,training plan,running printable,beginner running" \\
      --price 12.99 \\
      --file product.pdf \\
      --image cover.jpg \\
      --draft

listing.json format:
  {
    "title":       "...",         # max 140 chars
    "description": "...",
    "tags":        ["tag1", ...], # up to 13, max 20 chars each
    "price":       12.99,
    "file":        "product.pdf",
    "image":       "cover.jpg",   # optional
    "taxonomy_id": 68887608       # optional (default = Printables)
  }
"""

import argparse
import base64
import hashlib
import http.server
import json
import secrets
import sys
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────

DIR         = Path(__file__).parent
CONFIG_FILE = DIR / "etsy_config.json"
TOKENS_FILE = DIR / "etsy_tokens.json"

# ── Etsy constants ────────────────────────────────────────────────────────────

AUTH_URL     = "https://www.etsy.com/oauth/connect"
TOKEN_URL    = "https://api.etsy.com/v3/public/oauth/token"
API_BASE     = "https://openapi.etsy.com/v3"
REDIRECT_URI = "http://localhost:3003/callback"
SCOPES       = "listings_w listings_r shops_r"

# Etsy taxonomy ID for "Craft Supplies > Patterns & Tutorials > Printables"
DEFAULT_TAXONOMY = 68887608


# ── Config / token helpers ────────────────────────────────────────────────────

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        print(f"ERROR: {CONFIG_FILE} not found.")
        print('Create it with: {"client_id": "your_etsy_keystring"}')
        sys.exit(1)
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def load_tokens() -> dict:
    if not TOKENS_FILE.exists():
        print("Not authenticated. Run:  python create_listing.py --auth")
        sys.exit(1)
    return json.loads(TOKENS_FILE.read_text(encoding="utf-8"))


def save_tokens(data: dict):
    TOKENS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_valid_token() -> str:
    """Return a valid Bearer token, refreshing silently if expired."""
    cfg    = load_config()
    tokens = load_tokens()

    if time.time() >= tokens.get("expires_at", 0) - 60:
        print("  Refreshing access token...")
        r = requests.post(TOKEN_URL, data={
            "grant_type":    "refresh_token",
            "client_id":     cfg["client_id"],
            "refresh_token": tokens["refresh_token"],
        })
        r.raise_for_status()
        d = r.json()
        tokens["access_token"]  = d["access_token"]
        tokens["refresh_token"] = d.get("refresh_token", tokens["refresh_token"])
        tokens["expires_at"]    = time.time() + d.get("expires_in", 3600)
        save_tokens(tokens)

    return tokens["access_token"]


def auth_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "x-api-key":     load_config()["client_id"],
    }


# ── OAuth PKCE flow ───────────────────────────────────────────────────────────

def _pkce_pair() -> tuple[str, str]:
    # code_verifier: 43-128 chars from unreserved alphabet (RFC 7636)
    verifier  = secrets.token_urlsafe(64)   # ~86 chars, all URL-safe
    digest    = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def run_auth():
    cfg       = load_config()
    verifier, challenge = _pkce_pair()
    state     = secrets.token_urlsafe(16)

    params = urllib.parse.urlencode({
        "response_type":         "code",
        "client_id":             cfg["client_id"],
        "redirect_uri":          REDIRECT_URI,
        "scope":                 SCOPES,
        "code_challenge":        challenge,
        "code_challenge_method": "S256",
        "state":                 state,
    })
    auth_url = f"{AUTH_URL}?{params}"

    # Tiny local server to catch the redirect
    received: dict = {}

    class _Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            received["code"]  = qs.get("code",  [""])[0]
            received["state"] = qs.get("state", [""])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Authorized! You can close this tab.</h2>")
        def log_message(self, *_): pass  # silence access log

    server = http.server.HTTPServer(("localhost", 3003), _Handler)
    t = threading.Thread(target=server.handle_request, daemon=True)
    t.start()

    print("Opening Etsy authorization page in your browser...")
    webbrowser.open(auth_url)
    t.join(timeout=120)
    server.server_close()

    if not received.get("code"):
        print("ERROR: No authorization code received (timed out or cancelled).")
        sys.exit(1)
    if received.get("state") != state:
        print("ERROR: OAuth state mismatch.")
        sys.exit(1)

    # Exchange code + verifier for tokens
    r = requests.post(TOKEN_URL, data={
        "grant_type":    "authorization_code",
        "client_id":     cfg["client_id"],
        "redirect_uri":  REDIRECT_URI,
        "code":          received["code"],
        "code_verifier": verifier,
    })
    if not r.ok:
        print(f"ERROR {r.status_code}: {r.text}")
        sys.exit(1)

    d = r.json()
    save_tokens({
        "access_token":  d["access_token"],
        "refresh_token": d["refresh_token"],
        "expires_at":    time.time() + d.get("expires_in", 3600),
    })
    print(f"✓ Authenticated. Tokens saved to {TOKENS_FILE.name}")

    # Auto-detect and save shop_id
    token    = d["access_token"]
    shop_id  = _detect_shop_id(token)
    if shop_id:
        cfg["shop_id"] = shop_id
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        print(f"✓ Shop ID {shop_id} saved to {CONFIG_FILE.name}")


def _detect_shop_id(token: str) -> str | None:
    """Try to find the authenticated user's shop ID."""
    headers = {"Authorization": f"Bearer {token}", "x-api-key": load_config()["client_id"]}
    try:
        r = requests.get(f"{API_BASE}/application/users/me", headers=headers)
        r.raise_for_status()
        user_id = r.json().get("user_id")
        if user_id:
            r2 = requests.get(f"{API_BASE}/application/users/{user_id}/shops", headers=headers)
            r2.raise_for_status()
            shops = r2.json().get("results", [])
            if shops:
                return str(shops[0]["shop_id"])
    except Exception as e:
        print(f"  ⚠ Could not auto-detect shop_id ({e}). Add it to {CONFIG_FILE.name} manually.")
    return None


# ── Listing helpers ───────────────────────────────────────────────────────────

def get_shop_id(token: str) -> str:
    cfg = load_config()
    if "shop_id" in cfg:
        return str(cfg["shop_id"])
    shop_id = _detect_shop_id(token)
    if not shop_id:
        print(f'ERROR: Could not detect shop_id. Add it to {CONFIG_FILE.name}: {{"shop_id": 12345678}}')
        sys.exit(1)
    cfg["shop_id"] = shop_id
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return shop_id


def create_listing(token: str, shop_id: str, spec: dict, draft: bool) -> str:
    tags = [t[:20] for t in spec.get("tags", [])][:13]
    payload = {
        "quantity":    999,
        "title":       spec["title"][:140],
        "description": spec["description"],
        "price":       float(spec["price"]),
        "who_made":    "i_did",
        "when_made":   "2020_2025",
        "taxonomy_id": int(spec.get("taxonomy_id", DEFAULT_TAXONOMY)),
        "type":        "download",
        "is_digital":  True,
        "tags":        tags,
        "state":       "draft" if draft else "active",
    }
    r = requests.post(
        f"{API_BASE}/application/shops/{shop_id}/listings",
        headers={**auth_headers(token), "Content-Type": "application/json"},
        json=payload,
    )
    if not r.ok:
        print(f"ERROR {r.status_code} creating listing:\n{r.text}")
        sys.exit(1)
    listing_id = str(r.json()["listing_id"])
    print(f"  ✓ Listing created  → {listing_id}")
    return listing_id


def upload_file(token: str, shop_id: str, listing_id: str, path: Path):
    with path.open("rb") as fh:
        r = requests.post(
            f"{API_BASE}/application/shops/{shop_id}/listings/{listing_id}/files",
            headers=auth_headers(token),
            data={"name": path.name, "rank": 1},
            files={"file": (path.name, fh, "application/octet-stream")},
        )
    if not r.ok:
        print(f"ERROR {r.status_code} uploading file:\n{r.text}")
        sys.exit(1)
    print(f"  ✓ File uploaded    → {path.name}")


def upload_image(token: str, shop_id: str, listing_id: str, path: Path):
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    with path.open("rb") as fh:
        r = requests.post(
            f"{API_BASE}/application/shops/{shop_id}/listings/{listing_id}/images",
            headers=auth_headers(token),
            data={"rank": 1, "overwrite": "true"},
            files={"image": (path.name, fh, mime)},
        )
    if not r.ok:
        print(f"ERROR {r.status_code} uploading image:\n{r.text}")
        sys.exit(1)
    print(f"  ✓ Image uploaded   → {path.name}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_spec_from_args(args) -> dict:
    missing = [f for f, v in [("--title", args.title), ("--price", args.price), ("--file", args.file)] if not v]
    if missing:
        print(f"ERROR: {', '.join(missing)} required when not using --spec")
        sys.exit(1)
    return {
        "title":       args.title,
        "description": args.description or args.title,
        "tags":        [t.strip() for t in (args.tags or "").split(",") if t.strip()],
        "price":       float(args.price),
        "file":        args.file,
        "image":       args.image,
        "taxonomy_id": args.taxonomy_id or DEFAULT_TAXONOMY,
    }


def main():
    p = argparse.ArgumentParser(description="Create a digital Etsy listing.")
    p.add_argument("--auth",        action="store_true",  help="Run OAuth setup")
    p.add_argument("--spec",                              help="JSON spec file")
    p.add_argument("--title",                             help="Listing title (max 140 chars)")
    p.add_argument("--description",                       help="Listing description")
    p.add_argument("--tags",                              help="Comma-separated tags (max 13)")
    p.add_argument("--price",                             help="Price in USD")
    p.add_argument("--file",                              help="Digital file to deliver (PDF, ZIP…)")
    p.add_argument("--image",                             help="Cover image (JPG or PNG, optional)")
    p.add_argument("--taxonomy-id", type=int,             help=f"Taxonomy ID (default: {DEFAULT_TAXONOMY})")
    p.add_argument("--draft",       action="store_true",  help="Save as draft (don't publish)")
    args = p.parse_args()

    if args.auth:
        run_auth()
        return

    token    = get_valid_token()
    shop_id  = get_shop_id(token)
    print(f"Shop ID: {shop_id}")

    # Resolve spec
    if args.spec:
        spec_path = Path(args.spec)
        spec      = json.loads(spec_path.read_text(encoding="utf-8"))
        base_dir  = spec_path.parent
    else:
        spec     = build_spec_from_args(args)
        base_dir = Path.cwd()

    file_path  = base_dir / spec["file"]
    image_path = (base_dir / spec["image"]) if spec.get("image") else None

    if not file_path.exists():
        print(f"ERROR: file not found: {file_path}")
        sys.exit(1)

    print(f"\nCreating: {spec['title'][:70]}...")
    listing_id = create_listing(token, shop_id, spec, draft=args.draft)

    print("Uploading digital file...")
    upload_file(token, shop_id, listing_id, file_path)

    if image_path:
        if image_path.exists():
            print("Uploading cover image...")
            upload_image(token, shop_id, listing_id, image_path)
        else:
            print(f"  ⚠ Image not found ({image_path.name}) — skipping")

    state = "draft" if args.draft else "active"
    print(f"\n✓ Done — listing {listing_id} is {state}")
    print(f"  https://www.etsy.com/your/listings/{listing_id}/edit")


if __name__ == "__main__":
    main()
