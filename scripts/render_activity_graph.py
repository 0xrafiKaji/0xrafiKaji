#!/usr/bin/env python3
"""Render a contribution activity graph SVG (tokyo-night style) from the GitHub GraphQL API.

Self-hosted replacement for the github-readme-activity-graph service, which is no
longer reliably hosted. Uses only the Python standard library plus the `gh` CLI
(authenticated via GH_TOKEN on Actions runners, or the local gh auth here).

Output: assets/activity-graph.svg
"""

import datetime as dt
import json
import pathlib
import subprocess
import sys

USERNAME = "0xrafiKaji"
DAYS = 90
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "activity-graph.svg"

# tokyo-night-ish palette (matches the profile's cyan accent)
BG = "#1a1b26"
BORDER = "#24283b"
GRID = "#24283b"
TITLE = "#c0caf5"
MUTED = "#565f89"
ACCENT = "#22d3ee"
AREA = "#22d3ee"

W, H = 860, 230
ML, MR = 46, 24          # left/right margins for the plot area
TOP, BOTTOM = 62, 186    # vertical bounds of the plot area

QUERY = """
query($u:String!,$f:DateTime!,$t:DateTime!){
  user(login:$u){
    contributionsCollection(from:$f,to:$t){
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount } }
      }
    }
  }
}
"""


def fetch_days() -> tuple[list[tuple[str, int]], int]:
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = today - dt.timedelta(days=DAYS - 1)
    result = subprocess.run(
        [
            "gh", "api", "graphql",
            "-f", "query=" + QUERY,
            "-f", "u=" + USERNAME,
            "-F", "f=" + frm.isoformat() + "T00:00:00Z",
            "-F", "t=" + today.isoformat() + "T23:59:59Z",
        ],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    seen: dict[str, int] = {}
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            if frm.isoformat() <= day["date"] <= today.isoformat():
                seen[day["date"]] = day["contributionCount"]
    days = [(frm + dt.timedelta(days=i)).isoformat() for i in range(DAYS)]
    return [(d, seen.get(d, 0)) for d in days], cal["totalContributions"]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(days: list[tuple[str, int]], total: int, generated: str) -> str:
    counts = [c for _, c in days]
    peak = max(counts) or 1

    plot_w = W - ML - MR
    plot_h = BOTTOM - TOP
    step = plot_w / (len(days) - 1)

    def x(i: int) -> float:
        return ML + i * step

    def y(c: int) -> float:
        return BOTTOM - (c / peak) * plot_h

    # stepped line + filled area
    line = [f"M {x(0):.1f} {y(counts[0]):.1f}"]
    for i in range(1, len(days)):
        line.append(f"H {x(i):.1f}")
        line.append(f"V {y(counts[i]):.1f}")
    line.append(f"H {x(len(days) - 1) + step:.1f}")
    line_path = " ".join(line)

    area_path = (
        f"M {x(0):.1f} {y(counts[0]):.1f} "
        + " ".join(
            f"H {x(i):.1f} V {y(counts[i]):.1f}" for i in range(1, len(days))
        )
        + f" H {W - MR} V {BOTTOM} H {ML} Z"
    )

    # grid + y labels
    grid = []
    for frac, label in ((1.0, str(peak)), (0.5, f"{peak / 2:.0f}"), (0.0, "0")):
        gy = BOTTOM - frac * plot_h
        grid.append(f'<line x1="{ML}" y1="{gy:.1f}" x2="{W - MR}" y2="{gy:.1f}" stroke="{GRID}" stroke-width="1"/>')
        grid.append(
            f'<text x="{ML - 8}" y="{gy + 3.5:.1f}" text-anchor="end" font-size="10" fill="{MUTED}">{label}</text>'
        )

    # x labels roughly every 15 days
    labels = []
    for i in range(0, len(days), 15):
        d = dt.date.fromisoformat(days[i][0])
        labels.append(
            f'<text x="{x(i):.1f}" y="{BOTTOM + 16}" text-anchor="middle" font-size="10" fill="{MUTED}">{d.strftime("%b %d")}</text>'
        )

    # dots on active days
    dots = []
    for i, c in enumerate(counts):
        if c > 0:
            dots.append(f'<circle cx="{x(i):.1f}" cy="{y(c):.1f}" r="2" fill="{ACCENT}"/>')

    title = f"{USERNAME}'s contribution activity"
    subtitle = f"Last {DAYS} days &#183; {total} contributions &#183; updated {generated}"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">',
        '<rect width="100%" height="100%" fill="none"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>',
        f'<text x="24" y="30" font-family="Segoe UI, Ubuntu, Sans-serif" font-size="15" font-weight="600" fill="{TITLE}">{esc(title)}</text>',
        f'<text x="24" y="47" font-family="Segoe UI, Ubuntu, Sans-serif" font-size="11" fill="{MUTED}">{subtitle}</text>',
        *grid,
        f'<path d="{area_path}" fill="{AREA}" opacity="0.16"/>',
        f'<path d="{line_path}" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linejoin="round"/>',
        *dots,
        *labels,
        '</svg>',
    ]
    return "\n".join(parts)


def main() -> None:
    days, total = fetch_days()
    generated = dt.datetime.now(dt.timezone.utc).strftime("%b %d, %Y")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(days, total, generated), encoding="utf-8")
    print(f"wrote {OUT} ({total} contributions over {len(days)} days)")


if __name__ == "__main__":
    sys.exit(main())
