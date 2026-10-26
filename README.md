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
- **r²·mΔ/ħ² = 1**;
- first excited level 6-fold degenerate.

**Measured:**

- The first excited level is exactly 6-fold degenerate on the full lattice (L = 6, 8).
- **Box axis** (JE = 9, JB = 1; cloud width ≈ 1.3 sites):

| L | E₀ | E₁ (P-wave) | gap | r² | r²Δ/(2JE) |
|---|---|---|---|---|---|
| 6 | 23.960538 | 40.320633 | 16.360 | 2.597261 | 2.360 |
| 8 | 29.637907 | 40.403024 | 10.765 | 1.962201 | 1.174 |
| 10 | 30.372714 | 40.299401 | 9.927 | 1.671393 | 0.922 |
| 12 | 30.408253 | 40.278614 | 9.870 | 1.646813 | 0.903 |
| continuum | 31.177 | 41.569 | 10.392 | 1.732 | 1 |

The box error is gone by L = 12–14. E₀ changes by 0.0009 from L = 12 to 14.
The remaining gap to the continuum is **lattice-spacing error**, because the
cloud is only 1.3 sites wide. The spacing axis (wider clouds at L = 14–16) is
running; results go in `data/symscan.hbp`. Until it confirms r²mΔ/ħ² → 1, the
harmonic benchmark counts as *converged in box size, pending in spacing*.

### Linear string (the physics model)

**Pending.** It runs on the same two axes. Its dimensionless constant
c = r²mΔ/ħ² is what converts an e* mass limit into a size limit. It will be
reported only once it is stable in both box size and spacing.

## What experimentalists would see (mapping, `python/experiment_map.py`)

| quantity | current limit | source |
|---|---|---|
| Electron size (LEP form factor) | r < 2.8 × 10⁻¹⁹ m | [arXiv:2506.02450](https://arxiv.org/html/2506.02450v3) |
| Contact-interaction scale | Λ > 21.3 TeV (g²/4π = 1) | same |
| Excited electron e* | mass > 5.6 TeV (Λ = m*) | [CMS, arXiv:2001.04521](https://arxiv.org/abs/2001.04521v2) |
| Electron g − 2 | a_e = 0.00115965218059(13) | [PDG / Fan et al. 2023](https://pdglive.lbl.gov/view/S003MM) |

Mapping for a non-relativistic three-preon cloud, written with the calibration
value c = 1 until the linear-string c converges:

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
python/          experiment_map.py (limits mapping), integer_only_audit.py
data/            receipts (json=0)
```

## Not established

- That electrons are composite. Nothing here bears on that question directly.
- A relativistic, chirally protected composite model. This is the case experiment still allows.
- The linear-string constant c and the harmonic spacing limit (pending, above).
