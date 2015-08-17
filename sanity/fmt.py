#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import isfunction
from numeraltable import NUMBER_WORDS
import re
import unicodedata

import cast
from uniasciitable import ASCII_MAP


RE_TAG = re.compile(r'<[^>]*?>')
RE_TAG_PARA_BR = re.compile(r'<[\s\/]*(p|br)[\s\/]*>')
RE_WHITESPACE = re.compile(r'\s+')


def _power_as_word(length):
    values = (
        '',
        '',
        '',
        'hundred',
        'thousand',
        'thousand',
        'hundred',
        'million',
        'million',
        'hundred',
        'billion',
        'billion',
        'hundred',
    )

    try:
        return values[length]
    except:
        return ''


def _number_power(n, c=0):
    """
    This is an odd one, for sure. Given a number, we return a tuple that tells us
    the numerical format to use.  It makes a little more sense if you think of
    the second number in the tuple as a pointer into the list:
        ('', 'hundred', 'thousand', 'million', ...)

    ...so, given the input, '100', we return (1, 1), which can be read as (1, 'hundred')

    This could easily have been a lookup table of reasonable size,
    but what's the fun of that when we can use recursion?

    >>> _number_power('1')
    (1, 0)

    >>> _number_power('10')
    (10, 0)

    >>> _number_power('23')
    (10, 0)

    >>> _number_power('100')
    (1, 1)

    >>> _number_power('200')
    (1, 1)

    >>> _number_power('1000')
    (1, 2)

    >>> _number_power('1234')
    (1, 2)

    >>> _number_power('10000')
    (10, 2)

    >>> _number_power('100000')
    (100, 2)

    >>> _number_power('987654')
    (100, 2)

    >>> _number_power('1000000')
    (1, 3)

    >>> _number_power('10000000')
    (10, 3)

    >>> _number_power('100000000')
    (100, 3)

    >>> _number_power('1000000000')
    (1, 4)

    """
    s = str(n)
    # Regardless of the number passed-in, we only want a leading '1' followed by a string of '0's.
    bits = ['1']
    for ch in s:
      bits.append('0')

    s = ''.join(bits[:-1])
    
    n = int(s)
    l = len(s)
      
    if l > 3:
        num, new_c = _number_power(s[:-3], c + 1)
      
        return (num, new_c)
      
    elif n == 100:
        return (100 if c > 0 else 1, c + 1)

    elif n == 10:
        return (10, c + 1 if c > 0 else 0)

    else:
        return (1, c + 1 if c > 0 else 0)


def number_as_words(num, whole_only=True, add_leading_zero_to_floats=True):
    """
    The default behavior is Chicago style, where numbers <= 100 are
    spelled-out, along with whole numbers > 100.

    If you want any number > 100 spelled-out, set `whole_only` = False.

    >>> number_as_words(None)
    ''

    Non-numbers are returned as-is
    >>> number_as_words('cat')
    'cat'

    Floats are returned as-is
    >>> number_as_words(3.14)
    3.14

    Unless the don't have a leading zero
    >>> number_as_words('.14')
    '0.14'

    >>> number_as_words('.14', add_leading_zero_to_floats=False)
    '.14'

    >>> number_as_words(0)
    'zero'

    >>> number_as_words(1)
    'one'

    >>> number_as_words('1')
    'one'

    >>> number_as_words('10')
    'ten'

    >>> number_as_words(42)
    'forty-two'

    >>> number_as_words('99')
    'ninety-nine'

    >>> number_as_words('100')
    'one hundred'

    >>> number_as_words('101')
    '101'

    >>> number_as_words('110')
    '110'

    >>> number_as_words('190')
    '190'

    >>> number_as_words('200')
    'two hundred'

    >>> number_as_words('260')
    '260'

    >>> number_as_words('600')
    'six hundred'

    >>> number_as_words('1000')
    'one thousand'

    >>> number_as_words('1520')
    '1520'

    >>> number_as_words('1500')
    'fifteen hundred'

    >>> number_as_words('10000')
    'ten thousand'

    >>> number_as_words('100000')
    'one hundred thousand'

    >>> number_as_words('1000000')
    'one million'

    >>> number_as_words('2000')
    'two thousand'

    >>> number_as_words('2001')
    '2001'

    >>> number_as_words('2,001')
    '2,001'

    >>> number_as_words('2001', whole_only=False)
    'two thousand one'

    >>> number_as_words('2,001', whole_only=False)
    'two thousand one'

    >>> number_as_words('2342', whole_only=False)
    'two thousand three hundred forty-two'

    >>> number_as_words('21,342', whole_only=False)
    'twenty-one thousand three hundred forty-two'

    >>> number_as_words('23000')
    'twenty-three thousand'

    >>> number_as_words('23001')
    '23001'

    >>> number_as_words('421,342', whole_only=False)
    'four hundred twenty-one thousand three hundred forty-two'

    >>> number_as_words('5,421,342', whole_only=False)
    'five million four hundred twenty-one thousand three hundred forty-two'

    >>> number_as_words('15,421,342', whole_only=False)
    'fifteen million four hundred twenty-one thousand three hundred forty-two'

    >>> number_as_words('715,421,342', whole_only=False)
    'seven hundred fifteen million four hundred twenty-one thousand three hundred forty-two'

    >>> number_as_words('2,715,421,342', whole_only=False)
    'two billion seven hundred fifteen million four hundred twenty-one thousand three hundred forty-two'

    >>> number_as_words('40,715,421,342', whole_only=False)
    'forty billion seven hundred fifteen million four hundred twenty-one thousand three hundred forty-two'

    >>> number_as_words('540,715,421,342', whole_only=False)
    'five hundred forty billion seven hundred fifteen million four hundred twenty-one thousand three hundred forty-two'

    That's far enough
    >>> number_as_words('1,540,715,421,342', whole_only=False)
    '1,540,715,421,342'

    """
    global NUMBER_WORDS

    if num is None:
        return ''

    try:
        s = str(num).replace(',', '')
    except:
        return num

    # This technically isn't going to return a word, but it will help format
    # the float to be more Chicago-compliant:
    decimal_pos = s.find('.')
    if decimal_pos == 0:
        # This might be a float, but we should add a leading zero
        if add_leading_zero_to_floats is True:
            return '0{num}'.format(num=s)
        else:
            return num

    elif decimal_pos >= 0:
        # This might be a float that we can't work with
        return num

    # If we can't cast it into an int at this point, then we can't work with it.
    try:
        i = int(s)
    except:
        return num

    # We cheat with numbers under 100--we use a look-up table :-)
    if i <= 101:
        try:
            return NUMBER_WORDS[i]
        except:
            pass

    else:
        # For numbers over 100, Chicago only wants them spelled-out if the non-zero leading bits
        # are still under 100.  Ex., Given the number 23,000, the non-zero leading bits are '23',
        # so this can be converted.  A number like 23,456 would not (unless the caller has requested
        # to disable the `whole_only` flag.
        # 
        # Given s == 100000...
        non_zero_bit = s.rstrip('0')  # == '1'
        remainder = s[len(non_zero_bit):]  # == '00000'
        non_zero_int = int(non_zero_bit)  # == 1

        if non_zero_int < 100 and len(remainder) > 1:  # == yes
            is_whole = True
        else:
            is_whole = False

        leading_tens, multiple = _number_power('1{remain}'.format(remain=remainder))  # == 100, 2
        leading_str = str(leading_tens)  # == '100'

        # If the leading_str is longer than the non_zero_bit, then we need to slice
        # off a larger non_zero_bit.  Ex., given 10000, our non_zero_bit would start 
        # as '1', but the leading_str would be '10' (so we can return 'ten thousand'.)
        if len(leading_str) > len(non_zero_bit):  # == yes
            non_zero_bit = s[0:len(leading_str)]  # == '100'
            non_zero_int = int(non_zero_bit)  # == 100

        if whole_only is True:
            if non_zero_int < 101 and is_whole:
                bits = []
                bits.append(number_as_words(non_zero_bit))

                if multiple == 1:
                    bits.append('hundred')
                elif multiple == 2:
                    bits.append('thousand')
                elif multiple == 3:
                    bits.append('million')
                elif multiple == 4:
                    bits.append('billion')

                return ' '.join(bits)

        else:
            # Build a string from the number, no matter what the size
            bits = []
            l = len(s)

            if l == 3:
                bits.append(number_as_words(s[0:1]))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:3]))

            elif l == 4:
                bits.append(number_as_words(s[0:1], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:], whole_only=whole_only))

            elif l == 5:
                bits.append(number_as_words(s[0:2], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[2:], whole_only=whole_only))

            elif l == 6:
                bits.append(number_as_words(s[0:1], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:], whole_only=whole_only))

            elif l == 7:
                bits.append(number_as_words(s[0:1], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:], whole_only=whole_only))

            elif l == 8:
                bits.append(number_as_words(s[0:2], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[2:], whole_only=whole_only))

            elif l == 9:
                bits.append(number_as_words(s[0:1], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:], whole_only=whole_only))

            elif l == 10:
                bits.append(number_as_words(s[0:1], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:], whole_only=whole_only))

            elif l == 11:
                bits.append(number_as_words(s[0:2], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[2:], whole_only=whole_only))

            elif l == 12:
                bits.append(number_as_words(s[0:1], whole_only=whole_only))
                bits.append(_power_as_word(l))
                bits.append(number_as_words(s[1:], whole_only=whole_only))

            else:
                return num

            return ' '.join(bits)

    return num


def list_as_comma_string(bits, serial_comma=False):
    """
    >>> list_as_comma_string([])
    ''

    >>> list_as_comma_string(['hi'])
    'hi'

    >>> list_as_comma_string(['hi', 'there'])
    'hi and there'

    >>> list_as_comma_string(['hi', 'there', 'world'], serial_comma=False)
    'hi, there and world'

    >>> list_as_comma_string(['hi', 'there', 'world'], serial_comma=True)
    'hi, there, and world'

    >>> list_as_comma_string(['hi', 'there', 'world', 'invaders'], serial_comma=False)
    'hi, there, world and invaders'

    >>> list_as_comma_string(['hi', 'there', 'world', 'invaders'], serial_comma=True)
    'hi, there, world, and invaders'

    """
    if len(bits) > 2:
        i = 0
        # Add a comma after each bit
        while i < len(bits) :
            bits[i] = '{bit},'.format(bit=bits[i])
            i += 1

    # If we have more than one bit, stick the word 'and' between the last two bits
    if len(bits) > 1:
        if not serial_comma:
            # Strip the comma off the second-to-last bit
            bits[-2] = bits[-2].rstrip(',')

        bits.insert(len(bits)-1, 'and')

    # Since we'll have a comma at the end, strip it off before returning the new string
    return ' '.join(bits).rstrip(',')


def compress_whitespace(s, keep_ends=False):
    """
    Convert whitespace (ie., spaces, tabs, linebreaks, etc.) to spaces, and
    compress multiple-spaces into single-spaces.

    >>> compress_whitespace('   Oh   hai    there   ')
    'Oh hai there'

    >>> compress_whitespace('      ')
    ''

    >>> compress_whitespace("hi@there.com")
    'hi@there.com'

    >>> compress_whitespace("  hi   @ there . com ")
    'hi @ there . com'

    >>> compress_whitespace("  hi   @ there . com ", keep_ends=True)
    ' hi @ there . com '

    """
    # Using the pre-compiled pattern is a bit faster when calling
    # multiple times.  (Well, millions of times... ;-)
    global RE_WHITESPACE

    if keep_ends:
        return RE_WHITESPACE.sub(' ', s)
    else:
        return RE_WHITESPACE.sub(' ', s.strip())


def strip_and_compact_str(s):
    """
    Remove tags, spaces, etc.  Basically, if someone passed in multiple
    paragraphs, we're going to compact the text into a single block.

    >>> strip_and_compact_str('Hi there. <br /><br />Whats up?')
    'Hi there. Whats up?'

    >>> strip_and_compact_str('     Hi         there. <br />    <br />  Whats    up?   ')
    'Hi there. Whats up?'

    >>> strip_and_compact_str('''\t  Hi \r there. <br /><br />Whats up?''')
    'Hi there. Whats up?'

    >>> strip_and_compact_str('<p>Hi there. <br /><br />Whats up?</p>')
    'Hi there. Whats up?'

    >>> strip_and_compact_str("Hi there.  Let's have tea.")
    "Hi there. Let's have tea."

    >>> strip_and_compact_str(" Hi there ")
    'Hi there'

    >>> strip_and_compact_str("<i>Hi there.</i><i>Let's have tea.")
    "Hi there.Let's have tea."

    >>> strip_and_compact_str("hi@there.com")
    'hi@there.com'

    >>> strip_and_compact_str("  hi   @ there . com")
    'hi @ there . com'

    >>> strip_and_compact_str(None)


    """
    if not isinstance(s, (str,)):
        return s

    # Strip tabs
    s = strip_tags(s)

    # Compact whitespace
    s = compress_whitespace(s)

    return s


def super_flat(s):
    """
    >>> super_flat('')
    ''

    >>> super_flat(None)
    ''

    >>> super_flat('123-456-abc')
    '123456ABC'

    """
    if s is None:
        return ''

    return slugify(s).upper().replace('-', '')


def slugify(s):
    """
    >>> slugify('oh hai')
    'oh-hai'

    >>> slugify('OH HAI')
    'oh-hai'

    >>> slugify('"oh_hai!"')
    'oh-hai'

    >>> slugify('"oh_hai?"')
    'oh-hai'

    >>> slugify("oh_hai!'s")
    'oh-hais'
    """
    if s is None:
        return s

    value = re.sub('[^\w\s-]', '', str(s)).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    value = re.sub('[_\s]+', '-', value)
    return value


def add_leading_padding(s, c=' ', target_length=-1):
    """
    >>> add_leading_padding(s='hi')
    'hi'
    
    >>> add_leading_padding(s='hi', target_length=10)
    '        hi'
    
    >>> add_leading_padding(s='hi', c='-', target_length=3)
    '-hi'
    
    >>> add_leading_padding(s=900)
    '900'
    
    >>> add_leading_padding(s=900, c=0, target_length=5)
    '00900'
    
    >>> add_leading_padding(s='hit', target_length=2)  # See what I did there?
    'hi'
    
    >>> add_leading_padding(s='9021012', c='0', target_length=9)
    '009021012'
    
    """
    z = str(s)
    
    if target_length > 0:
        z = z[:target_length]
        sub_char = str(c)
        actual_length = len(z)

        if actual_length < target_length:
            bits = []
            for i in range(0, target_length - actual_length):
                bits.append(sub_char)
        
            bits.append(z)
    
            z = ''.join(bits)
    
    return z


def escape(s):
    """
    Returns the given string with ampersands, quotes and carets encoded.

    >>> escape('<b>oh hai</b>')
    '&lt;b&gt;oh hai&lt;/b&gt;'

    >>> escape("Quote's Test")
    'Quote&#39;s Test'

    """
    mapping = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
    )

    for tup in mapping:
        s = s.replace(tup[0], tup[1])

    return s


def replace_by_mapping(s, from_type, to_type, skip_list=None, debug=False):
    s = cast.to_unicode(s)

    if __debug__:
        if debug: print(u'replace_by_mapping(s="{s}", from_type="{ft}", to_type="{tt}"'.format(s=s, ft=from_type, tt=to_type))

    def _get_values_for_key(k, mapping, default=None):
        if __debug__:
            if debug: print('_get_values_for_key(k={k}, mapping={m}, default={d})'.format(k=k, m=mapping, d=default))

        if k in mapping:
            # Ultimately, we're trying to get a list of elements
            val = mapping[k]

            if isinstance(val, (str, unicode)):
                # Create a list from a single element
                if __debug__:
                    if debug: print('    -> casting to a list and returning val')
                return [val]

            elif isinstance(val, (tuple, list)):
                # Just keep the list
                if __debug__:
                    if debug: print('    -> returning val')
                return val

            else:
                if __debug__:
                    if debug: print('    -> WTF! val: {v} is of type: {t}'.format(v=val, t=type(val)))

        elif __debug__:
            if debug: print('    -> NO KEY; returning {d}'.format(d=default))

        return default

    for mapping in ASCII_MAP:
        from_entities = _get_values_for_key(from_type, mapping)

        if not from_entities:
            continue

        if __debug__:
            if debug: print(u'  using from_entities: {l}'.format(l=from_entities))
        
        to_entities = _get_values_for_key(to_type, mapping, default=None)

        if to_entities is not None:
            if __debug__:
                if debug: print('  using to_entities: {l}'.format(l=to_entities))

            for k in from_entities:
                if __debug__:
                    if debug: print(u'  "{s}".replace("{k}", "{v}")'.format(s=s, k=k, v=to_entities[0]))

                if skip_list and k in skip_list:
                    continue

                s = s.replace(k, to_entities[0])

                if __debug__:
                    if debug: print(u'  s -> {s}'.format(s=s))

        elif __debug__:
            if debug: print('  SKIP')

    return s
 

def hex_to_char_entity(s, skip_list=None, mode=None, debug=False):
    """
    >>> hex_to_char_entity('hi there')
    u'hi there'

    >>> hex_to_char_entity(u'hi\xc2\xa0there')
    u'hi&nbsp;there'

    >>> hex_to_char_entity('<p>hi there</p>')
    u'&lt;p&gt;hi there&lt;/p&gt;'

    >>> hex_to_char_entity('<p>hi there</p>', skip_list=[u'\x3C', u'\x3E'])
    u'<p>hi there</p>'

    >>> hex_to_char_entity('<p>hi&mdash;there</p>', mode='html')
    u'<p>hi&mdash;there</p>'

    >>> hex_to_char_entity('some &#226;€&#166; text filled with little errors', mode='html', debug=0)
    u'some &#226;&euro;&#166; text filled with little errors'

    >>> hex_to_char_entity('Unicode™MAGIK')
    u'Unicode&trade;MAGIK'

    """
    if mode == "html":
        if not skip_list:
            skip_list = []

        # Don't escape ", &, <, or >
        for k in [u'\x22', u'\x26', u'\x3C', u'\x3E']:
            if k not in skip_list:
                skip_list.append(k)

    s = replace_by_mapping(s, 'ansi_hex', 'html_entity', skip_list=skip_list, debug=debug)

    return s
   

def char_entities_to_decimal(s):
    """
    >>> char_entities_to_decimal('hi there')
    u'hi there'

    >>> char_entities_to_decimal('hi & there')
    u'hi &#38; there'

    >>> char_entities_to_decimal('hi there&mdash;woot')
    u'hi there&#8212;woot'

    >>> char_entities_to_decimal('hi &there')
    u'hi &#38;there'

    """    
    s = replace_by_mapping(s, 'html_entity', 'ansi_num')

    # Encode all ampersands that don't preceed a numerical identifier.
    s = re.sub(r'&([^#])', u'&#38;\g<1>', s)

    return s
   

def html_to_ascii(s, skip_list=None):
    """
    >>> html_to_ascii('hi there')
    u'hi there'

    >>> html_to_ascii('hi &amp; there')
    u'hi & there'

    >>> html_to_ascii('one &lt; two')
    u'one < two'

    >>> html_to_ascii('hi&#8212; there')
    u'hi-- there'

    """    
    s = replace_by_mapping(s, 'ansi_num', 'ascii_replace', skip_list=skip_list)
    s = replace_by_mapping(s, 'html_entity', 'ascii_replace', skip_list=skip_list)

    return s


def simplify_entities(s, include_named=True):
    """
    >>> simplify_entities('Hi &nbsp;there!')
    u'Hi  there!'

    >>> simplify_entities('Hi&mdash;there!')
    u'Hi--there!'

    >>> simplify_entities('here\u2014and there!')
    u'here--and there!'

    >>> simplify_entities('&ldquo;Hi there!&rdquo;')
    u'"Hi there!"'

    >>> simplify_entities('the word “birdbrain” ever')
    u'the word "birdbrain" ever'

    >>> simplify_entities('Owl&#8217;s solution is &#8220;birdbrain&#8221;')
    u'Owl\\'s solution is "birdbrain"'

    """
    mapping = {
        u'\u2013': '-',
        u'\u2014': '--',
        u'\u2018': "'",
        u'\u2019': "'",
        u'\u201c': '"',
        u'\u201C': '"',
        u'\u201d': '"',
        u'\u201D': '"',
        u'\u2026': '...',
        u'\\u2013': '-',
        u'\\u2014': '--',
        u'\\u2018': "'",
        u'\\u2019': "'",
        u'\\u201c': '"',
        u'\\u201C': '"',
        u'\\u201d': '"',
        u'\\u201D': '"',
        u'\\u2026': '...',
        u'\\r': '',
        u'\\n': '',
    }

    if include_named:
        mapping[u'&nbsp;'] = ' '
        mapping[u'&rsquo;'] = "'"
        mapping[u'&ldquo;'] = '"'
        mapping[u'&rdquo;'] = '"'
        mapping[u'&mdash;'] = '--'
        mapping[u'&ndash;'] = '-'
        mapping[u'&#8220;'] = '"'
        mapping[u'&#8221;'] = '"'
        mapping[u'&#8217;'] = "'"

    s = cast.to_unicode(s)

    for k, v in mapping.items():
        s = s.replace(k, v)

    return s


def remove_control_characters(s):
    """
    >>> remove_control_characters('hi there')
    u'hi there'

    This is an odd one:  unicodedata treats '\xad' as category 'Cf', so it gets stripped, but
    really, it's a valid 'hex' character (as definied in the hex_to_char_entity function.)
    Either way, this means that you probably want to hex_to_char_entity() on
    your string before you send it here.
    #>>> remove_control_characters('the Bah\xc3\xa1\u2019\xc3\xad belief')
    #u'the Bah\xc3\xa1\u2019\xc3\xad belief'

    """
    s = cast.to_unicode(s)

    return "".join([ch for ch in s if unicodedata.category(ch)[0] != "C"])


def remove_comments(s, mode='all'):
    """
    >>> remove_comments(None)

    >>> remove_comments('hi there')
    'hi there'

    >>> remove_comments('foo/')
    'foo/'

    >>> remove_comments('hi  # there')
    'hi'

    >>> remove_comments('hi; there')
    'hi; there'

    >>> remove_comments('# hi; there')
    ''

    >>> remove_comments("hi// WHERE=1")
    'hi'

    >>> remove_comments('hi /* there */')
    'hi'

    >>> remove_comments('hi / there /')
    'hi / there /'

    >>> remove_comments("hi@there.com")
    'hi@there.com'

    >>> remove_comments('<p>Hi <!-- something -->There</p>')
    '<p>Hi There</p>'

    >>> remove_comments('<p>Hi <! something -->There</p>')
    '<p>Hi There</p>'

    >>> remove_comments('<p>Hi There</p><!--[if !mso]>')
    '<p>Hi There</p>'

    >>> remove_comments('<p>Hi There</p><!--[if !mso]> But not this', mode='xml')
    '<p>Hi There</p> But not this'

    """
    if s is None:
        return None

    if mode in ('all',):
        s = s.split('//')[0]

    if mode in ('all',):
        s = s.split('#')[0]

    if mode in ('all',):
        s = re.sub(r'/\*.*\*/', '', s)

    if mode in ('all', 'html', 'xml'):
        # Remove HTML/XML comments
        s = re.sub(pattern=r'(<!)([^>]+)(>)', repl='', string=s)

    return s.strip()


def remove_punctuation(s):
    """
    NOTE: We're not yet removing unicode representations of punctuation, nor
    en- and em-dashes. This is currently best for basic, ASCII text.

    >>> remove_punctuation('')
    ''

    >>> remove_punctuation('Hi there. I, and, we like cats!')
    'Hi there I and we like cats'

    """
    punks = ('.', ',', ';', ':', '!', '?', '(', ')', '-', '"', "'")

    for p in punks:
        s = s.replace(p, '')

    return s


def scrub_sql(s):
    """
    >>> scrub_sql(None)


    >>> scrub_sql('hi there')
    'hi there'

    >>> scrub_sql('foo/')
    'foo'

    >>> scrub_sql('hi -- there')
    'hi   there'

    >>> scrub_sql('hi; there')
    'hi there'

    >>> scrub_sql("hi' WHERE=1")
    "hi' WHERE=1"

    >>> scrub_sql('hi /* there */')
    'hi  there'

    >>> scrub_sql("hi@there.com")
    'hi@there.com'

    >>> scrub_sql("Have you seen López?")
    'Have you seen L\\xc3\\xb3pez?'

    """
    if s is None:
        return None

    s = strip_tags(s).replace(';', '').replace('--', ' ').replace('/', '').replace('*', '').replace('/', '').replace("'", "\'").replace('"', '\"').strip()

    return s


def strip_tags(value):
    """
    Returns the given HTML with all tags stripped.

    >>> strip_tags('<b>oh hai</b>')
    'oh hai'

    >>> strip_tags(None)

    >>> strip_tags('<p>oh hai.</p><p>goodbye</p>')
    'oh hai.  goodbye'

    >>> strip_tags('<i>oh hai.</i><i>goodbye</i>')
    'oh hai.goodbye'

    >>> strip_tags('<i>oh hai.<br /></i><b>Hello, <i>goodbye</i></b>')
    'oh hai. Hello, goodbye'

    >>> strip_tags("hi@there.com")
    'hi@there.com'

    >>> strip_tags("  hi   @ there . com")
    '  hi   @ there . com'

    >>> strip_tags("Have you seen López?")
    'Have you seen L\\xc3\\xb3pez?'

    # Doesn't pass yet :-(
    #>>> strip_tags("<sc<script>ript>alert('XSS')</sc</script>ript>")
    #'alert('XSS')'

    """
    global RE_TAG, RE_TAG_PARA_BR

    if value == None:
        return None

    if not isinstance(value, (str, unicode)):
        return value

    # Replace paragraph tags with spaces...
    # s = RE_TAG_BR.sub(' ', value)
    s = RE_TAG_PARA_BR.sub(' ', value)
    # Remove all remaining tags
    s = RE_TAG.sub('', s)

    try:
        # If the original string had leading or trailing spaces, leave them be
        if value[0] == ' ' or value[-1] == ' ':
            return s
        else:
            # Otherwise, strip any that might have been created while removing tags
            return s.strip()

    except IndexError:
        return s


def remove_tag_and_contents(s, tag=None, tags=None):
    """
    >>> remove_tag_and_contents('hi there')
    'hi there'

    >>> remove_tag_and_contents('<p>hi</p> <style>p {font-weight: 400;}</style><p>there</p>', tag='style')
    '<p>hi</p> <p>there</p>'

    >>> remove_tag_and_contents('<span class="foo">hi there</span>', tag='span')
    ''

    >>> remove_tag_and_contents('<p>hi</p> <style>p {font-weight: 400;}</style><p>there</p>', tags=('p', 'style'))
    ' '

    >>> remove_tag_and_contents('<p>hi <span>there</span></p> <style>p {font-weight: 400;}</style><p>cat</p>', tags=('span', 'style'))
    '<p>hi </p> <p>cat</p>'

    >>> remove_tag_and_contents('<p>hi <span class="woot">there</span></p> <style>p {font-weight: 400;}</style><p>cat</p>', tags=('span', 'style'))
    '<p>hi </p> <p>cat</p>'

    >>> remove_tag_and_contents('<p>Hi There<object  classid="clsid:38481807-CA0E-42D2-BF39-B33AF135CC4D" id=ieooui></object></p>', tag='object')
    '<p>Hi There</p>'

    >>> remove_tag_and_contents('<p>Hi </object>there</p>', tag='object')
    '<p>Hi there</p>'

    >>> remove_tag_and_contents('<p>Hi <br/>there</p>', tag='br')
    '<p>Hi there</p>'

    """
    if tag:
        tags = [tag]

    if isinstance(tags, (list, tuple)):
        for t in tags:
            # Tries to match a normal tag structure
            s = re.sub(pattern=r'<{tag}.*?>.*?</{tag}>'.format(tag=t), repl='', string=s)

            # Match any hanging opening or closing versions
            s = re.sub(pattern=r'</{tag}[^>]*>'.format(tag=t), repl='', string=s)
            s = re.sub(pattern=r'<{tag}[^>]*/ *>'.format(tag=t), repl='', string=s)

    return s


def remove_css_styles(s):
    """
    >>> remove_css_styles('hi there')
    'hi there'

    >>> remove_css_styles('<p>hi</p> <style>p {font-weight: 400;}</style><p>there</p>')
    '<p>hi</p> <p>there</p>'

    >>> remove_css_styles('<span class="foo">hi there</span>')
    '<span class="foo">hi there</span>'

    >>> remove_css_styles('<span style="font-weight: bold;" class="foo">hi there</span>')
    '<span class="foo">hi there</span>'

    >>> remove_css_styles('<span class="foo" style="font-weight: bold;">hi there</span>')
    '<span class="foo">hi there</span>'

    """
    # Remove <style> tags..
    s = remove_tag_and_contents(s, tag='style')

    # Remove inline style attributes..
    s = re.sub(r'(<[^>]*?)( style="[^"]*")(.*?>)', '\g<1>\g<3>', s)

    return s


def nuke_newlines(s):
    return compress_whitespace(s.replace('\n', ' ').replace('\r', ' ').strip())


def remove_empty_tags(s, tags=('p', 'i', 'em', 'span')):
    """
    >>> remove_empty_tags('Hi there')
    'Hi there'

    >>> remove_empty_tags('<p>Hi there</p>')
    '<p>Hi there</p>'

    >>> remove_empty_tags('Hi there<p> </p>')
    'Hi there '

    >>> remove_empty_tags('Hi <span> </span>there')
    'Hi  there'

    """
    def _empty_tag_reducer(s, tag):
        return s.replace("<{tag}>&#160;</{tag}>".format(tag=tag), ' ')\
                .replace("<{tag}> </{tag}>".format(tag=tag), ' ')\
                .replace("<{tag}></{tag}>".format(tag=tag), ' ')

    for tag in tags:
        s = _empty_tag_reducer(s, tag)

    return s


def normalize_br_tags(s):
    """
    I like 'em this way.

    >>> normalize_br_tags('Hi there')
    'Hi there'

    >>> normalize_br_tags('Hi <br>there')
    'Hi <br />there'

    >>> normalize_br_tags('Hi there<br/>')
    'Hi there<br />'

    """
    return s.replace("<br>", "<br />").replace("<br/>", "<br />")


def cleaner_html(s):
    """
    >>> cleaner_html('<p>Hi&nbsp;there!</p>')
    u'<p>Hi&#160;there!</p>'
    """
    s = nuke_newlines(s)
    s = hex_to_char_entity(s, mode='html')
    s = remove_control_characters(s)
    s = char_entities_to_decimal(s)

    return s


def full_html_strip(s):
    """
    >>> full_html_strip('<p>Hi&nbsp;there!</p>')
    u'Hi there!'

    >>> full_html_strip(u'<p>Hi&mdash;there!</p>')
    u'Hi--there!'

    >>> full_html_strip(u'<p>Hi&trade;there!</p>')
    u'Hi&#153;there!'

    """
    s = hex_to_char_entity(s, mode='html')
    s = nuke_newlines(s)
    s = remove_control_characters(s)
    s = strip_tags(s)
    s = simplify_entities(s)
    s = char_entities_to_decimal(s)

    return s


def substitute_pattern_with_char(s, pattern, repl_char='x'):
    """
    This is a little different than re.sub(). It replaces all the characters
    that match the pattern with an equal number of `repl_char` characters.

    The resulting string should be the same length as the starting string.

    >>> substitute_pattern_with_char(s='Hi there', pattern=r'[a-z]+', repl_char='x')
    'Hx xxxxx'

    >>> substitute_pattern_with_char(s='With 42 cats', pattern=r'[\d]+', repl_char='x')
    'With xx cats'

    >>> substitute_pattern_with_char(s='With 42 cats and 12 dogs', pattern=r'[\d]+', repl_char='x')
    'With xx cats and xx dogs'

    >>> substitute_pattern_with_char(s='With 42 cats and 12 dogs', pattern=r'[\d]+\s+(cat[s]?|bird[s]?)', repl_char='x')
    'With xxxxxxx and 12 dogs'

    """
    for mo in re.finditer(pattern=pattern, string=s):
        m = mo.group(0)
        s = s.replace(m, ''.join([repl_char for i in range(0, len(m))]))

    return s


def substitute_patterns_with_char(s, patterns, repl_char='x'):
    """
    Like substitute_pattern_with_char, but takes a list of patterns.

    The resulting string should be the same length as the starting string.

    >>> substitute_patterns_with_char(s='Hi there', patterns=[r'[a-z]+'], repl_char='x')
    'Hx xxxxx'

    >>> substitute_patterns_with_char(s='With 42 cats', patterns=[r'[\d]+'], repl_char='x')
    'With xx cats'

    """
    if patterns is not None:
        for pat in patterns:
            s = substitute_pattern_with_char(s=s, pattern=pat, repl_char=repl_char)

    return s


def sub_with_exclusion_patterns(find_pattern, replace_with, s, exclusion_patterns):
    """
    @param    find_pattern        Regex used to find.
    @param    replace_with        Regex or Function used to replace. If a function, it will be called using the matched characters.
    @param    s                   String to replace characters within.
    @param    exclusion_patterns  Regex patterns used to mask areas that should not be used during the find/replace.

    >>> sub_with_exclusion_patterns(r'cat', r'CAT', 'His cat bought six more cats.', (r'cats',))
    'His CAT bought six more cats.'

    >>> sub_with_exclusion_patterns(r'\d', r'oh hai', 'He bought 6 more 22Bs.', (r'\d+\w+',))
    'He bought oh hai more 22Bs.'

    # This one fails because something is happening to the replace patterns' match codes which is turning them
    # into escapes somehow. Blame doctest I think.
    # >>> sub_with_exclusion_patterns(r'([A-Z])(\w+)', r'\2\1', 'The Brown Fox Jumped over the Lazy Moon.', (r'[JM]',))
    # -->  This is the correct response, which works outside of doctest: 'heT rownB oxF Jumped over the azyL Moon.'

    >>> def sayhi(s): return 'HAI'
    >>> sub_with_exclusion_patterns(r'cat', sayhi, 'His cat bought six more cats.', (r'cats',))
    'His HAI bought six more cats.'

    """
    # First, use the exclusion_patterns to mask the string
    # s might be: 'He bought 6 more 22Bs.'
    tmp = substitute_patterns_with_char(s, patterns=exclusion_patterns, repl_char='x')
    # now tmp might be: 'He bought 6 more xxBs.'

    # with the IGNORE patterns replaced with x's, we can now look for the remaining numbers
    bits = []
    working_string = s
    search_in_string = tmp

    for mo in re.finditer(find_pattern, tmp):
        m = mo.group(0)

        # Find the first match
        pos = search_in_string.find(m)

        if pos >= 0:
            # Append the clean (original) part of the string up until this point
            bits.append(working_string[0:pos])

            # Trim the string to strip off what we're already processed
            working_string = working_string[pos + len(m):]
            search_in_string = search_in_string[pos + len(m):]

            # Find out what to replace it with
            if isfunction(replace_with):
                replace_result = replace_with(m)
            else:
                replace_result = re.sub(find_pattern, replace_with, m)

            # Add the replacement to bits
            bits.append(replace_result)

        else:
            # Append the rest of the string
            bits.append(working_string[0:])
            break

    else:
        # Append the remainder
        bits.append(working_string[0:])

    return ''.join(bits)


def encode_subs(s, subs, substrings=True, pre_space=False, post_space=False):
    """
    >>> encode_subs('hi there', [])
    ('hi there', [])

    >>> encode_subs('hi there', ['hi'])
    ('g0SUB; there', [('hi', 'g0SUB;')])

    # Multiple patterns
    >>> encode_subs('hi there', ['hi', 're'], substrings=False)
    ('g0SUB; there', [('hi', 'g0SUB;')])

    # Multiple patterns
    >>> encode_subs('hi there', ['hi', 're'], substrings=True)
    ('g0SUB; theg1SUB;', [('hi', 'g0SUB;'), ('re', 'g1SUB;')])

    # Without space-options, the patter will be found within the words too
    >>> encode_subs('hi thiere', ['hi'])
    ('g0SUB; tg0SUB;ere', [('hi', 'g0SUB;')])

    # Here we require that 'hi' be followed by a space
    >>> encode_subs('hi there', subs=['hi'], post_space=True)
    ('g0SUB;there', [('hi ', 'g0SUB;')])

    # If we require a pre-space, then we can't encode the 'hi' here
    >>> encode_subs('hi there', subs=['hi'], pre_space=True)
    ('hi there', [])

    >>> encode_subs('hi hithere', subs=['hi'], pre_space=True)
    ('hig0SUB;there', [(' hi', 'g0SUB;')])

    >>> encode_subs('hi there', subs=['hi'], pre_space=True, post_space=True)
    ('hi there', [])

    """
    mapping = []

    search_str = r'{}'

    if pre_space:
        search_str = r'\s+{}'.format(search_str)
    else:
        if not substrings:
            search_str = r'\b{}'.format(search_str)

    if post_space:
        search_str = r'{}\s+'.format(search_str)
    else:
        if not substrings:
            search_str = r'{}\b'.format(search_str)

    for key in subs:
        search_key = search_str.format(key)

        mo = re.search(search_key, s)
        if mo is not None:

            tup = (mo.group(0), 'g{}SUB;'.format(len(mapping)))
            mapping.append(tup)
            s = re.sub(search_key, tup[1], s)

    return (s, mapping)


def decode_subs(s, mapping):
    """
    >>> decode_subs('hi there', [])
    'hi there'

    >>> decode_subs('g0SUB;there', [('hi ', 'g0SUB;')])
    'hi there'

    >>> decode_subs('g0SUB; theg1SUB;', [('hi', 'g0SUB;'), ('re', 'g1SUB;')])
    'hi there'
    """
    for tup in mapping:
        s = s.replace(tup[1], tup[0])

    return s


## ---------------------
if __name__ == "__main__":
    import doctest

    print("[fmt.py] Testing...")

    # Run the doctests
    doctest.testmod()

    # Now some that are trickier via doctest
    s = """
    This is
    a test
    """
    assert nuke_newlines(s) == "This is a test"

    # Woot!
    print("Done.")

