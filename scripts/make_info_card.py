"""Generate info-card.svg: neofetch-style card, colored ASCII portrait on the left, plain key/value lines on the right."""
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
from make_ascii_svg import ascii_group  # noqa: E402

USER = "gabsh"
W = 900
RX = 380  # right column x
LINE = 24

# ("name", text) big line | ("sub", text) | ("text", text) paragraph line | ("kv", key, value) | ("link", text) | None = gap
INFO = [
    ("name", "Gabin Hemmerle"),
    ("sub", "Full-Stack Developer · Master MIAGE"),
    None,
    ("text", "Backend, data, machine learning and DevOps."),
    ("text", "I learn new languages and frameworks by building"),
    ("text", "projects with them."),
    ("text", "I run my own VPS with a k3s cluster and deploy"),
    ("text", "and maintain my apps on it."),
    None,
    ("text", "Java, Python, Go, Spring Boot, Kubernetes, PyTorch..."),
    None,
    ("link", "mlens.fr · fsight.fr"),
    ("link", "linkedin.com/in/gabin-hemmerle"),
]

ascii_svg, aw, ah = ascii_group(x0=30, y0=64, delay=0.1)

rows = []
y = 84
i = 0
for item in INFO:
    if item is None:
        y += 12
        continue
    kind = item[0]
    d = f"animation-delay:{0.3 + i * 0.1:.2f}s"
    if kind == "name":
        rows.append(f'<text class="l" style="{d}" x="{RX}" y="{y}" fill="#ff7b5c" font-size="26" font-weight="700">{escape(item[1])}</text>')
        y += 8
    elif kind == "sub":
        rows.append(f'<text class="l" style="{d}" x="{RX}" y="{y + 14}" fill="#e6edf3">{escape(item[1])}</text>')
        y += 14
    elif kind == "text":
        rows.append(f'<text class="l" style="{d}" x="{RX}" y="{y + 12}" fill="#9da7b3">{escape(item[1])}</text>')
        y += 22
    elif kind == "kv":
        rows.append(
            f'<g class="l" style="{d}"><text x="{RX}" y="{y + 12}" fill="#ff7b5c">{item[1]}</text>'
            f'<text x="{RX + 70}" y="{y + 12}" fill="#c9d1d9">{escape(item[2])}</text></g>'
        )
        y += 22
    else:
        rows.append(f'<text class="l" style="{d}" x="{RX}" y="{y + 12}" fill="#58a6ff">{escape(item[1])}</text>')
        y += 22
    i += 1
y += 10

# classic terminal color blocks
y += 8
pal = ["#484f58", "#ff5f56", "#27c93f", "#ffbd2e", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]
rows.append("".join(f'<rect x="{RX + n * 22}" y="{y}" width="22" height="14" fill="{c}"/>' for n, c in enumerate(pal)))
y += 14

H = int(max(y + 40, ah + 64 + 50))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="art"><rect x="24" y="40" width="{RX - 24 - 16}" height="{H - 40}"/></clipPath></defs>
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace;font-size:14px}}
.l{{opacity:0;animation:fade .4s ease forwards}}
.row{{opacity:0;animation:fade .4s ease forwards}}
@keyframes fade{{to{{opacity:1}}}}
.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>
<rect width="{W}" height="32" rx="8" fill="#161b22"/><rect y="24" width="{W}" height="8" fill="#161b22"/>
<line x1="0" y1="32" x2="{W}" y2="32" stroke="#30363d"/>
<circle cx="18" cy="16" r="5" fill="#ff5f56"/><circle cx="36" cy="16" r="5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5" fill="#27c93f"/>
<text x="{W // 2}" y="20" font-size="12" fill="#8b949e" text-anchor="middle">{USER}@github: ~</text>
<g clip-path="url(#art)">{ascii_svg}</g>
{"".join(rows)}
<text x="30" y="{H - 16}" fill="#7ee787">$</text><rect class="cur" x="44" y="{H - 28}" width="8" height="15" fill="#c9d1d9"/>
</svg>'''
open("info-card.svg", "w", encoding="utf-8").write(svg)
print(f"info-card.svg {W}x{H}")
