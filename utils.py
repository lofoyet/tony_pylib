# -*- coding: utf-8 -*-
import os
import sys
import pickle
import csv
import pandas as pd

def ExtractW2IFromW2V(map_path, idx_path):
    map_w_idx = pd.read_csv(map_path, header=None, sep=",", quoting=csv.QUOTE_NONE,
                                encoding='utf-8', error_bad_lines=False, warn_bad_lines=False).iloc[:, 0:-1]
    map_w_idx.columns = ["word"] + range(0, 200)
    # use the first column to convert word to index, for future embedding look up in tensorflow
    # instead read json file
    # add final unk line
    unk_row = {"word": "<UNK>"}
    for i in range(0, 200):
        unk_row[i] = 0
    row_num = map_w_idx.shape[0]
    for k, v in unk_row.iteritems():
        map_w_idx.loc[row_num, k] = v

    dic_idx = {}
    for i in map_w_idx["word"].iteritems():
        if type(i[1]) != unicode:
            dic_idx["<UNK>"] = i[0]
        else:
            dic_idx[i[1]] = i[0]
    assert ("<UNK>" in dic_idx)
    pickle.dump(dic_idx, open(idx_path,"wb"))