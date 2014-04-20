#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata

import cast


__license__ = "MIT"
__version__ = "0.1"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."


def compress_whitespace(s):
    """
    Convert whitespace (ie., spaces, tabs, linebreaks, etc.) to spaces, and
    compress multiple-spaces into single-spaces.

    >>> compress_whitespace('   Oh   hai    there   ')
    'Oh hai there'

    >>> compress_whitespace('      ')
    ''

    >>> compress_whitespace("hi@there.com")
    'hi@there.com'

    >>> compress_whitespace("  hi   @ there . com")
    'hi @ there . com'

    """
    # Cast to string
    s = str(s).strip()

    # Sanity check
    if (len(s) == 0):
        return ''

    s = re.sub(r'\s', ' ', s)
    s = re.sub(r' +', ' ', s)

    return s.strip()

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

def add_leading_padding(s, char=' ', target_length=-1):
    """
    >>> add_leading_padding(s='hi')
    'hi'
    
    >>> add_leading_padding(s='hi', target_length=10)
    '        hi'
    
    >>> add_leading_padding(s='hi', char='-', target_length=3)
    '-hi'
    
    >>> add_leading_padding(s=900)
    '900'
    
    >>> add_leading_padding(s=900, char=0, target_length=5)
    '00900'
    
    >>> add_leading_padding(s='hit', target_length=2)  # See what I did there?
    'hi'
    
    >>> add_leading_padding(s='9021012', char='0', target_length=9)
    '009021012'
    
    """
    z = str(s)
    
    if target_length > 0:
        z = z[:target_length]
        sub_char = str(char)
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

def sub_greeks(s, as_unicode=True):
    """
    >>> sub_greeks('hi there')
    u'hi there'

    >>> sub_greeks(u'hi\xc2\xa0there', as_unicode=True)
    u'hi&nbsp;there'

    """
    # The following list was seeded using a dictionary within the ReportLab paraparser.py
    # library, licensed under a BSD License.  For more, see: http://www.reportlab.com/software/opensource/

    mapping = {
        u'\xc2\xa0': 'nbsp',
        u'\xc2\xa1': 'iexcl',
        u'\xc2\xa2': 'cent',
        u'\xc2\xa3': 'pound',
        u'\xc2\xa4': 'curren',
        u'\xc2\xa5': 'yen',
        u'\xc2\xa6': 'brvbar',
        u'\xc2\xa7': 'sect',
        u'\xc2\xa8': 'uml',
        u'\xc2\xa9': 'copy',
        u'\xc2\xaa': 'ordf',
        u'\xc2\xab': 'laquo',
        u'\xc2\xac': 'not',
        u'\xc2\xad': 'shy',
        u'\xc2\xae': 'reg',
        u'\xc2\xaf': 'macr',
        u'\xc2\xb0': 'deg',
        u'\xc2\xb1': 'plusmn',
        u'\xc2\xb2': 'sup2',
        u'\xc2\xb3': 'sup3',
        u'\xc2\xb4': 'acute',
        u'\xc2\xb5': 'micro',
        u'\xc2\xb5': 'mu',
        u'\xc2\xb6': 'para',
        u'\xc2\xb7': 'middot',
        u'\xc2\xb8': 'cedil',
        u'\xc2\xb9': 'sup1',
        u'\xc2\xba': 'ordm',
        u'\xc2\xbb': 'raquo',
        u'\xc2\xbc': 'frac14',
        u'\xc2\xbd': 'frac12',
        u'\xc2\xbe': 'frac34',
        u'\xc2\xbf': 'iquest',
        u'\xc3\x80': 'Agrave',
        u'\xc3\x81': 'Aacute',
        u'\xc3\x82': 'Acirc',
        u'\xc3\x83': 'Atilde',
        u'\xc3\x84': 'Auml',
        u'\xc3\x85': 'Aring',
        u'\xc3\x86': 'AElig',
        u'\xc3\x87': 'Ccedil',
        u'\xc3\x88': 'Egrave',
        u'\xc3\x89': 'Eacute',
        u'\xc3\x8a': 'Ecirc',
        u'\xc3\x8b': 'Euml',
        u'\xc3\x8c': 'Igrave',
        u'\xc3\x8d': 'Iacute',
        u'\xc3\x8e': 'Icirc',
        u'\xc3\x8f': 'Iuml',
        u'\xc3\x90': 'ETH',
        u'\xc3\x91': 'Ntilde',
        u'\xc3\x92': 'Ograve',
        u'\xc3\x93': 'Oacute',
        u'\xc3\x94': 'Ocirc',
        u'\xc3\x95': 'Otilde',
        u'\xc3\x96': 'Ouml',
        u'\xc3\x97': 'times',
        u'\xc3\x98': 'Oslash',
        u'\xc3\x99': 'Ugrave',
        u'\xc3\x9a': 'Uacute',
        u'\xc3\x9b': 'Ucirc',
        u'\xc3\x9c': 'Uuml',
        u'\xc3\x9d': 'Yacute',
        u'\xc3\x9e': 'THORN',
        u'\xc3\x9f': 'szlig',
        u'\xc3\xa0': 'agrave',
        u'\xc3\xa1': 'aacute',
        u'\xc3\xa2': 'acirc',
        u'\xc3\xa3': 'atilde',
        u'\xc3\xa4': 'auml',
        u'\xc3\xa5': 'aring',
        u'\xc3\xa6': 'aelig',
        u'\xc3\xa7': 'ccedil',
        u'\xc3\xa8': 'egrave',
        u'\xc3\xa9': 'eacute',
        u'\xc3\xaa': 'ecirc',
        u'\xc3\xab': 'euml',
        u'\xc3\xac': 'igrave',
        u'\xc3\xad': 'iacute',
        u'\xc3\xae': 'icirc',
        u'\xc3\xaf': 'iuml',
        u'\xc3\xb0': 'eth',
        u'\xc3\xb1': 'ntilde',
        u'\xc3\xb2': 'ograve',
        u'\xc3\xb3': 'oacute',
        u'\xc3\xb4': 'ocirc',
        u'\xc3\xb5': 'otilde',
        u'\xc3\xb6': 'ouml',
        u'\xc3\xb7': 'divide',
        u'\xc3\xb8': 'oslash',
        u'\xc3\xb9': 'ugrave',
        u'\xc3\xba': 'uacute',
        u'\xc3\xbb': 'ucirc',
        u'\xc3\xbc': 'uuml',
        u'\xc3\xbd': 'yacute',
        u'\xc3\xbe': 'thorn',
        u'\xc3\xbf': 'yuml',
        u'\xc5\x92': 'OElig',
        u'\xc5\x93': 'oelig',
        u'\xc5\xa0': 'Scaron',
        u'\xc5\xa1': 'scaron',
        u'\xc5\xb8': 'Yuml',
        u'\xc6\x92': 'fnof',
        u'\xcb\x86': 'circ',
        u'\xcb\x9c': 'tilde',
        u'\xce\x91': 'Alpha',
        u'\xce\x92': 'Beta',
        u'\xce\x93': 'Gamma',
        u'\xce\x95': 'Epsilon',
        u'\xce\x96': 'Zeta',
        u'\xce\x97': 'Eta',
        u'\xce\x98': 'Theta',
        u'\xce\x99': 'Iota',
        u'\xce\x9a': 'Kappa',
        u'\xce\x9b': 'Lambda',
        u'\xce\x9c': 'Mu',
        u'\xce\x9d': 'Nu',
        u'\xce\x9e': 'Xi',
        u'\xce\x9f': 'Omicron',
        u'\xce\xa0': 'Pi',
        u'\xce\xa1': 'Rho',
        u'\xce\xa3': 'Sigma',
        u'\xce\xa4': 'Tau',
        u'\xce\xa5': 'Upsilon',
        u'\xce\xa6': 'Phi',
        u'\xce\xa7': 'Chi',
        u'\xce\xa8': 'Psi',
        u'\xce\xb1': 'alpha',
        u'\xce\xb2': 'beta',
        u'\xce\xb3': 'gamma',
        u'\xce\xb4': 'delta',
        u'\xce\xb5': 'epsilon',
        u'\xce\xb5': 'epsiv',
        u'\xce\xb6': 'zeta',
        u'\xce\xb7': 'eta',
        u'\xce\xb8': 'theta',
        u'\xce\xb9': 'iota',
        u'\xce\xba': 'kappa',
        u'\xce\xbb': 'lambda',
        u'\xce\xbd': 'nu',
        u'\xce\xbe': 'xi',
        u'\xce\xbf': 'omicron',
        u'\xcf\x80': 'pi',
        u'\xcf\x81': 'rho',
        u'\xcf\x82': 'sigmaf',
        u'\xcf\x82': 'sigmav',
        u'\xcf\x83': 'sigma',
        u'\xcf\x84': 'tau',
        u'\xcf\x85': 'upsilon',
        u'\xcf\x86': 'phis',
        u'\xcf\x87': 'chi',
        u'\xcf\x88': 'psi',
        u'\xcf\x89': 'omega',
        u'\xcf\x91': 'thetasym',
        u'\xcf\x91': 'thetav',
        u'\xcf\x92': 'upsih',
        u'\xcf\x95': 'phi',
        u'\xcf\x96': 'piv',
        u'\xe2\x80\x82': 'ensp',
        u'\xe2\x80\x83': 'emsp',
        u'\xe2\x80\x89': 'thinsp',
        u'\xe2\x80\x8c': 'zwnj',
        u'\xe2\x80\x8d': 'zwj',
        u'\xe2\x80\x8e': 'lrm',
        u'\xe2\x80\x8f': 'rlm',
        u'\xe2\x80\x93': 'ndash',
        u'\xe2\x80\x94': 'mdash',
        u'\xe2\x80\x98': 'lsquo',
        u'\xe2\x80\x99': 'rsquo',
        u'\xe2\x80\x9a': 'sbquo',
        u'\xe2\x80\x9c': 'ldquo',
        u'\xe2\x80\x9d': 'rdquo',
        u'\xe2\x80\x9e': 'bdquo',
        u'\xe2\x80\xa0': 'dagger',
        u'\xe2\x80\xa1': 'Dagger',
        u'\xe2\x80\xa2': 'bull',
        u'\xe2\x80\xa6': 'hellip',
        u'\xe2\x80\xb0': 'permil',
        u'\xe2\x80\xb2': 'prime',
        u'\xe2\x80\xb3': 'Prime',
        u'\xe2\x80\xb9': 'lsaquo',
        u'\xe2\x80\xba': 'rsaquo',
        u'\xe2\x81\x84': 'frasl',
        u'\xe2\x82\xac': 'euro',
        u'\xe2\x84\x91': 'image',
        u'\xe2\x84\x98': 'weierp',
        u'\xe2\x84\x9c': 'real',
        u'\xe2\x84\xa6': 'Omega',
        u'\xe2\x84\xb5': 'alefsym',
        u'\xe2\x86\x90': 'larr',
        u'\xe2\x86\x91': 'uarr',
        u'\xe2\x86\x92': 'rarr',
        u'\xe2\x86\x93': 'darr',
        u'\xe2\x86\x94': 'harr',
        u'\xe2\x86\xb5': 'crarr',
        u'\xe2\x87\x90': 'lArr',
        u'\xe2\x87\x91': 'uArr',
        u'\xe2\x87\x92': 'rArr',
        u'\xe2\x87\x93': 'dArr',
        u'\xe2\x87\x94': 'hArr',
        u'\xe2\x88\x80': 'forall',
        u'\xe2\x88\x82': 'part',
        u'\xe2\x88\x83': 'exist',
        u'\xe2\x88\x85': 'empty',
        u'\xe2\x88\x86': 'Delta',
        u'\xe2\x88\x87': 'nabla',
        u'\xe2\x88\x88': 'isin',
        u'\xe2\x88\x89': 'notin',
        u'\xe2\x88\x8b': 'ni',
        u'\xe2\x88\x8f': 'prod',
        u'\xe2\x88\x91': 'sum',
        u'\xe2\x88\x92': 'minus',
        u'\xe2\x88\x97': 'lowast',
        u'\xe2\x88\x9a': 'radic',
        u'\xe2\x88\x9d': 'prop',
        u'\xe2\x88\x9e': 'infin',
        u'\xe2\x88\xa0': 'ang',
        u'\xe2\x88\xa7': 'and',
        u'\xe2\x88\xa8': 'or',
        u'\xe2\x88\xa9': 'cap',
        u'\xe2\x88\xaa': 'cup',
        u'\xe2\x88\xab': 'int',
        u'\xe2\x88\xb4': 'there4',
        u'\xe2\x88\xbc': 'sim',
        u'\xe2\x89\x85': 'cong',
        u'\xe2\x89\x88': 'asymp',
        u'\xe2\x89\xa0': 'ne',
        u'\xe2\x89\xa1': 'equiv',
        u'\xe2\x89\xa4': 'le',
        u'\xe2\x89\xa5': 'ge',
        u'\xe2\x8a\x82': 'sub',
        u'\xe2\x8a\x83': 'sup',
        u'\xe2\x8a\x84': 'nsub',
        u'\xe2\x8a\x86': 'sube',
        u'\xe2\x8a\x87': 'supe',
        u'\xe2\x8a\x95': 'oplus',
        u'\xe2\x8a\x97': 'otimes',
        u'\xe2\x8a\xa5': 'perp',
        u'\xe2\x8b\x85': 'sdot',
        u'\xe2\x8c\xa9': 'lang',
        u'\xe2\x8c\xaa': 'rang',
        u'\xe2\x97\x8a': 'loz',
        u'\xe2\x99\xa0': 'spades',
        u'\xe2\x99\xa3': 'clubs',
        u'\xe2\x99\xa5': 'hearts',
        u'\xe2\x99\xa6': 'diams',
        u'\xef\xa3\xa5': 'oline',
        u'\xef\xa3\xaa': 'trade',
        u'\xef\xa3\xae': 'lceil',
        u'\xef\xa3\xb0': 'lfloor',
        u'\xef\xa3\xb9': 'rceil',
        u'\xef\xa3\xbb': 'rfloor',
    }

    if as_unicode:
        s = cast.to_unicode(s)

        for k, v in mapping.items():
            s = s.replace(unicode(k), u'&{entity};'.format(entity=unicode(v)))

    else:
        for k, v in mapping.items():
            s = s.replace(k, '&{entity};'.format(entity=v))

    return s

def char_entities_to_decimal(s, as_unicode=False):
    """
    >>> char_entities_to_decimal('hi there')
    'hi there'

    >>> char_entities_to_decimal('hi & there')
    'hi &#38; there'

    >>> char_entities_to_decimal('hi there&mdash;woot')
    'hi there&#8212;woot'

    >>> char_entities_to_decimal('hi &there')
    'hi &#38;there'

    """
    mapping = {
        "&nbsp;": "&#160;",
        "&iexcl;": "&#161;",
        "&cent;": "&#162;",
        "&pound;": "&#163;",
        "&curren;": "&164;",
        "&yen;": "&#165;",
        "&brvbar;": "&#166;",
        "&sect;": "&#167;",
        "&uml;": "&#168;",
        "&copy;": "&#169;",
        "&ordf;": "&#170;",
        "&laquo;": "&#171;",
        "&not;": "&#172;",
        "&shy;": "&#173;",
        "&reg;": "&#174;",
        "&macr;": "&#175;",
        "&deg;": "&#176;",
        "&plusmn;": "&#177;",
        "&sup2;": "&#178;",
        "&sup3;": "&#179;",
        "&acute;": "&#180;",
        "&micro;": "&#181;",
        "&para;": "&#182;",
        "&middot;": "&#183;",
        "&cedil;": "&#184;",
        "&sup1;": "&#185;",
        "&ordm;": "&#186;",
        "&raquo;": "&#187;",
        "&frac14;": "&#188;",
        "&frac12;": "&#189;",
        "&frac34;": "&#190;",
        "&iquest;": "&#191;",
        "&Agrave;": "&#192;",
        "&Aacute;": "&#193;",
        "&Acirc;": "&#194;",
        "&Atilde;": "&#195;",
        "&Auml;": "&#196;",
        "&Aring;": "&#197;",
        "&AElig;": "&#198;",
        "&Ccedil;": "&#99;",
        "&Egrave;": "&#00;",
        "&Eacute;": "&#01;",
        "&Ecirc;": "&#202;",
        "&Euml;": "&#203;",
        "&Igrave;": "&#04;",
        "&Iacute;": "&#05;",
        "&Icirc;": "&#206;",
        "&Iuml;": "&#207;",
        "&ETH;": "&#208;",
        "&Ntilde;": "&#09;",
        "&Ograve;": "&#10;",
        "&Oacute;": "&#11;",
        "&Ocirc;": "&#212;",
        "&Otilde;": "&#13;",
        "&Ouml;": "&#214;",
        "&times;": "&#215;",
        "&Oslash;": "&#16;",
        "&Ugrave;": "&#17;",
        "&Uacute;": "&#18;",
        "&Ucirc;": "&#219;",
        "&Uuml;": "&#220;",
        "&Yacute;": "&#21;",
        "&THORN;": "&#222;",
        "&szlig;": "&#223;",
        "&agrave;": "&#24;",
        "&aacute;": "&#25;",
        "&acirc;": "&#226;",
        "&atilde;": "&#27;",
        "&auml;": "&#228;",
        "&aring;": "&#229;",
        "&aelig;": "&#230;",
        "&ccedil;": "&#31;",
        "&egrave;": "&#32;",
        "&eacute;": "&#33;",
        "&ecirc;": "&#234;",
        "&euml;": "&#235;",
        "&igrave;": "&#36;",
        "&iacute;": "&#37;",
        "&icirc;": "&#238;",
        "&iuml;": "&#239;",
        "&eth;": "&#240;",
        "&ntilde;": "&#41;",
        "&ograve;": "&#42;",
        "&oacute;": "&#43;",
        "&ocirc;": "&#244;",
        "&otilde;": "&#45;",
        "&ouml;": "&#246;",
        "&divide;": "&#47;",
        "&oslash;": "&#48;",
        "&ugrave;": "&#49;",
        "&uacute;": "&#50;",
        "&ucirc;": "&#251;",
        "&uuml;": "&#252;",
        "&yacute;": "&#53;",
        "&thorn;": "&#254;",
        "&yuml;": "&#255;",
        "&quot;": "&#34;",
        "&amp;": "&#38;",
        " & ": " &#38; ",
        " Q&A ": " Q&#38;A ",
        "&lt;": "&#38;",
        "&gt;": "&#62;",
        "&apos;": "&#39;",
        "&OElig;": "&#338;",
        "&oelig;": "&#339;",
        "&Scaron;": "&#352;",
        "&scaron;": "&#353;",
        "&Yuml;": "&#376;",
        "&circ;": "&#710;",
        "&tilde;": "&#732;",
        "&ensp;": "&#8194;",
        "&emsp;": "&#8195;",
        "&thinsp;": "&#8201;",
        "&zwnj;": "&#8204;",
        "&zwj;": "&#8205;",
        "&lrm;": "&#8206;",
        "&rlm;": "&#8207;",
        "&ndash;": "&#8211;",
        "&mdash;": "&#8212;",
        "&lsquo;": "&#8216;",
        "&rsquo;": "&#8217;",
        "&sbquo;": "&#8218;",
        "&ldquo;": "&#8220;",
        "&rdquo;": "&#8221;",
        "&bdquo;": "&#8222;",
        "&dagger;": "&#8224;",
        "&Dagger;": "&#8225;",
        "&permil;": "&#8240;",
        "&lsaquo;": "&#8249;",
        "&rsaquo;": "&#8250;",
        "&euro;": "&#8364;",
        "&fnof;": "&#402;",
        "&Alpha;": "&#913;",
        "&Beta;": "&#914;",
        "&Gamma;": "&#915;",
        "&Delta;": "&#916;",
        "&Epsilon;": "&#917;",
        "&Zeta;": "&#918;",
        "&Eta;": "&#919;",
        "&Theta;": "&#920;",
        "&Iota;": "&#921;",
        "&Kappa;": "&#922;",
        "&Lambda;": "&#923;",
        "&Mu;": "&#924;",
        "&Nu;": "&#925;",
        "&Xi;": "&#926;",
        "&Omicron;": "&#927;",
        "&Pi;": "&#928;",
        "&Rho;": "&#929;",
        "&Sigma;": "&#931;",
        "&Tau;": "&#932;",
        "&Upsilon;": "&#933;",
        "&Phi;": "&#934;",
        "&Chi;": "&#935;",
        "&Psi;": "&#936;",
        "&Omega;": "&#937;",
        "&alpha;": "&#945;",
        "&beta;": "&#946;",
        "&gamma;": "&#947;",
        "&delta;": "&#948;",
        "&epsilon;": "&#949;",
        "&zeta;": "&#950;",
        "&eta;": "&#951;",
        "&theta;": "&#952;",
        "&iota;": "&#953;",
        "&kappa;": "&#954;",
        "&lambda;": "&#955;",
        "&mu;": "&#956;",
        "&nu;": "&#957;",
        "&xi;": "&#958;",
        "&omicron;": "&#959;",
        "&pi;": "&#960;",
        "&rho;": "&#961;",
        "&sigmaf;": "&#962;",
        "&sigma;": "&#963;",
        "&tau;": "&#964;",
        "&upsilon;": "&#965;",
        "&phi;": "&#966;",
        "&chi;": "&#967;",
        "&psi;": "&#968;",
        "&omega;": "&#969;",
        "&thetasym;": "&#977;",
        "&upsih;": "&#978;",
        "&piv;": "&#982;",
        "&bull;": "&#8226;",
        "&hellip;": "&#8230;",
        "&prime;": "&#8242;",
        "&Prime;": "&#8243;",
        "&oline;": "&#8254;",
        "&frasl;": "&#8260;",
        "&weierp;": "&#8472;",
        "&image;": "&#8465;",
        "&real;": "&#8476;",
        "&trade;": "&#8482;",
        "&alefsym;": "&#8501;",
        "&larr;": "&#8592;",
        "&uarr;": "&#8593;",
        "&rarr;": "&#8594;",
        "&darr;": "&#8595;",
        "&harr;": "&#8596;",
        "&crarr;": "&#8629;",
        "&lArr;": "&#8656;",
        "&uArr;": "&#8657;",
        "&rArr;": "&#8658;",
        "&dArr;": "&#8659;",
        "&hArr;": "&#8660;",
        "&forall;": "&#8704;",
        "&part;": "&#8706;",
        "&exist;": "&#8707;",
        "&empty;": "&#8709;",
        "&nabla;": "&#8711;",
        "&isin;": "&#8712;",
        "&notin;": "&#8713;",
        "&ni;": "&#8715;",
        "&prod;": "&#8719;",
        "&sum;": "&#8721;",
        "&minus;": "&#8722;",
        "&lowast;": "&#8727;",
        "&radic;": "&#8730;",
        "&prop;": "&#8733;",
        "&infin;": "&#8734;",
        "&ang;": "&#8736;",
        "&and;": "&#8743;",
        "&or;": "&#8744;",
        "&cap;": "&#8745;",
        "&cup;": "&#8746;",
        "&int;": "&#8747;",
        "&there4;": "&#8756;",
        "&sim;": "&#8764;",
        "&cong;": "&#8773;",
        "&asymp;": "&#8776;",
        "&ne;": "&#8800;",
        "&equiv;": "&#8801;",
        "&le;": "&#8804;",
        "&ge;": "&#8805;",
        "&sub;": "&#8834;",
        "&sup;": "&#8835;",
        "&nsub;": "&#8836;",
        "&sube;": "&#8838;",
        "&supe;": "&#8839;",
        "&oplus;": "&#8853;",
        "&otimes;": "&#8855;",
        "&perp;": "&#8869;",
        "&sdot;": "&#8901;",
        "&lceil;": "&#8968;",
        "&rceil;": "&#8969;",
        "&lfloor;": "&#8970;",
        "&rfloor;": "&#8971;",
        "&lang;": "&#9001;",
        "&rang;": "&#9002;",
        "&loz;": "&#9674;",
        "&spades;": "&#9824;",
        "&clubs;": "&#9827;",
        "&hearts;": "&#9829;",
        "&diams;": "&#9830;",

        "\u2026": "&#8230;",
    }

    if as_unicode:
        s = cast.to_unicode(s)

        for k, v in mapping.items():
            s = s.replace(unicode(k), unicode(v))

    else:
        for k, v in mapping.items():
            s = s.replace(k, v)

    # Encode all ampersands that don't preceed a numerical identifier.
    s = re.sub(r'&([^#])', '&#38;\g<1>', s)

    return s

def simplify_entities(s, as_unicode=True):
    """
    >>> simplify_entities('Hi &nbsp;there!')
    u'Hi  there!'

    >>> simplify_entities('Hi&mdash;there!')
    u'Hi--there!'

    """
    mapping = {
        u'&nbsp;': ' ',
        u'&rsquo;': "'",
        u'&ldquo;': '"',
        u'&rdquo;': '"',
        u'&mdash;': '--',
        u'&ndash;': '-',
        u'\u2013': '-',
        u'\u2014': '--',
        u'\u2018': "'",
        u'\u2019': "'",
        u'\u201c': '"',
        u'\u201C': '"',
        u'\u201d': '"',
        u'\u201D': '"',
        u'\\r': '',
        u'\\n': '',
    }

    if as_unicode:
        s = cast.to_unicode(s)

        for k, v in mapping.items():
            s = s.replace(k, v)

    else:
        for k, v in mapping.items():
            s = s.replace(k, v)

    return s

def remove_control_characters(s):
    """
    >>> remove_control_characters('hi there')
    u'hi there'

    This is an odd one:  unicodedata treats '\xad' as category 'Cf', so it gets stripped, but
    really, it's a valid 'greek' character (as definied in the sub_greeks function, which is 
    probably poorly named.)  Either way, this means that you probably want to sub_greeks() on
    your string before you send it here.
    >>> remove_control_characters('the Bah\xc3\xa1\u2019\xc3\xad belief')
    u'the Bah\xc3\xa1\u2019\xc3\xad belief'

    """
    s = cast.to_unicode(s)

    return "".join([ch for ch in s if unicodedata.category(ch)[0] != "C"])

def remove_comments(s):
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

    """
    if s is None:
        return None

    s = s.replace('//', '#')

    s = s.split('#')[0]

    return s.strip()

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

    >>> strip_tags("hi@there.com")
    'hi@there.com'

    >>> strip_tags("  hi   @ there . com")
    '  hi   @ there . com'

    >>> strip_tags("Have you seen López?")
    'Have you seen L\\xc3\\xb3pez?'

    """
    if value == None:
        return None

    if not isinstance(value, (str, unicode)):
        return value

    s = re.sub(r'<\/?p>', ' ', value)
    s = re.sub(r'<[^>]*?>', '', s)

    try:
        # If the original string had leading or trailing spaces, leave them be
        if value[0] == ' ' or value[-1] == ' ':
            return s
        else:
            # Otherwise, strip any that might have been created while removing tags
            return s.strip()

    except IndexError:
        return s

## ---------------------
if __name__ == "__main__":
    import doctest
    print "Testing..."
    doctest.testmod()
    print "Done."
