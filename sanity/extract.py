#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime
import re

import cast
import fmt
import split


def date_by_pattern(s, pattern, return_match_str=False):
    """
    >>> date_by_pattern('4/20/2014', '%m/%d/%Y')
    datetime.date(2014, 4, 20)

    >>> date_by_pattern('4/20/2014 is a day', '%m/%d/%Y', return_match_str=True)
    (datetime.date(2014, 4, 20), '4/20/2014')

    >>> date_by_pattern('4-20-2014', '%m-%d-%Y', return_match_str=True)
    (datetime.date(2014, 4, 20), '4-20-2014')

    >>> date_by_pattern('4-20-14', '%m-%d-%y')
    datetime.date(2014, 4, 20)

    >>> today = date.today()
    >>> date_by_pattern('4/20', '%m/%d') == date(today.year, 4, 20)
    True

    >>> date_by_pattern('4.20', '%m.%d') == date(today.year, 4, 20)
    True

    >>> date_by_pattern('4-20', '%m-%d') == date(today.year, 4, 20)
    True

    >>> date_by_pattern('4-20-{}'.format(today.year), '%m-%d-%Y') == date(today.year, 4, 20)
    True

    >>> date_by_pattern('{}-4-20'.format(today.year), '%Y-%m-%d') == date(today.year, 4, 20)
    True

    >>> date_by_pattern('420', '%m/%d')

    """
    # tokenize..
    bits = s.split(' ')
    d = None

    # and scan..
    for bit in bits:
        try:
            parsed_date = datetime.strptime(bit, pattern).date()
        except ValueError:
            continue
        else:
            if parsed_date.year == 1900:
                d = date(datetime.now().year, parsed_date.month, parsed_date.day)
            else:
                d = date(parsed_date.year, parsed_date.month, parsed_date.day)

            break

    if return_match_str:
        # This is a little sketchy because we're returning a variable that is
        # conceptually just in the for-loop scope, but in python in sticks around.
        return d, bit
    else:
        return d


def just_numbers(s, decimals=False):
    """
    >>> just_numbers(123)
    '123'

    >>> just_numbers('123')
    '123'

    >>> just_numbers('1a2b3c')
    '123'

    >>> just_numbers('1-2-3-')
    '123'

    >>> just_numbers(None)
    ''

    >>> just_numbers(7)
    '7'

    >>> just_numbers('-1')
    '-1'

    >>> just_numbers(-3.14)
    '314'

    >>> just_numbers('-3.14')
    '-314'

    >>> just_numbers('-3.14', decimals=True)
    '-3.14'

    >>> just_numbers('-314', decimals=True)
    '-314'

    >>> just_numbers('314', decimals=True)
    '314'

    >>> just_numbers('-3.14.25')
    '-31425'

    >>> just_numbers('-3.14.25', decimals=True)
    '-3.14'

    >>> just_numbers('1,024')
    '1024'

    """
    if decimals:
        tmp = ''.join([i for i in cast.to_str(s) if ((i >= '0') and (i <= '9') or i == '.')])

        parts = tmp.split('.')

        try:
            output = '{a}.{b}'.format(a=parts[0], b=parts[1])
        except IndexError:
            output = parts[0]

    else:
        output = ''.join([i for i in cast.to_str(s) if (i >= '0') and (i <= '9')])

    try:
        if s[0] == '-':
            output = '-{s}'.format(s=output)
    except:
        pass

    return output


def number_range(s):
    """We're looking for <num>-<num>.

    >>> number_range("There were 9-10 cats.")
    (9, 10)

    >>> number_range("There cats were 4 and up.")
    (4, None)

    >>> number_range("There were 7+ cats.")
    (7, None)

    """
    lower = None
    upper = None

    # Start with the easy pattern
    mo = re.search(ur'\b([\d\,\.]+)\s*[-–]\s*([\d\,\.]+)\b', s)

    try:
        lower = int(mo.group(1))
        upper = int(mo.group(2))

    except:
        # Try the '2+' pattern
        mo = re.search(r'\b([\d\,\.]+)\s*\+(?!\d)', s)

        try:
            lower = int(mo.group(1))

        except:
            # Try the '2 and up' pattern.
            mo = re.search(r'\b([\d\,\.]+)\s+and\s+up\b', s)

            try:
                lower = int(mo.group(1))

            except:
                pass

    return (lower, upper)


def email(s, limit=1, liberal=False, clean=False, assume_tld='com'):
    """
    >>> email("hi@there.com")
    'hi@there.com'

    >>> email("hi@THERE.COM")
    'hi@there.com'

    # Two dots is invalid...
    >>> email("hi@there..com")

    # ...but the liberal parser will allow it. This is handy if you plan on
    # doing some cleanup/validation later anyway.
    >>> email("hi@there..com", liberal=True)
    'hi@there..com'

    # ...and the cleaner can clean it
    >>> email("hi@there..com", liberal=True, clean=True)
    'hi@there.com'

    >>> email("hi@there")

    >>> email("hi@there", liberal=True)
    'hi@there'

    >>> email("hi@there", liberal=True, clean=True)
    'hi@there.com'

    >>> email("hi@there", liberal=True, clean=True, assume_tld='net')
    'hi@there.net'

    >>> email("some text, and address hi@there.com and more text")
    'hi@there.com'

    >>> email("     hi@there.com     ")
    'hi@there.com'

    >>> email("Hi There <hi@there.com>")
    'hi@there.com'

    # For backwards compatibility, the default behaviour is to return
    # the first found address...
    >>> email("Hi There <hi@there.com> and foo@bar.co.uk")
    'hi@there.com'

    # ...but you can return more. A limit of zero means to return all.
    >>> email("Hi There <hi@there.com> and foo@bar.co.uk", limit=0)
    ['hi@there.com', 'foo@bar.co.uk']

    >>> email("one hi@there.com and another foo@bar.com address", limit=0)
    ['hi@there.com', 'foo@bar.com']

    >>> email("one hi@there.com and another foo@bar.com address", limit=7)
    ['hi@there.com', 'foo@bar.com']

    """
    results = []
    hits = 0

    if liberal:
        pattern = r'\b<?(\w[\w\.-]*)@([\w\.]+)>?\b'
    else:
        pattern = r'\b<?(\w[\w\.-]*)@(\w+)(\.\w+)(\.\w*)?>?\b'

    matches = re.findall(pattern, s)

    for t in matches:
        try:
            addy = '{front}@{back}'.format(front=t[0], back=''.join(t[1:]).lower())
        except:
            pass
        else:
            if clean:
                addy = re.sub(r'\.+', '.', addy)

                # A lame way to look for what might be a TDL
                might_be_tdls = re.findall(r'\.\w+$', addy)

                if len(might_be_tdls) == 0:
                    addy = '{base}.{tdl}'.format(base=addy, tdl=assume_tld)

            results.append(addy)
            hits += 1

    if hits == 0:
        return None

    elif hits == 1 or limit == 1:
        return results[0]

    else:
        if limit > 0:
            return results[:limit]
        else:
            return results


def price_like(s):
    """
    >>> price_like('')

    >>> price_like('coffee')

    >>> price_like('$19.95')
    '19.95'

    >>> price_like('19.95')
    '19.95'

    >>> price_like('-19.95')
    '-19.95'

    >>> price_like('+19.95')
    '19.95'

    >>> price_like('19.95345')
    '19.95'

    >>> price_like('19.5')
    '19.50'

    >>> price_like('19.')
    '19.00'

    >>> price_like('19')
    '19.00'

    >>> price_like('19.5.34')

    >>> price_like('.19')
    '0.19'

    """
    s = str(s)

    if s.strip() == '':
        return None

    parts = s.split('.')

    if not len(parts):  # == 0
        # This shouldn't happen. split() should always return at least a one-item list
        return None

    if len(parts) == 2:
        dollars = just_numbers(parts[0].strip())
        cents = just_numbers(parts[1].strip())

        # We didn't get any numbers
        if dollars == cents == '':
            return None

    elif len(parts) == 1:
        dollars = just_numbers(parts[0].strip())
        cents = '00'

        # We didn't get any numbers
        if dollars == '':
            return None

    else:
        return None

    if dollars == '':
        dollars = '0'

    if len(cents) == 2:
        pass

    elif len(cents) > 2:
        # Change '12345' to '12'
        cents = cents[:2]

    elif len(cents) == 1:
        # Chagne '5' to '50'
        cents = '%s0' % cents

    else:
        # Change '' to '00'
        cents = '00'

    found_amt = "{d}.{c}".format(d=dollars, c=cents)

    return found_amt


def price_like_float(s):
    """
    >>> price_like_float('')


    >>> price_like_float('$19.95')
    19.95

    >>> price_like_float('19.95')
    19.95

    >>> price_like_float('19.95345')
    19.95

    >>> price_like_float('19.5')
    19.5

    >>> price_like_float('19.')
    19.0

    >>> price_like_float('19')
    19.0

    >>> price_like_float('19.5.34')


    >>> price_like_float('.19')
    0.19

    """

    try:
        return float(price_like(s))

    except (TypeError, ValueError):
        return None


def zipcode(s):
    """
    >>> zipcode(s=90210)
    '90210'
    
    >>> zipcode(s='90210')
    '90210'

    >>> zipcode(s='90210  ')
    '90210'

    >>> zipcode(s='   90210')
    '90210'

    >>> zipcode(s='   90210   ')
    '90210'

    >>> zipcode(s='0210')
    '00210'

    >>> zipcode(s=210)
    '00210'

    >>> zipcode(s='902101234')
    '90210-1234'

    >>> zipcode(s='9021012')
    '00902-1012'

    >>> zipcode(s='90210-1234')
    '90210-1234'

    >>> zipcode(s='90210-12341234')
    '90210-1234'

    >>> zipcode(s='9021012341234')
    '90210-1234'

    """
    z = just_numbers(s)[:9]

    length = len(z)
    
    # Add leading zeros if the ZIP is less than 5 chars
    if length < 5:
        z = fmt.add_leading_padding(s=z, c='0', target_length=5)
    
    elif length == 5:
        pass

    elif length < 9:
        z = fmt.add_leading_padding(s=z, c='0', target_length=9)

    # Now put the '-' back in
    if len(z) == 9:
        z = '{front}-{back}'.format(front=z[0:5], back=z[5:])
        
    return z


def matching_pattern_but_not_others(s, pattern, others):
    """
    @param    s          String to process
    @param    pattern    Regex pattern matching the thing(s) we want.
    @param    others     Iterable containing regex patterns matching things we don't want.

    @returns  List of matches

    This test extracts numbers that aren't followed by an uppercase character: (And yes, you'd be
    better off using a look-ahead pattern for this instead, hence this is just a contrived example.)
    >>> matching_pattern_but_not_others(s='Hi 42 there 22B cars', pattern=r'[\d]+', others=[r'[\d]+[A-B]'])
    ['42']

    >>> matching_pattern_but_not_others(s='Hi 42 there 42B cars', pattern=r'[\d]+', others=[r'[\d]+[A-B]'])
    ['42']

    """
    # Reduce the string, eliminating the sub-strings that match acceptable patterns
    s = fmt.substitute_patterns_with_char(s, patterns=others, repl_char='x')

    # Then look for the desired pattern
    return re.findall(pattern=pattern, string=s)


def word_index(txt):
    """
    We're going a build a structure like this:
    
    {
        '<word>': [<pos>, <pos>, <pos>],
        ...
    }
    
    ...where 'word' is a word in the `txt`, and `pos` is an integer
    indicating the position(s) that said word can be found in the string.

    >>> word_index('The cat likes cat treats.')
    {'the': [0], 'treats': [4], 'likes': [2], 'cat': [1, 3]}

    """
    tree = dict()

    # Normalize the text we're working with.
    compressed_whitespace_txt = fmt.compress_whitespace(txt)

    # We also want a version of the string with no punctuation so that punctuation isn't
    # confusing the string matching.
    working_txt = fmt.remove_punctuation(compressed_whitespace_txt)

    # Now split on spaces, lowercasing all words in the process.
    bits = [s.lower() for s in working_txt.split(' ')]

    for pos, word in enumerate(bits):
        try:
            tree[word].append(pos)
        except KeyError:
            tree[word] = [pos]

    return tree


def snippet(keywords, txt, preserve_order=False, before=3, after=3):
    """
    Given a block of text, extract the shortest snippet containing the single, or two-closest, supplied keywords.

    @param   keywords         Iterable The keywords to search for.
    @param   txt              String   Text to search within.
    @param   preserve_order   Bool     True if the order of keywords matters. Default is False.
    @param   before           Integer  The number of words before the first keyword to include. Default is 3.
    @param   after            Integer  The number of words after the first keyword to include. Default is 3.

    >>> t = "The domestic cat is a small, usually furry, domesticated, and carnivorous mammal. They are often called a housecat when kept as an indoor pet or simply a cat when there is no need to distinguish them from other felids and felines. Cats are often valued by humans for companionship and their ability to hunt vermin and household pests."

    # With one keyword, we return the first instance
    >>> snippet(keywords='cat', txt=t)
    'The domestic cat is a small,'

    # Multiple keywords is better
    >>> snippet(keywords=['indoor', 'cat'], txt=t)
    'kept as an indoor pet or simply a cat when there is'

    # When only one word is found...
    >>> snippet(keywords=['cat', 'dog'], txt=t)
    'The domestic cat is a small,'

    >>> snippet(keywords=['dog', 'cat'], txt=t)
    'The domestic cat is a small,'

    >>> snippet(keywords=['indoor', 'cat'], txt=t, before=1, after=1)
    'an indoor pet or simply a cat when'

    # When not found, return an empty string
    >>> snippet(keywords=['dog'], txt=t)
    ''

    >>> snippet(keywords=['and', 'cats'], txt=t)
    'from other felids and felines. Cats are often valued'

    >>> snippet(keywords=['cats', 'and'], txt=t)
    'from other felids and felines. Cats are often valued'

    >>> snippet(keywords=['cats', 'and'], txt=t, preserve_order=True, before=0, after=0)
    'Cats are often valued by humans for companionship and'

    # This is an interesting case. We'll be returning the snippet with the shortest
    # distance between any two words in the list.
    >>> snippet(keywords=['when', 'and', 'cat'], txt=t)
    'or simply a cat when there is no'

    # To show that we can handle the end of a string (where 'after' would overflow.)
    >>> snippet(keywords=['vermin', 'pests'], txt=t)
    'ability to hunt vermin and household pests.'

    # To show that we can handle the beginning of a string (where 'before' would overflow.)
    >>> snippet(keywords=['The', 'cat'], txt=t)
    'The domestic cat is a small,'

    """
    # First, make sure `keywords` is iterable
    if not hasattr(keywords, '__iter__'):
        keywords = (keywords,)

    # If we have no keywords, we're done.
    if len(keywords) == 0:
        return ''

    # We keep a sliced version with punctuation to use when building the snippet.
    sliced_txt = fmt.compress_whitespace(txt).split(' ')

    # Now we use the text to create an index-table of words by position.
    tree = word_index(txt)

    start = None
    end = None

    # Now, let's remove any keywords that aren't even in the text. This may simplify the lookup.
    usable_keywords = []
    for key in keywords:
        try:
            _ = tree[key]
        except KeyError:
            continue
        else:
            usable_keywords.append(key)

    # Let's handle the single-keyword case first:
    if len(usable_keywords) == 1:
        try:
            pos = tree[usable_keywords[0]][0]
        except (IndexError, KeyError):
            # The word wasn't found
            return ''
        else:
            start = pos
            # Add 1 to move past the keyword
            end = pos + 1

    else:
        # Now that we know where each word is, let's find the shortest distances between
        # the keywords
        closest = None

        for pos, key in enumerate(usable_keywords):
            if pos == len(usable_keywords):
                # We're at the end of the list
                break

            # No need to catch KeyError since we've already eliminated non-existant keys
            key_word_positions = tree[key]

            compare_to_words = usable_keywords[pos+1:]

            for other_word in compare_to_words:
                # print('compare', key, 'with', other_word)

                other_word_positions = tree[other_word]
                # print(key_word_positions, other_word_positions)

                for p1 in key_word_positions:
                    last_distance = None

                    for p2 in other_word_positions:
                        distance = abs(p1 - p2)  # Use abs() to keep the number positive
                        # print('distance between:', p1, p2, 'is:', distance,'last:', last_distance)

                        if last_distance is not None and distance > last_distance:
                            # then we're not going to get any closer
                            break

                        if closest is None or distance < closest:
                            if preserve_order and p2 < p1:
                                continue

                            closest = distance

                            if p1 <= p2:
                                start = p1
                                end = p2 + 1  # To skip the keyword
                            else:
                                start = p2
                                end = p1 + 1  # To skip the keyword

                        last_distance = distance

        # print('closest is', closest, 'slice:', start, end)

    # If we didn't find a slice...
    if start is None or end is None:
        return ''

    # Expand the indexes to include the before and after words
    start = start - before
    end = end + after

    if start < 0:
        start = 0

    if start > len(sliced_txt):
        end = len(sliced_txt)

    return ' '.join(sliced_txt[start:end])


def word_frequency(s, word):
    """Return the number of times `word` is found in `s`.

    >>> word_frequency("The big cat caught a big mouse", "dog")
    0

    >>> word_frequency("The big cat caught a big mouse", "cat")
    1

    >>> word_frequency("The big cat caught a big mouse", "big")
    2

    >>> word_frequency("The big cat caught a big catfish", "big")
    2

    >>> word_frequency("It is ok to spook the hook", "ok")
    1

    """
    # normalize to lowercase with no punctuation
    s = fmt.remove_punctuation(s.lower())
    word = word.lower()

    # Neat Python feature that let's us split on a word. By breaking the string using the word, we
    # can deduce how often it was found.
    bits = re.split(r'\b{w}\b'.format(w=word), s)

    hit_count = len(bits) - 1

    if hit_count < 0:
        return 0
    else:
        return hit_count


DEFAULT_SKIP_WORDS = ['a', 'an', 'and', 'be', 'eg', 'for', 'if' 'in', 'is', 'not', 'of', 'on', 'or', 'that', 'the', 'to']
def top_word_frequency(s, minimum=1, limit=30, exclude=DEFAULT_SKIP_WORDS):
    """Return a structure containing the top `limit` number of words used in the document by their frequency of use.

    @param    s            String    The text to process.
    @param    minimum      Int       The lower limit a word must occur more than to be in the results. Default 1.
    @param    limit        Int       The maximum number of words to return. Default 30.
    @param    exclude      Iterable  A list of words to exclude from the results. Default None.

    >>> top_word_frequency("")
    []

    >>> top_word_frequency("The big cat caught a big mouse")
    [('big', 2)]

    >>> top_word_frequency("The big cat caught a big mouse", exclude=['big'])
    []

    >>> top_word_frequency("The big cat caught a big mouse that the dog liked because it looked like a cat.", exclude=None)
    [('a', 2), ('big', 2), ('cat', 2), ('the', 2)]


    >>> top_word_frequency("Sea shells on the sea shore make the sea home to sea shells.", exclude=['the', 'cat'])
    [('sea', 4), ('shells', 2)]

    """
    if not hasattr(exclude, '__iter__'):
        exclude = ()

    results = []

    # We'll leverage our word_index structure which returns a dictionary keyed by words, pointing at a list of positions in the text.
    # We'll count the number of positions to compute frequecy.
    d = word_index(s)

    # Now we iterate, skipping the lower-bounds, and converting into a list of tuples
    for k, v in d.items():
        if k in exclude:
            continue

        count = len(v)
        if count > minimum:
            results.append((k, count))

    # Return sorted list with up to `limit` items.
    return sorted(results, key=lambda x: x[1], reverse=True)[:limit]


def top_line_lenths(s, limit=30):
    """Return structure showing the top-`limit` line lengths along with their frequency.

    >>> top_line_lenths("")
    []

    >>> top_line_lenths("Hi there; this is pretty nice.")
    [(6, 1)]

    >>> top_line_lenths("Hi there. This is pretty nice. I guess I could use it somewhere.")
    [(7, 1), (4, 1), (2, 1)]

    >>> top_line_lenths("Hi there. This is pretty nice. Another four words here.")
    [(4, 2), (2, 1)]

    """
    results = []

    bits = split.sentences(s)

    d = dict()

    # Make something like:
    # {
    #   <line_length>: <count>,
    # }

    for line in bits:
        words = line.split(' ')

        try:
            d[len(words)] += 1
        except:
            d[len(words)] = 1

    for k, v in d.items():
        results.append((k, v))

    # Return sorted list with up to `limit` items.
    return sorted(results, key=lambda x: x[0], reverse=True)[:limit]

    return results

def word_count(s):
    """
    >>> word_count(None)

    >>> word_count(10)

    >>> word_count("one two three four five")
    5

    >>> word_count("one.two three-four five")
    3

    """
    if isinstance(s, (str, unicode)):
        return len(s.split())
    else:
        return None

## ---------------------
if __name__ == "__main__":
    import doctest
    print("[extract.py] Testing...")
    doctest.testmod()
    print("Done.")
