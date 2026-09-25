"""
Redraw the report's charts as clean, colour-blind-safe figures.
All values come from the report (data/*.csv); nothing is estimated.
Run from this folder:  python make_figures.py   -> writes PNGs to ../images/
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
DATA, OUT = HERE / "data", HERE.parent / "images"
OI = {"orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73", "blue": "#0072B2",
      "vermillion": "#D55E00", "purple": "#CC79A7", "yellow": "#F0E442"}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 200,
    "savefig.bbox": "tight", "figure.facecolor": "white",
})
NOTE = "Redrawn from the report's chart data (C. G. Shuvo)."


def importance():
    d = pd.read_csv(DATA / "relative_importance.csv", comment="#").sort_values("RF")
    cat_col = {"Topographic": OI["vermillion"], "Meteorological": OI["sky"],
               "Socio-economic": OI["purple"], "Land use & geology": OI["green"]}
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    y = range(len(d))
    for yy, (_, r) in zip(y, d.iterrows()):
        ax.plot([r.ANN, r.RF], [yy, yy], color="#c8c8c8", lw=2, zorder=1)
    ax.scatter(d.ANN, y, marker="o", facecolor="white", edgecolor="#333", s=38, zorder=2, label="ANN")
    ax.scatter(d.RF, y, marker="D", color="#333", s=34, zorder=3, label="Random Forest (final model)")
    ax.set_yticks(list(y))
    ax.set_yticklabels(d.factor)
    for lab, cat in zip(ax.get_yticklabels(), d.category):
        lab.set_color(cat_col[cat])
    ax.set_xlabel("Relative importance (%)")
    ax.set_xlim(0, 14.5)
    ax.grid(axis="x", color="#eee", lw=0.8)
    ax.set_axisbelow(True)
    h = [plt.Line2D([], [], color=c, lw=6) for c in cat_col.values()]
    leg1 = ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    ax.add_artist(leg1)
    ax.legend(h, cat_col.keys(), loc="center right", frameon=False, fontsize=7,
              title="Label colour = factor group", title_fontsize=7)
    ax.set_title("Relative importance of 17 factors: ANN vs Random Forest", loc="left")
    fig.text(0, -0.02, NOTE + " Figs 11-12.", fontsize=7, color="#555")
    fig.savefig(OUT / "factor-importance-ann-vs-rf.png")
    plt.close(fig)


def area_share():
    d = pd.read_csv(DATA / "gwp_area_share.csv", comment="#")
    cols = ["#1a7837", "#7fbf7b", "#f7e08a", "#f4a582", "#ca0020"]  # green (very high) -> red (very low)
    fig, ax = plt.subplots(figsize=(6.2, 1.6))
    left = 0
    for (_, r), c in zip(d.iterrows(), cols):
        ax.barh(0, r.area_percent, left=left, color=c, edgecolor="white", height=0.55)
        ax.text(left + r.area_percent / 2, 0, f"{r['class']}\n{r.area_percent:.2f}%", ha="center",
                va="center", fontsize=7.5, color="white" if c in ("#1a7837", "#ca0020") else "black")
        left += r.area_percent
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Share of Bangladesh's land area (%)")
    ax.set_title("Groundwater potential classes, final Random Forest map", loc="left")
    fig.text(0, -0.25, NOTE + " Fig. 17 / Section 5.1.", fontsize=7, color="#555")
    fig.savefig(OUT / "gwp-area-share-by-class.png")
    plt.close(fig)


if __name__ == "__main__":
    importance()
    area_share()
    print("written to", OUT.resolve())
