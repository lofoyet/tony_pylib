# -*- coding: utf-8 -*-
# Copyright 2017 Tianpei Liu at Bomoda. All Rights Reserved.
# @Author:    Tony Tianpei Liu
# @Date:   2017-07-14 18:48:32
# ==============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import Counter
import datetime


class LoadDrop:

    def __init__(self, input_path):

        self.data = []
        with open(input_path, "r") as f:
            for line in f.readlines():
                self.data.append(line.strip())

    def DropDuplicate(self, threshold, progress_interval):

        uniq_dic = {}
        counter = -1
        stt_time = datetime.datetime.now()
        self.data_dropped = []
        for line in self.data:
            counter += 1
            crnt_wd_ct = Counter(line.split("<>")[0])
            if counter == 0:
                uniq_dic[str(counter)] = crnt_wd_ct
                self.data_dropped.append(line)
            else:
                key_c = 0
                for uniq_dic_key in uniq_dic.keys():
                    eql_idx = 0
                    key_c += 1
                    for key in uniq_dic[uniq_dic_key].keys():
                        if key in crnt_wd_ct.keys():
                            if crnt_wd_ct[key] - uniq_dic[uniq_dic_key][key] == 0:
                                eql_idx += 1
                    if len(uniq_dic[uniq_dic_key].keys()) == 0:
                        continue
                    if float(eql_idx / len(uniq_dic[uniq_dic_key].keys())) < threshold:
                        if key_c == len(uniq_dic.keys()):
                            uniq_dic[str(counter)] = crnt_wd_ct
                            self.data_dropped.append(line)

                        else:
                            continue
                    else:
                        break

            crnt_time = datetime.datetime.now()
            if counter % progress_interval == 0:
                print("now processing {}% , {} lines remained".format(
                    str(100 * counter / len(self.data)), str(len(self.data) - counter)))
                print("elapsed time: {}".format(crnt_time - stt_time))

        return self.data_dropped
