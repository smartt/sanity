#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fmt

__license__ = "MIT"
__version__ = "0.1"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."



def taxonomy_tags(s):
    """
    >>> taxonomy_tags('hi there')
    ['hi there']

    >>> taxonomy_tags('hi, there')
    ['hi', 'there']

    >>> taxonomy_tags('hi/there')
    ['hi', 'there']

    >>> taxonomy_tags('hi; there')
    ['hi', 'there']

    >>> taxonomy_tags('Hi, There')
    ['hi', 'there']

    >>> taxonomy_tags('Hi, There friend, How goes it?')
    ['hi', 'there friend', 'how goes it']

    """
    if s is None:
        return None

    input = fmt.strip_tags(s)

    # Normalize delimeters
    for delim in (';', '/', ':'):
        input = input.replace(delim, ',')

    # Stash intentional hyphens
    input = input.replace('-', '*')

    tags = [fmt.slugify(fmt.strip_and_compact_str(tag)).replace('-', ' ').replace('*', '-') for tag in input.split(',')]

    return tags

## ---------------------
if __name__ == "__main__":
    import doctest
    print "Testing..."
    doctest.testmod()
    print "Done."
