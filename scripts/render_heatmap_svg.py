"""Render data/contributions.json into an animated terminal-style SVG heatmap."""
import json

COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL, GAP, PAD_X, PAD_TOP = 11, 3, 20, 62
STEP = CELL + GAP

data = json.load(open("data/contributions.json"))
weeks = data["weeks"]
days = [d for w in weeks for d in w]
best = cur = 0
for d in days:
    cur = cur + 1 if d["count"] else 0
    best = max(best, cur)
streak = 0
for d in reversed(days):
    if d["count"]:
        streak += 1
    elif d is not days[-1]:
        break
busiest = max(days, key=lambda d: d["count"])
active = sum(1 for d in days if d["count"])
width = PAD_X * 2 + len(weeks) * STEP
height = PAD_TOP + 7 * STEP + 40

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    "<style>",
    "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}",
    ".c{opacity:0;animation:in .4s ease forwards}",
    "@keyframes in{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}",
    ".c{transform-box:fill-box;transform-origin:center}",
    ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}",
    "</style>",
    f'<rect width="{width}" height="{height}" rx="10" fill="#0d1117" stroke="#30363d"/>',
    f'<text x="{PAD_X}" y="30" font-size="14" fill="#7ee787">{data["user"]}@github</text>',
    f'<text x="{PAD_X + 118}" y="30" font-size="14" fill="#8b949e">~ $ ./contributions.sh</text>',
    f'<text x="{PAD_X}" y="50" font-size="12" fill="#8b949e">{data["total"]} contributions in the last year</text>',
    f'<text x="{width - PAD_X}" y="50" font-size="12" fill="#8b949e" text-anchor="end">'
    f'<tspan fill="#ff7b5c">{streak}d streak</tspan> · longest {best}d · {active} active days</text>',
]
for x, week in enumerate(weeks):
    for y, day in enumerate(week):
        delay = round(x * 0.03 + y * 0.01, 2)
        p.append(
            f'<rect class="c" x="{PAD_X + x * STEP}" y="{PAD_TOP + y * STEP}" width="{CELL}" height="{CELL}" '
            f'rx="2" fill="{COLORS[day["level"]]}" style="animation-delay:{delay}s">'
            f'<title>{day["date"]}: {day["count"]}</title></rect>'
        )
ly = PAD_TOP + 7 * STEP + 22
p.append(f'<text x="{PAD_X}" y="{ly}" font-size="11" fill="#8b949e">Less</text>')
for i, c in enumerate(COLORS):
    p.append(f'<rect x="{PAD_X + 34 + i * STEP}" y="{ly - 10}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
p.append(f'<text x="{PAD_X + 40 + 5 * STEP}" y="{ly}" font-size="11" fill="#8b949e">More</text>')
p.append(f'<rect class="cur" x="{width - PAD_X - 9}" y="{ly - 11}" width="9" height="14" fill="#7ee787"/>')
p.append("</svg>")
open("contrib-heatmap.svg", "w", encoding="utf-8").write("\n".join(p))
