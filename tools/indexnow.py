"""Tell IndexNow which pages changed — run AFTER the deploy is live.

IndexNow is a ping, not a crawl queue: the search engine fetches the URL
shortly after being told. Announcing a page before GitHub Pages has published
it gets the OLD content indexed, so the order matters:

    bake -> commit -> push -> wait for the deploy -> this.

    python tools/indexnow.py            # every URL in sitemap.xml
    python tools/indexnow.py <url> ...  # only these

The key lives in the repository root as <key>.txt and is served at
https://sacrvm.dev/<key>.txt. That file is the proof of ownership and its
name IS the key, so there is no second copy to keep in sync. Deleting or
renaming it revokes the permission.

Stdlib only, like the site itself.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sacrvm.dev"
HOST = "sacrvm.dev"
ENDPOINT = "https://api.indexnow.org/indexnow"  # shared by every participant

STATUS = {
    200: "accepted",
    202: "accepted, key validation pending",
    400: "bad request",
    403: "key not valid for this host",
    422: "a URL does not belong to the host",
    429: "too many requests",
}


def find_key() -> str:
    """The key file is its own index: name without suffix == content."""
    for f in ROOT.glob("*.txt"):
        body = f.read_text(encoding="utf-8").strip()
        if f.stem == body and re.fullmatch(r"[0-9a-zA-Z-]{8,128}", body):
            return body
    raise SystemExit("no IndexNow key file in the repository root")


def live(url: str) -> bool:
    req = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "sacrvm.dev indexnow"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except urllib.error.URLError:
        return False


key = find_key()
urls = sys.argv[1:] or re.findall(
    r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8")
)

# One foreign or undeployed URL makes the whole batch worthless, so filter
# before submitting rather than explaining a 422 afterwards.
ready, skipped = [], []
for u in urls:
    (ready if u.startswith(SITE) and live(u) else skipped).append(u)

for u in skipped:
    print(f"  skipped (not live yet): {u}")
if not ready:
    raise SystemExit("nothing to submit")

payload = json.dumps(
    {
        "host": HOST,
        "key": key,
        "keyLocation": f"{SITE}/{key}.txt",
        "urlList": ready,
    }
).encode()

req = urllib.request.Request(
    ENDPOINT,
    data=payload,
    method="POST",
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        code, body = r.status, r.read().decode(errors="replace")
except urllib.error.HTTPError as e:
    code, body = e.code, e.read().decode(errors="replace")

for u in ready:
    print(f"  submitted: {u}")
print(f"{len(ready)} URL(s) -> HTTP {code} ({STATUS.get(code, 'unexpected')})")
if body.strip():
    print(body.strip()[:400])
