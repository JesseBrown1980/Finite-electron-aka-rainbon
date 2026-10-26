# Finite Electron (aka Rainbon)

*What would an electron look like if it were a finite cloud of sub-particles,
and what would experimentalists see?*

This repository builds an exactly specified **finite toy model of a composite
electron**: three equal-mass preons on a periodic cubic lattice, bound by an
integer potential, with the centre of mass removed. The ground state plays the
electron, and the first excitation plays the excited electron e* searched for at
colliders. We compute its size, its excitation gap and their dimensionless
product, then map the model onto today's experimental limits.

**What this can and cannot show.** A model cannot prove what electrons are made
of; only experiment can. What it can do is show whether, and how, a finite
composite electron fits inside current limits, and which signatures it would
leave. Every number below is labelled:

- **Measured**: integer computation with an exact residual bound (some eigenvalue lies within ε of the value).
- **Converged**: stable across box sizes *and* lattice spacings.
- **Pending**: not yet converged, so not used.

All arithmetic is integer-only (no floating point anywhere), with Rust 1.81 and
`clippy -D warnings`, and every receipt line ends in `json=0`. The solvers are
the ones from [The-matrix-law-essentials](https://github.com/JesseBrown1980/The-matrix-law-essentials).

```
./verify.sh      # build, exact symmetry-sector reproduction, harmonic calibration, mapping
```

## The model

The state is the pair of relative positions d₂ = x₂ − x₁ and d₃ = x₃ − x₁ on
Z_L³ × Z_L³, which gives L⁶ states.

H = JE·E + JB·M, where:

- **E (kinetic):** the lattice Laplacian of the three preons. Each state has 18 hops, and JE = ħ²/(2ma²).
- **M (binding potential)** on minimum-image pair vectors:
  - **harmonic:** Σ|rᵢⱼ|² (exactly solvable in the continuum, used for calibration);
  - **linear string:** Σ ⌊10|rᵢⱼ|⌋ (confining, integer square roots).
- **Charge radius:** equal charges on equal masses give ⟨r²⟩ = ⅓ Σ⟨|xᵢ − X|²⟩.

**Symmetry compression** (`symsec`). The 48 cube operations and the 6 preon
permutations reduce the problem to:

- **sector A**, fully symmetric, which holds the ground state: the electron is an **s-wave**;
- **sector Pz**, odd under z → −z, which holds the first excited multiplet: e* is a **P-wave** (orbital) excitation.

This reproduces the full-lattice E₀, E₁ and r² exactly at L = 6 and 8 with
29–200× fewer states, and makes L = 16 (16.7M full states) reachable.

## Results

### Harmonic calibration (continuum targets known exactly)

The continuum targets for three-body harmonic binding are:

- gap Δ = ħω = √(12·JE·JB);
- E₀ = 3ħω;
- r² = ħ/(mω);
- **c = r²·mΔ/ħ² = 1**;
- first excited level 6-fold degenerate.

**Measured:**

- The first excited level is exactly 6-fold degenerate on the full lattice (L = 6, 8).
- **Box axis** (JE = 9, JB = 1; cloud width ℓ = (JE/3)^¼ ≈ 1.32 sites):

| L | E₀ | E₁ (P-wave) | gap | r² | c |
|---|---|---|---|---|---|
| 6 | 23.960538 | 40.320633 | 16.360095 | 2.597261 | 2.3606 |
| 8 | 29.637907 | 40.403024 | 10.765117 | 1.962201 | 1.1735 |
| 10 | 30.372714 | 40.299401 | 9.926687 | 1.671393 | 0.9217 |
| 12 | 30.408253 | 40.278614 | 9.870361 | 1.646813 | 0.9030 |
| 14 | 30.409182 | 40.277789 | 9.868607 | 1.645724 | 0.9023 |
| 16 | 30.409197 | 40.277778 | 9.868581 | 1.645692 | 0.9023 |

The box error is gone by L = 14–16 (E₀ changes by 15 millionths).

- **Spacing axis.** Box-converged points only, meaning the two largest boxes agree to about 10⁻³:

| JE | ℓ² = (JE/3)^½ | boxes | c (largest box) |
|---|---|---|---|
| 9 | 1.732 | L = 14, 16 | 0.902258 |
| 12 | 2.000 | L = 14, 16 | 0.915556 |
| 16 | 2.309 | L = 14, 16 | 0.927035 |
| 25 | 2.887 | L = 16, 18 | 0.941770 |
| 36 | 3.464 | L = 18, 20 | 0.951548 |
| 49 | 4.041 | L = 18, 20 | 0.958590 |

**Continuum extrapolation** (`python/spacing_fit.py`, exact integer least
squares, `data/spacing_fit_harmonic.hbp`). The fit c(ℓ) = c∞ − C/ℓ² over six
points gives **c∞ = 1.000842** (C = 0.1706), with every residual at or below
78 millionths, so the 1/ℓ² discretisation law is tested rather than assumed.
Adding a 1/ℓ⁴ term gives c∞ = 1.000147 (residuals at or below 32 millionths).
The two fits bracket the exact value: **c∞ = 1.0001–1.0008 against the exact 1**.
That validates the integer three-body machinery (operator, symmetry sectors,
radius observable) on the exactly solvable case. JE = 81 and 144 are not
box-converged at L ≤ 16 and are not used.

**L = 6 note.** `data/scan.hbp` contains one unconverged excited energy,
40.832594, from the full-lattice deflated run. Its own receipt shows residual
radius 0.382990. The converged value is 40.320633 (sector Pz), inside the
block solver's certified interval [40.320558, 40.320711]. The bad value is
annotated in the file and excluded from every comparison.

### Linear string (the physics model)

The cloud width is ℓ = (JE/5)^⅓ sites (with JB = 1).

| JE | L | E₀ | E₁ (P-wave) | gap | r² | c |
|---|---|---|---|---|---|---|
| 20 | 16 | 94.739604 | 115.526871 | 20.787267 | 1.743909 | 0.906277 |
| 20 | 18 | 94.739621 | 115.526808 | 20.787187 | 1.743882 | 0.906260 |
| 40 | 16 | 120.354074 | 146.740169 | 26.386095 | 2.858511 | 0.942811 |
| 40 | 18 | 120.358845 | 146.730073 | 26.371228 | 2.854178 | 0.940852 |
| 80 | 18 | 152.314992 | 185.895337 | 33.580345 | 4.643827 | 0.974633 |
| 80 | 20 | 152.359124 | 185.834196 | 33.475072 | 4.607698 | 0.964018 |

Only JE = 20 is box-converged. JE = 40 still moves by 0.002 from L = 16 to 18,
and JE = 80 by 0.011 from L = 18 to 20. **The linear-string constant c∞ is
therefore pending.** It needs boxes of L = 22–24 at JE = 40–80 before it can be
extrapolated like the harmonic case. Until then the mapping below uses the
calibration value c = 1, noting that the linear-string values found so far lie
between 0.90 and 0.97 and rise with ℓ.

### Compute and reproducibility

- **Symmetry compression** (`symsec`): it reproduces the full lattice exactly at L = 6 and 8, and makes L = 20 (64M full states) reachable.
- **GitRAM lane** (`.github/workflows/gitram-symscan.yml`, template [GitRAM](https://github.com/JesseBrown1980/GitRAM)): 40 stateless GitHub-container cells and an all-or-nothing fan-in. Run 40253908502 returned 41/41 successful jobs, and the sealed receipt is `data/SYMSCAN-GITRAM.hbp` with its SHA-256.
- **Cross-check.** Twelve cases computed both in containers and locally agree in every numerical field (E, residual radius, r², sector size). Elapsed times and runner metadata differ, as expected (`data/crosscheck_gitram_vs_local.hbp`).

## What experimentalists would see (mapping, `python/experiment_map.py`)

| quantity | current limit | source |
|---|---|---|
| Electron size (LEP form factor) | r < 2.8 × 10⁻¹⁹ m | [arXiv:2506.02450](https://arxiv.org/html/2506.02450v3) |
| Contact-interaction scale | Λ > 21.3 TeV (g²/4π = 1) | same |
| Excited electron e* | mass > 5.6 TeV (Λ = m*) | [CMS, arXiv:2001.04521](https://arxiv.org/abs/2001.04521v2) |
| Electron g − 2 | a_e = 0.00115965218059(13) | [PDG / Fan et al. 2023](https://pdglive.lbl.gov/view/S003MM) |

Mapping for a non-relativistic three-preon cloud, written with the calibration
value c = 1 until the linear-string c∞ converges (values found so far are
0.90–0.97, which changes the radius by under 5%):

- **Size:** if e* ≥ 5.6 TeV, then r ≤ √c · ħc/Δ ≈ 3.5 × 10⁻²⁰ m at preon mass m = Δ, the edge of non-relativistic validity. That is about 8× below LEP's direct limit, so the e* searches are the stronger constraint.
- **Mass (the lightness problem):** such a cloud weighs at least 3 × 5.6 TeV, against the electron's 0.511 MeV, which is 1 part in 33 million. A light composite electron therefore needs either extreme fine-tuning or a protecting (chiral) symmetry. This is a known difficulty of composite-lepton models, made quantitative here.
- **g − 2:** without chiral protection the shift would be ~m_e/M, 700,000× larger than the measured uncertainty, so that case is excluded. With protection the shift is ~(m_e/M)² ≈ 8 × 10⁻¹⁵, which is allowed.

Scope: the mapping uses non-relativistic scaling, valid for preon mass ≳ Δ.
Light preons need a relativistic treatment, which this model does not provide.

## Layout

```
crates/rainbon   model: lib (lattice, potentials, hops, radius), cloudb (matrix file),
                 cloud (ground + deflated first excited, radius), symsec (symmetry sectors)
crates/evolvers  block solver `cluster`, Chebyshev `cheb`, `jumpto` (from The-matrix-law-essentials)
crates/sturmrs   interval Sturm inertia verifier (from The-matrix-law-essentials)
python/          experiment_map.py (limits mapping), spacing_fit.py (continuum fit), integer_only_audit.py
data/            receipts (json=0)
```

## Not established

- That electrons are composite. Nothing here bears on that question directly.
- A relativistic, chirally protected composite model. This is the case experiment still allows.
- The linear-string continuum constant c∞ (pending: larger boxes needed at JE = 40–80).
