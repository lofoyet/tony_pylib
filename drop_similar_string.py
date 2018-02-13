#! /usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def similarity(s1, s2):
    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    s1_score = 0
    s2_score = 0

    if s1 == "" or s2 == "":
        return s1_score, s2_score
    else:
        diff = levenshtein(s1, s2)
        if len(s1) < len(s2):
            sim = len(s2) - diff
        else:
            sim = len(s1) - diff

    s1_score = sim / len(s1)
    s2_score = sim / len(s2)

    return s1_score, s2_score


def drop_similar(data, score=0.7):
    for i in range(1, len(data)):
        for j in range(0, i):
            score_1, score_2 = similarity(data[j], data[i])
            if max(score_1, score_2) > score:
                if score_1 > score_2:
                    data[j] = ''
                else:
                    data[i] = ''
            else:
                pass
    return list(filter(None, data))
