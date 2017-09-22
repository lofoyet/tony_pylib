# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import sys

def time_count_down(start_time, total_len, counter, interval):
    assert (type(total_len) == int)
    assert (type(counter) == int)
    assert (type(interval) == int)
    if counter % interval == 0:
        current_time = datetime.datetime.now()
        elapsed_time = current_time - start_time
        expected_time = elapsed_time.total_seconds() / (counter + 1) * \
            (total_len - counter)
        expected_time_d, expected_time_d_remain = divmod(
            expected_time, 3600 * 24)
        expected_time_h, expected_time_h_remain = divmod(
            expected_time_d_remain, 3600)
        expected_time_m, expected_time_m_remain = divmod(
            expected_time_h_remain, 60)
        expected_time_s, expected_time_s_remain = divmod(
            expected_time_m_remain, 1)
        expected_time = datetime.time(int(expected_time_h), int(
            expected_time_m), int(expected_time_s)).strftime("%H:%M:%S")
        sys.stdout.write("Now processing %.2f%%. Expected remaining time: %s.\r" % (
            float(counter / total_len) * 100, expected_time))
        print(float(counter / total_len) * 100)
        sys.stdout.flush()