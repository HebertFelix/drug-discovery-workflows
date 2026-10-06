"""Pairwise alignment and positional conservation against a reference."""

from __future__ import annotations

import numpy as np

# Tiny BLOSUM-like match scores for demo (identity-focused).
MATCH = 2
MISMATCH = -1
GAP = -2


def needleman_wunsch(a: str, b: str) -> tuple[str, str]:
    """Global alignment; returns aligned strings."""
    n, m = len(a), len(b)
    score = np.zeros((n + 1, m + 1), dtype=int)
    ptr = np.zeros((n + 1, m + 1), dtype=np.uint8)  # 1=diag, 2=up, 3=left
    for i in range(1, n + 1):
        score[i, 0] = i * GAP
        ptr[i, 0] = 2
    for j in range(1, m + 1):
        score[0, j] = j * GAP
        ptr[0, j] = 3
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            s = MATCH if ai == b[j - 1] else MISMATCH
            diag = score[i - 1, j - 1] + s
            up = score[i - 1, j] + GAP
            left = score[i, j - 1] + GAP
            best = diag
            p = 1
            if up > best:
                best, p = up, 2
            if left > best:
                best, p = left, 3
            score[i, j] = best
            ptr[i, j] = p
    # traceback
    i, j = n, m
    aa: list[str] = []
    bb: list[str] = []
    while i > 0 or j > 0:
        p = ptr[i, j]
        if i > 0 and j > 0 and p == 1:
            aa.append(a[i - 1])
            bb.append(b[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or p == 2):
            aa.append(a[i - 1])
            bb.append("-")
            i -= 1
        else:
            aa.append("-")
            bb.append(b[j - 1])
            j -= 1
    return "".join(reversed(aa)), "".join(reversed(bb))


def conservation_vs_reference(
    reference: str,
    sequences: list[str],
) -> np.ndarray:
    """Fraction of non-gap ortholog residues matching the reference amino acid.

    Each ortholog is globally aligned to the reference; conservation is mapped
    back to ungapped reference coordinates.
    """
    cons = np.zeros(len(reference), dtype=float)
    if not sequences:
        return cons
    for seq in sequences:
        aln_ref, aln_seq = needleman_wunsch(reference, seq)
        ref_i = -1
        matches = np.zeros(len(reference), dtype=float)
        counted = np.zeros(len(reference), dtype=float)
        for r, s in zip(aln_ref, aln_seq):
            if r == "-":
                continue
            ref_i += 1
            if s == "-":
                continue
            counted[ref_i] = 1.0
            if s == r:
                matches[ref_i] = 1.0
        # positions with a residue in the ortholog contribute; gaps do not
        cons += matches
        # also track coverage separately via counted — for fraction use matches/n_seq
    return cons / float(len(sequences))
