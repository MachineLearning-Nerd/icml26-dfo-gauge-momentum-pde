
#!/usr/bin/env python3
'''Verify the published DFO bounded audit and live GitHub state.'''

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = 'icml26-dfo-gauge-momentum-pde'
CANONICAL_IDENTITIES = {
    ('MachineLearning-Nerd', 'MachineLearning-Nerd@users.noreply.github.com'),
    ('MachineLearning-Nerd', '37579156+MachineLearning-Nerd@users.noreply.github.com'),
}
EXPECTED_BRANCHES = {'main'}
ARCHIVE_SHA = 'abe4a05f8b7a6802d78b78bc8ed009f330859335009c184d0b333ae406fd120e'
SOURCE_SUMS_SHA = '84bf39ff44288f66b73f2cddb76a219d112a5f552b43069dd9239efb134a47cc'
MAIN_TEX_SHA = 'b17cc0a48f9022c0845c9c2d802e6ae12c6ca44fb3a472f170eab44a45aca46b'
MAIN_BBL_SHA = '7ea17b55a931a6aaf80fc68c298e28cfb73485ec5bdd9b4fad9cb1d01151f2fd'
CONTRACT_SHA = 'f762e3cf960ae3b57f14928308a4ba9cee385ed7ff4c50b80575e5766c12e15f'
CLAIM1_SUMMARY_SHA = '501ed71dfaae09e6937254ae3a6a0ef149da8e2dce94f2e40d900a0a68730ee8'
CLAIM1_SUMS_SHA = '9dfd3507c9a03be5ecfe8bf8bd31a4124765207a4ab046cd3b68fc9790096b2d'
CLAIM2_SUMMARY_SHA = '542740c27811d6ce4a6c2e6a616c2f404c964f13ffd2a7bea8b9c634c5c8da3f'
CLAIM2_SUMS_SHA = '5af8a2d35e5865c6670106c6bfc59ab481ab0135a4c7a11e27693ea9d9cc8a5b'
SOURCE_LOCATIONS_SHA = '18c1cf8690771b6b2d758414001826d2140a4eb295b08db00b253d275bb3532c'
EXPECTED_STATUSES = [
    'toy_finite_gauge_projection',
    'toy_finite_collision_algebra',
    'unverified',
    'unverified',
    'unverified',
]
REQUIRED = {
    '.gitignore', 'README.md', 'STATUS.md', 'AUTONOMOUS_STATE.json',
    'contract/live_claims.json', 'evidence/source/SHA256SUMS',
    'evidence/source/arxiv-2605.00284.tar.gz',
    'evidence/claim2_attempt1/source_locations.md',
    'outputs/claim1_gauge_toy/SHA256SUMS',
    'outputs/claim1_gauge_toy/summary.json',
    'outputs/claim2_proposition_a1_toy/SHA256SUMS',
    'outputs/claim2_proposition_a1_toy/summary.json',
    'src/claim1_gauge_toy.py', 'src/claim2_proposition_a1_toy.py',
    'tests/test_claim1.py', 'tests/test_claim2_proposition.py',
    'CLAIM_EVIDENCE.md', 'SOURCE_AUDIT.md', 'ENVIRONMENT.md', 'REPORT.md',
    'AUTHOR_THANK_YOU.md', 'CITATION.cff', 'BRANCH_AUDIT.md',
    'branch-audit.md', 'claims.json', 'EVIDENCE_MANIFEST.json', 'verify_final.py',
}
DOSSIER = {
    'CLAIM_EVIDENCE.md', 'SOURCE_AUDIT.md', 'ENVIRONMENT.md', 'REPORT.md',
    'AUTHOR_THANK_YOU.md', 'CITATION.cff', 'BRANCH_AUDIT.md',
    'branch-audit.md', 'claims.json', 'verify_final.py',
}


def fail(message: str) -> None:
    print(f'FINAL_AUDIT=FAILED {message}', file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True)
    if result.returncode:
        fail(f'command failed: {" ".join(args)}: {result.stderr.strip()}')
    return result.stdout


def current_bytes(path: str) -> bytes:
    local = ROOT / path
    if local.is_file():
        return local.read_bytes()
    result = subprocess.run(['git', 'show', f'HEAD:{path}'], cwd=ROOT, check=False, capture_output=True)
    if result.returncode:
        fail(f'missing path: {path}')
    return result.stdout


def current_json(path: str) -> object:
    try:
        return json.loads(current_bytes(path))
    except json.JSONDecodeError as exc:
        fail(f'invalid JSON in {path}: {exc}')
    return None


def sha256(path: str) -> str:
    return hashlib.sha256(current_bytes(path)).hexdigest()


def verify_git() -> tuple[int, int]:
    origin = run('git', 'config', '--get', 'remote.origin.url').strip()
    require(origin in {
        f'https://github.com/MachineLearning-Nerd/{REPOSITORY}.git',
        f'git@github.com:MachineLearning-Nerd/{REPOSITORY}.git',
    }, f'unexpected origin: {origin}')
    require('ref: refs/heads/main\tHEAD' in run('git', 'ls-remote', '--symref', 'origin', 'HEAD'),
            'remote default branch is not main')
    remote_heads = {}
    for line in run('git', 'ls-remote', '--heads', 'origin').splitlines():
        commit, ref = line.split('\t', 1)
        remote_heads[ref.removeprefix('refs/heads/')] = commit
    require(set(remote_heads) == EXPECTED_BRANCHES, f'remote branch set changed: {remote_heads}')
    for branch in EXPECTED_BRANCHES:
        require(remote_heads[branch] == run('git', 'rev-parse', f'origin/{branch}').strip(),
                f'origin/{branch} is stale')
    local_heads = set(run('git', 'for-each-ref', '--format=%(refname:strip=2)', 'refs/heads').splitlines())
    require(local_heads <= EXPECTED_BRANCHES and run('git', 'branch', '--show-current').strip() == 'main',
            f'local branches changed: {sorted(local_heads)}')
    refs = run('git', 'for-each-ref', '--format=%(refname)', 'refs').splitlines()
    require(not any('refs/original/' in ref for ref in refs), 'refs/original remains')
    identities = set()
    for line in run('git', 'log', '--all', '--format=%an\t%ae\t%cn\t%ce').splitlines():
        if line.strip():
            identities.add(tuple(line.split('\t')))
    require(identities and all(
        (author, author_email) in CANONICAL_IDENTITIES
        and (committer, committer_email) in CANONICAL_IDENTITIES
        and author == 'MachineLearning-Nerd'
        and committer == 'MachineLearning-Nerd'
        for author, author_email, committer, committer_email in identities
    ),
            f'non-canonical reachable identity: {sorted(identities)}')
    require('co-authored-by:' not in run('git', 'log', '--all', '--format=%B').lower(),
            'co-author trailer found')
    commits = int(run('git', 'rev-list', '--count', '--all').strip())
    require(commits >= 5, f'commit count too low: {commits}')
    return len(remote_heads), commits


def verify_source_and_evidence() -> None:
    require(sha256('evidence/source/arxiv-2605.00284.tar.gz') == ARCHIVE_SHA,
            'source archive hash changed')
    require(sha256('evidence/source/SHA256SUMS') == SOURCE_SUMS_SHA,
            'source checksum record changed')
    require(ARCHIVE_SHA in current_bytes('evidence/source/SHA256SUMS').decode(),
            'source checksum record does not bind archive')
    with tarfile.open(ROOT / 'evidence/source/arxiv-2605.00284.tar.gz', 'r:gz') as archive:
        files = [member for member in archive.getmembers() if member.isfile()]
        names = {member.name for member in files}
        main_tex = archive.extractfile('main.tex').read()
        main_bbl = archive.extractfile('main.bbl').read()
    require(len(files) == 23 and sha256_bytes(main_tex) == MAIN_TEX_SHA
            and sha256_bytes(main_bbl) == MAIN_BBL_SHA, 'source archive contents changed')
    require(not any(Path(name).suffix.lower() in {'.py', '.sh', '.ipynb', '.r', '.jl'} for name in names),
            'executable file appeared in source archive')
    require(sha256('contract/live_claims.json') == CONTRACT_SHA,
            'claim contract hash changed')
    require(sha256('outputs/claim1_gauge_toy/summary.json') == CLAIM1_SUMMARY_SHA
            and sha256('outputs/claim1_gauge_toy/SHA256SUMS') == CLAIM1_SUMS_SHA
            and sha256('outputs/claim2_proposition_a1_toy/summary.json') == CLAIM2_SUMMARY_SHA
            and sha256('outputs/claim2_proposition_a1_toy/SHA256SUMS') == CLAIM2_SUMS_SHA
            and sha256('evidence/claim2_attempt1/source_locations.md') == SOURCE_LOCATIONS_SHA,
            'toy evidence hash changed')
    claim1 = current_json('outputs/claim1_gauge_toy/summary.json')
    require(claim1.get('verdict') == 'toy' and claim1.get('df_residual_norm') == 0.0
            and claim1.get('dfo_residual_norm') == 0.0
            and claim1.get('nullspace_momentum') == [0.0, 0.0, 5.0],
            'Claim 1 toy result changed')
    claim2 = current_json('outputs/claim2_proposition_a1_toy/summary.json')
    require(claim2.get('verdict') == 'toy' and claim2.get('all_exact') is True
            and len(claim2.get('rows', [])) == 4
            and max(row.get('max_abs_error_vs_q', 1.0) for row in claim2['rows']) <= 1.2e-16,
            'Claim 2 toy result changed')


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_claims_and_state() -> None:
    claims = current_json('claims.json')
    require(claims.get('repository') == f'MachineLearning-Nerd/{REPOSITORY}'
            and [row.get('status') for row in claims.get('claims', [])] == EXPECTED_STATUSES
            and claims.get('publication_allowed') is False,
            'claim dossier changed')
    state = current_json('AUTONOMOUS_STATE.json')
    require(state.get('phase') == 'published_and_verified'
            and state.get('publication_allowed') is False
            and state.get('branch_set') == ['main']
            and state.get('claim_statuses') == dict(zip(['C1', 'C2', 'C3', 'C4', 'C5'], EXPECTED_STATUSES)),
            'state is not final')
    checkpoint = state.get('last_known_git_commit')
    require(isinstance(checkpoint, str) and len(checkpoint) == 40, 'state checkpoint is not full SHA')
    run('git', 'cat-file', '-e', checkpoint)
    run('git', 'merge-base', '--is-ancestor', checkpoint, 'HEAD')


def verify_manifest() -> None:
    manifest = current_json('EVIDENCE_MANIFEST.json')
    require(manifest.get('schema_version') == 1 and manifest.get('hash_algorithm') == 'sha256',
            'manifest schema changed')
    entries = manifest.get('entries')
    require(isinstance(entries, list) and len(entries) == 26, 'manifest entry count changed')
    seen = set()
    for entry in entries:
        path, expected = entry.get('path'), entry.get('sha256')
        require(isinstance(path, str) and path not in seen and '..' not in Path(path).parts
                and not Path(path).is_absolute(), f'bad manifest path: {path}')
        require(isinstance(expected, str) and len(expected) == 64, f'bad manifest hash: {path}')
        seen.add(path)
        require((ROOT / path).is_file() and sha256(path) == expected, f'manifest mismatch: {path}')
    require(DOSSIER <= seen and 'AUTONOMOUS_STATE.json' not in seen
            and 'EVIDENCE_MANIFEST.json' not in seen, 'manifest coverage or cycle changed')


def verify_hygiene() -> None:
    readme = current_bytes('README.md').decode().lower()
    for phrase in ['citation', 'thank you', 'claim ledger', 'branch inventory', 'full implementation']:
        require(phrase in readme, f'readme phrase missing: {phrase}')
    tracked = run('git', 'ls-files').splitlines()
    require(not any(path == '.DS_Store' or '__pycache__' in path or '.pytest_cache' in path
                    or path.startswith('.venv/') for path in tracked),
            'generated private path is tracked')


def main() -> None:
    branches, commits = verify_git()
    require(set(REQUIRED) <= {path for path in run('git', 'ls-files').splitlines()}
            or all((ROOT / path).is_file() for path in REQUIRED),
            'required dossier path missing')
    verify_source_and_evidence()
    verify_claims_and_state()
    verify_manifest()
    verify_hygiene()
    print('FINAL_AUDIT=VERIFIED '
          f'branches={branches} commits={commits} '
          'claims=C1:toy_finite_gauge_projection,'
          'C2:toy_finite_collision_algebra,C3:unverified,C4:unverified,C5:unverified '
          'publication_allowed=false')


if __name__ == '__main__':
    main()
