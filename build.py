"""Build index.html, a standalone slide viewer, from the files in deck/.

Run: python3 build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DECK = ROOT / "deck"

ARROW = (
    '<svg width="56" height="24" viewBox="0 0 56 24" style="align-self:center;flex:none" '
    'aria-hidden="true"><path d="M2 12 H46" stroke="{c}" stroke-width="4" fill="none"/>'
    '<path d="M42 4 L54 12 L42 20 Z" fill="{c}"/></svg>'
)


def convert(html: str) -> str:
    # x-connector is a Slides-only element: swap it for a plain SVG arrow.
    def connector(m):
        color = re.search(r"color:(#[0-9A-Fa-f]{6})", m.group(0))
        return ARROW.format(c=color.group(1) if color else "#1F6F66")

    html = re.sub(r"<x-connector[^>]*></x-connector>", connector, html)
    # x-icon is Slides-only too, and decorative here, so drop it.
    html = re.sub(r"<x-icon[^>]*></x-icon>", "", html)
    html = html.replace('style="margin-top:20px"', "")
    return html


def main():
    meta = json.loads((DECK / "deck.json").read_text())
    css = (DECK / "deck.css").read_text()
    fonts = "\n".join(
        f'<link rel="stylesheet" href="{f["href"]}">' for f in meta["faces"].values()
    )
    slides = "\n".join(
        convert((DECK / "slides" / f"{sid}.html").read_text()).replace(
            '<p class="pnum"></p>', f'<p class="pnum">{n}</p>'
        )
        for n, sid in enumerate(meta["order"], start=1)
    )
    page = TEMPLATE.replace("{{title}}", meta["title"])
    page = page.replace("{{fonts}}", fonts).replace("{{css}}", css)
    page = page.replace("{{slides}}", slides)
    (ROOT / "index.html").write_text(page)
    print(f"Built index.html with {len(meta['order'])} slides")


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
{{fonts}}
<style>
{{css}}
html, body { margin: 0; height: 100%; background: #111316; overflow: hidden; }
#stage { position: absolute; left: 50%; top: 50%; width: 1920px; height: 1080px;
  transform-origin: center center; }
#stage > section { position: absolute; inset: 0; width: 1920px; height: 1080px; display: none; }
#stage > section.on { display: flex; }
section h1, section h2, section h3, section p { margin-top: 0; }
section ul { margin-top: 0; }
section a { color: inherit; }
section table { border-collapse: collapse; }
section th { text-align: left; font-weight: 700; border-bottom: 2px solid #1E2226; padding: 14px 20px; }
section td { border-bottom: 1px solid #D9D5CB; padding: 14px 20px; vertical-align: top; }
section aside { display: none; }
.pnum::after { content: none; }
#notes { position: fixed; left: 0; right: 0; bottom: 0; max-height: 30vh; overflow: auto;
  background: #23272C; color: #EDEBE5; font: 16px/1.5 Inter, Arial, sans-serif;
  padding: 16px 24px; display: none; }
#notes.on { display: block; }
#hint { position: fixed; right: 12px; bottom: 8px; color: #8A9099;
  font: 12px Inter, Arial, sans-serif; }
</style>
</head>
<body>
<div id="stage">
{{slides}}
</div>
<div id="notes"></div>
<div id="hint">Arrows or click to move, N for notes, F for fullscreen</div>
<script>
const slides = [...document.querySelectorAll('#stage > section')];
const stage = document.getElementById('stage');
const notes = document.getElementById('notes');
let i = Math.max(0, Math.min(slides.length - 1, (parseInt(location.hash.slice(1)) || 1) - 1));

function fit() {
  const s = Math.min(innerWidth / 1920, innerHeight / 1080);
  stage.style.transform = `translate(-50%, -50%) scale(${s})`;
}
function show(n) {
  i = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((el, k) => el.classList.toggle('on', k === i));
  const aside = slides[i].querySelector('aside');
  notes.textContent = aside ? aside.textContent : '';
  history.replaceState(null, '', '#' + (i + 1));
}
addEventListener('resize', fit);
addEventListener('keydown', e => {
  if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) show(i + 1);
  else if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) show(i - 1);
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(slides.length - 1);
  else if (e.key === 'n' || e.key === 'N') notes.classList.toggle('on');
  else if (e.key === 'f' || e.key === 'F') document.documentElement.requestFullscreen?.();
});
stage.addEventListener('click', e => {
  if (e.target.closest('a')) return;
  show(e.clientX > innerWidth / 2 ? i + 1 : i - 1);
});
fit();
show(i);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
