"""
GitHub Actions-d zoriulsan huvilbar.
Neg ajillagaa ~5 cag 50 minut turshid minut tutam shalgana.
URL, TOPIC-iig GitHub Secrets-ees avna (kod dotor bichihgui).
"""

import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta

URL = os.environ["URL"]
TOPIC = os.environ["TOPIC"]
COUNTRY = "Mongolia"

RUN_SECONDS = 21000   # ~5 cag 50 minut
INTERVAL = 60         # minut tutam
RENOTIFY_SECONDS = 300  # Tuluv oorchlogdson uyd 5 minut tutam davtaj mendchilne


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


def log(msg):
    now = datetime.now(timezone(timedelta(hours=8)))  # Ulaanbaatar tsag
    print(f"[{now:%H:%M:%S} UB] {msg}", flush=True)


def main():
    end = time.time() + RUN_SECONDS
    ok_reads = 0
    last_notify = 0
    while True:
        try:
            text = fetch_text(URL)
            i = text.find(COUNTRY)
            if i == -1:
                log("Mongolia mor oldsongui. Huudas JavaScript-eer achaalldag baij magadgui.")
            else:
                ok_reads += 1
                snippet = text[i + len(COUNTRY): i + len(COUNTRY) + 12].upper()
                log("Snippet: " + snippet)
                if "PAUSED" not in snippet:
                    log("TULUV OORCHLOGDLOO!")
                    if time.time() - last_notify > RENOTIFY_SECONDS:
                        notify("Mongolia-iin tuluv oorchlogdloo! Odoo huudsaa shalga: " + URL)
                        last_notify = time.time()
        except Exception as e:
            log(f"Aldaa: {e}")

        if time.time() + INTERVAL > end:
            break
        time.sleep(INTERVAL)

    if ok_reads == 0:
        log("Neg ch udaa amjilttai unshigdsangui.")
        sys.exit(1)  # Ajillagaa fail bolj, GitHub email yavuulna
    log("Ajillagaa duuslaa.")


if __name__ == "__main__":
    main()
