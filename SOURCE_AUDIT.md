# Source and provenance audit

## Paper identity

- Paper: **A Dirac-Frenkel-Onsager principle: Instantaneous residual minimization with gauge momentum for nonlinear parametrizations of PDE solutions**
- Authors: Matteo Raviola and Benjamin Peherstorfer
- arXiv: [2605.00284](https://arxiv.org/abs/2605.00284)
- OpenReview: [aDPbUSUCwh](https://openreview.net/forum?id=aDPbUSUCwh)
- Current repository: [MachineLearning-Nerd/icml26-dfo-gauge-momentum-pde](https://github.com/MachineLearning-Nerd/icml26-dfo-gauge-momentum-pde)
- Former repository name: <code>icml26-repro-aDPbUSUCwh-dfo-gauge-momentum-pde</code>

## Pinned source

The arXiv source archive is retained at
<code>evidence/source/arxiv-2605.00284.tar.gz</code>.

- Archive SHA-256:
  <code>abe4a05f8b7a6802d78b78bc8ed009f330859335009c184d0b333ae406fd120e</code>
- Archive file count: 23 regular files
- <code>main.tex</code> SHA-256:
  <code>b17cc0a48f9022c0845c9c2d802e6ae12c6ca44fb3a472f170eab44a45aca46b</code>
- <code>main.bbl</code> SHA-256:
  <code>7ea17b55a931a6aaf80fc68c298e28cfb73485ec5bdd9b4fad9cb1d01151f2fd</code>
- No executable files are present in the source archive.
- The archive checksum record is
  <code>evidence/source/SHA256SUMS</code>, SHA-256
  <code>84bf39ff44288f66b73f2cddb76a219d112a5f552b43069dd9239efb134a47cc</code>.

The local five-claim contract is
<code>contract/live_claims.json</code>, SHA-256
<code>f762e3cf960ae3b57f14928308a4ba9cee385ed7ff4c50b80575e5766c12e15f</code>.
The source record and contract are provenance anchors; they do not imply that
the missing experiments were reproduced.

## Independent evidence

The only independent producers currently present are
<code>src/claim1_gauge_toy.py</code> and
<code>src/claim2_proposition_a1_toy.py</code>. Their recorded summaries and
checksum files are committed. No author implementation, benchmark dataset,
PDE checkpoint, or full numerical pipeline is vendored.

