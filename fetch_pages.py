"""Save each homepage's visible text, verbatim, for flawline xray to check quotes against."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

STRIP_JS = """() => {
  document.querySelectorAll('nav, footer, script, style, noscript, [role=navigation], [aria-hidden=true]')
    .forEach(el => el.remove());
  return document.body ? document.body.innerText : '';
}"""

out = Path("pages"); out.mkdir(exist_ok=True)
sample = json.load(open("sample.json", encoding="utf-8"))
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page(viewport={"width": 1366, "height": 900})
    for co in sample:
        try:
            page.goto(co["website"], wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(1500)
            text = page.evaluate(STRIP_JS)
        except Exception as exc:
            print("FAIL", co["slug"], str(exc)[:80]); continue
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        (out / f'{co["slug"]}.md').write_text("\n".join(lines), encoding="utf-8")
        print(co["slug"], len(lines), "lines", sum(len(l.split()) for l in lines), "words")
    browser.close()
