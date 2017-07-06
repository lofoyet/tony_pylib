# -*- coding: utf-8 -*-
# Copyright 2017 Tianpei Liu at Bomoda. All Rights Reserved.
# @Author:    Tony Tianpei Liu
# @Date:   2016-07-26 13:48:32
# ==============================================================================
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function


def strip_spaces(a_string):
    the_unicode = unicode(a_string)
    assert (type(the_unicode) == unicode)
    spaces = [u"\u0020", u"\u1680", u"\u180E", u"\u00A0", u"\u2000", u"\u2001", u"\u2002", u"\u2003",
              u"\u2004", u"\u2005", u"\u2006", u"\u2007", u"\u2008", u"\u2009", u"\u200A", u"\u200B",
              u"\u202F", u"\u205F", u"\u2060", u"\u3000", u"\uFEFF"]

    for space in spaces:
        the_unicode = the_unicode.strip(space)

    return the_unicode
