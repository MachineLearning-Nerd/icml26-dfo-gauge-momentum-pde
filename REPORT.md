# Scoped reproduction report

## Verdict

<code>INCONCLUSIVE_SCOPED_TO_FINITE_TOYS</code>

| Claim | Result | Evidence |
| --- | --- | --- |
| C1 | <code>TOY_FINITE_GAUGE_PROJECTION</code> | The fixed 2 x 3 fixture gives exact DF and DFO residual norms of 0.0. |
| C2 | <code>TOY_FINITE_COLLISION_ALGEBRA</code> | Four tau values reproduce the declared finite vector identity with maximum error 1.11e-16. |
| C3 | <code>UNVERIFIED</code> | No low-dimensional PDE benchmark artifacts. |
| C4 | <code>UNVERIFIED</code> | No five-dimensional Fokker-Planck artifacts. |
| C5 | <code>UNVERIFIED</code> | No independent Algorithm 1 implementation. |

The source and contract are pinned, but the repository does not contain a
complete DFO solver or the data/checkpoints needed for the paper's numerical
claims. No competition score, formal-proof replacement, or author endorsement
is claimed.

## Exact finite evidence

- C1: <code>df_residual_norm=0.0</code> and
  <code>dfo_residual_norm=0.0</code>; the nullspace momentum is
  <code>[0.0, 0.0, 5.0]</code>.
- C2: tau in <code>{0.25, 0.5, 1.0, 2.0}</code>; all rows are marked
  <code>all_exact=true</code>; maximum recorded error is
  <code>1.1102230246251565e-16</code>.

These finite checks support the stated fixtures only. They do not establish
the universal theorem or any paper-scale benchmark result.

