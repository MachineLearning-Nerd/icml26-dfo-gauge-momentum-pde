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

All reachable final commits use:

<code>MachineLearning-Nerd &lt;MachineLearning-Nerd@users.noreply.github.com&gt;</code>

No <code>orx</code>, experiment, author-code, or hidden results branch remains
in the final local or remote ref set.

