#!/usr/bin/env python3
"""
Two-flavour survival probability vs. propagation distance and vs. energy.

The disappearance counterpart of Booth (2021) Fig. 2.4, which plots the
*appearance* probability. Generated for Sec.~\\ref{sec:two-flavour} of the theory
chapter, and drawn to show exactly the four statements made there:

  left  panel  P vs L at fixed E  -- sinusoidal in L; the mixing angle sets the
               depth through sin^2(2*theta), marked by the double-headed arrow at
               the first minimum. Delta m^2 sets the frequency, i.e. the spacing
               of successive minima.
  right panel  P vs E at fixed L  -- NOT sinusoidal in E, since the phase goes as
               1/E: oscillations crowd together towards low energy, and towards
               high energy the phase shrinks and P returns to unity. The depth is
               the same sin^2(2*theta) -- drawn with the same double-headed arrow,
               which is the point of using it in both panels. The highest-energy
               minimum sits at E_max, labelled on the axis.

Physics
-------
    P(nu_a -> nu_a) = 1 - sin^2(2*theta) sin^2( K * dm2[eV^2] L[km] / E[GeV] )

with K = 1.267 fixed by hbar*c (computed below, not hard-coded). Hence

    L_osc  = 4*pi*E / dm2      -> (pi / K)   E[GeV] / dm2[eV^2]  = 2.48 E / dm2  km
    E_max  (phase = pi/2)      -> (2*K / pi) dm2[eV^2] L[km]     = 0.81 dm2 L    GeV

L_osc is the full period in L (maximum to maximum); the first minimum, i.e.
maximal disappearance, is at L_osc/2. In energy the minima lie at E_max/(2n-1),
which is why the pattern is not periodic in E.

Outputs (matches main.tex \\graphicspath{{images/}}):
    images/two_flavour_survival.pdf
    images/two_flavour_survival.svg
    images/two_flavour_survival.png   (preview only)

Usage
-----
    python scripts/two_flavour_survival.py
    python scripts/two_flavour_survival.py --verify-only
"""

from __future__ import annotations

import argparse
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
# Unit conversion -- derived from hbar*c rather than hard-coded as 1.27
# ---------------------------------------------------------------------------
HBAR_C_GEV_M = 1.973269804e-16  # GeV m (PDG 2024)

# phase = dm2 L / (4E) in natural units; with dm2/eV^2, L/km, E/GeV this becomes
# K * dm2 L / E, where K = (1e-18 GeV^2/eV^2)(1e3 m/km) / (4 hbar c).
K_PHASE = 1e-18 * 1e3 / (4.0 * HBAR_C_GEV_M)  # ~= 1.2669

L_OSC_COEFF = np.pi / K_PHASE   # L_osc[km]  = 2.480 E[GeV] / dm2[eV^2]
E_MAX_COEFF = 2.0 * K_PHASE / np.pi  # E_max[GeV] = 0.807 dm2[eV^2] L[km]

# ---------------------------------------------------------------------------
# Oscillation parameters
#
# Deliberately generic: the figure illustrates the two-flavour formula, not a
# NOvA measurement. dm2 is atmospheric-scale and sin^2(2*theta) is set below
# maximal mixing so that the depth annotation is visibly distinct from unity.
# ---------------------------------------------------------------------------
DM2 = 2.4e-3        # eV^2
SIN2_2THETA = 0.85  # dimensionless
E_FIXED = 2.0       # GeV, left panel
L_FIXED = 810.0     # km,  right panel

N_L = 4000       # samples, left panel
N_E = 400_000    # samples, right panel (dense: phase ~ 1/E crowds at low E)

# main.tex is 11pt article with 1in margins, so \textwidth = 469.755pt = 6.50in.
# Drawing at exactly that width means \includegraphics[width=\textwidth] applies no
# rescaling, so the font sizes below are the sizes that actually appear in print.
# Keep them a little under the 11pt body text. If this figure is ever included at
# some other width, the annotation text will scale with it.
FIG_WIDTH_IN = 6.50
# Panels are deliberately wide rather than square: at this height each axes is
# roughly 2:1, which suits a sinusoid and keeps the crowded low-E end of the
# right panel legible.
FIG_HEIGHT_IN = 2.05
FS_ANNOT = 10  # sin^2 2theta, E_max
FS_TICK = 9

# ---------------------------------------------------------------------------
# Colour system -- matches scripts/decay_energy_spectra.py
# ---------------------------------------------------------------------------
NAVY = "#1B2A4A"
TERRACOTTA = "#C45C26"
CHARCOAL = "#2C2C2C"
GRID = "#9A9A9A"
BG = "#FFFFFF"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def p_survival(length_km, energy_gev, dm2=DM2, sin2_2theta=SIN2_2THETA):
    """Two-flavour survival probability, practical units (eV^2, km, GeV)."""
    phase = K_PHASE * dm2 * np.asarray(length_km, dtype=float) / np.asarray(
        energy_gev, dtype=float
    )
    return 1.0 - sin2_2theta * np.sin(phase) ** 2


def l_osc(energy_gev, dm2=DM2):
    """Oscillation length in km: the period in L (maximum to maximum)."""
    return L_OSC_COEFF * energy_gev / dm2


def e_max(length_km, dm2=DM2):
    """Energy of the first (highest-energy) oscillation maximum, in GeV."""
    return E_MAX_COEFF * dm2 * length_km


def _local_minima(x, y):
    """Indices of interior local minima of a densely sampled curve."""
    interior = np.arange(1, len(y) - 1)
    is_min = (y[interior] < y[interior - 1]) & (y[interior] <= y[interior + 1])
    return interior[is_min]


# ---------------------------------------------------------------------------
# Verification -- every claim the figure makes, checked numerically
# ---------------------------------------------------------------------------
def verify(verbose=True):
    def report(name, ok, detail):
        if verbose:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        assert ok, f"{name}: {detail}"

    if verbose:
        print("Verifying the two-flavour survival figure\n")
        print("Constants")

    report(
        "phase coefficient K = 1.27",
        abs(K_PHASE - 1.27) / 1.27 < 3e-3,
        f"K = {K_PHASE:.5f}, quoted 1.27 (rel. diff {abs(K_PHASE-1.27)/1.27:.2e})",
    )
    report(
        "L_osc coefficient = 2.48 (as in eq:osc-length)",
        abs(round(L_OSC_COEFF, 2) - 2.48) < 1e-9,
        f"pi/K = {L_OSC_COEFF:.4f} -> 2.48",
    )
    report(
        "E_max coefficient = 0.81 (as in eq:first-max)",
        abs(round(E_MAX_COEFF, 2) - 0.81) < 1e-9,
        f"2K/pi = {E_MAX_COEFF:.5f} -> 0.81",
    )
    report(
        "L_osc = 4*pi*E/dm2 in natural units",
        abs(l_osc(E_FIXED) - L_OSC_COEFF * E_FIXED / DM2) < 1e-9,
        f"L_osc({E_FIXED} GeV) = {l_osc(E_FIXED):.1f} km",
    )

    # --- left panel: P vs L at fixed E ------------------------------------
    if verbose:
        print("\nLeft panel  P vs L at fixed E")

    lo = l_osc(E_FIXED)
    ell = np.linspace(0.0, 4.2 * lo, 2_000_001)
    p_l = p_survival(ell, E_FIXED)
    minima_l = ell[_local_minima(ell, p_l)]

    report(
        "P = 1 at L = 0 (no oscillation at source)",
        abs(p_survival(0.0, E_FIXED) - 1.0) < 1e-12,
        f"P(0) = {p_survival(0.0, E_FIXED):.12f}",
    )
    report(
        "depth of every minimum equals sin^2(2*theta)",
        abs((1.0 - p_l.min()) - SIN2_2THETA) < 1e-6,
        f"1 - P_min = {1.0 - p_l.min():.8f}, sin^2(2th) = {SIN2_2THETA}",
    )
    report(
        "first minimum at L = L_osc/2 (maximal disappearance)",
        abs(minima_l[0] - lo / 2.0) / (lo / 2.0) < 1e-5,
        f"found {minima_l[0]:.3f} km, expected {lo/2.0:.3f} km",
    )
    spacings = np.diff(minima_l)
    report(
        "successive minima are evenly spaced by L_osc (periodic in L)",
        np.all(np.abs(spacings - lo) / lo < 1e-5),
        f"spacings = {np.array2string(spacings, precision=1)} km, L_osc = {lo:.1f} km",
    )
    report(
        "L_osc scales as E / dm2",
        abs(l_osc(2 * E_FIXED) - 2 * lo) < 1e-9
        and abs(l_osc(E_FIXED, 2 * DM2) - lo / 2) < 1e-9,
        "doubling E doubles L_osc; doubling dm2 halves it",
    )

    # --- right panel: P vs E at fixed L ------------------------------------
    if verbose:
        print("\nRight panel  P vs E at fixed L")

    em = e_max(L_FIXED)
    energy = np.linspace(0.01 * em, 6.0 * em, 4_000_001)
    p_e = p_survival(L_FIXED, energy)
    minima_e = energy[_local_minima(energy, p_e)]
    minima_e_desc = minima_e[::-1]  # highest energy first

    report(
        "E_max = 0.81 dm2 L matches phase = pi/2",
        abs(K_PHASE * DM2 * L_FIXED / em - np.pi / 2) < 1e-12,
        f"E_max = {em:.4f} GeV, phase there = {K_PHASE*DM2*L_FIXED/em:.6f} rad",
    )
    report(
        "highest-energy minimum of the curve is at E_max",
        abs(minima_e_desc[0] - em) / em < 1e-4,
        f"found {minima_e_desc[0]:.4f} GeV, expected {em:.4f} GeV",
    )
    report(
        "no minimum above E_max (it is the first maximum)",
        minima_e.max() <= em * (1 + 1e-4),
        f"max minimum found = {minima_e.max():.4f} GeV",
    )
    expected = em / (2 * np.arange(1, 6) - 1.0)  # E_max, E_max/3, E_max/5, ...
    report(
        "minima lie at E_max/(2n-1)",
        np.all(np.abs(minima_e_desc[:5] - expected) / expected < 1e-3),
        f"found {np.array2string(minima_e_desc[:5], precision=3)}, "
        f"expected {np.array2string(expected, precision=3)} GeV",
    )
    gaps = -np.diff(minima_e_desc[:5])
    report(
        "spacing in E is NOT constant -- the curve is not sinusoidal in E",
        gaps.max() / gaps.min() > 3.0,
        f"gaps = {np.array2string(gaps, precision=3)} GeV, "
        f"ratio widest/narrowest = {gaps.max()/gaps.min():.1f}",
    )
    report(
        "oscillations crowd towards low energy",
        np.all(np.diff(gaps) < 0),
        "successive gaps shrink monotonically as E decreases",
    )
    report(
        "depth in E is the same sin^2(2*theta)",
        abs((1.0 - p_e.min()) - SIN2_2THETA) < 1e-6,
        f"1 - P_min = {1.0 - p_e.min():.8f}",
    )
    report(
        "P -> 1 towards high energy",
        p_survival(L_FIXED, 50.0 * em) > 0.999
        and p_survival(L_FIXED, 6.0 * em) > p_survival(L_FIXED, 2.0 * em),
        f"P(6 E_max) = {p_survival(L_FIXED, 6*em):.4f}, "
        f"P(50 E_max) = {p_survival(L_FIXED, 50*em):.6f}",
    )

    # --- cross-checks against the numbers quoted in the text ---------------
    if verbose:
        print("\nNumbers quoted in sections/03_oscillations.tex")

    nova = e_max(810.0, 2.455e-3)  # PDG dm2_32, normal ordering, Table 1
    report(
        "NOvA: E_max ~ 1.6 GeV at L = 810 km",
        abs(nova - 1.6) < 0.05,
        f"E_max = {nova:.3f} GeV",
    )

    if verbose:
        print("\nAll checks passed.\n")
    return True


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def build_figure(show_floor_line=False, show_floor_tick=False):
    """Draw the two-panel figure.

    The survival probability swings between 1 and 1 - sin^2(2*theta). Unlike
    Booth's appearance version -- which swings between 0 and sin^2(2*theta), so
    that the axis itself marks the bottom -- neither end of the swing here is the
    axis, and the floor needs marking explicitly. `show_floor_tick` labels it on
    the y-axis, which is enough: it is the same value in both panels, since the
    amplitude depends on neither L nor E. `show_floor_line` additionally rules a
    dashed guide across the panel; that was the original choice, dropped as
    redundant once the tick is present. Both False is the sparest version, with
    the depth carried by the annotated arrow alone.
    """
    mpl.rcParams.update(
        {
            "text.usetex": False,
            "mathtext.fontset": "cm",
            "font.family": "serif",
            "font.size": 9,
            "axes.labelsize": 11,
            "xtick.labelsize": FS_TICK,
            "ytick.labelsize": FS_TICK,
            "axes.linewidth": 1.05,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    lo = l_osc(E_FIXED)
    em = e_max(L_FIXED)
    floor = 1.0 - SIN2_2THETA

    # With the L_osc arrow gone there is nothing to draw below the curve minima,
    # so the floor sits close to the axis and the panels read wider.
    y_lo, y_hi = floor - 0.10, 1.12

    fig, (ax_l, ax_e) = plt.subplots(1, 2, figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN), facecolor=BG)
    fig.subplots_adjust(wspace=0.42)

    for ax in (ax_l, ax_e):
        if show_floor_line:
            ax.axhline(floor, color=GRID, ls=(0, (4, 3)), lw=0.8, zorder=1)
        ax.set_ylim(y_lo, y_hi)
        if show_floor_tick:
            ax.set_yticks([floor, 1.0])
            ax.set_yticklabels([r"$1-\sin^{2}2\theta$", r"$1$"], fontsize=FS_TICK)
        else:
            # Mark the floor with an unlabelled tick. The level is still on the
            # axis, but the long "1 - sin^2 2theta" string no longer reserves
            # horizontal space and shoves the y-axis label away from the canvas;
            # the annotated arrow is what names the depth.
            ax.set_yticks([floor, 1.0])
            ax.set_yticklabels(["", r"$1$"], fontsize=FS_TICK)
        ax.set_ylabel(r"$P(\nu_\alpha \to \nu_\alpha)$", labelpad=2)
        ax.tick_params(colors=CHARCOAL)
        for spine in ax.spines.values():
            spine.set_color(CHARCOAL)

    # =====================================================================
    # Left: P vs L at fixed E -- sinusoidal, period L_osc
    # =====================================================================
    ell = np.linspace(0.0, 4.25 * lo, N_L)
    ax_l.plot(ell, p_survival(ell, E_FIXED), color=CHARCOAL, lw=1.2, zorder=3)

    # Depth = sin^2(2 theta), at the first minimum (L = L_osc/2)
    ax_l.annotate(
        "",
        xy=(lo / 2.0, 1.0),
        xytext=(lo / 2.0, floor),
        arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.5, shrinkA=0, shrinkB=0),
        zorder=5,
    )
    ax_l.text(
        lo / 2.0 - 0.035 * lo,
        (1.0 + floor) / 2.0,
        r"$\sin^{2}2\theta$",
        color=NAVY,
        rotation=90,
        ha="right",
        va="center",
        fontsize=FS_ANNOT,
        bbox=dict(facecolor=BG, edgecolor="none", pad=1.0),
        zorder=6,
    )

    # Maximal disappearance at the first minimum
    ax_l.plot([lo / 2.0], [floor], marker="o", ms=4.2, color=NAVY, zorder=6)
    ax_l.set_xticks([])
    ax_l.set_xlim(0.0, 4.25 * lo)
    ax_l.set_xlabel(r"$L$")

    # =====================================================================
    # Right: P vs E at fixed L -- phase ~ 1/E, so not periodic in E
    # =====================================================================
    e_lo, e_hi = 0.05 * em, 5.0 * em
    energy = np.linspace(e_lo, e_hi, N_E)
    ax_e.plot(energy, p_survival(L_FIXED, energy), color=CHARCOAL, lw=0.9, zorder=3)

    # Depth at the highest-energy minimum. Same double-headed arrow as the left
    # panel, and deliberately so: the amplitude is sin^2(2*theta) whether the
    # curve is drawn against L or against E. The label sits to the right of the
    # arrow, where the curve is smooth -- to its left the oscillations crowd.
    ax_e.annotate(
        "",
        xy=(em, 1.0),
        xytext=(em, floor),
        arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.5, shrinkA=0, shrinkB=0),
        zorder=5,
    )
    ax_e.text(
        em + 0.10 * em,
        (1.0 + floor) / 2.0,
        r"$\sin^{2}2\theta$",
        color=NAVY,
        rotation=90,
        ha="left",
        va="center",
        fontsize=FS_ANNOT,
        bbox=dict(facecolor=BG, edgecolor="none", pad=1.0),
        zorder=6,
    )
    ax_e.plot([em], [floor], marker="o", ms=4.2, color=TERRACOTTA, zorder=6)

    ax_e.set_xlim(e_lo, e_hi)
    ax_e.set_xticks([em])
    ax_e.set_xticklabels([r"$E_{\mathrm{max}}$"], fontsize=FS_TICK)
    ax_e.get_xticklabels()[0].set_color(TERRACOTTA)
    ax_e.set_xlabel(r"$E$")

    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="run the numerical checks without writing the figure",
    )
    args = parser.parse_args()

    verify()
    if args.verify_only:
        return

    fig = build_figure()
    for ext in ("pdf", "svg", "png"):
        path = OUT_DIR / f"two_flavour_survival.{ext}"
        fig.savefig(path, format=ext, bbox_inches="tight", pad_inches=0.08,
                    facecolor=BG, edgecolor="none")
        print(f"Wrote {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
