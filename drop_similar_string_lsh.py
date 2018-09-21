#! /usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import datetime
from hashlib import sha1

import numpy as np
import pandas as pd

from nltk.tokenize import TweetTokenizer

try:
    from datasketch.minhash import MinHash
    from datasketch.weighted_minhash import WeightedMinHashGenerator
    from datasketch.lsh import MinHashLSH
except ImportError as import_err:
    raise import_err("Please pip install -U datasketch")


class DropNearDuplicate(object):

    def __init__(self):
        self.eng_tokenizer = TweetTokenizer()
        sys.stdout.write("Use unicode.")

    def _create_ngram(self, text, language, char_ngram=3):
        if language == "cn":
            return self._create_ngram_cn(text, char_ngram)
        elif language == "en":
            return self._create_ngram_en(text, char_ngram)

    def _create_ngram_en(self, text, char_ngram=3):
        if isinstance(text, unicode):
            text = self.eng_tokenizer.tokenize(text.encode("utf-8"))
        if len(text) > char_ngram:
            ngram = []
            for head in range(0, len(text) - char_ngram):
                ngram.append("".join(text[head:head + char_ngram]))
            return set(ngram)
        else:
            return set("".join(text))

    def _create_ngram_cn(self, text, char_ngram=3):
        if isinstance(text, unicode):
            text = text.encode("utf-8")
        if len(text) > char_ngram:
            ngram = []
            for head in range(0, len(text) - char_ngram):
                ngram.append(text[head:head + char_ngram])
            return set(ngram)
        else:
            return set(text)

    def _fill_min_hash(self, hash_obj, ngram_set):
        for ngram in ngram_set:
            hash_obj.update(ngram)
        return hash_obj

    def drop_from_dataframe(self,
                            dataframe,
                            by_column,
                            language,
                            threshold=0.5,
                            num_perm=128,
                            min_len=10,
                            char_ngram=3,
                            ):
        assert dataframe.shape[0]
        assert by_column in dataframe.columns
        assert type(dataframe[by_column].iloc[0]) in [unicode, str]

        dataframe = dataframe.drop_duplicates(subset=by_column)
        dataframe.reset_index(drop=True, inplace=True)
        indicator = pd.Series([True] * dataframe.shape[0],
                              index=dataframe.index)
        lsh = MinHashLSH(threshold, num_perm)
        min_hashes = []
        for index, each_text in dataframe[by_column].iteritems():
            mh = MinHash(num_perm)
            ngram_set = self._create_ngram(each_text, language, char_ngram)
            mh = self._fill_min_hash(mh, ngram_set)
            lsh.insert("{:d}".format(index), mh)
            min_hashes.append(mh)
        for index, if_keep in indicator.iteritems():
            if if_keep and len(dataframe[by_column].iloc[index]) > min_len:
                similar_row_indices = map(int, lsh.query(min_hashes[index]))
                first_silimar_row = min(similar_row_indices)
                if first_silimar_row < index:
                    indicator.iat[int(index)] = False
        return dataframe[indicator]
