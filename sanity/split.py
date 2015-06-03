#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import fmt


def on_pattern(r, s):
    """
    Split a string based on matches with a regex pattern.
    Returns a list of tuples, containing a sub-string and a boolean
    indicating whether or not the sub-string matched the regex.

    NOTE: YOU CANNOT PASS A PATTERN WITH GROUPINGS!!! THE RESULTS WILL BE WHACK.

    >>> on_pattern(r'\s', 'hi there')
    [('hi', False), (' ', True), ('there', False)]

    >>> on_pattern(r'\s', 'hithere')
    [('hithere', False)]

    >>> on_pattern(r'[0-9]+', '[555] 555-5555')
    [('[', False), ('555', True), ('] ', False), ('555', True), ('-', False), ('5555', True)]

    # This will work, but it's misleading
    #>>> on_pattern(r'(mid|non|pre|re|semi|under|over)\-\w+', 'hithere')
    #[('hithere', False)]

    # This will totally fail
    #>>> on_pattern(r'(mid|non|pre|re|semi|under|over)\-\w+', 'It was non-relevant indeed')
    #[('It was ', False), ('non-relevant', True), (' indeed', False)]

    """
    bits_that_match = re.findall(r, s)

    match_count = len(bits_that_match)

    if match_count == 0:
        return [(s, False)]

    bits_that_dont = re.split(r, s)

    dont_match_count = len(bits_that_dont)

    new_length = 0

    #
    # Make the two lists the same length
    if match_count > dont_match_count:
        # Pad bits_that_dont
        difference = match_count - dont_match_count

        for i in range(difference):
            bits_that_dont.append('')

        new_length = match_count

    elif dont_match_count > match_count:
        # Pad bits_that_match
        difference = dont_match_count - match_count

        for i in range(difference):
            bits_that_match.append('')

        new_length = dont_match_count

    else:
        # Either size will do
        new_length = match_count

    # print("match")
    # print(bits_that_match)
    # print("dont")
    # print(bits_that_dont)

    new_list = []

    #
    # Now weave them together
    if s.find(bits_that_match[0]) == 0:
        # Start with the matching bits
        for i in range(new_length):
            new_list.append((bits_that_match[i], True))
            new_list.append((bits_that_dont[i], False))

    elif s.find(bits_that_dont[0]) == 0:
        # Start with the matching bits
        for i in range(new_length):
            new_list.append((bits_that_dont[i], False))
            new_list.append((bits_that_match[i], True))

    else:
        # Uhhhh...
        pass

    # print("zipped")
    # print(new_list)

    # Now we have to trim off any extra padding we added because of the matching array lengths
    trim_count = 0
    for tup in reversed(new_list):
        if tup[0] == '':
            trim_count += 1
        else:
            break

    # print("Trim {c}".format(c=trim_count))

    results = new_list[0:(len(new_list)-trim_count)]

    # print("trimmed")
    # print(results)

    return results

def taxonomy_tags(s, split_spaces=False):
    """
    >>> taxonomy_tags('hi there')
    ['hi-there']

    >>> taxonomy_tags('hi, there')
    ['hi', 'there']

    >>> taxonomy_tags('hi/there')
    ['hi', 'there']

    >>> taxonomy_tags('hi; there')
    ['hi', 'there']

    >>> taxonomy_tags('Hi, There')
    ['hi', 'there']

    >>> taxonomy_tags('Hi, There friend, How goes it?')
    ['hi', 'there-friend', 'how-goes-it']

    >>> taxonomy_tags('hi there', split_spaces=True)
    ['hi', 'there']

    >>> taxonomy_tags('hi there, friend', split_spaces=True)
    ['hi', 'there', 'friend']

    >>> taxonomy_tags("the cat's books", split_spaces=True)
    ['the', 'cats', 'books']

    >>> taxonomy_tags('one, "two three", four')
    ['two three', 'one', 'four']

    >>> taxonomy_tags('one "two three" four', split_spaces=True)
    ['two three', 'one', 'four']

    """
    if s is None:
        return None

    tags = []
    s = fmt.strip_tags(s)

    # Extract quoted bits first
    quoted_str_pattern = r'[\ ]?"[^"]*"'
    matched_strings = []

    # Save the matches
    for match in re.findall(quoted_str_pattern, s):
        # Create a tag, removing the quote marks and trailing spaces
        tags.append(match.replace('"', '').strip())
        # But keep track of what we used so we can purge it
        matched_strings.append(match)

    # Remove the matches from the string
    for m in matched_strings:
        s = s.replace(m, '', 1)

    # Now we do regular string splitting
    delimeters = [';', '/', ':']

    if split_spaces:
        delimeters.append(' ')

    # Normalize delimeters
    for delim in delimeters:
        s = s.replace(delim, ',')

    tags.extend([fmt.slugify(fmt.strip_and_compact_str(tag)) for tag in s.split(',') if tag])

    return tags


def _find_troublemakers(s):
    """
    Scan the text and update the trouble_maker dictionary with
    tricky patterns.  This is a black art...

    We'll start with multi-letter (2+), all-caps abbreviations, like this:

    >>> _find_troublemakers('The Hobbit was written by J.R.R. Tolkien.')
    {'J.R.R.': 'nEWSLUGJRR'}

    >>> _find_troublemakers('J.R.R. Tolkien changed society as we know it.')
    {'J.R.R.': 'nEWSLUGJRR'}

    >>> _find_troublemakers('The presentation by H.R. Roberts was wonderful.')
    {'H.R.': 'nEWSLUGHR'}

    >>> _find_troublemakers('H.R. Roberts called J.R.R. Tolkien and Mr. T. about the book.')
    {'T.': 'nEWSLUGT', 'H.R.': 'nEWSLUGHR', 'J.R.R.': 'nEWSLUGJRR'}

    # We also run into bad behavior with dates, like this:
    >>> _find_troublemakers('Some txt (2004) is better than others.')
    {'(2004)': 'nEWSLUGp2004'}

    # This is a problematic sentence structure we'll deal with via a hack
    >>> _find_troublemakers('Last year (again) Mike was better than others.')
    {'n) M': 'nEWSLUGnPSM'}

    # How about this mid-sentence punctuation?!
    >>> _find_troublemakers('Last year really? was better than others.')
    {'? w': 'nEWSLUGQPUNCw'}

    """
    d = dict()

    # First, we're looking for initials
    initials_matches = re.findall(r'\b(([A-Z]\.)+)', s)

    for term in initials_matches:
        d[term[0]] = 'nEWSLUG{st}'.format(st=term[0].replace('.', ''))

    # Now look for years in parenthesis
    paren_num_matches = re.findall(r'(\()([0-9]+?)(\))', s)

    for term in paren_num_matches:
        d["({x})".format(x=term[1])] = 'nEWSLUGp{x}'.format(x=term[1])

    # Now look for capital words that follow words (or numbers) in parenthesis
    blasted_capitals_after_parens = re.findall(r'([a-z0-9])\)\s([A-Z0-9])', s)
    for term in blasted_capitals_after_parens:
        d["{x}) {y}".format(x=term[0], y=term[1])] = 'nEWSLUG{x}PS{y}'.format(x=term[0], y=term[1])

    # Now we go for question marks in the middle of a sentence.  Seriously.
    mid_sentence_punctuation = re.findall(r'(\?)\s+([a-z])', s)
    for term in mid_sentence_punctuation:
        d["? {x}".format(x=term[1])] = 'nEWSLUGQPUNC{x}'.format(x=term[1])

    return d


def _slug_trouble_makers(s, patterns, verbose=False):
    """
    Swap trouble-maker's like 'Mr.' and 'Mrs.' for easily identifiable slugs.

    >>> _slug_trouble_makers('Hello Mrs. Robinson.', patterns={'Mrs.': 'tMPSLUGMRS'})
    'Hello tMPSLUGMRS Robinson.'

    """
    for k, v in patterns.items():
        try:
            s = s.replace(k, v)
        except Exception as e:
            if __debug__ and verbose:
                print('ERROR: _slug_trouble_makers: {e}'.format(e=e))

            continue

    return s


def _unslug_trouble_makers(s, patterns, verbose=False):
    """
    Swap trouble-maker's back in.

    >>> _unslug_trouble_makers('Hello tMPSLUGMRS Robinson.', patterns={'Mrs.': 'tMPSLUGMRS'})
    'Hello Mrs. Robinson.'

    """
    for k, v in patterns.items():
        try:
            s = s.replace(v, k)
        except Exception as e:
            if __debug__ and verbose:
                print('ERROR: _unslug_trouble_makers: {e}'.format(e=e))
            continue

    return s


def sentences(s):
    """Split a block of text into sentences. Or try anyway.

    >>> sentences('')
    []

    >>> sentences("Hello World!")
    ['Hello World!']

    >>> sentences("Hello World. I am a cat.")
    ['Hello World.', 'I am a cat.']

    """
    # These are known trouble-maker patterns, given the period and the likelyhood that the next character
    # will be capitalized.  In other words, to a basic parser, they look like the end of a sentence.
    trouble_slugs = {
        'Det.':  'tMPSLUGDET',
        'Dr.':  'tMPSLUGDR',
        'etc.': 'tMPSLUGetc',
        'Etc.': 'tMPSLUGEtc',
        'Mr.':  'tMPSLUGMISTER',
        'Mrs.': 'tMPSLUGMRS',
        'Ms.':  'tMPSLUGMS',
        '(p.':  'tMPQUOTEPAGECOUNT',
    }

    new_troublemakers = _find_troublemakers(s)

    for k, v in new_troublemakers:
        trouble_slugs[k] = v

    slugged_s = _slug_trouble_makers(s, trouble_slugs)

    bits = re.findall(r'[\w\s\,\:\;]+[\.\!\?\)]\"?', slugged_s)

    unslugged_lines = []

    for txt in bits:
        unslugged_lines.append(_unslug_trouble_makers(txt.strip(), trouble_slugs))

    return unslugged_lines


## ---------------------
if __name__ == "__main__":
    import doctest
    print("[split.py] Testing...")
    doctest.testmod()
    print("Done.")
