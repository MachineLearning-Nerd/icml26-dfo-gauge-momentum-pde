# DFO: Source-Pinned Reproduction Audit

This repository tracks a source-pinned, claim-by-claim audit of:

> **A Dirac-Frenkel-Onsager principle: Instantaneous residual minimization with gauge momentum for nonlinear parametrizations of PDE solutions**

The repository is intentionally evidence-first. It currently contains two bounded algebraic toys; it does **not** contain a full implementation of the DFO PDE solver, the paper's benchmark suite, or an independent verification of the paper's theorem.

| Resource | Link |
| --- | --- |
| Paper | [arXiv:2605.00284](https://arxiv.org/abs/2605.00284) |
| OpenReview submission | [aDPbUSUCwh](https://openreview.net/forum?id=aDPbUSUCwh) |
| Pinned source archive | [`evidence/source/arxiv-2605.00284.tar.gz`](evidence/source/arxiv-2605.00284.tar.gz) |

## Current status

**Overall result: inconclusive.** Claim 1 has a finite linear gauge-projection toy, and Claim 2 has a finite algebraic audit of the collision identity in Proposition A.1. Neither result reproduces a nonlinear PDE, verifies the continuous-time proposition, or reproduces the paper's numerical tables.

The current compute policy allows local CPU and a local GTX 1050 only. It does not allow Hugging Face upgrades, remote compute, paid compute, or jobs. The machine-readable state records this as `publication_allowed: false`.

The next repository action is an independent review of the Claim 2 toy against the literal Proposition A.1 source statement.

## What the paper does

The paper studies local-in-time nonlinear parameterizations of PDE solutions. Standard Dirac-Frenkel dynamics choose a parameter velocity that minimizes the instantaneous PDE residual, but rank deficiency or ill-conditioning in the parameterization Jacobian can make the parameter trajectory non-unique.

The proposed Dirac-Frenkel-Onsager (DFO) principle treats the non-uniqueness as gauge freedom:

1. Compute the minimum-norm Dirac-Frenkel reference velocity `eta_bar` from the residual least-squares problem.
2. Maintain a history variable `m` using an Onsager relaxation filter, `tau * dot(m) = eta_bar - m`.
3. Project the history only into the Jacobian/Gram-matrix nullspace and update parameters with `dot(theta) = eta_bar + lambda * P(theta) * m`.

The paper's time-discrete algorithm uses a truncated SVD, an exponential moving average with `beta = tau / (tau + dt)`, a nullspace projection, and then the parameter update. Its experiments study tangent-space collapse, three low-dimensional PDE examples, and a five-dimensional Fokker-Planck problem. Proposition A.1 analyzes exact wave collision (`rho = 0`) and gives `lambda = (1 - exp(-2/tau))^-1` for the stated continuous-time crossing continuation.

## What this repository contains

| Path | Purpose |
| --- | --- |
| `AUTONOMOUS_STATE.json` | Machine-readable phase, compute policy, next action, and bounded outcomes |
| `STATUS.md` | Short human-readable audit status |
| `contract/live_claims.json` | Five paper claims with an explicit verification contract |
| `evidence/source/arxiv-2605.00284.tar.gz` | Pinned arXiv source archive |
| `evidence/source/SHA256SUMS` | Checksum for the pinned source archive |
| `evidence/claim2_attempt1/source_locations.md` | Source mapping for the Proposition A.1 toy |
| `src/claim1_gauge_toy.py` | Exact finite-dimensional nullspace projection fixture |
| `src/claim2_proposition_a1_toy.py` | Finite algebraic audit of the collision identity |
| `outputs/claim1_gauge_toy/summary.json` | Claim 1 toy result |
| `outputs/claim2_proposition_a1_toy/summary.json` | Claim 2 toy result across four `tau` values |
| `tests/` | Minimal checks for the two bounded artifacts |
| `.trackio/logbook/` | Experiment log for the bounded Claim 2 attempt |

These files are audit artifacts, not a complete DFO implementation. The source archive is the evidence anchor for paper statements; the generated JSON files are the only independent numerical outputs currently present.

## Branch inventory

Only one branch currently exists:

| Branch | Purpose | Current state |
| --- | --- | --- |
| `main` | Source-pinned DFO reproduction audit | Contains the paper-source checksum, claim contract, two bounded toys, and their summaries |

There are no feature, experiment, or results branches in this repository at the time of this audit. Branch names are already clean; no `orx`-style branch rename is needed here.

## Claim ledger: what each claim means and how it is produced

The following claims come from `contract/live_claims.json`. They describe claims made by the paper; they are not automatically established by this repository.

| ID | Paper claim | How the paper produces the claim | Evidence currently in this repo | Status |
| --- | --- | --- | --- | --- |
| C1 | DFO injects momentum only along gauge/nullspace directions, preserving instantaneous residual minimization while selecting smoother parameter trajectories. | Derive the nullspace projector from the Jacobian/Gram matrix, evolve the Onsager history variable, and add only the projected history to the minimum-norm Dirac-Frenkel velocity. | `src/claim1_gauge_toy.py` and `outputs/claim1_gauge_toy/summary.json` verify the residual-preserving identity for a fixed `2 x 3` linear fixture. | **Toy only; full claim unverified** |
| C2 | Proposition A.1 gives exact wave-collision continuation for `rho = 0` when `lambda = (1 - exp(-2/tau))^-1`, while minimum-norm Dirac-Frenkel dynamics fail at collapse. | Analyze the continuous-time wave path, the collision nullspace, the pre-collision memory, and the projected momentum at the collision; see the pinned source at `main.tex:649-714`. | `src/claim2_proposition_a1_toy.py` checks the displayed finite-vector identity at `tau` values `0.25`, `0.5`, `1`, and `2`; all four rows have `all_exact: true`. | **Algebraic toy; PDE/theorem unverified** |
| C3 | DFO reduces error over standard Dirac-Frenkel dynamics on three low-dimensional PDE benchmarks. | Run the rotating-detonation-wave, transport-through-flow-field, and charged-particle/Vlasov simulations with the paper's discretization and compare relative error over time. | No benchmark code, trajectory, metric table, or figure reconstruction is present. | **Unverified** |
| C4 | On a five-dimensional Fokker-Planck problem, DFO improves error and RDFO reduces runtime while preserving accuracy. | Fit the stated MLP, solve the five-dimensional Fokker-Planck equation with the paper's sampling and tSVD/RDFO setup, then compare mean/covariance errors and runtime. | No Fokker-Planck implementation, result table, or runtime measurement is present. | **Unverified** |
| C5 | Algorithm 1 uses truncated SVD, `beta = tau/(tau+dt)` momentum, nullspace projection, and a parameter update in that order. | Implement each algorithm step, record the numerical configuration, and compare the resulting trajectories and costs with the paper's experiments. | The pinned source and claim contract record the claim, but this repository has no implementation of Algorithm 1 beyond the two bounded algebraic fixtures. | **Unverified** |

## Reproduction boundary

It is important to distinguish three statements:

1. **Paper-reported:** a theorem, method, number, or conclusion appearing in the DFO paper.
2. **Source-audited:** the paper source or a repository artifact has been pinned and inspected.
3. **Reproduced here:** this repository independently ran the relevant experiment and stored verifiable output.

At present, this repository supports the second category and two deliberately bounded pieces of the third category. It does not support the full numerical or theoretical claims above.

```text
verdict: inconclusive
claim 1: finite gauge-projection toy only
claim 2: finite collision-algebra toy only
full PDE benchmark executed: no
continuous-time proposition verified: no
```

## Verification commands

From the repository root:

```bash
python3 src/claim1_gauge_toy.py
python3 src/claim2_proposition_a1_toy.py
python3 -m pytest -q tests/test_claim1.py tests/test_claim2_proposition.py  # if pytest is installed
shasum -a 256 evidence/source/arxiv-2605.00284.tar.gz
```

The expected source-archive hash is recorded in `evidence/source/SHA256SUMS`. The toy outputs intentionally report their limited scope rather than a paper-level reproduction verdict.

## Citation

If this audit or the paper is useful, please cite the paper:

```bibtex
@misc{raviola2026dirac,
  title={A Dirac-Frenkel-Onsager principle: Instantaneous residual minimization with gauge momentum for nonlinear parametrizations of PDE solutions},
  author={Matteo Raviola and Benjamin Peherstorfer},
  year={2026},
  eprint={2605.00284},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
  url={https://arxiv.org/abs/2605.00284}
}
```

## Thank you

Thank you to **Matteo Raviola and Benjamin Peherstorfer** for making the DFO paper and its source archive available. The paper gives a clear formulation of gauge momentum for nonlinear PDE parameterizations and provides a useful basis for careful, claim-level reproduction work.
