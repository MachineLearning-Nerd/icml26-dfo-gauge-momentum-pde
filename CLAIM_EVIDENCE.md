# Claim-to-evidence audit

This repository contains five paper claims in the live contract. Only two
bounded finite toys have been executed. The toy results are useful evidence
for their exact fixtures, but do not establish the paper-level PDE or theorem
claims.

| Claim | Paper statement | Producer path | Evidence | Status and boundary |
| --- | --- | --- | --- | --- |
| C1 | DFO injects momentum only in Gram-matrix nullspace directions while preserving the instantaneous residual minimization. | <code>src/claim1_gauge_toy.py</code> constructs a fixed 2 x 3 Jacobian, the minimum-norm DF velocity, and the projected momentum. | <code>outputs/claim1_gauge_toy/summary.json</code>; both residual norms are 0.0. | <code>TOY_FINITE_GAUGE_PROJECTION</code>. No nonlinear parametrization, PDE solver, or trajectory-smoothness claim is established. |
| C2 | Proposition A.1 recovers the exact wave crossing at rho=0 with lambda=(1-exp(-2/tau))^-1. | <code>src/claim2_proposition_a1_toy.py</code> evaluates the displayed finite-vector collision identity at four tau values. | <code>outputs/claim2_proposition_a1_toy/summary.json</code>; all four rows are exact to at most 1.11e-16. | <code>TOY_FINITE_COLLISION_ALGEBRA</code>. This is not a wave-PDE solve or a proof check of the continuous-time proposition. |
| C3 | DFO reduces error over standard Dirac-Frenkel dynamics on three low-dimensional PDE benchmarks. | The paper produces this claim through the three stated benchmark simulations and error comparisons. | No benchmark implementation, trajectory, table, or figure reconstruction is present. | <code>UNVERIFIED</code>. |
| C4 | DFO improves error and RDFO reduces runtime on a five-dimensional Fokker-Planck problem. | The paper produces this claim through its MLP, sampling, tSVD/RDFO, error, and runtime protocol. | No Fokker-Planck implementation, checkpoint, metric table, or runtime record is present. | <code>UNVERIFIED</code>. |
| C5 | Algorithm 1 uses truncated SVD, EMA momentum, nullspace projection, and the parameter update in that order. | The paper specifies the algorithmic sequence and its beta=tau/(tau+dt) update. | The source and contract are pinned, but no independent Algorithm 1 implementation is present. | <code>UNVERIFIED</code>. |

## Production order

<code>pinned paper/source and contract -> finite toy producer -> JSON summary ->
focused tests -> scoped dossier and final-state verifier</code>

The two producers are deterministic local Python fixtures. They are not
substitutes for the unavailable nonlinear PDE, benchmark, runtime, or proof
pipelines.

