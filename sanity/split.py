#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import fmt

__license__ = "MIT"
__version__ = "0.2"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."


def on_pattern(r, s):
    """
    Split a string based on matches with a regex pattern.
    Returns a list of tuples, containing a sub-string and a boolean
    indicating whether or not the sub-string matched the regex.

    >>> on_pattern(r'\s', 'hi there')
    [('hi', False), (' ', True), ('there', False)]

    >>> on_pattern(r'\s', 'hithere')
    [('hithere', False)]

    >>> on_pattern(r'[0-9]+', '[555] 555-5555')
    [('[', False), ('555', True), ('] ', False), ('555', True), ('-', False), ('5555', True)]

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

## ---------------------
if __name__ == "__main__":
    import doctest
    print "[split.py] Testing..."
    doctest.testmod()
    print "Done."
