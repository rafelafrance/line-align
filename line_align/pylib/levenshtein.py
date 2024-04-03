"""
Functions related to Levenshtein distances.

The functions are geared towards OCR errors and not human
errors. OCR engines will often mistake one letter for another
or drop/add a character (particularly from the ends) but
will seldom transpose characters, which humans do often.

Therefore: I do not consider transpositions in the
Levenshtein distances.
"""

from typing import NamedTuple

import numpy as np


class Distance(NamedTuple):
    dist: int
    idx1: int
    idx2: int


# Modified from: https://en.wikipedia.org/wiki/Levenshtein_distance
def levenshtein(str1: str, str2: str) -> int:
    """
    Compute the Levenshtein distance for 2 strings.

    @param str1 Is a string to compare.
    @param str2 The other string to compare.
    @return The Levenshtein distance is an integer. The lower the number the more
            similar the strings.
    """
    len1: int = len(str1)
    len2: int = len(str2)

    v0: np.array = np.array(list(range(len2 + 1)), dtype=np.int32)
    v1: np.array = np.zeros(len2 + 1, dtype=np.int32)

    for i in range(len1):
        v1[0] = i + 1

        for j in range(len2):
            del_: int = v0[j + 1] + 1
            ins: int = v1[j] + 1
            sub: int = v0[j] if str1[i] == str2[j] else v0[j] + 1

            min_: int = del_ if del_ < ins else ins
            min_ = min_ if min_ < sub else sub

            v1[j + 1] = min_

        v0, v1 = v1, v0

    return v0[len2]


def levenshtein_all(strings: list[str]) -> list[Distance]:
    """
    Compute a Levenshtein distance for every pair of strings in the list.

    @param strings A list of strings to compare.
    @return A sorted list of Distance objects, each contain:
        - dist: The Levenshtein distance of the pair of strings.
        - idx1: The index of the first string compared.
        - idx2: The index of the second string compared.
        The Distance objects are sorted by distance.
    """
    results: list[Distance] = []

    len_ = len(strings)

    for i in range(len_ - 1):
        for j in range(i + 1, len_):
            dist = levenshtein(strings[i], strings[j])
            results.append(Distance(dist, i, j))

    results = sorted(results, key=lambda r: (r.dist, r.idx1, r.idx2))

    return results
