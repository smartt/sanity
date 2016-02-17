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

    >>> calendar_date('4/20/2014')
    (datetime.date(2014, 4, 20), '')

    >>> calendar_date('4-20-14')
    (datetime.date(2014, 4, 20), '')

    >>> calendar_date('4-20-2014')
    (datetime.date(2014, 4, 20), '')

    >>> result = calendar_date('coffee on 4/20')
    >>> result == (date(date.today().year, 4, 20), 'coffee on')
    True

    >>> result = calendar_date('3.53 for coffee on 4/20')
    >>> result == (date(date.today().year, 4, 20), '3.53 for coffee on')
    True

    >>> result = calendar_date('3.53 for coffee on 4.20')
    >>> result == (date(date.today().year, 4, 20), '3.53 for coffee on')
    True

    >>> today = date.today()
    >>> res = calendar_date('today')
    >>> res == (today, '')
    True

    >>> res = calendar_date('tomorrow')
    >>> res == (today + timedelta(days=1), '')
    True

    >>> res = calendar_date('coffee tomorrow')
    >>> res == (today + timedelta(days=1), 'coffee')
    True

    >>> calendar_date('foobar')
    (None, 'foobar')

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
    d = None

    if s.find('today') >= 0:
        d = today
        s = s.replace('today', '', 1)

    elif s.find('tomorrow') >= 0:
        d = today + timedelta(days=1)
        s = s.replace('tomorrow', '', 1)

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
        # Split up the patterns so we don't have to test ALL of them if some don't seem likely to match
        slash_patterns = ["%m/%d", "%m/%d/%y", "%m/%d/%Y", "%Y/%m/%d"]
        dash_patterns = ["%m-%d-%y", "%m-%d-%Y", "%Y-%m-%d"]
        dot_patterns = ["%m.%d"]

        use_patterns = []

        if s.find('/') >= 0:
            use_patterns.extend(slash_patterns)

        if s.find('-') >= 0:
            use_patterns.extend(dash_patterns)

        if s.find('.') >= 0:
            use_patterns.extend(dot_patterns)

        # Tokenize and scan for date-like strings
        for pat in use_patterns:
            # If the next bit finds something, `d` will be a datetime object, and
            # `matched_str` will be the string that the code thinks is the date.
            # Everything else will be removed. (Unless a date isn't found at all
            # in the string, in which case `d` will be None and `matched_str` will
            # be whatever we passed-in.
            d, matched_str = extract.date_by_pattern(s, pattern=pat, return_match_str=True)

            if d is not None:
                # If we found a date, remove that part of the string from the source string,
                # but only once.
                s = s.replace(matched_str, '', 1)
                break

    s = _prepstr(s)

    return d, s

# --
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['test', 'unittest', 'doctest'])
    except getopt.GetoptError as err:
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

