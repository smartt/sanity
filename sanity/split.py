#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import fmt

__license__ = "MIT"
__version__ = "0.1"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."



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
