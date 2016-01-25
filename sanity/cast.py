#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, datetime
import json


def to_ascii(s, replace=''):
    """
    >>> to_ascii(None)
    ''

    >>> to_ascii('hi there')
    'hi there'

    >>> to_ascii('hi €there')
    'hi there'

    Watch what happens here -- a reminder that unicode chars take multiple bytes!
    >>> to_ascii('hi €there', replace='!')
    'hi !!!there'

    >>> to_ascii(u'hi there')
    'hi there'

    >>> to_ascii(u'hi&mdash;there')
    'hi&mdash;there'

    >>> to_ascii(1)
    '1'

    >>> to_ascii(3.14)
    '3.14'

    """
    if s is None:
        return ''

    if not isinstance(s, (str, unicode)):
        s = to_str(s)

    letters = []

    for c in s:
        try:
            c = str(c)
        except:
            letters.append(replace)
        else:
            if 0 <= ord(c) <= 128:
                letters.append(c)
            else:
                letters.append(replace)

    return ''.join(letters)

def to_bool(input):
    """
    >>> to_bool('1')
    True

    >>> to_bool('True')
    True

    >>> to_bool('true')
    True

    >>> to_bool(True)
    True

    >>> to_bool(False)
    False

    >>> to_bool('False')
    False

    >>> to_bool('false')
    False

    >>> to_bool('0')
    False

    >>> to_bool(None)
    False

    >>> to_bool('on')
    True

    >>> to_bool('off')
    False

    >>> to_bool('yes')
    True

    >>> to_bool('no')
    False

    """
    if input is None:
        return False

    if input in (u'0', '0'):
        return False

    elif input in (u'False', 'False', u'false', 'false'):
        return False

    elif input in (u'off', 'off', u'no', 'no'):
        return False

    else:
        if bool(input):
            return True
        else:
            return False

def to_int(arg, default=0):
    """
    >>> to_int('0')
    0

    >>> to_int('1')
    1

    >>> to_int('a')
    0

    >>> to_int('12.3')
    0

    >>> to_int('1a2b3c')
    0

    >>> to_int('<1a2b3c/>')
    0

    >>> to_int(None)
    0

    >>> to_int('None')
    0

    >>> to_int(1)
    1

    >>> to_int(u'')
    0

    >>> to_int(1, None)
    1

    >>> to_int('hi', 0)
    0

    >>> to_int(None, 0)
    0

    >>> to_int(None, None)

    >>> to_int(u'', 0)
    0

    >>> to_int(u'-1')
    -1

    """
    try:
        return int(arg)
    except:
        return default

def to_jsonable(d, date_format='%Y-%m-%d', datetime_format='%Y-%m-%dT%H-%M-%SZ'):
    """
    >>> to_jsonable(None)
    ''

    >>> to_jsonable('hi')
    'hi'

    >>> to_jsonable({'hi':'there'})
    {'hi': 'there'}

    >>> to_jsonable({'hi':'there', 'one': 1})
    {'hi': 'there', 'one': 1}

    >>> t = date.today()
    >>> result = to_jsonable({'hi':'there', 'today': t})
    >>> expected = {'hi': 'there', 'today': '{}'.format(t.strftime('%Y-%m-%d'))}
    >>> result == expected
    True
    >>> result['today'] == '{}'.format(t.strftime('%Y-%m-%d'))
    True

    >>> to_jsonable({'hi':'there', 'one': [1, 2, 3, 4]})
    {'hi': 'there', 'one': [1, 2, 3, 4]}

    >>> to_jsonable({'hi':'there', 'one': ['1', '2', '3', '4']})
    {'hi': 'there', 'one': ['1', '2', '3', '4']}

    >>> f = TestObject()
    >>> to_jsonable({'hi': f})
    {'hi': 'TestObject'}

    >>> to_jsonable({'hi':'there', 'one': [f, f, f]})
    {'hi': 'there', 'one': ['TestObject', 'TestObject', 'TestObject']}

    """
    if d is None:
        return ''

    elif isinstance(d, (dict)):
        results = {}

        for k, v in d.items():
            results[k] = to_jsonable(v)
        
        return results

    elif isinstance(d, (str, unicode)):
        return d

    elif isinstance(d, (int, float)):
        return d

    elif isinstance(d, (date,)):
        return '{}'.format(d.strftime(date_format))

    elif isinstance(d, (datetime,)):
        return '{}'.format(d.strftime(datetime_format))

    elif isinstance(d, (list,)):
        results = []

        for item in d:
            results.append(to_jsonable(item))

        return results

    elif isinstance(d, (object,)):
        string_representation = str(d)

        if string_representation.startswith('<') and string_representation.endswith('>'):
            # Then it's probably a generic Type representation, and not something we want
            # to send over JSON.
            try:
                # Extract the classname and use that
                string_representation = str(d.__class__).split('.')[-1]
            except:
                pass

        return string_representation

    else:
        return str(d)

def to_json(d, date_format='%Y-%m-%d', datetime_format='%Y-%m-%dT%H-%M-%SZ'):
    """
    >>> to_json({'hi':'there'})
    '{"hi": "there"}'

    >>> to_json({'hi':'there', 'one': 1})
    '{"hi": "there", "one": 1}'

    >>> t = date.today()
    >>> result = to_json({'hi':'there', 'today': t})
    >>> expected = '{{"hi": "there", "today": "{}"}}'.format(t.strftime('%Y-%m-%d'))
    >>> result == expected
    True

    >>> f = TestObject()
    >>> to_json({'hi': f})
    '{"hi": "TestObject"}'

    """
    return json.dumps(to_jsonable(d))

def to_latin_one(s):
    return to_str(s, encoding='latin-1',  errors='ignore')

def to_str(s, encoding='utf-8', errors='strict'):
    """
    MOSTLY FROM DJANGO 1.3 django.utils.encoding

    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    >>> to_str('Hi There')
    'Hi There'

    """
    if not isinstance(s, basestring):
        try:
            return str(s)

        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([to_str(arg, encoding, errors) for arg in s])

            return unicode(s).encode(encoding, errors)

    elif isinstance(s, unicode):
        return s.encode(encoding, errors)

    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)

    else:
        return s

def to_unicode(s, encoding='utf-8', errors='strict'):
    """
    MOSTLY FROM DJANGO 1.3 django.utils.encoding

    >>> to_unicode('Hi There')
    u'Hi There'

    """
    # Handle the common case first, saves 30-40% in performance when s
    # is an instance of unicode. This function gets called often in that
    # setting.
    if isinstance(s, unicode):
        return s

    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)

            else:
                try:
                    s = unicode(str(s), encoding, errors)

                except UnicodeEncodeError:
                    s = ' '.join([to_unicode(arg, encoding, errors) for arg in s])

        elif not isinstance(s, unicode):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            s = s.decode(encoding, errors)

    except UnicodeDecodeError:
        s = ' '.join([to_unicode(arg, encoding, errors) for arg in s])

    return s

## ---------------------
if __name__ == "__main__":
    import doctest
    print("[cast.py] Testing...")

    class TestObject():
        message = 'howdy'

    doctest.testmod()
    print("Done.")
