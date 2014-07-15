#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata

import cast


__license__ = "MIT"
__version__ = "0.3.3"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."

# Some of the items in `ascii_map` were seeded using a dictionary found within ReportLab's paraparser.py
# library, licensed under a BSD License.  For more, see: http://www.reportlab.com/software/opensource/
#
# Other's were found via unicode charts, code generation, and lots of trial and error.

ascii_map = [
    {'ansi_num': '&#32;', 'ansi_hex': u'\x20', 'ascii_replace': ' '},
    {'ansi_num': '&#33;', 'ansi_hex': u'\x21', 'ascii_replace': '!'},
    {'ansi_num': '&#34;', 'ansi_hex': u'\x22', 'ascii_replace': '"', 'html_entity': '&quot;'},
    {'ansi_num': '&#35;', 'ansi_hex': u'\x23', 'ascii_replace': '#'},
    {'ansi_num': '&#36;', 'ansi_hex': u'\x24', 'ascii_replace': '$'},
    {'ansi_num': '&#37;', 'ansi_hex': u'\x25', 'ascii_replace': '%'},
    {'ansi_num': '&#38;', 'ansi_hex': u'\x26', 'ascii_replace': '&', 'html_entity': '&amp;'},
    {'ansi_num': '&#39;', 'ansi_hex': u'\x27', 'ascii_replace': "'"},
    {'ansi_num': '&#40;', 'ansi_hex': u'\x28', 'ascii_replace': '('},
    {'ansi_num': '&#41;', 'ansi_hex': u'\x29', 'ascii_replace': ')'},
    {'ansi_num': '&#42;', 'ansi_hex': u'\x2A', 'ascii_replace': '*'},
    {'ansi_num': '&#43;', 'ansi_hex': u'\x2B', 'ascii_replace': '+'},
    {'ansi_num': '&#44;', 'ansi_hex': u'\x2C', 'ascii_replace': ','},
    {'ansi_num': '&#45;', 'ansi_hex': u'\x2D', 'ascii_replace': '-'},
    {'ansi_num': '&#46;', 'ansi_hex': u'\x2E', 'ascii_replace': '.'},
    {'ansi_num': '&#47;', 'ansi_hex': u'\x2F', 'ascii_replace': '/'},
    {'ansi_num': '&#48;', 'ansi_hex': u'\x30', 'ascii_replace': '0'},
    {'ansi_num': '&#49;', 'ansi_hex': u'\x31', 'ascii_replace': '1'},
    {'ansi_num': '&#50;', 'ansi_hex': u'\x32', 'ascii_replace': '2'},
    {'ansi_num': '&#51;', 'ansi_hex': u'\x33', 'ascii_replace': '3'},
    {'ansi_num': '&#52;', 'ansi_hex': u'\x34', 'ascii_replace': '4'},
    {'ansi_num': '&#53;', 'ansi_hex': u'\x35', 'ascii_replace': '5'},
    {'ansi_num': '&#54;', 'ansi_hex': u'\x36', 'ascii_replace': '6'},
    {'ansi_num': '&#55;', 'ansi_hex': u'\x37', 'ascii_replace': '7'},
    {'ansi_num': '&#56;', 'ansi_hex': u'\x38', 'ascii_replace': '8'},
    {'ansi_num': '&#57;', 'ansi_hex': u'\x39', 'ascii_replace': '9'},
    {'ansi_num': '&#58;', 'ansi_hex': u'\x3A', 'ascii_replace': ':'},
    {'ansi_num': '&#59;', 'ansi_hex': u'\x3B', 'ascii_replace': ';'},
    {'ansi_num': '&#60;', 'ansi_hex': u'\x3C', 'ascii_replace': '<', 'html_entity': '&lt;'},
    {'ansi_num': '&#61;', 'ansi_hex': u'\x3D', 'ascii_replace': '='},
    {'ansi_num': '&#62;', 'ansi_hex': u'\x3E', 'ascii_replace': '>', 'html_entity': '&gt;'},
    {'ansi_num': '&#63;', 'ansi_hex': u'\x3F', 'ascii_replace': '?'},
    {'ansi_num': '&#64;', 'ansi_hex': u'\x40', 'ascii_replace': '@'},
    {'ansi_num': '&#65;', 'ansi_hex': u'\x41', 'ascii_replace': 'A'},
    {'ansi_num': '&#66;', 'ansi_hex': u'\x42', 'ascii_replace': 'B'},
    {'ansi_num': '&#67;', 'ansi_hex': u'\x43', 'ascii_replace': 'C'},
    {'ansi_num': '&#68;', 'ansi_hex': u'\x44', 'ascii_replace': 'D'},
    {'ansi_num': '&#69;', 'ansi_hex': u'\x45', 'ascii_replace': 'E'},
    {'ansi_num': '&#70;', 'ansi_hex': u'\x46', 'ascii_replace': 'F'},
    {'ansi_num': '&#71;', 'ansi_hex': u'\x47', 'ascii_replace': 'G'},
    {'ansi_num': '&#72;', 'ansi_hex': u'\x48', 'ascii_replace': 'H'},
    {'ansi_num': '&#73;', 'ansi_hex': u'\x49', 'ascii_replace': 'I'},
    {'ansi_num': '&#74;', 'ansi_hex': u'\x4A', 'ascii_replace': 'J'},
    {'ansi_num': '&#75;', 'ansi_hex': u'\x4B', 'ascii_replace': 'K'},
    {'ansi_num': '&#76;', 'ansi_hex': u'\x4C', 'ascii_replace': 'L'},
    {'ansi_num': '&#77;', 'ansi_hex': u'\x4D', 'ascii_replace': 'M'},
    {'ansi_num': '&#78;', 'ansi_hex': u'\x4E', 'ascii_replace': 'N'},
    {'ansi_num': '&#79;', 'ansi_hex': u'\x4F', 'ascii_replace': 'O'},
    {'ansi_num': '&#80;', 'ansi_hex': u'\x50', 'ascii_replace': 'P'},
    {'ansi_num': '&#81;', 'ansi_hex': u'\x51', 'ascii_replace': 'Q'},
    {'ansi_num': '&#82;', 'ansi_hex': u'\x52', 'ascii_replace': 'R'},
    {'ansi_num': '&#83;', 'ansi_hex': u'\x53', 'ascii_replace': 'S'},
    {'ansi_num': '&#84;', 'ansi_hex': u'\x54', 'ascii_replace': 'T'},
    {'ansi_num': '&#85;', 'ansi_hex': u'\x55', 'ascii_replace': 'U'},
    {'ansi_num': '&#86;', 'ansi_hex': u'\x56', 'ascii_replace': 'V'},
    {'ansi_num': '&#87;', 'ansi_hex': u'\x57', 'ascii_replace': 'W'},
    {'ansi_num': '&#88;', 'ansi_hex': u'\x58', 'ascii_replace': 'X'},
    {'ansi_num': '&#89;', 'ansi_hex': u'\x59', 'ascii_replace': 'Y'},
    {'ansi_num': '&#90;', 'ansi_hex': u'\x5A', 'ascii_replace': 'Z'},
    {'ansi_num': '&#91;', 'ansi_hex': u'\x5B', 'ascii_replace': '['},
    {'ansi_num': '&#92;', 'ansi_hex': u'\x5C', 'ascii_replace': '\\'},
    {'ansi_num': '&#93;', 'ansi_hex': u'\x5D', 'ascii_replace': ']'},
    {'ansi_num': '&#94;', 'ansi_hex': u'\x5E', 'ascii_replace': '^'},
    {'ansi_num': '&#95;', 'ansi_hex': u'\x5F', 'ascii_replace': '_'},
    {'ansi_num': '&#96;', 'ansi_hex': u'\x60', 'ascii_replace': '`'},
    {'ansi_num': '&#97;', 'ansi_hex': u'\x61', 'ascii_replace': 'a'},
    {'ansi_num': '&#98;', 'ansi_hex': u'\x62', 'ascii_replace': 'b'},
    {'ansi_num': '&#99;', 'ansi_hex': u'\x63', 'ascii_replace': 'c'},
    {'ansi_num': '&#100;', 'ansi_hex': u'\x64', 'ascii_replace': 'd'},
    {'ansi_num': '&#101;', 'ansi_hex': u'\x65', 'ascii_replace': 'e'},
    {'ansi_num': '&#102;', 'ansi_hex': u'\x66', 'ascii_replace': 'f'},
    {'ansi_num': '&#103;', 'ansi_hex': u'\x67', 'ascii_replace': 'g'},
    {'ansi_num': '&#104;', 'ansi_hex': u'\x68', 'ascii_replace': 'h'},
    {'ansi_num': '&#105;', 'ansi_hex': u'\x69', 'ascii_replace': 'i'},
    {'ansi_num': '&#106;', 'ansi_hex': u'\x6A', 'ascii_replace': 'j'},
    {'ansi_num': '&#107;', 'ansi_hex': u'\x6B', 'ascii_replace': 'k'},
    {'ansi_num': '&#108;', 'ansi_hex': u'\x6C', 'ascii_replace': 'l'},
    {'ansi_num': '&#109;', 'ansi_hex': u'\x6D', 'ascii_replace': 'm'},
    {'ansi_num': '&#110;', 'ansi_hex': u'\x6E', 'ascii_replace': 'n'},
    {'ansi_num': '&#111;', 'ansi_hex': u'\x6F', 'ascii_replace': 'o'},
    {'ansi_num': '&#112;', 'ansi_hex': u'\x70', 'ascii_replace': 'p'},
    {'ansi_num': '&#113;', 'ansi_hex': u'\x71', 'ascii_replace': 'q'},
    {'ansi_num': '&#114;', 'ansi_hex': u'\x72', 'ascii_replace': 'r'},
    {'ansi_num': '&#115;', 'ansi_hex': u'\x73', 'ascii_replace': 's'},
    {'ansi_num': '&#116;', 'ansi_hex': u'\x74', 'ascii_replace': 't'},
    {'ansi_num': '&#117;', 'ansi_hex': u'\x75', 'ascii_replace': 'u'},
    {'ansi_num': '&#118;', 'ansi_hex': u'\x76', 'ascii_replace': 'v'},
    {'ansi_num': '&#119;', 'ansi_hex': u'\x77', 'ascii_replace': 'w'},
    {'ansi_num': '&#120;', 'ansi_hex': u'\x78', 'ascii_replace': 'x'},
    {'ansi_num': '&#121;', 'ansi_hex': u'\x79', 'ascii_replace': 'y'},
    {'ansi_num': '&#122;', 'ansi_hex': u'\x7A', 'ascii_replace': 'z'},
    {'ansi_num': '&#123;', 'ansi_hex': u'\x7B', 'ascii_replace': '{'},
    {'ansi_num': '&#124;', 'ansi_hex': u'\x7C', 'ascii_replace': '|'},
    {'ansi_num': '&#125;', 'ansi_hex': u'\x7D', 'ascii_replace': '}'},
    {'ansi_num': '&#126;', 'ansi_hex': u'\x7E', 'ascii_replace': '~'},
    {'ansi_num': '&#127;', 'ansi_hex': u'\x7F'},
    {'ansi_num': '&#128;', 'ansi_hex': u'€'},
    {'ansi_num': '&#129;', 'ansi_hex': u'\x81'},
    {'ansi_num': '&#130;', 'ansi_hex': u'‚', 'ascii_replace': ','},
    {'ansi_num': '&#131;', 'ansi_hex': u'ƒ'},
    {'ansi_num': '&#132;', 'ansi_hex': u'„'},
    {'ansi_num': '&#133;', 'ansi_hex': u'…', 'ascii_replace': '...'},
    {'ansi_num': '&#134;', 'ansi_hex': u'†'},
    {'ansi_num': '&#135;', 'ansi_hex': u'‡'},
    {'ansi_num': '&#136;', 'ansi_hex': u'ˆ', 'ascii_replace': '^'},
    {'ansi_num': '&#137;', 'ansi_hex': u'‰'},
    {'ansi_num': '&#138;', 'ansi_hex': u'Š'},
    {'ansi_num': '&#139;', 'ansi_hex': u'‹', 'ascii_replace': '<'},
    {'ansi_num': '&#140;', 'ansi_hex': u'Œ'},
    {'ansi_num': '&#141;', 'ansi_hex': u'\x8D'},
    {'ansi_num': '&#142;', 'ansi_hex': u'Ž'},
    {'ansi_num': '&#143;', 'ansi_hex': u'\x8F'},
    {'ansi_num': '&#144;', 'ansi_hex': u'\x90'},
    {'ansi_num': '&#145;', 'ansi_hex': u'‘'},
    {'ansi_num': '&#146;', 'ansi_hex': u'’'},
    {'ansi_num': '&#147;', 'ansi_hex': u'“', 'ascii_replace': '"'},
    {'ansi_num': '&#148;', 'ansi_hex': u'”', 'ascii_replace': '"'},
    {'ansi_num': '&#149;', 'ansi_hex': u'•'},
    {'ansi_num': '&#150;', 'ansi_hex': u'–'},
    {'ansi_num': '&#151;', 'ansi_hex': u'—'},
    {'ansi_num': '&#152;', 'ansi_hex': u'˜', 'ascii_replace': '~'},
    {'ansi_num': '&#153;', 'ansi_hex': u'™', 'html_entity': '&trade;'},
    {'ansi_num': '&#154;', 'ansi_hex': u'š'},
    {'ansi_num': '&#155;', 'ansi_hex': u'›', 'ascii_replace': '>'},
    {'ansi_num': '&#156;', 'ansi_hex': u'œ'},
    {'ansi_num': '&#157;', 'ansi_hex': u'\x9D'},
    {'ansi_num': '&#158;', 'ansi_hex': u'ž'},
    {'ansi_num': '&#159;', 'ansi_hex': u'Ÿ'},
    {'ansi_num': '&#160;', 'ansi_hex': (u'\xc2\xa0', u'\xA0'), 'html_entity': '&nbsp;'},
    {'ansi_num': '&#161;', 'ansi_hex': (u'¡', u'\xc2\xa1', u'\xA1'), 'html_entity': '&iexcl;'},
    {'ansi_num': '&#162;', 'ansi_hex': (u'¢', u'\xc2\xa2', u'\xA2'), 'html_entity': '&cent;'},
    {'ansi_num': '&#163;', 'ansi_hex': (u'£', u'\xc2\xa3', u'\xA3'), 'html_entity': '&pound;'},
    {'ansi_num': '&#164;', 'ansi_hex': (u'¤', u'\xc2\xa4', u'\xA4'), 'html_entity': '&curren;'},
    {'ansi_num': '&#165;', 'ansi_hex': (u'¥', u'\xc2\xa5', u'\xA5'), 'html_entity': '&yen;'},
    {'ansi_num': '&#166;', 'ansi_hex': (u'¦', u'\xc2\xa6', u'\xA6'), 'html_entity': '&brvbar;'},
    {'ansi_num': '&#167;', 'ansi_hex': (u'§', u'\xc2\xa7', u'\xA7'), 'html_entity': '&sect;'},
    {'ansi_num': '&#168;', 'ansi_hex': (u'¨', u'\xc2\xa8', u'\xA8'), 'html_entity': '&uml;'},
    {'ansi_num': '&#169;', 'ansi_hex': (u'©', u'\xc2\xa9', u'\xA9'), 'html_entity': '&copy;'},
    {'ansi_num': '&#170;', 'ansi_hex': (u'ª', u'\xc2\xaa', u'\xAA'), 'html_entity': '&ordf;'},
    {'ansi_num': '&#171;', 'ansi_hex': (u'«', u'\xc2\xab', u'\xAB'), 'html_entity': '&laquo;'},
    {'ansi_num': '&#172;', 'ansi_hex': (u'¬', u'\xc2\xac', u'\xAC'), 'html_entity': '&not;'},
    {'ansi_num': '&#173;', 'ansi_hex': (u'\xc2\xad', u'\xAD'), 'html_entity': '&shy;'},
    {'ansi_num': '&#174;', 'ansi_hex': (u'®', u'\xc2\xae', u'\xAE'), 'html_entity': '&reg;'},
    {'ansi_num': '&#175;', 'ansi_hex': (u'¯', u'\xc2\xaf', u'\xAF'), 'html_entity': '&macr;'},
    {'ansi_num': '&#176;', 'ansi_hex': (u'°', u'\xc2\xb0', u'\xB0'), 'html_entity': '&deg;'},
    {'ansi_num': '&#177;', 'ansi_hex': (u'±', u'\xc2\xb1', u'\xB1'), 'html_entity': '&plusmn;'},
    {'ansi_num': '&#178;', 'ansi_hex': (u'²', u'\xc2\xb2', u'\xB2'), 'html_entity': '&sup2;'},
    {'ansi_num': '&#179;', 'ansi_hex': (u'³', u'\xc2\xb3', u'\xB3'), 'html_entity': '&sup3;'},
    {'ansi_num': '&#180;', 'ansi_hex': (u'´', u'\xc2\xb4', u'\xB4'), 'html_entity': '&acute;'},
    {'ansi_num': '&#181;', 'ansi_hex': (u'µ', u'\xc2\xb5', u'\xB5'), 'html_entity': '&micro;'},
    {'ansi_num': '&#182;', 'ansi_hex': (u'¶', u'\xc2\xb6', u'\xB6'), 'html_entity': '&para;'},
    {'ansi_num': '&#183;', 'ansi_hex': (u'·', u'\xc2\xb7', u'\xB7'), 'html_entity': '&middot;'},
    {'ansi_num': '&#184;', 'ansi_hex': (u'¸', u'\xc2\xb8', u'\xB8'), 'html_entity': '&cedil;'},
    {'ansi_num': '&#185;', 'ansi_hex': (u'¹', u'\xc2\xb9', u'\xB9'), 'html_entity': '&sup1;'},
    {'ansi_num': '&#186;', 'ansi_hex': (u'º', u'\xc2\xba', u'\xBA'), 'html_entity': '&ordm;'},
    {'ansi_num': '&#187;', 'ansi_hex': (u'»', u'\xc2\xbb', u'\xBB'), 'html_entity': '&raquo;'},
    {'ansi_num': '&#188;', 'ansi_hex': (u'¼', u'\xc2\xbc', u'\xBC'), 'html_entity': '&frac14;'},
    {'ansi_num': '&#189;', 'ansi_hex': (u'½', u'\xc2\xbd', u'\xBD'), 'html_entity': '&frac12;'},
    {'ansi_num': '&#190;', 'ansi_hex': (u'¾', u'\xc2\xbe', u'\xBE'), 'html_entity': '&frac34;'},
    {'ansi_num': '&#191;', 'ansi_hex': (u'¿', u'\xc2\xbf', u'\xBF'), 'html_entity': '&iquest;'},
    {'ansi_num': '&#192;', 'ansi_hex': (u'À', u'\xc3\x80', u'\xC0'), 'html_entity': '&Agrave;'},
    {'ansi_num': '&#193;', 'ansi_hex': (u'Á', u'\xc3\x81', u'\xC1'), 'html_entity': '&Aacute;'},
    {'ansi_num': '&#194;', 'ansi_hex': (u'Â', u'\xc3\x82', u'\xC2'), 'html_entity': '&Acirc;'},
    {'ansi_num': '&#195;', 'ansi_hex': (u'Ã', u'\xc3\x83', u'\xC3'), 'html_entity': '&Atilde;'},
    {'ansi_num': '&#196;', 'ansi_hex': (u'Ä', u'\xc3\x84', u'\xC4'), 'html_entity': '&Auml;'},
    {'ansi_num': '&#197;', 'ansi_hex': (u'Å', u'\xc3\x85', u'\xC5'), 'html_entity': '&Aring;'},
    {'ansi_num': '&#198;', 'ansi_hex': (u'Æ', u'\xc3\x86', u'\xC6'), 'html_entity': '&AElig;'},
    {'ansi_num': '&#199;', 'ansi_hex': (u'Ç', u'\xc3\x87', u'\xC7'), 'html_entity': '&Ccedil;'},
    {'ansi_num': '&#200;', 'ansi_hex': (u'È', u'\xc3\x88', u'\xC8'), 'html_entity': '&Egrave;'},
    {'ansi_num': '&#201;', 'ansi_hex': (u'É', u'\xc3\x89', u'\xC9'), 'html_entity': '&Eacute;'},
    {'ansi_num': '&#202;', 'ansi_hex': (u'Ê', u'\xc3\x8a', u'\xCA'), 'html_entity': '&Ecirc;'},
    {'ansi_num': '&#203;', 'ansi_hex': (u'Ë', u'\xc3\x8b', u'\xCB'), 'html_entity': '&Euml;'},
    {'ansi_num': '&#204;', 'ansi_hex': (u'Ì', u'\xc3\x8c', u'\xCC'), 'html_entity': '&Igrave;'},
    {'ansi_num': '&#205;', 'ansi_hex': (u'Í', u'\xc3\x8d', u'\xCD'), 'html_entity': '&Iacute;'},
    {'ansi_num': '&#206;', 'ansi_hex': (u'Î', u'\xc3\x8e', u'\xCE'), 'html_entity': '&Icirc;'},
    {'ansi_num': '&#207;', 'ansi_hex': (u'Ï', u'\xc3\x8f', u'\xCF'), 'html_entity': '&Iuml;'},
    {'ansi_num': '&#208;', 'ansi_hex': (u'Ð', u'\xc3\x90', u'\xD0'), 'html_entity': '&ETH;'},
    {'ansi_num': '&#209;', 'ansi_hex': (u'Ñ', u'\xc3\x91', u'\xD1'), 'html_entity': '&Ntilde;'},
    {'ansi_num': '&#210;', 'ansi_hex': (u'Ò', u'\xc3\x92', u'\xD2'), 'html_entity': '&Ograve;'},
    {'ansi_num': '&#211;', 'ansi_hex': (u'Ó', u'\xc3\x93', u'\xD3'), 'html_entity': '&Oacute;'},
    {'ansi_num': '&#212;', 'ansi_hex': (u'Ô', u'\xc3\x94', u'\xD4'), 'html_entity': '&Ocirc;'},
    {'ansi_num': '&#213;', 'ansi_hex': (u'Õ', u'\xc3\x95', u'\xD5'), 'html_entity': '&Otilde;'},
    {'ansi_num': '&#214;', 'ansi_hex': (u'Ö', u'\xc3\x96', u'\xD6'), 'html_entity': '&Ouml;'},
    {'ansi_num': '&#215;', 'ansi_hex': (u'×', u'\xc3\x97', u'\xD7'), 'html_entity': '&times;'},
    {'ansi_num': '&#216;', 'ansi_hex': (u'Ø', u'\xc3\x98', u'\xD8'), 'html_entity': '&Oslash;'},
    {'ansi_num': '&#217;', 'ansi_hex': (u'Ù', u'\xc3\x99', u'\xD9'), 'html_entity': '&Ugrave;'},
    {'ansi_num': '&#218;', 'ansi_hex': (u'Ú', u'\xc3\x9a', u'\xDA'), 'html_entity': '&Uacute;'},
    {'ansi_num': '&#219;', 'ansi_hex': (u'Û', u'\xc3\x9b', u'\xDB'), 'html_entity': '&Ucirc;'},
    {'ansi_num': '&#220;', 'ansi_hex': (u'Ü', u'\xc3\x9c', u'\xDC'), 'html_entity': '&Uuml;'},
    {'ansi_num': '&#221;', 'ansi_hex': (u'Ý', u'\xc3\x9d', u'\xDD'), 'html_entity': '&Yacute;'},
    {'ansi_num': '&#222;', 'ansi_hex': (u'Þ', u'\xc3\x9e', u'\xDE'), 'html_entity': '&THORN;'},
    {'ansi_num': '&#223;', 'ansi_hex': (u'ß', u'\xc3\x9f', u'\xDF'), 'html_entity': '&szlig;'},
    {'ansi_num': ('&#224;', '&#24;'), 'ansi_hex': (u'à', u'\xc3\xa0', u'\xE0'), 'html_entity': '&agrave;'},
    {'ansi_num': ('&#225;', '&#25;'), 'ansi_hex': (u'á', u'\xc3\xa1', u'\xE1'), 'html_entity': '&aacute;'},
    {'ansi_num': '&#226;', 'ansi_hex': (u'â', u'\xc3\xa2', u'\xE2'), 'html_entity': '&acirc;'},
    {'ansi_num': '&#227;', 'ansi_hex': (u'ã', u'\xc3\xa3', u'\xE3'), 'html_entity': '&atilde;'},
    {'ansi_num': '&#228;', 'ansi_hex': (u'ä', u'\xc3\xa4', u'\xE4'), 'html_entity': '&auml;'},
    {'ansi_num': '&#229;', 'ansi_hex': (u'å', u'\xc3\xa5', u'\xE5'), 'html_entity': '&aring;'},
    {'ansi_num': '&#230;', 'ansi_hex': (u'æ', u'\xc3\xa6', u'\xE6'), 'html_entity': '&aelig;'},
    {'ansi_num': '&#231;', 'ansi_hex': (u'ç', u'\xc3\xa7', u'\xE7'), 'html_entity': '&ccedil;'},
    {'ansi_num': '&#232;', 'ansi_hex': (u'è', u'\xc3\xa8', u'\xE8'), 'html_entity': '&egrave;'},
    {'ansi_num': '&#233;', 'ansi_hex': (u'é', u'\xc3\xa9', u'\xE9'), 'html_entity': '&eacute;'},
    {'ansi_num': '&#234;', 'ansi_hex': (u'ê', u'\xc3\xaa', u'\xEA'), 'html_entity': '&ecirc;'},
    {'ansi_num': '&#235;', 'ansi_hex': (u'ë', u'\xc3\xab', u'\xEB'), 'html_entity': '&euml;'},
    {'ansi_num': '&#236;', 'ansi_hex': (u'ì', u'\xc3\xac', u'\xEC'), 'html_entity': '&igrave;'},
    {'ansi_num': '&#237;', 'ansi_hex': (u'í', u'\xc3\xad', u'\xED'), 'html_entity': '&iacute;'},
    {'ansi_num': '&#238;', 'ansi_hex': (u'î', u'\xc3\xae', u'\xEE'), 'html_entity': '&icirc;'},
    {'ansi_num': '&#239;', 'ansi_hex': (u'ï', u'\xc3\xaf', u'\xEF'), 'html_entity': '&iuml;'},
    {'ansi_num': '&#240;', 'ansi_hex': (u'ð', u'\xc3\xb0', u'\xF0'), 'html_entity': '&eth;'},
    {'ansi_num': '&#241;', 'ansi_hex': (u'ñ', u'\xc3\xb1', u'\xF1'), 'html_entity': '&ntilde;'},
    {'ansi_num': '&#242;', 'ansi_hex': (u'ò', u'\xc3\xb2', u'\xF2'), 'html_entity': '&ograve;'},
    {'ansi_num': '&#243;', 'ansi_hex': (u'ó', u'\xc3\xb3', u'\xF3'), 'html_entity': '&oacute;'},
    {'ansi_num': '&#244;', 'ansi_hex': (u'ô', u'\xc3\xb4', u'\xF4', u'\xf4'), 'html_entity': '&ocirc;'},
    {'ansi_num': '&#245;', 'ansi_hex': (u'õ', u'\xc3\xb5', u'\xF5'), 'html_entity': '&otilde;'},
    {'ansi_num': '&#246;', 'ansi_hex': (u'ö', u'\xc3\xb6', u'\xF6'), 'html_entity': '&ouml;'},
    {'ansi_num': '&#247;', 'ansi_hex': (u'÷', u'\xc3\xb7', u'\xF7'), 'html_entity': '&divide;'},
    {'ansi_num': '&#248;', 'ansi_hex': (u'ø', u'\xc3\xb8', u'\xF8'), 'html_entity': '&oslash;'},
    {'ansi_num': '&#249;', 'ansi_hex': (u'ù', u'\xc3\xb9', u'\xF9'), 'html_entity': '&ugrave;'},
    {'ansi_num': '&#250;', 'ansi_hex': (u'ú', u'\xc3\xba', u'\xFA'), 'html_entity': '&uacute;'},
    {'ansi_num': '&#251;', 'ansi_hex': (u'û', u'\xc3\xbb', u'\xFB'), 'html_entity': '&ucirc;'},
    {'ansi_num': '&#252;', 'ansi_hex': (u'ü', u'\xc3\xbc', u'\xFC'), 'html_entity': '&uuml;'},
    {'ansi_num': '&#253;', 'ansi_hex': (u'ý', u'\xc3\xbd', u'\xFD'), 'html_entity': '&yacute;'},
    {'ansi_num': '&#254;', 'ansi_hex': (u'þ', u'\xc3\xbe', u'\xFE'), 'html_entity': '&thorn;'},
    {'ansi_num': '&#255;', 'ansi_hex': (u'ÿ', u'\xc3\xbf', u'\xFF'), 'html_entity': '&yuml;'},
    {'ansi_num': '&#256;', 'ansi_hex': u'Ā'},
    {'ansi_num': '&#257;', 'ansi_hex': u'ā'},
    {'ansi_num': '&#258;', 'ansi_hex': u'Ă'},
    {'ansi_num': '&#259;', 'ansi_hex': u'ă'},
    {'ansi_num': '&#260;', 'ansi_hex': u'Ą'},
    {'ansi_num': '&#261;', 'ansi_hex': u'ą'},
    {'ansi_num': '&#262;', 'ansi_hex': u'Ć'},
    {'ansi_num': '&#263;', 'ansi_hex': u'ć'},
    {'ansi_num': '&#264;', 'ansi_hex': u'Ĉ'},
    {'ansi_num': '&#265;', 'ansi_hex': u'ĉ'},
    {'ansi_num': '&#266;', 'ansi_hex': u'Ċ'},
    {'ansi_num': '&#267;', 'ansi_hex': u'ċ'},
    {'ansi_num': '&#268;', 'ansi_hex': u'Č'},
    {'ansi_num': '&#269;', 'ansi_hex': u'č'},
    {'ansi_num': '&#270;', 'ansi_hex': u'Ď'},
    {'ansi_num': '&#271;', 'ansi_hex': u'ď'},
    {'ansi_num': '&#272;', 'ansi_hex': u'Đ'},
    {'ansi_num': '&#273;', 'ansi_hex': u'đ'},
    {'ansi_num': '&#274;', 'ansi_hex': u'Ē'},
    {'ansi_num': '&#275;', 'ansi_hex': u'ē'},
    {'ansi_num': '&#276;', 'ansi_hex': u'Ĕ'},
    {'ansi_num': '&#277;', 'ansi_hex': u'ĕ'},
    {'ansi_num': '&#278;', 'ansi_hex': u'Ė'},
    {'ansi_num': '&#279;', 'ansi_hex': u'ė'},
    {'ansi_num': '&#280;', 'ansi_hex': u'Ę'},
    {'ansi_num': '&#281;', 'ansi_hex': u'ę'},
    {'ansi_num': '&#282;', 'ansi_hex': u'Ě'},
    {'ansi_num': '&#283;', 'ansi_hex': u'ě'},
    {'ansi_num': '&#284;', 'ansi_hex': u'Ĝ'},
    {'ansi_num': '&#285;', 'ansi_hex': u'ĝ'},
    {'ansi_num': '&#286;', 'ansi_hex': u'Ğ'},
    {'ansi_num': '&#287;', 'ansi_hex': u'ğ'},
    {'ansi_num': '&#288;', 'ansi_hex': u'Ġ'},
    {'ansi_num': '&#289;', 'ansi_hex': u'ġ'},
    {'ansi_num': '&#290;', 'ansi_hex': u'Ģ'},
    {'ansi_num': '&#291;', 'ansi_hex': u'ģ'},
    {'ansi_num': '&#292;', 'ansi_hex': u'Ĥ'},
    {'ansi_num': '&#293;', 'ansi_hex': u'ĥ'},
    {'ansi_num': '&#294;', 'ansi_hex': u'Ħ'},
    {'ansi_num': '&#295;', 'ansi_hex': u'ħ'},
    {'ansi_num': '&#296;', 'ansi_hex': u'Ĩ'},
    {'ansi_num': '&#297;', 'ansi_hex': u'ĩ'},
    {'ansi_num': '&#298;', 'ansi_hex': u'Ī'},
    {'ansi_num': '&#299;', 'ansi_hex': u'ī'},
    {'ansi_num': '&#300;', 'ansi_hex': u'Ĭ'},
    {'ansi_num': '&#301;', 'ansi_hex': u'ĭ'},
    {'ansi_num': '&#302;', 'ansi_hex': u'Į'},
    {'ansi_num': '&#303;', 'ansi_hex': u'į'},
    {'ansi_num': '&#304;', 'ansi_hex': u'İ'},
    {'ansi_num': '&#305;', 'ansi_hex': u'ı'},
    {'ansi_num': '&#306;', 'ansi_hex': u'Ĳ'},
    {'ansi_num': '&#307;', 'ansi_hex': u'ĳ'},
    {'ansi_num': '&#308;', 'ansi_hex': u'Ĵ'},
    {'ansi_num': '&#309;', 'ansi_hex': u'ĵ'},
    {'ansi_num': '&#310;', 'ansi_hex': u'Ķ'},
    {'ansi_num': '&#311;', 'ansi_hex': u'ķ'},
    {'ansi_num': '&#312;', 'ansi_hex': u'ĸ'},
    {'ansi_num': '&#313;', 'ansi_hex': u'Ĺ'},
    {'ansi_num': '&#314;', 'ansi_hex': u'ĺ'},
    {'ansi_num': '&#315;', 'ansi_hex': u'Ļ'},
    {'ansi_num': '&#316;', 'ansi_hex': u'ļ'},
    {'ansi_num': '&#317;', 'ansi_hex': u'Ľ'},
    {'ansi_num': '&#318;', 'ansi_hex': u'ľ'},
    {'ansi_num': '&#319;', 'ansi_hex': u'Ŀ'},
    {'ansi_num': '&#320;', 'ansi_hex': u'ŀ'},
    {'ansi_num': '&#321;', 'ansi_hex': u'Ł'},
    {'ansi_num': '&#322;', 'ansi_hex': u'ł'},
    {'ansi_num': '&#323;', 'ansi_hex': u'Ń'},
    {'ansi_num': '&#324;', 'ansi_hex': u'ń'},
    {'ansi_num': '&#325;', 'ansi_hex': u'Ņ'},
    {'ansi_num': '&#326;', 'ansi_hex': u'ņ'},
    {'ansi_num': '&#327;', 'ansi_hex': u'Ň'},
    {'ansi_num': '&#328;', 'ansi_hex': u'ň'},
    {'ansi_num': '&#329;', 'ansi_hex': u'ŉ'},
    {'ansi_num': '&#330;', 'ansi_hex': u'Ŋ'},
    {'ansi_num': '&#331;', 'ansi_hex': u'ŋ'},
    {'ansi_num': '&#332;', 'ansi_hex': u'Ō'},
    {'ansi_num': '&#333;', 'ansi_hex': u'ō'},
    {'ansi_num': '&#334;', 'ansi_hex': u'Ŏ'},
    {'ansi_num': '&#335;', 'ansi_hex': u'ŏ'},
    {'ansi_num': '&#336;', 'ansi_hex': u'Ő'},
    {'ansi_num': '&#337;', 'ansi_hex': u'ő'},
    {'ansi_num': '&#338;', 'ansi_hex': (u'Œ', u'\xc5\x92', u'\x8C'), 'html_entity': '&OElig;'},
    {'ansi_num': '&#339;', 'ansi_hex': (u'œ', u'\xc5\x93', u'\x9C'), 'html_entity': '&oelig;'},
    {'ansi_num': '&#340;', 'ansi_hex': u'Ŕ'},
    {'ansi_num': '&#341;', 'ansi_hex': u'ŕ'},
    {'ansi_num': '&#342;', 'ansi_hex': u'Ŗ'},
    {'ansi_num': '&#343;', 'ansi_hex': u'ŗ'},
    {'ansi_num': '&#344;', 'ansi_hex': u'Ř'},
    {'ansi_num': '&#345;', 'ansi_hex': u'ř'},
    {'ansi_num': '&#346;', 'ansi_hex': u'Ś'},
    {'ansi_num': '&#347;', 'ansi_hex': u'ś'},
    {'ansi_num': '&#348;', 'ansi_hex': u'Ŝ'},
    {'ansi_num': '&#349;', 'ansi_hex': u'ŝ'},
    {'ansi_num': '&#350;', 'ansi_hex': u'Ş'},
    {'ansi_num': '&#351;', 'ansi_hex': u'ş'},
    {'ansi_num': '&#352;', 'ansi_hex': (u'Š', u'\xc5\xa0', u'\x8A'), 'html_entity': '&Scaron;'},
    {'ansi_num': '&#353;', 'ansi_hex': (u'š', u'\xc5\xa1', u'\x9A'), 'html_entity': '&scaron;'},
    {'ansi_num': '&#354;', 'ansi_hex': u'Ţ'},
    {'ansi_num': '&#355;', 'ansi_hex': u'ţ'},
    {'ansi_num': '&#356;', 'ansi_hex': u'Ť'},
    {'ansi_num': '&#357;', 'ansi_hex': u'ť'},
    {'ansi_num': '&#358;', 'ansi_hex': u'Ŧ'},
    {'ansi_num': '&#359;', 'ansi_hex': u'ŧ'},
    {'ansi_num': '&#360;', 'ansi_hex': u'Ũ'},
    {'ansi_num': '&#361;', 'ansi_hex': u'ũ'},
    {'ansi_num': '&#362;', 'ansi_hex': u'Ū'},
    {'ansi_num': '&#363;', 'ansi_hex': u'ū'},
    {'ansi_num': '&#364;', 'ansi_hex': u'Ŭ'},
    {'ansi_num': '&#365;', 'ansi_hex': u'ŭ'},
    {'ansi_num': '&#366;', 'ansi_hex': u'Ů'},
    {'ansi_num': '&#367;', 'ansi_hex': u'ů'},
    {'ansi_num': '&#368;', 'ansi_hex': u'Ű'},
    {'ansi_num': '&#369;', 'ansi_hex': u'ű'},
    {'ansi_num': '&#370;', 'ansi_hex': u'Ų'},
    {'ansi_num': '&#371;', 'ansi_hex': u'ų'},
    {'ansi_num': '&#372;', 'ansi_hex': u'Ŵ'},
    {'ansi_num': '&#373;', 'ansi_hex': u'ŵ'},
    {'ansi_num': '&#374;', 'ansi_hex': u'Ŷ'},
    {'ansi_num': '&#375;', 'ansi_hex': u'ŷ'},
    {'ansi_num': '&#376;', 'ansi_hex': (u'Ÿ', u'\xc5\xb8', u'\x9F'), 'html_entity': '&Yuml;'},
    {'ansi_num': '&#377;', 'ansi_hex': u'Ź'},
    {'ansi_num': '&#378;', 'ansi_hex': u'ź'},
    {'ansi_num': '&#379;', 'ansi_hex': u'Ż'},
    {'ansi_num': '&#380;', 'ansi_hex': u'ż'},
    {'ansi_num': '&#381;', 'ansi_hex': u'\x8E'},
    {'ansi_num': '&#382;', 'ansi_hex': u'\x9E'},
    {'ansi_num': '&#383;', 'ansi_hex': u'ſ'},
    {'ansi_num': '&#384;', 'ansi_hex': u'ƀ'},
    {'ansi_num': '&#385;', 'ansi_hex': u'Ɓ'},
    {'ansi_num': '&#386;', 'ansi_hex': u'Ƃ'},
    {'ansi_num': '&#387;', 'ansi_hex': u'ƃ'},
    {'ansi_num': '&#388;', 'ansi_hex': u'Ƅ'},
    {'ansi_num': '&#389;', 'ansi_hex': u'ƅ'},
    {'ansi_num': '&#390;', 'ansi_hex': u'Ɔ'},
    {'ansi_num': '&#391;', 'ansi_hex': u'Ƈ'},
    {'ansi_num': '&#392;', 'ansi_hex': u'ƈ'},
    {'ansi_num': '&#393;', 'ansi_hex': u'Ɖ'},
    {'ansi_num': '&#394;', 'ansi_hex': u'Ɗ'},
    {'ansi_num': '&#395;', 'ansi_hex': u'Ƌ'},
    {'ansi_num': '&#396;', 'ansi_hex': u'ƌ'},
    {'ansi_num': '&#397;', 'ansi_hex': u'ƍ'},
    {'ansi_num': '&#398;', 'ansi_hex': u'Ǝ'},
    {'ansi_num': '&#399;', 'ansi_hex': u'Ə'},
    {'ansi_num': '&#400;', 'ansi_hex': u'Ɛ'},
    {'ansi_num': '&#401;', 'ansi_hex': u'Ƒ'},
    {'ansi_num': '&#402;', 'ansi_hex': (u'ƒ', u'\xc6\x92', u'\x83'), 'html_entity': '&fnof;'},
    {'ansi_num': '&#403;', 'ansi_hex': u'Ɠ'},
    {'ansi_num': '&#404;', 'ansi_hex': u'Ɣ'},
    {'ansi_num': '&#405;', 'ansi_hex': u'ƕ'},
    {'ansi_num': '&#406;', 'ansi_hex': u'Ɩ'},
    {'ansi_num': '&#407;', 'ansi_hex': u'Ɨ'},
    {'ansi_num': '&#408;', 'ansi_hex': u'Ƙ'},
    {'ansi_num': '&#409;', 'ansi_hex': u'ƙ'},
    {'ansi_num': '&#410;', 'ansi_hex': u'ƚ'},
    {'ansi_num': '&#411;', 'ansi_hex': u'ƛ'},
    {'ansi_num': '&#412;', 'ansi_hex': u'Ɯ'},
    {'ansi_num': '&#413;', 'ansi_hex': u'Ɲ'},
    {'ansi_num': '&#414;', 'ansi_hex': u'ƞ'},
    {'ansi_num': '&#415;', 'ansi_hex': u'Ɵ'},
    {'ansi_num': '&#416;', 'ansi_hex': u'Ơ'},
    {'ansi_num': '&#417;', 'ansi_hex': u'ơ'},
    {'ansi_num': '&#418;', 'ansi_hex': u'Ƣ'},
    {'ansi_num': '&#419;', 'ansi_hex': u'ƣ'},
    {'ansi_num': '&#420;', 'ansi_hex': u'Ƥ'},
    {'ansi_num': '&#421;', 'ansi_hex': u'ƥ'},
    {'ansi_num': '&#422;', 'ansi_hex': u'Ʀ'},
    {'ansi_num': '&#423;', 'ansi_hex': u'Ƨ'},
    {'ansi_num': '&#424;', 'ansi_hex': u'ƨ'},
    {'ansi_num': '&#425;', 'ansi_hex': u'Ʃ'},
    {'ansi_num': '&#426;', 'ansi_hex': u'ƪ'},
    {'ansi_num': '&#427;', 'ansi_hex': u'ƫ'},
    {'ansi_num': '&#428;', 'ansi_hex': u'Ƭ'},
    {'ansi_num': '&#429;', 'ansi_hex': u'ƭ'},
    {'ansi_num': '&#430;', 'ansi_hex': u'Ʈ'},
    {'ansi_num': '&#431;', 'ansi_hex': u'Ư'},
    {'ansi_num': '&#432;', 'ansi_hex': u'ư'},
    {'ansi_num': '&#433;', 'ansi_hex': u'Ʊ'},
    {'ansi_num': '&#434;', 'ansi_hex': u'Ʋ'},
    {'ansi_num': '&#435;', 'ansi_hex': u'Ƴ'},
    {'ansi_num': '&#436;', 'ansi_hex': u'ƴ'},
    {'ansi_num': '&#437;', 'ansi_hex': u'Ƶ'},
    {'ansi_num': '&#438;', 'ansi_hex': u'ƶ'},
    {'ansi_num': '&#439;', 'ansi_hex': u'Ʒ'},
    {'ansi_num': '&#440;', 'ansi_hex': u'Ƹ'},
    {'ansi_num': '&#441;', 'ansi_hex': u'ƹ'},
    {'ansi_num': '&#442;', 'ansi_hex': u'ƺ'},
    {'ansi_num': '&#443;', 'ansi_hex': u'ƻ'},
    {'ansi_num': '&#444;', 'ansi_hex': u'Ƽ'},
    {'ansi_num': '&#445;', 'ansi_hex': u'ƽ'},
    {'ansi_num': '&#446;', 'ansi_hex': u'ƾ'},
    {'ansi_num': '&#447;', 'ansi_hex': u'ƿ'},
    {'ansi_num': '&#448;', 'ansi_hex': u'ǀ'},
    {'ansi_num': '&#449;', 'ansi_hex': u'ǁ'},
    {'ansi_num': '&#450;', 'ansi_hex': u'ǂ'},
    {'ansi_num': '&#451;', 'ansi_hex': u'ǃ'},
    {'ansi_num': '&#452;', 'ansi_hex': u'Ǆ'},
    {'ansi_num': '&#453;', 'ansi_hex': u'ǅ'},
    {'ansi_num': '&#454;', 'ansi_hex': u'ǆ'},
    {'ansi_num': '&#455;', 'ansi_hex': u'Ǉ'},
    {'ansi_num': '&#456;', 'ansi_hex': u'ǈ'},
    {'ansi_num': '&#457;', 'ansi_hex': u'ǉ'},
    {'ansi_num': '&#458;', 'ansi_hex': u'Ǌ'},
    {'ansi_num': '&#459;', 'ansi_hex': u'ǋ'},
    {'ansi_num': '&#460;', 'ansi_hex': u'ǌ'},
    {'ansi_num': '&#461;', 'ansi_hex': u'Ǎ'},
    {'ansi_num': '&#462;', 'ansi_hex': u'ǎ'},
    {'ansi_num': '&#463;', 'ansi_hex': u'Ǐ'},
    {'ansi_num': '&#464;', 'ansi_hex': u'ǐ'},
    {'ansi_num': '&#465;', 'ansi_hex': u'Ǒ'},
    {'ansi_num': '&#466;', 'ansi_hex': u'ǒ'},
    {'ansi_num': '&#467;', 'ansi_hex': u'Ǔ'},
    {'ansi_num': '&#468;', 'ansi_hex': u'ǔ'},
    {'ansi_num': '&#469;', 'ansi_hex': u'Ǖ'},
    {'ansi_num': '&#470;', 'ansi_hex': u'ǖ'},
    {'ansi_num': '&#471;', 'ansi_hex': u'Ǘ'},
    {'ansi_num': '&#472;', 'ansi_hex': u'ǘ'},
    {'ansi_num': '&#473;', 'ansi_hex': u'Ǚ'},
    {'ansi_num': '&#474;', 'ansi_hex': u'ǚ'},
    {'ansi_num': '&#475;', 'ansi_hex': u'Ǜ'},
    {'ansi_num': '&#476;', 'ansi_hex': u'ǜ'},
    {'ansi_num': '&#477;', 'ansi_hex': u'ǝ'},
    {'ansi_num': '&#478;', 'ansi_hex': u'Ǟ'},
    {'ansi_num': '&#479;', 'ansi_hex': u'ǟ'},
    {'ansi_num': '&#480;', 'ansi_hex': u'Ǡ'},
    {'ansi_num': '&#481;', 'ansi_hex': u'ǡ'},
    {'ansi_num': '&#482;', 'ansi_hex': u'Ǣ'},
    {'ansi_num': '&#483;', 'ansi_hex': u'ǣ'},
    {'ansi_num': '&#484;', 'ansi_hex': u'Ǥ'},
    {'ansi_num': '&#485;', 'ansi_hex': u'ǥ'},
    {'ansi_num': '&#486;', 'ansi_hex': u'Ǧ'},
    {'ansi_num': '&#487;', 'ansi_hex': u'ǧ'},
    {'ansi_num': '&#488;', 'ansi_hex': u'Ǩ'},
    {'ansi_num': '&#489;', 'ansi_hex': u'ǩ'},
    {'ansi_num': '&#490;', 'ansi_hex': u'Ǫ'},
    {'ansi_num': '&#491;', 'ansi_hex': u'ǫ'},
    {'ansi_num': '&#492;', 'ansi_hex': u'Ǭ'},
    {'ansi_num': '&#493;', 'ansi_hex': u'ǭ'},
    {'ansi_num': '&#494;', 'ansi_hex': u'Ǯ'},
    {'ansi_num': '&#495;', 'ansi_hex': u'ǯ'},
    {'ansi_num': '&#496;', 'ansi_hex': u'ǰ'},
    {'ansi_num': '&#497;', 'ansi_hex': u'Ǳ'},
    {'ansi_num': '&#498;', 'ansi_hex': u'ǲ'},
    {'ansi_num': '&#499;', 'ansi_hex': u'ǳ'},
    {'ansi_num': '&#500;', 'ansi_hex': u'Ǵ'},
    {'ansi_num': '&#501;', 'ansi_hex': u'ǵ'},
    {'ansi_num': '&#502;', 'ansi_hex': u'Ƕ'},
    {'ansi_num': '&#503;', 'ansi_hex': u'Ƿ'},
    {'ansi_num': '&#504;', 'ansi_hex': u'Ǹ'},
    {'ansi_num': '&#505;', 'ansi_hex': u'ǹ'},
    {'ansi_num': '&#506;', 'ansi_hex': u'Ǻ'},
    {'ansi_num': '&#507;', 'ansi_hex': u'ǻ'},
    {'ansi_num': '&#508;', 'ansi_hex': u'Ǽ'},
    {'ansi_num': '&#509;', 'ansi_hex': u'ǽ'},
    {'ansi_num': '&#510;', 'ansi_hex': u'Ǿ'},
    {'ansi_num': '&#511;', 'ansi_hex': u'ǿ'},
    {'ansi_num': '&#512;', 'ansi_hex': u'Ȁ'},
    {'ansi_num': '&#513;', 'ansi_hex': u'ȁ'},
    {'ansi_num': '&#514;', 'ansi_hex': u'Ȃ'},
    {'ansi_num': '&#515;', 'ansi_hex': u'ȃ'},
    {'ansi_num': '&#516;', 'ansi_hex': u'Ȅ'},
    {'ansi_num': '&#517;', 'ansi_hex': u'ȅ'},
    {'ansi_num': '&#518;', 'ansi_hex': u'Ȇ'},
    {'ansi_num': '&#519;', 'ansi_hex': u'ȇ'},
    {'ansi_num': '&#520;', 'ansi_hex': u'Ȉ'},
    {'ansi_num': '&#521;', 'ansi_hex': u'ȉ'},
    {'ansi_num': '&#522;', 'ansi_hex': u'Ȋ'},
    {'ansi_num': '&#523;', 'ansi_hex': u'ȋ'},
    {'ansi_num': '&#524;', 'ansi_hex': u'Ȍ'},
    {'ansi_num': '&#525;', 'ansi_hex': u'ȍ'},
    {'ansi_num': '&#526;', 'ansi_hex': u'Ȏ'},
    {'ansi_num': '&#527;', 'ansi_hex': u'ȏ'},
    {'ansi_num': '&#528;', 'ansi_hex': u'Ȑ'},
    {'ansi_num': '&#529;', 'ansi_hex': u'ȑ'},
    {'ansi_num': '&#530;', 'ansi_hex': u'Ȓ'},
    {'ansi_num': '&#531;', 'ansi_hex': u'ȓ'},
    {'ansi_num': '&#532;', 'ansi_hex': u'Ȕ'},
    {'ansi_num': '&#533;', 'ansi_hex': u'ȕ'},
    {'ansi_num': '&#534;', 'ansi_hex': u'Ȗ'},
    {'ansi_num': '&#535;', 'ansi_hex': u'ȗ'},
    {'ansi_num': '&#536;', 'ansi_hex': u'Ș'},
    {'ansi_num': '&#537;', 'ansi_hex': u'ș'},
    {'ansi_num': '&#538;', 'ansi_hex': u'Ț'},
    {'ansi_num': '&#539;', 'ansi_hex': u'ț'},
    {'ansi_num': '&#540;', 'ansi_hex': u'Ȝ'},
    {'ansi_num': '&#541;', 'ansi_hex': u'ȝ'},
    {'ansi_num': '&#542;', 'ansi_hex': u'Ȟ'},
    {'ansi_num': '&#543;', 'ansi_hex': u'ȟ'},
    {'ansi_num': '&#544;', 'ansi_hex': u'Ƞ'},
    {'ansi_num': '&#545;', 'ansi_hex': u'ȡ'},
    {'ansi_num': '&#546;', 'ansi_hex': u'Ȣ'},
    {'ansi_num': '&#547;', 'ansi_hex': u'ȣ'},
    {'ansi_num': '&#548;', 'ansi_hex': u'Ȥ'},
    {'ansi_num': '&#549;', 'ansi_hex': u'ȥ'},
    {'ansi_num': '&#550;', 'ansi_hex': u'Ȧ'},
    {'ansi_num': '&#551;', 'ansi_hex': u'ȧ'},
    {'ansi_num': '&#552;', 'ansi_hex': u'Ȩ'},
    {'ansi_num': '&#553;', 'ansi_hex': u'ȩ'},
    {'ansi_num': '&#554;', 'ansi_hex': u'Ȫ'},
    {'ansi_num': '&#555;', 'ansi_hex': u'ȫ'},
    {'ansi_num': '&#556;', 'ansi_hex': u'Ȭ'},
    {'ansi_num': '&#557;', 'ansi_hex': u'ȭ'},
    {'ansi_num': '&#558;', 'ansi_hex': u'Ȯ'},
    {'ansi_num': '&#559;', 'ansi_hex': u'ȯ'},
    {'ansi_num': '&#560;', 'ansi_hex': u'Ȱ'},
    {'ansi_num': '&#561;', 'ansi_hex': u'ȱ'},
    {'ansi_num': '&#562;', 'ansi_hex': u'Ȳ'},
    {'ansi_num': '&#563;', 'ansi_hex': u'ȳ'},
    {'ansi_num': '&#564;', 'ansi_hex': u'ȴ'},
    {'ansi_num': '&#565;', 'ansi_hex': u'ȵ'},
    {'ansi_num': '&#566;', 'ansi_hex': u'ȶ'},
    {'ansi_num': '&#567;', 'ansi_hex': u'ȷ'},
    {'ansi_num': '&#568;', 'ansi_hex': u'ȸ'},
    {'ansi_num': '&#569;', 'ansi_hex': u'ȹ'},
    {'ansi_num': '&#570;', 'ansi_hex': u'Ⱥ'},
    {'ansi_num': '&#571;', 'ansi_hex': u'Ȼ'},
    {'ansi_num': '&#572;', 'ansi_hex': u'ȼ'},
    {'ansi_num': '&#573;', 'ansi_hex': u'Ƚ'},
    {'ansi_num': '&#574;', 'ansi_hex': u'Ⱦ'},
    {'ansi_num': '&#575;', 'ansi_hex': u'ȿ'},
    {'ansi_num': '&#576;', 'ansi_hex': u'ɀ'},
    {'ansi_num': '&#577;', 'ansi_hex': u'Ɂ'},
    {'ansi_num': '&#578;', 'ansi_hex': u'ɂ'},
    {'ansi_num': '&#579;', 'ansi_hex': u'Ƀ'},
    {'ansi_num': '&#580;', 'ansi_hex': u'Ʉ'},
    {'ansi_num': '&#581;', 'ansi_hex': u'Ʌ'},
    {'ansi_num': '&#582;', 'ansi_hex': u'Ɇ'},
    {'ansi_num': '&#583;', 'ansi_hex': u'ɇ'},
    {'ansi_num': '&#584;', 'ansi_hex': u'Ɉ'},
    {'ansi_num': '&#585;', 'ansi_hex': u'ɉ'},
    {'ansi_num': '&#586;', 'ansi_hex': u'Ɋ'},
    {'ansi_num': '&#587;', 'ansi_hex': u'ɋ'},
    {'ansi_num': '&#588;', 'ansi_hex': u'Ɍ'},
    {'ansi_num': '&#589;', 'ansi_hex': u'ɍ'},
    {'ansi_num': '&#590;', 'ansi_hex': u'Ɏ'},
    {'ansi_num': '&#591;', 'ansi_hex': u'ɏ'},
    {'ansi_num': '&#592;', 'ansi_hex': u'ɐ'},
    {'ansi_num': '&#593;', 'ansi_hex': u'ɑ'},
    {'ansi_num': '&#594;', 'ansi_hex': u'ɒ'},
    {'ansi_num': '&#595;', 'ansi_hex': u'ɓ'},
    {'ansi_num': '&#596;', 'ansi_hex': u'ɔ'},
    {'ansi_num': '&#597;', 'ansi_hex': u'ɕ'},
    {'ansi_num': '&#598;', 'ansi_hex': u'ɖ'},
    {'ansi_num': '&#599;', 'ansi_hex': u'ɗ'},
    {'ansi_num': '&#600;', 'ansi_hex': u'ɘ'},
    {'ansi_num': '&#601;', 'ansi_hex': u'ə'},
    {'ansi_num': '&#602;', 'ansi_hex': u'ɚ'},
    {'ansi_num': '&#603;', 'ansi_hex': u'ɛ'},
    {'ansi_num': '&#604;', 'ansi_hex': u'ɜ'},
    {'ansi_num': '&#605;', 'ansi_hex': u'ɝ'},
    {'ansi_num': '&#606;', 'ansi_hex': u'ɞ'},
    {'ansi_num': '&#607;', 'ansi_hex': u'ɟ'},
    {'ansi_num': '&#608;', 'ansi_hex': u'ɠ'},
    {'ansi_num': '&#609;', 'ansi_hex': u'ɡ'},
    {'ansi_num': '&#610;', 'ansi_hex': u'ɢ'},
    {'ansi_num': '&#611;', 'ansi_hex': u'ɣ'},
    {'ansi_num': '&#612;', 'ansi_hex': u'ɤ'},
    {'ansi_num': '&#613;', 'ansi_hex': u'ɥ'},
    {'ansi_num': '&#614;', 'ansi_hex': u'ɦ'},
    {'ansi_num': '&#615;', 'ansi_hex': u'ɧ'},
    {'ansi_num': '&#616;', 'ansi_hex': u'ɨ'},
    {'ansi_num': '&#617;', 'ansi_hex': u'ɩ'},
    {'ansi_num': '&#618;', 'ansi_hex': u'ɪ'},
    {'ansi_num': '&#619;', 'ansi_hex': u'ɫ'},
    {'ansi_num': '&#620;', 'ansi_hex': u'ɬ'},
    {'ansi_num': '&#621;', 'ansi_hex': u'ɭ'},
    {'ansi_num': '&#622;', 'ansi_hex': u'ɮ'},
    {'ansi_num': '&#623;', 'ansi_hex': u'ɯ'},
    {'ansi_num': '&#624;', 'ansi_hex': u'ɰ'},
    {'ansi_num': '&#625;', 'ansi_hex': u'ɱ'},
    {'ansi_num': '&#626;', 'ansi_hex': u'ɲ'},
    {'ansi_num': '&#627;', 'ansi_hex': u'ɳ'},
    {'ansi_num': '&#628;', 'ansi_hex': u'ɴ'},
    {'ansi_num': '&#629;', 'ansi_hex': u'ɵ'},
    {'ansi_num': '&#630;', 'ansi_hex': u'ɶ'},
    {'ansi_num': '&#631;', 'ansi_hex': u'ɷ'},
    {'ansi_num': '&#632;', 'ansi_hex': u'ɸ'},
    {'ansi_num': '&#633;', 'ansi_hex': u'ɹ'},
    {'ansi_num': '&#634;', 'ansi_hex': u'ɺ'},
    {'ansi_num': '&#635;', 'ansi_hex': u'ɻ'},
    {'ansi_num': '&#636;', 'ansi_hex': u'ɼ'},
    {'ansi_num': '&#637;', 'ansi_hex': u'ɽ'},
    {'ansi_num': '&#638;', 'ansi_hex': u'ɾ'},
    {'ansi_num': '&#639;', 'ansi_hex': u'ɿ'},
    {'ansi_num': '&#640;', 'ansi_hex': u'ʀ'},
    {'ansi_num': '&#641;', 'ansi_hex': u'ʁ'},
    {'ansi_num': '&#642;', 'ansi_hex': u'ʂ'},
    {'ansi_num': '&#643;', 'ansi_hex': u'ʃ'},
    {'ansi_num': '&#644;', 'ansi_hex': u'ʄ'},
    {'ansi_num': '&#645;', 'ansi_hex': u'ʅ'},
    {'ansi_num': '&#646;', 'ansi_hex': u'ʆ'},
    {'ansi_num': '&#647;', 'ansi_hex': u'ʇ'},
    {'ansi_num': '&#648;', 'ansi_hex': u'ʈ'},
    {'ansi_num': '&#649;', 'ansi_hex': u'ʉ'},
    {'ansi_num': '&#650;', 'ansi_hex': u'ʊ'},
    {'ansi_num': '&#651;', 'ansi_hex': u'ʋ'},
    {'ansi_num': '&#652;', 'ansi_hex': u'ʌ'},
    {'ansi_num': '&#653;', 'ansi_hex': u'ʍ'},
    {'ansi_num': '&#654;', 'ansi_hex': u'ʎ'},
    {'ansi_num': '&#655;', 'ansi_hex': u'ʏ'},
    {'ansi_num': '&#656;', 'ansi_hex': u'ʐ'},
    {'ansi_num': '&#657;', 'ansi_hex': u'ʑ'},
    {'ansi_num': '&#658;', 'ansi_hex': u'ʒ'},
    {'ansi_num': '&#659;', 'ansi_hex': u'ʓ'},
    {'ansi_num': '&#660;', 'ansi_hex': u'ʔ'},
    {'ansi_num': '&#661;', 'ansi_hex': u'ʕ'},
    {'ansi_num': '&#662;', 'ansi_hex': u'ʖ'},
    {'ansi_num': '&#663;', 'ansi_hex': u'ʗ'},
    {'ansi_num': '&#664;', 'ansi_hex': u'ʘ'},
    {'ansi_num': '&#665;', 'ansi_hex': u'ʙ'},
    {'ansi_num': '&#666;', 'ansi_hex': u'ʚ'},
    {'ansi_num': '&#667;', 'ansi_hex': u'ʛ'},
    {'ansi_num': '&#668;', 'ansi_hex': u'ʜ'},
    {'ansi_num': '&#669;', 'ansi_hex': u'ʝ'},
    {'ansi_num': '&#670;', 'ansi_hex': u'ʞ'},
    {'ansi_num': '&#671;', 'ansi_hex': u'ʟ'},
    {'ansi_num': '&#672;', 'ansi_hex': u'ʠ'},
    {'ansi_num': '&#673;', 'ansi_hex': u'ʡ'},
    {'ansi_num': '&#674;', 'ansi_hex': u'ʢ'},
    {'ansi_num': '&#675;', 'ansi_hex': u'ʣ'},
    {'ansi_num': '&#676;', 'ansi_hex': u'ʤ'},
    {'ansi_num': '&#677;', 'ansi_hex': u'ʥ'},
    {'ansi_num': '&#678;', 'ansi_hex': u'ʦ'},
    {'ansi_num': '&#679;', 'ansi_hex': u'ʧ'},
    {'ansi_num': '&#680;', 'ansi_hex': u'ʨ'},
    {'ansi_num': '&#681;', 'ansi_hex': u'ʩ'},
    {'ansi_num': '&#682;', 'ansi_hex': u'ʪ'},
    {'ansi_num': '&#683;', 'ansi_hex': u'ʫ'},
    {'ansi_num': '&#684;', 'ansi_hex': u'ʬ'},
    {'ansi_num': '&#685;', 'ansi_hex': u'ʭ'},
    {'ansi_num': '&#686;', 'ansi_hex': u'ʮ'},
    {'ansi_num': '&#687;', 'ansi_hex': u'ʯ'},
    {'ansi_num': '&#688;', 'ansi_hex': u'ʰ'},
    {'ansi_num': '&#689;', 'ansi_hex': u'ʱ'},
    {'ansi_num': '&#690;', 'ansi_hex': u'ʲ'},
    {'ansi_num': '&#691;', 'ansi_hex': u'ʳ'},
    {'ansi_num': '&#692;', 'ansi_hex': u'ʴ'},
    {'ansi_num': '&#693;', 'ansi_hex': u'ʵ'},
    {'ansi_num': '&#694;', 'ansi_hex': u'ʶ'},
    {'ansi_num': '&#695;', 'ansi_hex': u'ʷ'},
    {'ansi_num': '&#696;', 'ansi_hex': u'ʸ'},
    {'ansi_num': '&#697;', 'ansi_hex': u'ʹ'},
    {'ansi_num': '&#698;', 'ansi_hex': u'ʺ'},
    {'ansi_num': '&#699;', 'ansi_hex': u'ʻ'},
    {'ansi_num': '&#700;', 'ansi_hex': u'ʼ'},
    {'ansi_num': '&#701;', 'ansi_hex': u'ʽ'},
    {'ansi_num': '&#702;', 'ansi_hex': u'ʾ'},
    {'ansi_num': '&#703;', 'ansi_hex': u'ʿ'},
    {'ansi_num': '&#704;', 'ansi_hex': u'ˀ'},
    {'ansi_num': '&#705;', 'ansi_hex': u'ˁ'},
    {'ansi_num': '&#706;', 'ansi_hex': u'˂'},
    {'ansi_num': '&#707;', 'ansi_hex': u'˃'},
    {'ansi_num': '&#708;', 'ansi_hex': u'˄'},
    {'ansi_num': '&#709;', 'ansi_hex': u'˅'},
    {'ansi_num': '&#710;', 'ansi_hex': (u'ˆ', u'\xcb\x86', u'\x88'), 'html_entity': '&circ;'},
    {'ansi_num': '&#711;', 'ansi_hex': u'ˇ'},
    {'ansi_num': '&#712;', 'ansi_hex': u'ˈ'},
    {'ansi_num': '&#713;', 'ansi_hex': u'ˉ'},
    {'ansi_num': '&#714;', 'ansi_hex': u'ˊ'},
    {'ansi_num': '&#715;', 'ansi_hex': u'ˋ'},
    {'ansi_num': '&#716;', 'ansi_hex': u'ˌ'},
    {'ansi_num': '&#717;', 'ansi_hex': u'ˍ'},
    {'ansi_num': '&#718;', 'ansi_hex': u'ˎ'},
    {'ansi_num': '&#719;', 'ansi_hex': u'ˏ'},
    {'ansi_num': '&#720;', 'ansi_hex': u'ː'},
    {'ansi_num': '&#721;', 'ansi_hex': u'ˑ'},
    {'ansi_num': '&#722;', 'ansi_hex': u'˒'},
    {'ansi_num': '&#723;', 'ansi_hex': u'˓'},
    {'ansi_num': '&#724;', 'ansi_hex': u'˔'},
    {'ansi_num': '&#725;', 'ansi_hex': u'˕'},
    {'ansi_num': '&#726;', 'ansi_hex': u'˖'},
    {'ansi_num': '&#727;', 'ansi_hex': u'˗'},
    {'ansi_num': '&#728;', 'ansi_hex': u'˘'},
    {'ansi_num': '&#729;', 'ansi_hex': u'˙'},
    {'ansi_num': '&#730;', 'ansi_hex': u'˚'},
    {'ansi_num': '&#731;', 'ansi_hex': u'˛'},
    {'ansi_num': '&#732;', 'ansi_hex': (u'˜', u'\xcb\x9c', u'\x98'), 'html_entity': '&tilde;'},
    {'ansi_num': '&#733;', 'ansi_hex': u'˝'},
    {'ansi_num': '&#734;', 'ansi_hex': u'˞'},
    {'ansi_num': '&#735;', 'ansi_hex': u'˟'},
    {'ansi_num': '&#736;', 'ansi_hex': u'ˠ'},
    {'ansi_num': '&#737;', 'ansi_hex': u'ˡ'},
    {'ansi_num': '&#738;', 'ansi_hex': u'ˢ'},
    {'ansi_num': '&#739;', 'ansi_hex': u'ˣ'},
    {'ansi_num': '&#740;', 'ansi_hex': u'ˤ'},
    {'ansi_num': '&#741;', 'ansi_hex': u'˥'},
    {'ansi_num': '&#742;', 'ansi_hex': u'˦'},
    {'ansi_num': '&#743;', 'ansi_hex': u'˧'},
    {'ansi_num': '&#744;', 'ansi_hex': u'˨'},
    {'ansi_num': '&#745;', 'ansi_hex': u'˩'},
    {'ansi_num': '&#746;', 'ansi_hex': u'˪'},
    {'ansi_num': '&#747;', 'ansi_hex': u'˫'},
    {'ansi_num': '&#748;', 'ansi_hex': u'ˬ'},
    {'ansi_num': '&#749;', 'ansi_hex': u'˭'},
    {'ansi_num': '&#750;', 'ansi_hex': u'ˮ'},
    {'ansi_num': '&#751;', 'ansi_hex': u'˯'},
    {'ansi_num': '&#752;', 'ansi_hex': u'˰'},
    {'ansi_num': '&#753;', 'ansi_hex': u'˱'},
    {'ansi_num': '&#754;', 'ansi_hex': u'˲'},
    {'ansi_num': '&#755;', 'ansi_hex': u'˳'},
    {'ansi_num': '&#756;', 'ansi_hex': u'˴'},
    {'ansi_num': '&#757;', 'ansi_hex': u'˵'},
    {'ansi_num': '&#758;', 'ansi_hex': u'˶'},
    {'ansi_num': '&#759;', 'ansi_hex': u'˷'},
    {'ansi_num': '&#760;', 'ansi_hex': u'˸'},
    {'ansi_num': '&#761;', 'ansi_hex': u'˹'},
    {'ansi_num': '&#762;', 'ansi_hex': u'˺'},
    {'ansi_num': '&#763;', 'ansi_hex': u'˻'},
    {'ansi_num': '&#764;', 'ansi_hex': u'˼'},
    {'ansi_num': '&#765;', 'ansi_hex': u'˽'},
    {'ansi_num': '&#766;', 'ansi_hex': u'˾'},
    {'ansi_num': '&#767;', 'ansi_hex': u'˿'},
    {'ansi_num': '&#768;', 'ansi_hex': u'̀'},
    {'ansi_num': '&#769;', 'ansi_hex': u'́'},
    {'ansi_num': '&#770;', 'ansi_hex': u'̂'},
    {'ansi_num': '&#771;', 'ansi_hex': u'̃'},
    {'ansi_num': '&#772;', 'ansi_hex': u'̄'},
    {'ansi_num': '&#773;', 'ansi_hex': u'̅'},
    {'ansi_num': '&#774;', 'ansi_hex': u'̆'},
    {'ansi_num': '&#775;', 'ansi_hex': u'̇'},
    {'ansi_num': '&#776;', 'ansi_hex': u'̈'},
    {'ansi_num': '&#777;', 'ansi_hex': u'̉'},
    {'ansi_num': '&#778;', 'ansi_hex': u'̊'},
    {'ansi_num': '&#779;', 'ansi_hex': u'̋'},
    {'ansi_num': '&#780;', 'ansi_hex': u'̌'},
    {'ansi_num': '&#781;', 'ansi_hex': u'̍'},
    {'ansi_num': '&#782;', 'ansi_hex': u'̎'},
    {'ansi_num': '&#783;', 'ansi_hex': u'̏'},
    {'ansi_num': '&#784;', 'ansi_hex': u'̐'},
    {'ansi_num': '&#785;', 'ansi_hex': u'̑'},
    {'ansi_num': '&#786;', 'ansi_hex': u'̒'},
    {'ansi_num': '&#787;', 'ansi_hex': u'̓'},
    {'ansi_num': '&#788;', 'ansi_hex': u'̔'},
    {'ansi_num': '&#789;', 'ansi_hex': u'̕'},
    {'ansi_num': '&#790;', 'ansi_hex': u'̖'},
    {'ansi_num': '&#791;', 'ansi_hex': u'̗'},
    {'ansi_num': '&#792;', 'ansi_hex': u'̘'},
    {'ansi_num': '&#793;', 'ansi_hex': u'̙'},
    {'ansi_num': '&#794;', 'ansi_hex': u'̚'},
    {'ansi_num': '&#795;', 'ansi_hex': u'̛'},
    {'ansi_num': '&#796;', 'ansi_hex': u'̜'},
    {'ansi_num': '&#797;', 'ansi_hex': u'̝'},
    {'ansi_num': '&#798;', 'ansi_hex': u'̞'},
    {'ansi_num': '&#799;', 'ansi_hex': u'̟'},
    {'ansi_num': '&#800;', 'ansi_hex': u'̠'},
    {'ansi_num': '&#801;', 'ansi_hex': u'̡'},
    {'ansi_num': '&#802;', 'ansi_hex': u'̢'},
    {'ansi_num': '&#803;', 'ansi_hex': u'̣'},
    {'ansi_num': '&#804;', 'ansi_hex': u'̤'},
    {'ansi_num': '&#805;', 'ansi_hex': u'̥'},
    {'ansi_num': '&#806;', 'ansi_hex': u'̦'},
    {'ansi_num': '&#807;', 'ansi_hex': u'̧'},
    {'ansi_num': '&#808;', 'ansi_hex': u'̨'},
    {'ansi_num': '&#809;', 'ansi_hex': u'̩'},
    {'ansi_num': '&#810;', 'ansi_hex': u'̪'},
    {'ansi_num': '&#811;', 'ansi_hex': u'̫'},
    {'ansi_num': '&#812;', 'ansi_hex': u'̬'},
    {'ansi_num': '&#813;', 'ansi_hex': u'̭'},
    {'ansi_num': '&#814;', 'ansi_hex': u'̮'},
    {'ansi_num': '&#815;', 'ansi_hex': u'̯'},
    {'ansi_num': '&#816;', 'ansi_hex': u'̰'},
    {'ansi_num': '&#817;', 'ansi_hex': u'̱'},
    {'ansi_num': '&#818;', 'ansi_hex': u'̲'},
    {'ansi_num': '&#819;', 'ansi_hex': u'̳'},
    {'ansi_num': '&#820;', 'ansi_hex': u'̴'},
    {'ansi_num': '&#821;', 'ansi_hex': u'̵'},
    {'ansi_num': '&#822;', 'ansi_hex': u'̶'},
    {'ansi_num': '&#823;', 'ansi_hex': u'̷'},
    {'ansi_num': '&#824;', 'ansi_hex': u'̸'},
    {'ansi_num': '&#825;', 'ansi_hex': u'̹'},
    {'ansi_num': '&#826;', 'ansi_hex': u'̺'},
    {'ansi_num': '&#827;', 'ansi_hex': u'̻'},
    {'ansi_num': '&#828;', 'ansi_hex': u'̼'},
    {'ansi_num': '&#829;', 'ansi_hex': u'̽'},
    {'ansi_num': '&#830;', 'ansi_hex': u'̾'},
    {'ansi_num': '&#831;', 'ansi_hex': u'̿'},
    {'ansi_num': '&#832;', 'ansi_hex': u'̀'},
    {'ansi_num': '&#833;', 'ansi_hex': u'́'},
    {'ansi_num': '&#834;', 'ansi_hex': u'͂'},
    {'ansi_num': '&#835;', 'ansi_hex': u'̓'},
    {'ansi_num': '&#836;', 'ansi_hex': u'̈́'},
    {'ansi_num': '&#837;', 'ansi_hex': u'ͅ'},
    {'ansi_num': '&#838;', 'ansi_hex': u'͆'},
    {'ansi_num': '&#839;', 'ansi_hex': u'͇'},
    {'ansi_num': '&#840;', 'ansi_hex': u'͈'},
    {'ansi_num': '&#841;', 'ansi_hex': u'͉'},
    {'ansi_num': '&#842;', 'ansi_hex': u'͊'},
    {'ansi_num': '&#843;', 'ansi_hex': u'͋'},
    {'ansi_num': '&#844;', 'ansi_hex': u'͌'},
    {'ansi_num': '&#845;', 'ansi_hex': u'͍'},
    {'ansi_num': '&#846;', 'ansi_hex': u'͎'},
    {'ansi_num': '&#847;', 'ansi_hex': u'͏'},
    {'ansi_num': '&#848;', 'ansi_hex': u'͐'},
    {'ansi_num': '&#849;', 'ansi_hex': u'͑'},
    {'ansi_num': '&#850;', 'ansi_hex': u'͒'},
    {'ansi_num': '&#851;', 'ansi_hex': u'͓'},
    {'ansi_num': '&#852;', 'ansi_hex': u'͔'},
    {'ansi_num': '&#853;', 'ansi_hex': u'͕'},
    {'ansi_num': '&#854;', 'ansi_hex': u'͖'},
    {'ansi_num': '&#855;', 'ansi_hex': u'͗'},
    {'ansi_num': '&#856;', 'ansi_hex': u'͘'},
    {'ansi_num': '&#857;', 'ansi_hex': u'͙'},
    {'ansi_num': '&#858;', 'ansi_hex': u'͚'},
    {'ansi_num': '&#859;', 'ansi_hex': u'͛'},
    {'ansi_num': '&#860;', 'ansi_hex': u'͜'},
    {'ansi_num': '&#861;', 'ansi_hex': u'͝'},
    {'ansi_num': '&#862;', 'ansi_hex': u'͞'},
    {'ansi_num': '&#863;', 'ansi_hex': u'͟'},
    {'ansi_num': '&#864;', 'ansi_hex': u'͠'},
    {'ansi_num': '&#865;', 'ansi_hex': u'͡'},
    {'ansi_num': '&#866;', 'ansi_hex': u'͢'},
    {'ansi_num': '&#867;', 'ansi_hex': u'ͣ'},
    {'ansi_num': '&#868;', 'ansi_hex': u'ͤ'},
    {'ansi_num': '&#869;', 'ansi_hex': u'ͥ'},
    {'ansi_num': '&#870;', 'ansi_hex': u'ͦ'},
    {'ansi_num': '&#871;', 'ansi_hex': u'ͧ'},
    {'ansi_num': '&#872;', 'ansi_hex': u'ͨ'},
    {'ansi_num': '&#873;', 'ansi_hex': u'ͩ'},
    {'ansi_num': '&#874;', 'ansi_hex': u'ͪ'},
    {'ansi_num': '&#875;', 'ansi_hex': u'ͫ'},
    {'ansi_num': '&#876;', 'ansi_hex': u'ͬ'},
    {'ansi_num': '&#877;', 'ansi_hex': u'ͭ'},
    {'ansi_num': '&#878;', 'ansi_hex': u'ͮ'},
    {'ansi_num': '&#879;', 'ansi_hex': u'ͯ'},
    {'ansi_num': '&#880;', 'ansi_hex': u'Ͱ'},
    {'ansi_num': '&#881;', 'ansi_hex': u'ͱ'},
    {'ansi_num': '&#882;', 'ansi_hex': u'Ͳ'},
    {'ansi_num': '&#883;', 'ansi_hex': u'ͳ'},
    {'ansi_num': '&#884;', 'ansi_hex': u'ʹ'},
    {'ansi_num': '&#885;', 'ansi_hex': u'͵'},
    {'ansi_num': '&#886;', 'ansi_hex': u'Ͷ'},
    {'ansi_num': '&#887;', 'ansi_hex': u'ͷ'},
    {'ansi_num': '&#888;', 'ansi_hex': u'͸'},
    {'ansi_num': '&#889;', 'ansi_hex': u'͹'},
    {'ansi_num': '&#890;', 'ansi_hex': u'ͺ'},
    {'ansi_num': '&#891;', 'ansi_hex': u'ͻ'},
    {'ansi_num': '&#892;', 'ansi_hex': u'ͼ'},
    {'ansi_num': '&#893;', 'ansi_hex': u'ͽ'},
    {'ansi_num': '&#894;', 'ansi_hex': u';'},
    {'ansi_num': '&#895;', 'ansi_hex': u'Ϳ'},
    {'ansi_num': '&#896;', 'ansi_hex': u'΀'},
    {'ansi_num': '&#897;', 'ansi_hex': u'΁'},
    {'ansi_num': '&#898;', 'ansi_hex': u'΂'},
    {'ansi_num': '&#899;', 'ansi_hex': u'΃'},
    {'ansi_num': '&#900;', 'ansi_hex': u'΄'},
    {'ansi_num': '&#901;', 'ansi_hex': u'΅'},
    {'ansi_num': '&#902;', 'ansi_hex': u'Ά'},
    {'ansi_num': '&#903;', 'ansi_hex': u'·'},
    {'ansi_num': '&#904;', 'ansi_hex': u'Έ'},
    {'ansi_num': '&#905;', 'ansi_hex': u'Ή'},
    {'ansi_num': '&#906;', 'ansi_hex': u'Ί'},
    {'ansi_num': '&#907;', 'ansi_hex': u'΋'},
    {'ansi_num': '&#908;', 'ansi_hex': u'Ό'},
    {'ansi_num': '&#909;', 'ansi_hex': u'΍'},
    {'ansi_num': '&#910;', 'ansi_hex': u'Ύ'},
    {'ansi_num': '&#911;', 'ansi_hex': u'Ώ'},
    {'ansi_num': '&#912;', 'ansi_hex': u'ΐ'},
    {'ansi_num': "&#913;", 'ansi_hex': (u'Α', u'\xce\x91'), 'html_entity': "&Alpha;"},
    {'ansi_num': "&#914;", 'ansi_hex': (u'Β', u'\xce\x92'), 'html_entity': "&Beta;"},
    {'ansi_num': "&#915;", 'ansi_hex': (u'Γ', u'\xce\x93'), 'html_entity': "&Gamma;"},
    {'ansi_num': "&#916;", 'ansi_hex': (u'Δ', u'\xe2\x88\x86'), 'html_entity': "&Delta;"},
    {'ansi_num': "&#917;", 'ansi_hex': (u'Ε', u'\xce\x95'), 'html_entity': "&Epsilon;"},
    {'ansi_num': "&#918;", 'ansi_hex': (u'Ζ', u'\xce\x96'), 'html_entity': "&Zeta;"},
    {'ansi_num': "&#919;", 'ansi_hex': (u'Η', u'\xce\x97'), 'html_entity': "&Eta;"},
    {'ansi_num': "&#920;", 'ansi_hex': (u'Θ', u'\xce\x98'), 'html_entity': "&Theta;"},
    {'ansi_num': "&#921;", 'ansi_hex': (u'Ι', u'\xce\x99'), 'html_entity': "&Iota;"},
    {'ansi_num': "&#922;", 'ansi_hex': (u'Κ', u'\xce\x9a'), 'html_entity': "&Kappa;"},
    {'ansi_num': "&#923;", 'ansi_hex': (u'Λ', u'\xce\x9b'), 'html_entity': "&Lambda;"},
    {'ansi_num': "&#924;", 'ansi_hex': (u'Μ', u'\xce\x9c'), 'html_entity': "&Mu;"},
    {'ansi_num': "&#925;", 'ansi_hex': (u'Ν', u'\xce\x9d'), 'html_entity': "&Nu;"},
    {'ansi_num': "&#926;", 'ansi_hex': (u'Ξ', u'\xce\x9e'), 'html_entity': "&Xi;"},
    {'ansi_num': "&#927;", 'ansi_hex': (u'Ο', u'\xce\x9f'), 'html_entity': "&Omicron;"},
    {'ansi_num': "&#928;", 'ansi_hex': (u'Π', u'\xce\xa0'), 'html_entity': "&Pi;"},
    {'ansi_num': "&#929;", 'ansi_hex': (u'Ρ', u'\xce\xa1'), 'html_entity': "&Rho;"},
    {'ansi_num': '&#930;', 'ansi_hex': u'΢'},
    {'ansi_num': "&#931;", 'ansi_hex': (u'Σ', u'\xce\xa3'), 'html_entity': "&Sigma;"},
    {'ansi_num': "&#932;", 'ansi_hex': (u'Τ', u'\xce\xa4'), 'html_entity': "&Tau;"},
    {'ansi_num': "&#933;", 'ansi_hex': (u'Υ', u'\xce\xa5'), 'html_entity': "&Upsilon;"},
    {'ansi_num': "&#934;", 'ansi_hex': (u'Φ', u'\xce\xa6'), 'html_entity': "&Phi;"},
    {'ansi_num': "&#935;", 'ansi_hex': u'Χ', 'html_entity': "&Chi;"},
    {'ansi_num': "&#936;", 'ansi_hex': u'Ψ', 'html_entity': "&Psi;"},
    {'ansi_num': "&#937;", 'ansi_hex': (u'Ω', u'\xe2\x84\xa6'), 'html_entity': "&Omega;"},
    {'ansi_num': '&#938;', 'ansi_hex': u'Ϊ'},
    {'ansi_num': '&#939;', 'ansi_hex': u'Ϋ'},
    {'ansi_num': '&#940;', 'ansi_hex': u'ά'},
    {'ansi_num': '&#941;', 'ansi_hex': u'έ'},
    {'ansi_num': '&#942;', 'ansi_hex': u'ή'},
    {'ansi_num': '&#943;', 'ansi_hex': u'ί'},
    {'ansi_num': '&#944;', 'ansi_hex': u'ΰ'},
    {'ansi_num': "&#945;", 'ansi_hex': (u'α', u'\xce\xb1'), 'html_entity': "&alpha;"},
    {'ansi_num': "&#946;", 'ansi_hex': (u'β', u'\xce\xb2'), 'html_entity': "&beta;"},
    {'ansi_num': "&#947;", 'ansi_hex': (u'γ', u'\xce\xb3'), 'html_entity': "&gamma;"},
    {'ansi_num': "&#948;", 'ansi_hex': (u'δ', u'\xce\xb4'), 'html_entity': "&delta;"},
    {'ansi_num': "&#949;", 'ansi_hex': (u'ε', u'\xce\xb5'), 'html_entity': "&epsilon;"},
    {'ansi_num': "&#950;", 'ansi_hex': (u'ζ', u'\xce\xb6'), 'html_entity': "&zeta;"},
    {'ansi_num': "&#951;", 'ansi_hex': (u'η', u'\xce\xb7'), 'html_entity': "&eta;"},
    {'ansi_num': "&#952;", 'ansi_hex': (u'θ', u'\xce\xb8'), 'html_entity': "&theta;"},
    {'ansi_num': "&#953;", 'ansi_hex': (u'ι', u'\xce\xb9'), 'html_entity': "&iota;"},
    {'ansi_num': "&#954;", 'ansi_hex': (u'κ', u'\xce\xba'), 'html_entity': "&kappa;"},
    {'ansi_num': "&#955;", 'ansi_hex': (u'λ', u'\xce\xbb'), 'html_entity': "&lambda;"},
    {'ansi_num': "&#956;", 'ansi_hex': u'μ', 'html_entity': "&mu;"},
    {'ansi_num': "&#957;", 'ansi_hex': (u'ν', u'\xce\xbd'), 'html_entity': "&nu;"},
    {'ansi_num': "&#958;", 'ansi_hex': (u'ξ', u'\xce\xbe'), 'html_entity': "&xi;"},
    {'ansi_num': "&#959;", 'ansi_hex': (u'ο', u'\xce\xbf'), 'html_entity': "&omicron;"},
    {'ansi_num': "&#960;", 'ansi_hex': (u'π', u'\xcf\x80'), 'html_entity': "&pi;"},
    {'ansi_num': "&#961;", 'ansi_hex': (u'ρ', u'\xcf\x81'), 'html_entity': "&rho;"},
    {'ansi_num': "&#962;", 'ansi_hex': (u'ς', u'\xcf\x82'), 'html_entity': "&sigmaf;"},
    {'ansi_num': "&#963;", 'ansi_hex': (u'σ', u'\xcf\x83'), 'html_entity': "&sigma;"},
    {'ansi_num': "&#964;", 'ansi_hex': (u'τ', u'\xcf\x84'), 'html_entity': "&tau;"},
    {'ansi_num': "&#965;", 'ansi_hex': (u'υ', u'\xcf\x85'), 'html_entity': "&upsilon;"},
    {'ansi_num': "&#966;", 'ansi_hex': (u'φ', u'\xcf\x95'), 'html_entity': "&phi;"},
    {'ansi_num': "&#967;", 'ansi_hex': (u'χ', u'\xcf\x87'), 'html_entity': "&chi;"},
    {'ansi_num': "&#968;", 'ansi_hex': (u'ψ', u'\xcf\x88'), 'html_entity': "&psi;"},
    {'ansi_num': "&#969;", 'ansi_hex': (u'ω', u'\xcf\x89'), 'html_entity': "&omega;"},
    {'ansi_num': '&#970;', 'ansi_hex': u'ϊ'},
    {'ansi_num': '&#971;', 'ansi_hex': u'ϋ'},
    {'ansi_num': '&#972;', 'ansi_hex': u'ό'},
    {'ansi_num': '&#973;', 'ansi_hex': u'ύ'},
    {'ansi_num': '&#974;', 'ansi_hex': u'ώ'},
    {'ansi_num': '&#975;', 'ansi_hex': u'Ϗ'},
    {'ansi_num': '&#976;', 'ansi_hex': u'ϐ'},
    {'ansi_num': "&#977;", 'ansi_hex': (u'ϑ', u'\xcf\x91'), 'html_entity': "&thetasym;"},
    {'ansi_num': "&#978;", 'ansi_hex': (u'ϒ', u'\xcf\x92'), 'html_entity': "&upsih;"},
    {'ansi_num': '&#979;', 'ansi_hex': u'ϓ'},
    {'ansi_num': '&#980;', 'ansi_hex': u'ϔ'},
    {'ansi_num': '&#981;', 'ansi_hex': u'ϕ'},
    {'ansi_num': "&#982;", 'ansi_hex': (u'ϖ', u'\xcf\x96'), 'html_entity': "&piv;"},
    {'ansi_num': '&#983;', 'ansi_hex': u'ϗ'},
    {'ansi_num': '&#984;', 'ansi_hex': u'Ϙ'},
    {'ansi_num': '&#985;', 'ansi_hex': u'ϙ'},
    {'ansi_num': '&#986;', 'ansi_hex': u'Ϛ'},
    {'ansi_num': '&#987;', 'ansi_hex': u'ϛ'},
    {'ansi_num': '&#988;', 'ansi_hex': u'Ϝ'},
    {'ansi_num': '&#989;', 'ansi_hex': u'ϝ'},
    {'ansi_num': '&#990;', 'ansi_hex': u'Ϟ'},
    {'ansi_num': '&#991;', 'ansi_hex': u'ϟ'},
    {'ansi_num': '&#992;', 'ansi_hex': u'Ϡ'},
    {'ansi_num': '&#993;', 'ansi_hex': u'ϡ'},
    {'ansi_num': '&#994;', 'ansi_hex': u'Ϣ'},
    {'ansi_num': '&#995;', 'ansi_hex': u'ϣ'},
    {'ansi_num': '&#996;', 'ansi_hex': u'Ϥ'},
    {'ansi_num': '&#997;', 'ansi_hex': u'ϥ'},
    {'ansi_num': '&#998;', 'ansi_hex': u'Ϧ'},
    {'ansi_num': '&#999;', 'ansi_hex': u'ϧ'},
    
    {'ansi_num': "&#8194;", 'ansi_hex': u'\xe2\x80\x82', 'html_entity': "&ensp;"},
    {'ansi_num': "&#8195;", 'ansi_hex': u'\xe2\x80\x83', 'html_entity': "&emsp;"},
    
    {'ansi_num': "&#8201;", 'ansi_hex': u'\xe2\x80\x89', 'html_entity': "&thinsp;"},
    {'ansi_num': "&#8204;", 'ansi_hex': u'\xe2\x80\x8c', 'html_entity': "&zwnj;"},
    {'ansi_num': "&#8205;", 'ansi_hex': u'\xe2\x80\x8d', 'html_entity': "&zwj;"},
    {'ansi_num': "&#8206;", 'ansi_hex': u'\xe2\x80\x8e', 'html_entity': "&lrm;"},
    {'ansi_num': "&#8207;", 'ansi_hex': u'\xe2\x80\x8f', 'html_entity': "&rlm;"},
    {'ansi_num': "&#8211;", 'ansi_hex': (u'–', u'\xe2\x80\x93', u'\x96'), 'html_entity': "&ndash;"},
    {'ansi_num': '&#8212;', 'ansi_hex': (u'—', u'\xe2\x80\x94', u'\x97'), 'html_entity': '&mdash;'},
    {'ansi_num': '&#8216;', 'ansi_hex': (u'‘', u'\xe2\x80\x98', u'\x91'), 'html_entity': '&lsquo;'},
    {'ansi_num': '&#8217;', 'ansi_hex': (u'’', u'\xe2\x80\x99', u'\x92'), 'html_entity': '&rsquo;'},
    {'ansi_num': '&#8218;', 'ansi_hex': (u'‚', u'\xe2\x80\x9a', u'\x82'), 'html_entity': '&sbquo;'},
    {'ansi_num': '&#8220;', 'ansi_hex': (u'“', u'\xe2\x80\x9c', u'\x93'), 'html_entity': '&ldquo;'},
    {'ansi_num': '&#8221;', 'ansi_hex': (u'”', u'\xe2\x80\x9d', u'\x94'), 'html_entity': '&rdquo;'},
    {'ansi_num': '&#8222;', 'ansi_hex': (u'„', u'\xe2\x80\x9e', u'\x84'), 'html_entity': '&bdquo;'},
    {'ansi_num': '&#8224;', 'ansi_hex': (u'†', u'\xe2\x80\xa0', u'\x86'), 'html_entity': '&dagger;'},
    {'ansi_num': '&#8225;', 'ansi_hex': (u'‡', u'\xe2\x80\xa1', u'\x87'), 'html_entity': '&Dagger;'},
    {'ansi_num': '&#8226;', 'ansi_hex': (u'•', u'\xe2\x80\xa2', u'\x95'), 'html_entity': '&bull;'},
    {'ansi_num': '&#8230;', 'ansi_hex': (u'…', u'\xe2\x80\xa6', u'\x85'), 'html_entity': '&hellip;'},
    {'ansi_num': '&#8240;', 'ansi_hex': (u'‰', u'\xe2\x80\xb0', u'\x89'), 'html_entity': '&permil;'},
    {'ansi_num': "&#8242;", 'ansi_hex': (u'′', u'\xe2\x80\xb2'), 'html_entity': "&prime;"},
    {'ansi_num': "&#8243;", 'ansi_hex': (u'″', u'\xe2\x80\xb3'), 'html_entity': "&Prime;"},
    {'ansi_num': '&#8249;', 'ansi_hex': (u'‹', u'\xe2\x80\xb9', u'\x8B'), 'html_entity': '&lsaquo;'},
    {'ansi_num': '&#8250;', 'ansi_hex': (u'›', u'\xe2\x80\xba', u'\x9B'), 'html_entity': '&rsaquo;'},
    {'ansi_num': "&#8254;", 'ansi_hex': (u'‾', u'\xef\xa3\xa5'), 'html_entity': "&oline;"},
    {'ansi_num': "&#8260;", 'ansi_hex': (u'⁄', u'\xe2\x81\x84'), 'html_entity': "&frasl;"},

    {'ansi_num': '&#8364;', 'ansi_hex': (u'€', u'\xe2\x82\xac', u'\x80'), 'html_entity': '&euro;'},

    {'ansi_num': "&#8465;", 'ansi_hex': (u'ℑ', u'\xe2\x84\x91'), 'html_entity': "&image;"},
    {'ansi_num': "&#8472;", 'ansi_hex': (u'℘', u'\xe2\x84\x98'), 'html_entity': "&weierp;"},
    {'ansi_num': "&#8476;", 'ansi_hex': (u'ℜ', u'\xe2\x84\x9c'), 'html_entity': "&real;"},
    {'ansi_num': "&#8482;", 'ansi_hex': (u'™', u'\xef\xa3\xaa'  u'\x99'), 'html_entity': "&trade;"},

    {'ansi_num': "&#8501;", 'ansi_hex': (u'ℵ', u'\xe2\x84\xb5'), 'html_entity': "&alefsym;"},
    {'ansi_num': "&#8592;", 'ansi_hex': (u'←', u'\xe2\x86\x90'), 'html_entity': "&larr;"},
    {'ansi_num': "&#8593;", 'ansi_hex': (u'↑', u'\xe2\x86\x91'), 'html_entity': "&uarr;"},
    {'ansi_num': "&#8594;", 'ansi_hex': (u'→', u'\xe2\x86\x92'), 'html_entity': "&rarr;"},
    {'ansi_num': "&#8595;", 'ansi_hex': (u'↓', u'\xe2\x86\x93'), 'html_entity': "&darr;"},
    {'ansi_num': "&#8596;", 'ansi_hex': (u'↔', u'\xe2\x86\x94'), 'html_entity': "&harr;"},

    {'ansi_num': "&#8629;", 'ansi_hex': (u'↵', u'\xe2\x86\xb5'), 'html_entity': "&crarr;"},
    {'ansi_num': "&#8656;", 'ansi_hex': (u'⇐', u'\xe2\x87\x90'), 'html_entity': "&lArr;"},
    {'ansi_num': "&#8657;", 'ansi_hex': (u'⇑', u'\xe2\x87\x91'), 'html_entity': "&uArr;"},
    {'ansi_num': "&#8658;", 'ansi_hex': (u'⇒', u'\xe2\x87\x92'), 'html_entity': "&rArr;"},
    {'ansi_num': "&#8659;", 'ansi_hex': (u'⇓', u'\xe2\x87\x93'), 'html_entity': "&dArr;"},
    {'ansi_num': "&#8660;", 'ansi_hex': (u'⇔', u'\xe2\x87\x94'), 'html_entity': "&hArr;"},

    {'ansi_num': "&#8704;", 'ansi_hex': (u'∀', u'\xe2\x88\x80'), 'html_entity': "&forall;"},
    {'ansi_num': "&#8706;", 'ansi_hex': (u'∂', u'\xe2\x88\x82'), 'html_entity': "&part;"},
    {'ansi_num': "&#8707;", 'ansi_hex': (u'∃', u'\xe2\x88\x83'), 'html_entity': "&exist;"},
    {'ansi_num': "&#8709;", 'ansi_hex': (u'∅', u'\xe2\x88\x85'), 'html_entity': "&empty;"},
    {'ansi_num': "&#8711;", 'ansi_hex': (u'∇', u'\xe2\x88\x87'), 'html_entity': "&nabla;"},
    {'ansi_num': "&#8712;", 'ansi_hex': (u'∈', u'\xe2\x88\x88'), 'html_entity': "&isin;"},
    {'ansi_num': "&#8713;", 'ansi_hex': (u'∉', u'\xe2\x88\x89'), 'html_entity': "&notin;"},
    {'ansi_num': "&#8715;", 'ansi_hex': (u'∋', u'\xe2\x88\x8b'), 'html_entity': "&ni;"},
    {'ansi_num': "&#8719;", 'ansi_hex': (u'∏', u'\xe2\x88\x8f'), 'html_entity': "&prod;"},
    {'ansi_num': "&#8721;", 'ansi_hex': (u'∑', u'\xe2\x88\x91'), 'html_entity': "&sum;"},
    {'ansi_num': "&#8722;", 'ansi_hex': (u'−', u'\xe2\x88\x92'), 'html_entity': "&minus;"},
    {'ansi_num': "&#8727;", 'ansi_hex': (u'∗', u'\xe2\x88\x97'), 'html_entity': "&lowast;"},
    {'ansi_num': "&#8730;", 'ansi_hex': (u'√', u'\xe2\x88\x9a'), 'html_entity': "&radic;"},
    {'ansi_num': "&#8733;", 'ansi_hex': (u'∝', u'\xe2\x88\x9d'), 'html_entity': "&prop;"},
    {'ansi_num': "&#8734;", 'ansi_hex': (u'∞', u'\xe2\x88\x9e'), 'html_entity': "&infin;"},
    {'ansi_num': "&#8736;", 'ansi_hex': (u'∠', u'\xe2\x88\xa0'), 'html_entity': "&ang;"},
    {'ansi_num': "&#8743;", 'ansi_hex': (u'∧', u'\xe2\x88\xa7'), 'html_entity': "&and;"},
    {'ansi_num': "&#8744;", 'ansi_hex': (u'∨', u'\xe2\x88\xa8'), 'html_entity': "&or;"},
    {'ansi_num': "&#8745;", 'ansi_hex': (u'∩', u'\xe2\x88\xa9'), 'html_entity': "&cap;"},
    {'ansi_num': "&#8746;", 'ansi_hex': (u'∪', u'\xe2\x88\xaa'), 'html_entity': "&cup;"},
    {'ansi_num': "&#8747;", 'ansi_hex': (u'∫', u'\xe2\x88\xab'), 'html_entity': "&int;"},
    {'ansi_num': "&#8756;", 'ansi_hex': (u'∴', u'\xe2\x88\xb4'), 'html_entity': "&there4;"},
    {'ansi_num': "&#8764;", 'ansi_hex': (u'∼', u'\xe2\x88\xbc'), 'html_entity': "&sim;"},
    {'ansi_num': "&#8773;", 'ansi_hex': (u'≅', u'\xe2\x89\x85'), 'html_entity': "&cong;"},
    {'ansi_num': "&#8776;", 'ansi_hex': (u'≈', u'\xe2\x89\x88'), 'html_entity': "&asymp;"},

    {'ansi_num': "&#8800;", 'ansi_hex': (u'≠', u'\xe2\x89\xa0'), 'html_entity': "&ne;"},
    {'ansi_num': "&#8801;", 'ansi_hex': (u'≡', u'\xe2\x89\xa1'), 'html_entity': "&equiv;"},
    {'ansi_num': "&#8804;", 'ansi_hex': (u'≤', u'\xe2\x89\xa4'), 'html_entity': "&le;"},
    {'ansi_num': "&#8805;", 'ansi_hex': (u'≥', u'\xe2\x89\xa5'), 'html_entity': "&ge;"},
    {'ansi_num': "&#8834;", 'ansi_hex': (u'⊂', u'\xe2\x8a\x82'), 'html_entity': "&sub;"},
    {'ansi_num': "&#8835;", 'ansi_hex': (u'⊃', u'\xe2\x8a\x83'), 'html_entity': "&sup;"},
    {'ansi_num': "&#8836;", 'ansi_hex': (u'⊄', u'\xe2\x8a\x84'), 'html_entity': "&nsub;"},
    {'ansi_num': "&#8838;", 'ansi_hex': (u'⊆', u'\xe2\x8a\x86'), 'html_entity': "&sube;"},
    {'ansi_num': "&#8839;", 'ansi_hex': (u'⊇', u'\xe2\x8a\x87'), 'html_entity': "&supe;"},
    {'ansi_num': "&#8853;", 'ansi_hex': (u'⊕', u'\xe2\x8a\x95'), 'html_entity': "&oplus;"},
    {'ansi_num': "&#8855;", 'ansi_hex': (u'⊗', u'\xe2\x8a\x97'), 'html_entity': "&otimes;"},
    {'ansi_num': "&#8869;", 'ansi_hex': (u'⊥', u'\xe2\x8a\xa5'), 'html_entity': "&perp;"},

    {'ansi_num': "&#8901;", 'ansi_hex': (u'⋅', u'\xe2\x8b\x85'), 'html_entity': "&sdot;"},
    {'ansi_num': "&#8968;", 'ansi_hex': (u'⌈', u'\xef\xa3\xae'), 'html_entity': "&lceil;"},
    {'ansi_num': "&#8969;", 'ansi_hex': (u'⌉', u'\xef\xa3\xb9'), 'html_entity': "&rceil;"},
    {'ansi_num': "&#8970;", 'ansi_hex': (u'⌊', u'\xef\xa3\xb0'), 'html_entity': "&lfloor;"},
    {'ansi_num': "&#8971;", 'ansi_hex': (u'⌋', u'\xef\xa3\xbb'), 'html_entity': "&rfloor;"},
    
    {'ansi_num': "&#9001;", 'ansi_hex': (u'⟨', u'\xe2\x8c\xa9'), 'html_entity': "&lang;"},
    {'ansi_num': "&#9002;", 'ansi_hex': (u'⟩', u'\xe2\x8c\xaa'), 'html_entity': "&rang;"},
    
    {'ansi_num': "&#9674;", 'ansi_hex': (u'◊', u'\xe2\x97\x8a'), 'html_entity': "&loz;"},
    
    {'ansi_num': "&#9824;", 'ansi_hex': (u'♠', u'\xe2\x99\xa0'), 'html_entity': "&spades;"},
    {'ansi_num': "&#9827;", 'ansi_hex': (u'♣', u'\xe2\x99\xa3'), 'html_entity': "&clubs;"},
    {'ansi_num': "&#9829;", 'ansi_hex': (u'♥', u'\xe2\x99\xa5'), 'html_entity': "&hearts;"},
    {'ansi_num': "&#9830;", 'ansi_hex': (u'♦', u'\xe2\x99\xa6'), 'html_entity': "&diams;"},
  
    {'ansi_hex': u'\xcf\x86', 'html_entity': '&phis;'},
    {'ansi_hex': u'\xce\xb5', 'ansi_hex': u'ϵ', 'html_entity': '&epsiv;'},
    {'ansi_hex': u'\xcf\x82', 'ansi_hex': u'ς', 'html_entity': '&sigmav;'},
    {'ansi_hex': u'\xcf\x91', 'ansi_hex': u'ϑ', 'html_entity': '&thetav;'},
]


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

def replace_by_mapping(s, from_type, to_type, skip_list=None, debug=False):
    s = cast.to_unicode(s)

    if debug: print(u'replace_by_mapping(s="{s}", from_type="{ft}", to_type="{tt}"'.format(s=s, ft=from_type, tt=to_type))

    def _get_values_for_key(k, mapping, default=None):
        if debug: print('_get_values_for_key(k={k}, mapping={m}, default={d})'.format(k=k, m=mapping, d=default))

        if k in mapping:
            # Ultimately, we're trying to get a list of elements
            val = mapping[k]

            if isinstance(val, (str, unicode)):
                # Create a list from a single element
                if debug: print('    -> casting to a list and returning val')
                return [val]

            elif isinstance(val, (tuple, list)):
                # Just keep the list
                if debug: print('    -> returning val')
                return val

            else:
                if debug: print('    -> WTF! val: {v} is of type: {t}'.format(v=val, t=type(val)))

        else:
            if debug: print('    -> NO KEY; returning {d}'.format(d=default))

        return default

    for mapping in ascii_map:
        from_entities = _get_values_for_key(from_type, mapping)

        if not from_entities:
            continue

        if debug: print(u'  using from_entities: {l}'.format(l=from_entities))
        
        to_entities = _get_values_for_key(to_type, mapping, default=None)

        if to_entities is not None:
            if debug: print('  using to_entities: {l}'.format(l=to_entities))

            for k in from_entities:
                if debug: print(u'  "{s}".replace("{k}", "{v}")'.format(s=s, k=k, v=to_entities[0]))

                if skip_list and k in skip_list:
                    continue

                s = s.replace(k, to_entities[0])

                if debug: print(u'  s -> {s}'.format(s=s))

        else:
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

    """    
    s = replace_by_mapping(s, 'html_entity', 'ascii_replace', skip_list=skip_list)

    return s

def simplify_entities(s):
    """
    >>> simplify_entities('Hi &nbsp;there!')
    u'Hi  there!'

    >>> simplify_entities('Hi&mdash;there!')
    u'Hi--there!'

    >>> simplify_entities('here\u2014and there!')
    u'here--and there!'

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
    >>> remove_control_characters('the Bah\xc3\xa1\u2019\xc3\xad belief')
    u'the Bah\xc3\xa1\u2019\xc3\xad belief'

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


## ---------------------
if __name__ == "__main__":
    import doctest

    print "[fmt.py] Testing..."

    # Run the doctests
    doctest.testmod()

    # Now some that are trickier via doctest
    s = """
    This is
    a test
    """
    assert nuke_newlines(s) == "This is a test"

    # Woot!
    print "Done."

