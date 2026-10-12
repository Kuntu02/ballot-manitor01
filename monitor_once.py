"""
GitHub Actions-d zoriulsan huvilbar: neg udaa shalgaad duusna.
URL, TOPIC-iig GitHub Secrets-ees avna (kod dotor bichihgui).
"""

import os
import re
import sys
import urllib.request

URL = os.environ["URL"]
TOPIC = os.environ["TOPIC"]
COUNTRY = "Greece"


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="ignore")
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text)


def notify(message):
    req = urllib.request.Request(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8"),
        headers={"Title": "Visa 462 ballot", "Priority": "urgent", "Tags": "rotating_light"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=30)


def main():
    text = fetch_text(URL)
    i = text.find(COUNTRY)
    if i == -1:
        print("Mongolia mor oldsongui. Huudas JavaScript-eer achaalldag baij magadgui.")
        sys.exit(1)  # Ajillagaa fail bolj, GitHub email yavuulna
    snippet = text[i + len(COUNTRY): i + len(COUNTRY) + 12].upper()
    print("Snippet:", snippet)
    if "PAUSED" in snippet:
        print("Odoogoor PAUSED.")
    else:
        print("TULUV OORCHLOGDLOO!")
        notify("Mongolia-iin tuluv oorchlogdloo! Odoo huudsaa shalga: " + URL)


if __name__ == "__main__":
    main()
