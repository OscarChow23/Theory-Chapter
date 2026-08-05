# Neutrino Theory Chapter

This context defines the canonical language used to plan the thesis theory chapter. The chapter
develops neutrino oscillation theory toward a disappearance-led account of the NOvA far-detector
energy spectrum.

## Chapter argument

**Spectrum-first**:
An explanatory structure in which oscillation theory is developed toward observable features in
the far-detector energy spectrum and the parameter sensitivity those features provide.
_Avoid_: Textbook-first

**Disappearance-led**:
The chapter's primary emphasis on the muon-neutrino survival channel because it is most relevant
to the thesis measurement. Appearance remains part of the three-flavour account but is shorter.
_Avoid_: Disappearance-only

**Spectral features**:
The interpretation of spectral features in terms of oscillation parameters, especially the
position and depth of the muon-neutrino disappearance dip.
_Avoid_: Spectrum description; Spectrum reading

## Oscillation channels

**Disappearance channel**:
The measurement of the reduced survival probability of an initially produced neutrino flavour.
In this chapter, it canonically means \(\nu_\mu\to\nu_\mu\).
_Avoid_: Muon component

**Appearance channel**:
The measurement of a neutrino flavour different from the initially produced flavour. In this
chapter, it canonically means \(\nu_\mu\to\nu_e\).
_Avoid_: Electron side

**NOvA oscillation window**:
The restricted baseline-to-energy region sampled by NOvA, centred on the first atmospheric
oscillation maximum and displaying a single broad oscillation cycle.
_Avoid_: NOvA point

**Disappearance dip**:
The broad minimum in the far-detector \(\nu_\mu\) energy spectrum whose position primarily
constrains \(\Delta m^2_{32}\) and whose depth primarily constrains \(\sin^2(2\theta_{23})\).
_Avoid_: Oscillation dip when the channel is ambiguous

## Parameter sensitivity

**Matter effect**:
The modification of flavour evolution caused by coherent forward scattering in matter. At NOvA,
its most visible consequences occur in the appearance channel.
_Avoid_: MSW effect when referring generically to all matter-modified propagation

**Octant degeneracy**:
The leading-order inability of disappearance data expressed through
\(\sin^2(2\theta_{23})\) to distinguish \(\theta_{23}<45^\circ\) from
\(\theta_{23}>45^\circ\).
_Avoid_: Octant ambiguity

**Experimental landscape**:
The account of which experiments constrain each oscillation parameter, the remaining
open questions, and how upcoming measurements extend present sensitivity.
_Avoid_: Experiment catalogue, Status report

**Parameter provenance**:
The organising principle of the landscape section: each oscillation parameter is traced to
the class of measurement that constrains it, rather than being presented as a bare number.
_Avoid_: Parameter summary

**Solar pair**:
\(\sin^2\theta_{12}\) and \(\Delta m^2_{21}\), taken together. Canonically what JUNO's first
result measures. Note that JUNO does _not_ measure \(\Delta m^2_{31}\) in that result; it
enters the fit as an external constraint.
_Avoid_: Solar parameters when the reader might read it as "parameters measured by solar
experiments" specifically

**Leading direct measurement**:
The single-experiment result that currently exceeds the global-fit precision for a given
parameter. Distinguished from the global fit because NuFIT 6.0 closes in September 2024 and
several headline results postdate it.
_Avoid_: Best measurement, World best

**Wider programme**:
The experiments covered for the completeness of the field rather than for thesis relevance:
Hyper-Kamiokande, IceCube DeepCore, KM3NeT/ORCA. Quarantined in its own subsection so that
breadth cannot displace the disappearance-led core.
_Avoid_: Other experiments

## Citation and figure conventions (section 5)

**Page-exact citation**:
`\citep[p.~N]{key}`, where N refers to the arXiv version named in the bib entry's `version`
field, not journal pagination. Every such page number must be verified by opening the source
PDF; unverified page numbers are not written.
_Avoid_: Citing a page from a conference slide deck

**Reprinted figure**:
A published result plot included as a cropped vector page from the source PDF
(`images/*_src.pdf` plus `trim`/`clip`), captioned "Reproduced from ..., Fig. N, p. X".
Distinguished from a generated figure, which is produced by a script in `scripts/`.
_Avoid_: Digitising and redrawing a published confidence contour

**Exposure-indexed sensitivity**:
A future-experiment sensitivity quoted against accumulated exposure (kt·MW·yr, POT) rather
than a calendar year, so the claim does not go stale as schedules move.
_Avoid_: "DUNE will measure X by 20NN"
