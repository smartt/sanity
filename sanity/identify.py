#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def is_only_numeric(s, *args, **kwargs):
    """
    True if string `s` contains nothing but numbers (and whitespace)

    >>> is_only_numeric('Hi there')
    False

    >>> is_only_numeric('Number 9')
    False

    >>> is_only_numeric('42')
    True

    >>> is_only_numeric('  4   3 2 1')
    True

    """
    non_nums_or_spaces = re.sub(r'[\d\s]', '', s)

    return len(non_nums_or_spaces) == 0

def is_only_whitespace(s, *args, **kwargs):
    """
    If the string only contains spaces and or tabs.


    >>> is_only_whitespace('Hi there')
    False

    >>> is_only_whitespace('42')
    False

    >>> is_only_whitespace('            7 ')
    False

    >>> is_only_whitespace('              ')
    True

    >>> is_only_whitespace(' ')
    True

    """
    for c in s:
        if c not in (' ', '\t'):
            return False

    return True


## ---------------------
if __name__ == "__main__":
    import doctest
    print "[is.py] Testing..."
    doctest.testmod()
    print "Done."

