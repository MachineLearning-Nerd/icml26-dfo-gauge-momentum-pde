# Environment and reproduction boundary

## Recorded environment policy

The machine-readable state permits local CPU and a local GTX 1050 only. It
does not authorize remote, paid, Hugging Face, or Jobs compute. The final
dossier uses the committed toy outputs and does not launch the missing PDE
experiments.

## Lightweight checks

From the repository root:

<code>python3 src/claim1_gauge_toy.py</code>

<code>python3 src/claim2_proposition_a1_toy.py</code>

<code>python3 -m pytest -q tests/test_claim1.py tests/test_claim2_proposition.py</code>

<code>python3 verify_final.py</code>

The final verifier checks source and contract hashes, toy summaries, claim
boundaries, branch/ref hygiene, canonical commit attribution, and the
evidence manifest. It does not download data, run a PDE solver, or claim a
full-paper reproduction.

## Not rerun by the final verifier

- the nonlinear PDE benchmark suite;
- the five-dimensional Fokker-Planck experiment;
- the continuous-time Proposition A.1 proof;
- the paper's full Algorithm 1 training and runtime protocol.

