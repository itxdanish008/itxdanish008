#!/usr/bin/env python3
"""Generates the self-hosted SVG assets for the profile README."""

import pathlib
import random
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)

SANS = "Segoe UI,Ubuntu,Helvetica Neue,Arial,sans-serif"
MONO = "SFMono-Regular,Consolas,Liberation Mono,monospace"

# palette per folio design language
DARK = dict(
    bg="#0A0A0F", panel="#111119", border="#1E1E2A",
    text="#F4F4F5", muted="#A1A1AA", dim="#52525B",
)
LIGHT = dict(
    bg="#FFFFFF", panel="#F6F6F9", border="#E4E4E9",
    text="#0A0A0F", muted="#52525B", dim="#A1A1AA",
)
FROM, TO, AMBER = "#6D5CFF", "#9B6DFF", "#FFB86C"


def defs(t: dict, glow: bool = True) -> str:
    g = f"""
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{TO}" stop-opacity="{0.30 if t is DARK else 0.16}"/>
    <stop offset="100%" stop-color="{TO}" stop-opacity="0"/>
  </radialGradient>""" if glow else ""
    return f"""<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{FROM}"/><stop offset="100%" stop-color="{TO}"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{FROM}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{TO}" stop-opacity="1"/>
    <stop offset="100%" stop-color="{FROM}" stop-opacity="0"/>
  </linearGradient>{g}
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.1" fill="{t['border']}"/>
  </pattern>
</defs>"""


# ---------------------------------------------------------------- hero banner

def hero(t: dict, name: str) -> None:
    W, H = 1000, 250
    random.seed(7)
    # decorative node-network on the right
    nodes = [(760 + random.randint(0, 200), 40 + random.randint(0, 170)) for _ in range(14)]
    edges = []
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes[i + 1:], i + 1):
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 5200:
                edges.append((x1, y1, x2, y2))

    net = "".join(
        f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{FROM}" stroke-opacity="0.28" stroke-width="1"/>'
        for a, b, c, d in edges
    )
    net += "".join(
        f'<circle cx="{x}" cy="{y}" r="{2.6 + (i % 3)}" fill="url(#accent)" opacity="0.85">'
        f'<animate attributeName="opacity" values="0.85;0.25;0.85" dur="{2.6 + (i % 5) * 0.45:.1f}s"'
        f' repeatCount="indefinite" begin="{i * 0.21:.2f}s"/></circle>'
        for i, (x, y) in enumerate(nodes)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(name)}, Sr. AI Engineer, Full-Stack">
{defs(t)}
  <rect width="{W}" height="{H}" rx="18" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#dots)" opacity="0.55"/>
  <ellipse cx="880" cy="70" rx="300" ry="190" fill="url(#glow)"/>
  <g clip-path="inset(0 round 18)">{net}</g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t['border']}"/>

  <rect x="54" y="46" width="3" height="34" rx="1.5" fill="url(#accent)"/>
  <text x="72" y="73" font-family="{SANS}" font-size="40" font-weight="700"
        fill="{t['text']}" letter-spacing="0.5">{escape(name)}</text>

  <text x="73" y="104" font-family="{MONO}" font-size="15.5" font-weight="600" fill="url(#accent)"
        letter-spacing="1.6">SR. AI ENGINEER · FULL-STACK</text>

  <text x="73" y="140" font-family="{SANS}" font-size="16" fill="{t['muted']}">I ship privacy-first AI systems and the full-stack</text>
  <text x="73" y="163" font-family="{SANS}" font-size="16" fill="{t['muted']}">products around them.</text>

  <rect x="73" y="186" width="150" height="26" rx="13" fill="{FROM}" fill-opacity="0.12" stroke="{FROM}" stroke-opacity="0.45"/>
  <circle cx="88" cy="199" r="3.5" fill="{AMBER}">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="98" y="203" font-family="{MONO}" font-size="11" fill="{t['muted']}" letter-spacing="0.4">OPEN TO WORK</text>

  <text x="240" y="203" font-family="{MONO}" font-size="11.5" fill="{t['muted']}" letter-spacing="0.4">REMOTE · LAHORE, PK   ·   4+ YRS AI/ML   ·   8+ YRS ENG</text>

  <g clip-path="inset(0 round 18)">
    <rect x="-320" y="{H - 3}" width="320" height="3" fill="url(#sweep)">
      <animate attributeName="x" values="-320;{W};-320" dur="9s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>"""
    suffix = "dark" if t is DARK else "light"
    (OUT / f"hero-{suffix}.svg").write_text(svg)


# ------------------------------------------------------------------ stat band

STATS = [
    ("4+", "YEARS IN AI/ML"),
    ("8+", "YEARS ENGINEERING"),
    ("20+", "PRODUCTION SYSTEMS"),
    ("85%", "EXCEPTION HANDLING CUT"),
    ("75%", "CLIENT IT COST CUT"),
]


def stats(t: dict) -> None:
    W, H, gap = 1000, 108, 12
    cw = (W - gap * (len(STATS) - 1)) / len(STATS)
    cards = []
    for i, (value, label) in enumerate(STATS):
        x = i * (cw + gap)
        cards.append(f"""  <g>
    <rect x="{x:.1f}" y="0" width="{cw:.1f}" height="{H}" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
    <rect x="{x + 16:.1f}" y="22" width="26" height="2.5" rx="1.25" fill="url(#accent)"/>
    <text x="{x + 16:.1f}" y="66" font-family="{SANS}" font-size="34" font-weight="700" fill="url(#accent)">{value}</text>
    <text x="{x + 16:.1f}" y="88" font-family="{MONO}" font-size="9.5" fill="{t['muted']}" letter-spacing="0.8">{label}</text>
  </g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{'; '.join(f'{v} {l.lower()}' for v, l in STATS)}">
{defs(t, glow=False)}
{chr(10).join(cards)}
</svg>"""
    (OUT / f"stats-{'dark' if t is DARK else 'light'}.svg").write_text(svg)


# -------------------------------------------------------------- skills matrix
# maturity mirrors content/site.ts: core=3, proficient=2, working=1

SKILLS = {
    "AI & ML": [
        ("PyTorch", 3), ("Hugging Face", 3), ("OpenCV", 3), ("TensorFlow", 2),
        ("PEFT / LoRA", 2), ("YOLO", 2), ("ONNX / TensorRT", 1), ("Coqui / Kokoro TTS", 1),
    ],
    "LLM / Agents": [
        ("RAG Pipelines", 3), ("LangChain / LangGraph", 3), ("MCP", 3), ("Hermes Agents", 3),
        ("CrewAI", 2), ("LlamaIndex", 2), ("OpenRouter", 2),
    ],
    "Backend / UI": [
        ("Python", 3), ("FastAPI", 3), ("Next.js", 3), ("React.js", 3),
        ("Django", 2), ("TypeScript", 2),
    ],
    "Data & Vector": [
        ("Postgres", 3), ("Pinecone / ChromaDB", 2), ("Redis", 2),
    ],
    "MLOps": [
        ("Docker", 3), ("GitHub Actions", 2), ("MLflow", 2),
        ("Weights & Biases", 2), ("Airflow / Prefect", 2), ("DVC / BentoML / Ray", 1),
    ],
    "AWS & Cloud": [
        ("Lambda", 3), ("EC2", 3), ("S3 / CloudWatch", 2), ("SageMaker", 2),
        ("Bedrock", 2), ("ECS / EKS", 2), ("CodePipeline", 2), ("Hostinger VPS", 2),
        ("Kubernetes", 1),
    ],
    "Automation": [
        ("n8n", 2), ("Zapier", 2), ("Make.com", 2),
    ],
}

EXPLORING = ["Agentic RAG"]
COLUMNS = [
    ["AI & ML", "Automation"],
    ["LLM / Agents", "Data & Vector"],
    ["AWS & Cloud", "Exploring"],
    ["MLOps", "Backend / UI"],
]

ROW_H, HEAD_H, LEGEND_H = 25, 34, 30


def _col_height(col: list[str]) -> int:
    total = 0
    for cat in col:
        n = len(EXPLORING) if cat == "Exploring" else len(SKILLS[cat])
        total += HEAD_H + n * ROW_H + 6
    return total


def _meter(x: float, y: float, level: int, t: dict) -> str:
    return "".join(
        f'<rect x="{x + s * 20:.1f}" y="{y:.1f}" width="16" height="6" rx="3" '
        f'fill="{"url(#accent)" if s < level else t["border"]}"/>'
        for s in range(3)
    )


def skills_matrix(t: dict) -> None:
    W, pad, col_gap = 1000, 20, 12
    n = len(COLUMNS)
    cw = (W - pad * 2 - col_gap * (n - 1)) / n
    panel_h = max(_col_height(c) for c in COLUMNS) + 14
    H = panel_h + pad * 2 + LEGEND_H

    parts = []
    for ci, col in enumerate(COLUMNS):
        x = pad + ci * (cw + col_gap)
        y = pad
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{panel_h}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        y += 6
        for cat in col:
            label = "CURRENTLY EXPLORING" if cat == "Exploring" else cat.upper()
            parts.append(
                f'<text x="{x + 16:.1f}" y="{y + 22}" font-family="{MONO}" font-size="10.5" '
                f'font-weight="700" fill="url(#accent)" letter-spacing="1.2">{escape(label)}</text>'
            )
            y += HEAD_H
            if cat == "Exploring":
                for item in EXPLORING:
                    parts.append(
                        f'<circle cx="{x + 20:.1f}" cy="{y + 10}" r="3" fill="{AMBER}"/>'
                        f'<text x="{x + 32:.1f}" y="{y + 15}" font-family="{SANS}" font-size="12" '
                        f'fill="{t["muted"]}">{escape(item)}</text>'
                    )
                    y += ROW_H
            else:
                for skill, level in SKILLS[cat]:
                    parts.append(
                        f'<text x="{x + 16:.1f}" y="{y + 15}" font-family="{SANS}" font-size="12" '
                        f'fill="{t["text"]}">{escape(skill)}</text>'
                    )
                    parts.append(_meter(x + cw - 16 - 56, y + 5, level, t))
                    y += ROW_H
            y += 6

    # legend uses real meter swatches rather than block glyphs
    ly = H - 14
    legend = [f'<text x="{pad + 4}" y="{ly}" font-family="{MONO}" font-size="9.5" fill="{t["muted"]}" letter-spacing="0.8">MATURITY</text>']
    lx = pad + 78
    for level, name in ((3, "CORE"), (2, "PROFICIENT"), (1, "WORKING")):
        legend.append(_meter(lx, ly - 9, level, t))
        legend.append(f'<text x="{lx + 64}" y="{ly}" font-family="{MONO}" font-size="9.5" fill="{t["muted"]}" letter-spacing="0.8">{name}</text>')
        lx += 64 + len(name) * 6.6 + 26

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Skill matrix by maturity: core, proficient, working">
{defs(t, glow=False)}
{chr(10).join('  ' + p for p in parts)}
{chr(10).join('  ' + p for p in legend)}
</svg>"""
    (OUT / f"skills-{'dark' if t is DARK else 'light'}.svg").write_text(svg)


for theme in (DARK, LIGHT):
    hero(theme, "M. Danish Bashir")
    stats(theme)
    skills_matrix(theme)

for f in sorted(OUT.iterdir()):
    print(f"{f.name:22} {f.stat().st_size:>7,} bytes")
