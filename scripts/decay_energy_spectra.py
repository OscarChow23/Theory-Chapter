#!/usr/bin/env python3
"""
Energy spectra of α, γ, and β⁻ nuclear decays — publication figure.

Generates a vector graphic contrasting discrete two-body (α, γ) lines with the
continuous three-body β⁻ electron spectrum. Intended for the historical
background section of the neutrino theory chapter (Pauli's continuum argument).

Physics
-------
* α and γ: two-body decays → monoenergetic lines (δ-function spikes).
* β⁻: three-body decay (daughter + e⁻ + ν̄_e) → continuous spectrum.
  Allowed phase-space approximation (massless neutrino, no Coulomb factor):
      I(E) ∝ E² (E_max − E)²    for  0 ≤ E ≤ E_max,
  which vanishes at the endpoints and peaks at E = E_max / 2.

Outputs (matches main.tex \\graphicspath{{images/}}):
    images/decay_energy_spectra.pdf
    images/decay_energy_spectra.svg

Usage
-----
    python scripts/decay_energy_spectra.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Physics parameters (schematic, relative energy units)
# ---------------------------------------------------------------------------
E_ALPHA = 2.35
E_GAMMA = 4.10
E_MAX = 5.50
N_POINTS = 2500

# Narrow Gaussian width for δ-like discrete spikes (visual rendering only)
SPIKE_SIGMA = 0.010
SPIKE_AMPLITUDE = 1.0

# ---------------------------------------------------------------------------
# Colour system — high-contrast academic palette
# ---------------------------------------------------------------------------
NAVY = "#1B2A4A"
TERRACOTTA = "#C45C26"
CHARCOAL = "#2C2C2C"
GRID = "#9A9A9A"
BG = "#FFFFFF"

# ---------------------------------------------------------------------------
# Spectrum models
# ---------------------------------------------------------------------------


def beta_spectrum(e: np.ndarray, e_max: float) -> np.ndarray:
    """Allowed β⁻ phase-space approximation (massless ν, no Coulomb).

    Intensity ∝ E² (E_max − E)² on [0, E_max], else 0.
    Analytic maximum at E = E_max / 2; I → 0 at E = 0 and E = E_max.
    """
    intensity = np.zeros_like(e, dtype=float)
    mask = (e > 0.0) & (e < e_max)
    intensity[mask] = (e[mask] ** 2) * ((e_max - e[mask]) ** 2)
    peak = intensity.max()
    if peak > 0.0:
        intensity /= peak
    return intensity


def discrete_spike(e: np.ndarray, e0: float, amplitude: float, sigma: float) -> np.ndarray:
    """Unit-height narrow Gaussian standing in for a δ-function line."""
    return amplitude * np.exp(-0.5 * ((e - e0) / sigma) ** 2)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------


def build_figure() -> mpl.figure.Figure:
    # Matplotlib mathtext (internal LaTeX-like renderer; no system TeX needed)
    mpl.rcParams.update(
        {
            "text.usetex": False,
            "mathtext.fontset": "cm",
            "font.family": "serif",
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "axes.linewidth": 1.05,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.08,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    e = np.linspace(0.0, 6.9, N_POINTS)
    beta = beta_spectrum(e, E_MAX)
    e_peak = 0.5 * E_MAX
    i_peak = float(np.interp(e_peak, e, beta))

    fig, ax = plt.subplots(figsize=(8.4, 5.1), facecolor=BG)
    ax.set_facecolor(BG)

    ax.grid(
        True,
        which="major",
        linestyle="--",
        linewidth=0.6,
        color=GRID,
        alpha=0.45,
        zorder=0,
    )
    ax.set_axisbelow(True)

    # --- β continuum -------------------------------------------------------
    ax.fill_between(
        e,
        beta,
        color=TERRACOTTA,
        alpha=0.28,
        linewidth=0,
        zorder=2,
        label=r"$\beta^{-}$ continuum",
    )
    ax.plot(
        e,
        beta,
        color=TERRACOTTA,
        linewidth=2.05,
        solid_capstyle="round",
        zorder=3,
    )

    # --- Discrete α / γ spikes ---------------------------------------------
    for e0 in (E_ALPHA, E_GAMMA):
        spike = discrete_spike(e, e0, SPIKE_AMPLITUDE, SPIKE_SIGMA)
        ax.plot(e, spike, color=NAVY, linewidth=1.05, zorder=4)
        ax.vlines(e0, 0.0, SPIKE_AMPLITUDE, colors=NAVY, linewidths=1.75, zorder=5)

    # Single legend entry for both discrete lines
    ax.plot([], [], color=NAVY, linewidth=1.75, label=r"$\alpha,\,\gamma$ (discrete)")

    # --- Axis frame --------------------------------------------------------
    ax.set_xlim(-0.25, 6.95)
    ax.set_ylim(-0.08, 1.32)
    ax.set_xlabel(r"Kinetic Energy of Emitted Particle ($E$)")
    ax.set_ylabel(r"Relative Intensity / Event Count")
    ax.set_title(r"Energy Spectra Characterization in Nuclear Decay Modes", pad=14)
    ax.tick_params(colors=CHARCOAL, length=0)
    for spine in ax.spines.values():
        spine.set_color(CHARCOAL)

    # Schematic axis: no numeric ticks; characteristic energies labelled below
    ax.set_xticks([])
    ax.set_yticks([])

    # --- Annotations -------------------------------------------------------
    ax.annotate(
        r"Discrete Energies ($E_{\alpha},\,E_{\gamma}$ from 2-body decay)",
        xy=(E_GAMMA, SPIKE_AMPLITUDE),
        xytext=(2.55, 1.18),
        fontsize=9.5,
        color=NAVY,
        ha="left",
        va="center",
        arrowprops=dict(
            arrowstyle="-|>",
            color=NAVY,
            lw=1.15,
            connectionstyle="arc3,rad=-0.18",
            shrinkA=2,
            shrinkB=3,
        ),
        zorder=6,
    )
    # Companion arrow to the α line from the same label
    ax.annotate(
        "",
        xy=(E_ALPHA, SPIKE_AMPLITUDE * 0.97),
        xytext=(3.35, 1.14),
        arrowprops=dict(
            arrowstyle="-|>",
            color=NAVY,
            lw=1.15,
            connectionstyle="arc3,rad=0.28",
            shrinkA=0,
            shrinkB=2,
        ),
        zorder=6,
    )

    ax.annotate(
        r"Continuous Electron Spectrum (3-body decay)",
        xy=(e_peak * 0.85, i_peak * 0.78),
        xytext=(0.28, 0.78),
        fontsize=9.5,
        color=TERRACOTTA,
        ha="left",
        va="center",
        arrowprops=dict(
            arrowstyle="-|>",
            color=TERRACOTTA,
            lw=1.15,
            connectionstyle="arc3,rad=0.12",
            shrinkA=2,
            shrinkB=3,
        ),
        zorder=6,
    )

    ax.annotate(
        r"Maximum Endpoint Energy  $E_{\mathrm{max}}$",
        xy=(E_MAX, 0.0),
        xytext=(E_MAX - 0.15, 0.42),
        fontsize=9.5,
        color=TERRACOTTA,
        ha="center",
        va="bottom",
        arrowprops=dict(
            arrowstyle="-|>",
            color=TERRACOTTA,
            lw=1.2,
            connectionstyle="arc3,rad=0.0",
            shrinkA=2,
            shrinkB=2,
        ),
        zorder=6,
    )
    ax.plot([E_MAX], [0.0], marker="o", markersize=5.0, color=TERRACOTTA, zorder=7)

    # Characteristic-energy tick marks on the baseline
    for e0, lab, col in (
        (E_ALPHA, r"$E_{\alpha}$", NAVY),
        (E_GAMMA, r"$E_{\gamma}$", NAVY),
        (E_MAX, r"$E_{\mathrm{max}}$", TERRACOTTA),
    ):
        ax.plot([e0, e0], [-0.025, 0.0], color=col, linewidth=1.1, clip_on=False, zorder=7)
        ax.text(e0, -0.065, lab, ha="center", va="top", fontsize=9, color=col, clip_on=False)

    ax.legend(
        loc="upper right",
        frameon=True,
        fancybox=False,
        edgecolor=GRID,
        framealpha=0.96,
        fontsize=9,
        borderpad=0.6,
    )

    fig.tight_layout()
    return fig


def main() -> None:
    fig = build_figure()
    pdf_path = OUT_DIR / "decay_energy_spectra.pdf"
    svg_path = OUT_DIR / "decay_energy_spectra.svg"
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight", facecolor=BG, edgecolor="none")
    fig.savefig(svg_path, format="svg", bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"Wrote {pdf_path}")
    print(f"Wrote {svg_path}")


if __name__ == "__main__":
    main()
