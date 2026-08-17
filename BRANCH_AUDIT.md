# Branch audit

The published repository has one public branch:

| Branch | Role | State |
| --- | --- | --- |
| <code>main</code> | Canonical DFO source pins, bounded toys, claim contract, dossier, and final verifier | Default and only remote branch |

The former local backup branch
<code>backup/pre-machinelearning-nerd-attribution</code> contained superseded
pre-normalization commits and was removed after confirming it was absent from
the remote. The stale <code>refs/original</code> attribution ref was also
removed.

All reachable final commits use the MachineLearning-Nerd account. The existing
audit history uses the account-scoped GitHub noreply address
<code>37579156+MachineLearning-Nerd@users.noreply.github.com</code>; later
publication tooling may use the shorter
<code>MachineLearning-Nerd@users.noreply.github.com</code> alias. Both are
MachineLearning-Nerd-owned GitHub noreply identities.

No <code>orx</code>, experiment, author-code, or hidden results branch remains
in the final local or remote ref set.
