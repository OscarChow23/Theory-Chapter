#!/usr/bin/env python3
"""
Mechanism diagrams for α, β⁻, and γ nuclear decays — publication figures.

Companion to decay_energy_spectra.py. Generates three standalone vector
diagrams illustrating the fundamental decay mechanisms for the historical
background section of the neutrino theory chapter.

Outputs (written next to this repo's graphicspath):
    images/alpha_decay.svg
    images/beta_decay.svg
    images/gamma_decay.svg
"""

from __future__ import annotations

import os

# Headless / sandbox-safe defaults before pyplot import
os.environ.setdefault("MPLBACKEND", "Agg")

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Colour system — high-contrast academic palette
# ---------------------------------------------------------------------------
CHARCOAL = "#2C2C2C"
NAVY = "#1B2A4A"
PROTON = "#3A6EA5"
NEUTRON = "#C45C5C"
PROTON_EDGE = "#1E3A5F"
NEUTRON_EDGE = "#8B3A3A"
ALPHA_FILL = "#E8F0F8"
PARENT_FILL = "#F5EDE8"
PHOTON = "#E07A2F"
NEUTRINO = "#2A9D6E"
ELECTRON = "#1B2A4A"
W_BOSON = "#6B4C9A"
QUARK_D = "#3A6EA5"
QUARK_U = "#C45C5C"
TITLE_BG = "#F4F6F9"
TITLE_EDGE = "#C5CDD8"
LABEL_MUTED = "#5A6570"
BG = "#FFFFFF"

# ---------------------------------------------------------------------------
# Global rcParams
# ---------------------------------------------------------------------------


def _configure_style() -> None:
    mpl.rcParams.update(
        {
            "text.usetex": False,
            "mathtext.fontset": "cm",
            "font.family": "serif",
            "font.size": 11,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.10,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def _new_axes(figsize=(8.0, 5.5)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _title_card(ax, text: str, xy=(0.5, 0.94), width=0.72) -> None:
    x, y = xy
    card = FancyBboxPatch(
        (x - width / 2, y - 0.045),
        width,
        0.075,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        transform=ax.transAxes,
        facecolor=TITLE_BG,
        edgecolor=TITLE_EDGE,
        linewidth=1.2,
        zorder=20,
        clip_on=False,
    )
    ax.add_patch(card)
    ax.text(
        x,
        y - 0.005,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=13,
        color=NAVY,
        fontweight="bold",
        zorder=21,
    )


def _energy_sublabel(ax, x, y, text: str, color=LABEL_MUTED, ha="center") -> None:
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va="top",
        fontsize=8.5,
        color=color,
        style="italic",
        zorder=15,
    )


# ===========================================================================
# α Decay — macroscopic 2-body kinematics
# ===========================================================================


def _draw_nucleon(ax, x, y, kind: str, r=0.11, zorder=5) -> None:
    face, edge = (PROTON, PROTON_EDGE) if kind == "p" else (NEUTRON, NEUTRON_EDGE)
    ax.add_patch(
        Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=1.0, zorder=zorder)
    )


def draw_alpha_decay() -> mpl.figure.Figure:
    fig, ax = _new_axes(figsize=(9.2, 5.8))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.3)

    _title_card(ax, r"Alpha Decay: 2-Body Kinematics", xy=(0.5, 0.955), width=0.62)

    # Parent nucleus envelope (α mid-escape through the right boundary)
    parent = Ellipse(
        (3.0, 2.75),
        width=4.2,
        height=3.8,
        facecolor=PARENT_FILL,
        edgecolor=NAVY,
        linewidth=1.9,
        zorder=2,
        alpha=0.95,
    )
    ax.add_patch(parent)

    # Mixed nucleons inside parent (leave a corridor on the right for α exit)
    rng = np.random.default_rng(7)
    positions = []
    for _ in range(32):
        for _try in range(50):
            dx = rng.uniform(-1.75, 1.35)
            dy = rng.uniform(-1.55, 1.55)
            if (dx / 1.85) ** 2 + (dy / 1.65) ** 2 >= 1.0:
                continue
            # Keep clear of the α exit corridor
            if dx > 0.95 and abs(dy) < 0.85:
                continue
            positions.append((3.0 + dx, 2.75 + dy))
            break

    for i, (nx, ny) in enumerate(positions):
        _draw_nucleon(ax, nx, ny, "p" if i % 2 == 0 else "n", r=0.125, zorder=4)

    ax.text(3.0, 5.05, r"Parent nucleus", ha="center", va="bottom", fontsize=11, color=NAVY)
    ax.text(
        3.0,
        4.72,
        r"$(A,\,Z)$  $\rightarrow$  $(A\!-\!4,\,Z\!-\!2)$",
        ha="center",
        va="bottom",
        fontsize=9,
        color=LABEL_MUTED,
    )

    # Compact α cluster escaping through the right boundary
    alpha_cx, alpha_cy = 6.55, 2.75
    ax.add_patch(
        Ellipse(
            (alpha_cx, alpha_cy),
            width=1.55,
            height=1.45,
            facecolor=ALPHA_FILL,
            edgecolor=NAVY,
            linewidth=1.7,
            zorder=6,
            alpha=0.98,
        )
    )
    for dx, dy, kind in (
        (-0.28, 0.22, "p"),
        (0.28, 0.22, "n"),
        (-0.28, -0.28, "n"),
        (0.28, -0.28, "p"),
    ):
        _draw_nucleon(ax, alpha_cx + dx, alpha_cy + dy, kind, r=0.175, zorder=7)

    ax.text(
        alpha_cx,
        3.95,
        r"$\alpha \equiv {}^{4}_{2}\mathrm{He}^{2+}$",
        ha="center",
        va="bottom",
        fontsize=12,
        color=NAVY,
    )
    _energy_sublabel(ax, alpha_cx, 3.82, "Discrete Energy")

    # Fast α momentum (right)
    ax.annotate(
        "",
        xy=(9.55, 2.75),
        xytext=(7.55, 2.75),
        arrowprops=dict(arrowstyle="-|>", color=CHARCOAL, lw=2.5, mutation_scale=18),
        zorder=12,
    )
    ax.text(9.75, 3.15, r"$\vec{p}_{\alpha}$", ha="left", va="bottom", fontsize=12, color=CHARCOAL)
    ax.text(
        9.75,
        2.55,
        "(fast)",
        ha="left",
        va="top",
        fontsize=8.5,
        color=LABEL_MUTED,
        style="italic",
    )

    # Heavy daughter recoil (left, shorter)
    ax.annotate(
        "",
        xy=(0.45, 2.75),
        xytext=(1.25, 2.75),
        arrowprops=dict(arrowstyle="-|>", color=CHARCOAL, lw=1.6, mutation_scale=12),
        zorder=12,
    )
    ax.text(0.25, 3.15, r"$\vec{p}_{\mathrm{D}}$", ha="center", va="bottom", fontsize=11, color=CHARCOAL)
    ax.text(
        0.25,
        2.55,
        "(recoil)",
        ha="center",
        va="top",
        fontsize=8.5,
        color=LABEL_MUTED,
        style="italic",
    )

    ax.text(
        5.0,
        0.25,
        r"$\vec{p}_{\alpha} + \vec{p}_{\mathrm{D}} = 0$  (CM frame)"
        r"  $\Rightarrow$  discrete $E_{\alpha}$",
        ha="center",
        va="center",
        fontsize=10,
        color=LABEL_MUTED,
    )

    legend_elems = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=PROTON,
            markeredgecolor=PROTON_EDGE,
            markersize=10,
            label="Proton",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=NEUTRON,
            markeredgecolor=NEUTRON_EDGE,
            markersize=10,
            label="Neutron",
        ),
    ]
    ax.legend(
        handles=legend_elems,
        loc="upper right",
        frameon=True,
        fancybox=False,
        edgecolor=TITLE_EDGE,
        fontsize=9,
        framealpha=0.95,
    )
    return fig


# ===========================================================================
# β⁻ Decay — QFT Feynman diagram (3-body)
# ===========================================================================


def _fermion_arrow(ax, x0, y0, x1, y1, color, lw=1.8, t=0.55, zorder=5):
    """Draw a fermion segment with an arrow at fraction t along the segment.

    Arrow direction follows (x0,y0) → (x1,y1).
    """
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle="round", zorder=zorder)
    mx = x0 + t * (x1 - x0)
    my = y0 + t * (y1 - y0)
    dx, dy = x1 - x0, y1 - y0
    ax.annotate(
        "",
        xy=(mx + 0.04 * dx, my + 0.04 * dy),
        xytext=(mx - 0.04 * dx, my - 0.04 * dy),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw * 0.85, mutation_scale=14),
        zorder=zorder + 1,
    )


def _wavy_boson(ax, x0, y0, x1, y1, color, n_waves=6, amp=0.18, lw=1.8, zorder=5):
    t = np.linspace(0, 1, 400)
    dx, dy = x1 - x0, y1 - y0
    length = np.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    s = t * length
    offset = amp * np.sin(2 * np.pi * n_waves * t)
    ax.plot(
        x0 + ux * s + px * offset,
        y0 + uy * s + py * offset,
        color=color,
        lw=lw,
        solid_capstyle="round",
        zorder=zorder,
    )


def draw_beta_decay() -> mpl.figure.Figure:
    fig, ax = _new_axes(figsize=(9.4, 6.4))
    ax.set_xlim(-0.3, 10.6)
    ax.set_ylim(-0.55, 6.85)

    _title_card(ax, r"Beta Decay ($\beta^{-}$): 3-Body Kinematics", xy=(0.5, 0.96), width=0.72)

    # Process summary — clear of the title card
    ax.text(
        5.15,
        6.05,
        r"$d \;\rightarrow\; u + W^{-} \;\rightarrow\; u + e^{-} + \bar{\nu}_{e}$",
        ha="center",
        va="center",
        fontsize=11,
        color=CHARCOAL,
        zorder=12,
    )

    # Time axis
    ax.annotate(
        "",
        xy=(9.8, 0.25),
        xytext=(0.5, 0.25),
        arrowprops=dict(arrowstyle="-|>", color=LABEL_MUTED, lw=1.2, mutation_scale=12),
    )
    ax.text(5.15, -0.05, r"time $\longrightarrow$", ha="center", va="top", fontsize=9, color=LABEL_MUTED)

    # Vertices
    v1 = (3.4, 3.55)  # d → u + W⁻
    v2 = (6.8, 2.15)  # W⁻ → e⁻ ν̄_e

    # Spectator quarks (dashed)
    ax.plot([0.7, 5.2], [5.15, 5.15], color="#A0A8B0", lw=1.15, ls="--", zorder=2)
    ax.plot([0.7, 5.2], [4.55, 4.55], color="#A0A8B0", lw=1.15, ls="--", zorder=2)
    ax.text(
        2.9,
        5.35,
        "spectator quarks",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color="#A0A8B0",
        style="italic",
    )

    # Incoming d (left → vertex), outgoing u (vertex → right): proper time flow
    _fermion_arrow(ax, 0.6, 2.35, v1[0], v1[1], QUARK_D, lw=2.05, t=0.55)
    ax.text(0.45, 2.15, r"$d$", ha="center", va="top", fontsize=15, color=QUARK_D)

    _fermion_arrow(ax, v1[0], v1[1], 5.4, 4.85, QUARK_U, lw=2.05, t=0.55)
    ax.text(5.55, 5.0, r"$u$", ha="left", va="bottom", fontsize=15, color=QUARK_U)

    ax.plot(*v1, "o", color=CHARCOAL, markersize=7.5, zorder=8)

    # W⁻ boson (wavy) down-right to lepton vertex
    _wavy_boson(ax, v1[0], v1[1], v2[0], v2[1], W_BOSON, n_waves=7, amp=0.20, lw=2.05)
    ax.text(4.85, 2.55, r"$W^{-}$", ha="center", va="top", fontsize=13, color=W_BOSON)

    ax.plot(*v2, "o", color=CHARCOAL, markersize=7.5, zorder=8)

    # e⁻ outgoing forward in time
    _fermion_arrow(ax, v2[0], v2[1], 9.7, 0.95, ELECTRON, lw=2.05, t=0.55)
    ax.text(9.9, 0.85, r"$e^{-}$", ha="left", va="top", fontsize=14, color=ELECTRON)
    _energy_sublabel(ax, 9.9, 0.45, "Continuous Energy\n— Shares $E$", ha="left")

    # Antineutrino line: drawn to the upper-right, arrow points BACKWARD (←)
    x_nu, y_nu = 9.7, 3.55
    ax.plot([v2[0], x_nu], [v2[1], y_nu], color=NEUTRINO, lw=2.05, solid_capstyle="round", zorder=5)
    # Arrow oriented toward the past (toward V2)
    t_arr = 0.58
    mx = v2[0] + t_arr * (x_nu - v2[0])
    my = v2[1] + t_arr * (y_nu - v2[1])
    ax.annotate(
        "",
        xy=(mx - 0.10 * (x_nu - v2[0]), my - 0.10 * (y_nu - v2[1])),
        xytext=(mx + 0.10 * (x_nu - v2[0]), my + 0.10 * (y_nu - v2[1])),
        arrowprops=dict(arrowstyle="-|>", color=NEUTRINO, lw=1.7, mutation_scale=14),
        zorder=6,
    )
    ax.text(9.9, 3.7, r"$\bar{\nu}_{e}$", ha="left", va="bottom", fontsize=14, color=NEUTRINO)
    _energy_sublabel(ax, 9.9, 3.4, "Continuous Energy\n— Shares $E$", ha="left")

    # Stueckelberg convention callout (kept inside axes)
    ax.annotate(
        "arrow $\\leftarrow$ time\n(antiparticle)",
        xy=(mx, my),
        xytext=(7.6, 4.55),
        fontsize=8,
        color=NEUTRINO,
        ha="center",
        va="center",
        arrowprops=dict(
            arrowstyle="-|>",
            color=NEUTRINO,
            lw=0.9,
            connectionstyle="arc3,rad=-0.25",
        ),
        bbox=dict(
            boxstyle="round,pad=0.28",
            facecolor="#F0FAF5",
            edgecolor=NEUTRINO,
            linewidth=0.85,
        ),
        zorder=12,
    )
    return fig


# ===========================================================================
# γ Decay — nuclear de-excitation
# ===========================================================================


def _sine_photon(ax, x0, y0, x1, y1, color, n_waves=5.5, amp=0.30, lw=2.2, zorder=6):
    t = np.linspace(0, 1, 500)
    dx, dy = x1 - x0, y1 - y0
    length = np.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    envelope = np.sin(np.pi * t) ** 0.55
    s = t * length
    offset = amp * envelope * np.sin(2 * np.pi * n_waves * t)
    ax.plot(
        x0 + ux * s + px * offset,
        y0 + uy * s + py * offset,
        color=color,
        lw=lw,
        solid_capstyle="round",
        zorder=zorder,
    )
    ax.annotate(
        "",
        xy=(x1, y1),
        xytext=(x1 - 0.38 * ux, y1 - 0.38 * uy),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw * 0.9, mutation_scale=16),
        zorder=zorder + 1,
    )


def draw_gamma_decay() -> mpl.figure.Figure:
    fig, ax = _new_axes(figsize=(9.0, 5.8))
    ax.set_xlim(-0.3, 10.2)
    ax.set_ylim(-0.4, 6.35)

    _title_card(ax, r"Gamma Decay: 2-Body Kinematics", xy=(0.5, 0.96), width=0.62)

    ax.text(
        5.0,
        5.55,
        r"$X^{*} \;\longrightarrow\; X + \gamma$",
        ha="center",
        va="center",
        fontsize=12,
        color=CHARCOAL,
        zorder=12,
    )

    # Time axis
    ax.annotate(
        "",
        xy=(9.5, 0.3),
        xytext=(0.6, 0.3),
        arrowprops=dict(arrowstyle="-|>", color=LABEL_MUTED, lw=1.2, mutation_scale=12),
    )
    ax.text(5.0, 0.0, r"time $\longrightarrow$", ha="center", va="top", fontsize=9, color=LABEL_MUTED)

    # Energy-level guides
    for y_lvl in (4.15, 1.95):
        ax.plot([0.7, 4.5], [y_lvl, y_lvl], color=TITLE_EDGE, lw=1.0, ls=":", zorder=1)

    v = (4.9, 3.05)

    # Excited nucleus X*
    ax.plot([0.7, v[0]], [4.15, v[1]], color=NAVY, lw=3.5, solid_capstyle="round", zorder=5)
    ax.annotate(
        "",
        xy=(3.0, 3.5),
        xytext=(2.55, 3.68),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.2, mutation_scale=14),
        zorder=6,
    )
    ax.text(1.5, 4.5, r"$X^{*}$", ha="center", va="bottom", fontsize=16, color=NAVY)
    ax.text(
        1.5,
        4.9,
        "excited nucleus",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=LABEL_MUTED,
        style="italic",
    )

    # Ground-state nucleus X
    ax.plot([v[0], 9.2], [v[1], 1.95], color=NAVY, lw=3.5, solid_capstyle="round", zorder=5)
    ax.annotate(
        "",
        xy=(7.35, 2.4),
        xytext=(6.85, 2.55),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.2, mutation_scale=14),
        zorder=6,
    )
    ax.text(8.5, 1.5, r"$X$", ha="center", va="top", fontsize=16, color=NAVY)
    ax.text(
        8.5,
        1.1,
        "ground state",
        ha="center",
        va="top",
        fontsize=8.5,
        color=LABEL_MUTED,
        style="italic",
    )

    ax.plot(*v, "o", color=CHARCOAL, markersize=8.5, zorder=8)

    # γ photon packet
    _sine_photon(ax, v[0], v[1], 8.75, 4.75, PHOTON, n_waves=5.5, amp=0.32, lw=2.35)
    ax.text(9.0, 5.05, r"$\gamma$", ha="left", va="bottom", fontsize=16, color=PHOTON)
    _energy_sublabel(ax, 9.0, 4.85, "Discrete Energy", ha="left")

    # Level gap
    ax.annotate(
        "",
        xy=(3.5, 4.15),
        xytext=(3.5, 2.45),
        arrowprops=dict(arrowstyle="<->", color=LABEL_MUTED, lw=1.0),
        zorder=4,
    )
    ax.text(
        3.2,
        3.3,
        r"$E_{\gamma} = E^{*} - E_{0}$",
        ha="right",
        va="center",
        fontsize=10,
        color=LABEL_MUTED,
        rotation=90,
    )
    return fig


# ===========================================================================
# Main
# ===========================================================================


def main() -> None:
    _configure_style()

    builders = {
        "alpha_decay.svg": draw_alpha_decay,
        "beta_decay.svg": draw_beta_decay,
        "gamma_decay.svg": draw_gamma_decay,
    }

    for filename, builder in builders.items():
        fig = builder()
        out = OUT_DIR / filename
        fig.savefig(out, format="svg", bbox_inches="tight", facecolor=BG, edgecolor="none")
        plt.close(fig)
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
