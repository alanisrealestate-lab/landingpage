"""Build the Go High Level copies of each page into ghl/.

GHL only receives the code you paste, not this repo's images/ folder or other files, so the
GHL copies load photos from GHL Media and link between pages using GHL funnel-step paths.
Run after editing index.html, privacy.html or terms.html:  python3 build_ghl.py
"""
import os, re

MEDIA = "https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/njoCXV0Cts3zCT2uviub/media/"
IMAGES = {
    "images/adrian.webp": MEDIA + "69270a02580f40b6a370ca9d.png",
    "images/family.webp": MEDIA + "692711900863c387eb461dfb.jpg",
}
# Paths of the GHL funnel steps (set these in GHL to match, or change them here)
LINKS = {
    "homeUrl": "/",
    "privacyPolicyUrl": "/privacy-policy",
    "termsUrl": "/terms-of-use",
}
NOTE = "<!-- GHL VERSION, built by build_ghl.py. Paste this file into GHL; edit the repo version, not this one. -->\n"

os.makedirs("ghl", exist_ok=True)
for name in ("index.html", "privacy.html", "terms.html"):
    s = open(name).read()
    for local, url in IMAGES.items():
        s = s.replace(f'src="{local}"', f'src="{url}"')
    for key, url in LINKS.items():
        s = re.sub(rf'(\n\s*{key}:\s*)"[^"]*"', rf'\1"{url}"', s)
    s = s.replace("<!doctype html>\n", "<!doctype html>\n" + NOTE, 1)
    open(os.path.join("ghl", name), "w").write(s)
    print("built ghl/" + name)
