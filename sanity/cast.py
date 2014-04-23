#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = "MIT"
__version__ = "0.2"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."


def to_bool(input):
    """
    >>> to_bool('1')
    True

    >>> to_bool('True')
    True

    >>> to_bool(True)
    True

    >>> to_bool(False)
    False

    >>> to_bool('False')
    False

    >>> to_bool('0')
    False

    >>> to_bool(None)
    False

    >>> to_bool('on')
    True

    >>> to_bool('off')
    False

    """
    if input is None:
        return False

    if input in (u'0', '0'):
        return False

    elif input in (u'False', 'False'):
        return False

    elif input in (u'off', 'off'):
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

def to_ascii(s):
    """
    >>> to_ascii('hi there')
    'hi there'

    >>> to_ascii('hi €there')
    'hi there'

    >>> to_ascii(u'hi there')
    'hi there'

    >>> to_ascii(u'hi&mdash;there')
    'hi&mdash;there'

    """
    return str(''.join([c for c in s if 0 <= ord(c) <= 128]))

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

def to_latin_one(s):
    return to_str(s, encoding='latin-1',  errors='ignore')

## ---------------------
if __name__ == "__main__":
    import doctest
    print "Testing..."
    doctest.testmod()
    print "Done."
