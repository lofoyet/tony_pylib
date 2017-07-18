# -*- coding: utf-8 -*-
# Copyright 2017 Tianpei Liu at Bomoda. All Rights Reserved.
# @Author:    Tony Tianpei Liu
# @Date:   2017-07-10 13:48:32
# ==============================================================================
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function


def strip_spaces(a_string, other_characters = []):
    the_unicode = unicode(a_string)
    assert (type(the_unicode) == unicode)
    spaces = [u"\u0020", u"\u1680", u"\u180E", u"\u00A0", u"\u2000", u"\u2001", u"\u2002", u"\u2003",
              u"\u2004", u"\u2005", u"\u2006", u"\u2007", u"\u2008", u"\u2009", u"\u200A", u"\u200B",
              u"\u202F", u"\u205F", u"\u2060", u"\u3000", u"\uFEFF", u"\n",     u"\t"]

    spaces += other_characters

    for space in spaces:
        the_unicode = the_unicode.strip(space)

    return the_unicode


def strip_character(a_string, characters, if_include_spaces = False):

    # First without spaces
    if if_include_spaces:

        return strip_spaces(a_string, characters)

    else :

        the_unicode = unicode(a_string)

        for character in characters:
            the_unicode = the_unicode.strip(character)

        return the_unicode

