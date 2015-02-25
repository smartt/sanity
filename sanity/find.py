#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, timedelta

import extract, fmt

def _prepstr(s):
    """
    >>> _prepstr(s='')
    ''

    >>> _prepstr(s='$')
    '$'

    >>> _prepstr(s='      ')
    ''

    >>> _prepstr(s='hello world')
    'hello world'

    >>> _prepstr(s='hello    world')
    'hello world'

    >>> _prepstr(s='Hello World')
    'hello world'

    >>> _prepstr(s='HELLO WORLD')
    'hello world'

    """

    return fmt.compress_whitespace(s.lower())

def dollar_amount(s):
    #
    # Find the amount
    """
    >>> dollar_amount('19.99')
    (19.99, '')

    >>> dollar_amount('-19.99')
    (-19.99, '')

    >>> dollar_amount('+19.99')
    (19.99, '')

    >>> dollar_amount('$19.99')
    (19.99, '')

    >>> dollar_amount('19.99 for coffee')
    (19.99, 'for coffee')

    >>> dollar_amount('$19.99 for coffee')
    (19.99, 'for coffee')

    >>> dollar_amount('coffee 19.99')
    (19.99, 'coffee')

    >>> dollar_amount('coffee $19.99')
    (19.99, 'coffee')

    >>> dollar_amount('$19.99 for coffee at 4.20 bar')
    (19.99, 'for coffee at 4.20 bar')

    >>> dollar_amount('4.20 $19.99 wine')
    (19.99, '4.20 wine')

    >>> dollar_amount('sold 1,900.99 comics')
    (1900.99, 'sold comics')

    >>> dollar_amount('bought $12,345,900.99 comics')
    (12345900.99, 'bought comics')

    >>> dollar_amount('hi there kitty kat')
    (None, 'hi there kitty kat')

    >>> dollar_amount('19.12345000001')
    (19.12, '')

    >>> dollar_amount('19.129')
    (19.12, '')

    """
    s = _prepstr(s)
    amt = None
    matched_amt = ''

    # First, split up the string and hunt for price-like things
    bits = s.split(' ')

    for chunk in bits:
        if chunk[0] == '$' and len(chunk) > 1:
            # Then we probably have it
            str_amt = extract.price_like(chunk)

            try:
                amt = float(str_amt)
            except (TypeError, ValueError):
                pass
            else:
                if amt:
                    matched_amt = chunk
                    break

    if not amt:
        # Keep looking
        for chunk in bits:
            str_amt = extract.price_like(chunk)

            try:
                amt = float(str_amt)
            except (TypeError, ValueError):
                pass
            else:
                if amt:
                    matched_amt = chunk
                    break

    # If we found something, remove it from the string
    if amt and matched_amt:
        s = s.replace(matched_amt, '', 1)

    s = _prepstr(s.replace('$', ''))

    return amt, s

def calendar_date(s):
    """
    >>> calendar_date('4/20/14')
    (datetime.date(2014, 4, 20), '')

    >>> calendar_date('coffee on 4/20')
    (datetime.date(2015, 4, 20), 'coffee on')

    >>> calendar_date('3.53 for coffee on 4/20')
    (datetime.date(2015, 4, 20), '3.53 for coffee on')

    >>> calendar_date('3.53 for coffee on 4.20')
    (datetime.date(2015, 4, 20), '3.53 for coffee on')

    """
    def _sub_dayofweek(dow, num, s):
        d = today - timedelta(days=today.isoweekday() - num)

        if d > today:
            d = d - timedelta(days=7)

        s = s.replace(dow, '', 1)

        return d, s

    s = _prepstr(s)

    #
    # Find the date.  Default to 'today' if not resolved
    today = date.today()
    d = today

    if s.find('today') >= 0:
        d = timedelta(days=1)
        s = s.replace('today', '', 1)

    elif s.find('yesterday') >= 0:
        d = today - timedelta(days=1)
        s = s.replace('yesterday', '', 1)

    elif s.find('monday') >= 0:
        d, s = _sub_dayofweek('monday', 1, s)

    elif s.find('tuesday') >= 0:
        d, s = _sub_dayofweek('tuesday', 2, s)

    elif s.find('wednesday') >= 0:
        d, s = _sub_dayofweek('wednesday', 3, s)

    elif s.find('thursday') >= 0:
        d, s = _sub_dayofweek('thursday', 4, s)

    elif s.find('friday') >= 0:
        d, s = _sub_dayofweek('friday', 5, s)

    elif s.find('saturday') >= 0:
        d, s = _sub_dayofweek('saturday', 6, s)

    elif s.find('sunday') >= 0:
        d, s = _sub_dayofweek('sunday', 7, s)

    else:
        # tokenize and scan for date-like strings
        def _find_date_by_patterns(s, patterns):
            for pat in patterns:
                d, matched_str = extract.date_by_pattern(s, pat, return_match_str=True)

                if d:
                    #matched_str = d.strftime(pat)
                    s = s.replace(matched_str, '', 1)
                    break

            return d, s

        # TODO: Pull the patterns from some kind of preferences
        d, s = _find_date_by_patterns(s, patterns=("%m/%d", "%m/%d/%y", "%m/%d/%Y", "%m.%d"))

        if not d:
            d = today

    s = _prepstr(s)

    return d, s

# --
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['test', 'unittest', 'doctest'])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    run_doc_tests = False
    run_unit_tests = False
    run_all_tests = False

    for o, a in opts:
        if o in ["--test"]:
            run_all_tests = True

        if o in ["--doctest"]:
            run_doc_tests = True

        if o in ["--unittest"]:
            run_unit_tests = True

    def _run_doctests():
        import doctest

        print("[find.py] Running doctest...")
        doctest.testmod()

        print("Done.")

    if run_all_tests:
        _run_doctests()

    elif run_doc_tests:
        _run_doctests()

    sys.exit(2)

