#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata

import cast


__license__ = "MIT"
__version__ = "0.2"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."

# Some of the items in `ascii_map` were seeded using a dictionary found within ReportLab's paraparser.py
# library, licensed under a BSD License.  For more, see: http://www.reportlab.com/software/opensource/
#
# Other's were found via unicode charts and lots of trial and error.

ascii_map = [
    {'ansi_num': '&#32;', 'ansi_hex': u'\x20', 'ascii_replace': ' '},
    {'ansi_num': '&#33;', 'ansi_hex': u'\x21', 'ascii_replace': '!'},
    {'ansi_num': '&#34;', 'ansi_hex': u'\x22', 'html_entity': '&quot;'},
    {'ansi_num': '&#35;', 'ansi_hex': u'\x23', 'ascii_replace': '#'},
    {'ansi_num': '&#36;', 'ansi_hex': u'\x24', 'ascii_replace': '$'},
    {'ansi_num': '&#37;', 'ansi_hex': u'\x25', 'ascii_replace': '%'},
    {'ansi_num': '&#38;', 'ansi_hex': u'\x26', 'html_entity': '&amp;'},
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
    {'ansi_num': '&#60;', 'ansi_hex': u'\x3C', 'html_entity': '&lt;'},
    {'ansi_num': '&#61;', 'ansi_hex': u'\x3D', 'ascii_replace': '='},
    {'ansi_num': '&#62;', 'ansi_hex': u'\x3E', 'html_entity': '&gt;'},
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
    {'ansi_num': '&#123;', 'ansi_hex': u'\x7B'},
    {'ansi_num': '&#124;', 'ansi_hex': u'\x7C'},
    {'ansi_num': '&#125;', 'ansi_hex': u'\x7D'},
    {'ansi_num': '&#126;', 'ansi_hex': u'\x7E'},
    {'ansi_num': '&#127;', 'ansi_hex': u'\x7F'},
    {'ansi_num': '&#129;', 'ansi_hex': u'\x81'},
    {'ansi_num': '&#141;', 'ansi_hex': u'\x8D'},
    {'ansi_num': '&#143;', 'ansi_hex': u'\x8F'},
    {'ansi_num': '&#144;', 'ansi_hex': u'\x90'},
    {'ansi_num': '&#157;', 'ansi_hex': u'\x9D'},
    {'ansi_num': '&#160;', 'ansi_hex': (u'\xc2\xa0', u'\xA0'), 'html_entity': '&nbsp;'},
    {'ansi_num': '&#161;', 'ansi_hex': (u'\xc2\xa1', u'\xA1'), 'html_entity': '&iexcl;'},
    {'ansi_num': '&#162;', 'ansi_hex': (u'\xc2\xa2', u'\xA2'), 'html_entity': '&cent;'},
    {'ansi_num': '&#163;', 'ansi_hex': (u'\xc2\xa3', u'\xA3'), 'html_entity': '&pound;'},
    {'ansi_num': '&#164;', 'ansi_hex': (u'\xc2\xa4', u'\xA4'), 'html_entity': '&curren;'},
    {'ansi_num': '&#165;', 'ansi_hex': (u'\xc2\xa5', u'\xA5'), 'html_entity': '&yen;'},
    {'ansi_num': '&#166;', 'ansi_hex': (u'\xc2\xa6', u'\xA6'), 'html_entity': '&brvbar;'},
    {'ansi_num': '&#167;', 'ansi_hex': (u'\xc2\xa7', u'\xA7'), 'html_entity': '&sect;'},
    {'ansi_num': '&#168;', 'ansi_hex': (u'\xc2\xa8', u'\xA8'), 'html_entity': '&uml;'},
    {'ansi_num': '&#169;', 'ansi_hex': (u'\xc2\xa9', u'\xA9'), 'html_entity': '&copy;'},
    {'ansi_num': '&#170;', 'ansi_hex': (u'\xc2\xaa', u'\xAA'), 'html_entity': '&ordf;'},
    {'ansi_num': '&#171;', 'ansi_hex': (u'\xc2\xab', u'\xAB'), 'html_entity': '&laquo;'},
    {'ansi_num': '&#172;', 'ansi_hex': (u'\xc2\xac', u'\xAC'), 'html_entity': '&not;'},
    {'ansi_num': '&#173;', 'ansi_hex': (u'\xc2\xad', u'\xAD'), 'html_entity': '&shy;'},
    {'ansi_num': '&#174;', 'ansi_hex': (u'\xc2\xae', u'\xAE'), 'html_entity': '&reg;'},
    {'ansi_num': '&#175;', 'ansi_hex': (u'\xc2\xaf', u'\xAF'), 'html_entity': '&macr;'},
    {'ansi_num': '&#176;', 'ansi_hex': (u'\xc2\xb0', u'\xB0'), 'html_entity': '&deg;'},
    {'ansi_num': '&#177;', 'ansi_hex': (u'\xc2\xb1', u'\xB1'), 'html_entity': '&plusmn;'},
    {'ansi_num': '&#178;', 'ansi_hex': (u'\xc2\xb2', u'\xB2'), 'html_entity': '&sup2;'},
    {'ansi_num': '&#179;', 'ansi_hex': (u'\xc2\xb3', u'\xB3'), 'html_entity': '&sup3;'},
    {'ansi_num': '&#180;', 'ansi_hex': (u'\xc2\xb4', u'\xB4'), 'html_entity': '&acute;'},
    {'ansi_num': '&#181;', 'ansi_hex': (u'\xc2\xb5', u'\xB5'), 'html_entity': '&micro;'},
    {'ansi_num': '&#182;', 'ansi_hex': (u'\xc2\xb6', u'\xB6'), 'html_entity': '&para;'},
    {'ansi_num': '&#183;', 'ansi_hex': (u'\xc2\xb7', u'\xB7'), 'html_entity': '&middot;'},
    {'ansi_num': '&#184;', 'ansi_hex': (u'\xc2\xb8', u'\xB8'), 'html_entity': '&cedil;'},
    {'ansi_num': '&#185;', 'ansi_hex': (u'\xc2\xb9', u'\xB9'), 'html_entity': '&sup1;'},
    {'ansi_num': '&#186;', 'ansi_hex': (u'\xc2\xba', u'\xBA'), 'html_entity': '&ordm;'},
    {'ansi_num': '&#187;', 'ansi_hex': (u'\xc2\xbb', u'\xBB'), 'html_entity': '&raquo;'},
    {'ansi_num': '&#188;', 'ansi_hex': (u'\xc2\xbc', u'\xBC'), 'html_entity': '&frac14;'},
    {'ansi_num': '&#189;', 'ansi_hex': (u'\xc2\xbd', u'\xBD'), 'html_entity': '&frac12;'},
    {'ansi_num': '&#190;', 'ansi_hex': (u'\xc2\xbe', u'\xBE'), 'html_entity': '&frac34;'},
    {'ansi_num': '&#191;', 'ansi_hex': (u'\xc2\xbf', u'\xBF'), 'html_entity': '&iquest;'},
    {'ansi_num': '&#192;', 'ansi_hex': (u'\xc3\x80', u'\xC0'), 'html_entity': '&Agrave;'},
    {'ansi_num': '&#193;', 'ansi_hex': (u'\xc3\x81', u'\xC1'), 'html_entity': '&Aacute;'},
    {'ansi_num': '&#194;', 'ansi_hex': (u'\xc3\x82', u'\xC2'), 'html_entity': '&Acirc;'},
    {'ansi_num': '&#195;', 'ansi_hex': (u'\xc3\x83', u'\xC3'), 'html_entity': '&Atilde;'},
    {'ansi_num': '&#196;', 'ansi_hex': (u'\xc3\x84', u'\xC4'), 'html_entity': '&Auml;'},
    {'ansi_num': '&#197;', 'ansi_hex': (u'\xc3\x85', u'\xC5'), 'html_entity': '&Aring;'},
    {'ansi_num': '&#198;', 'ansi_hex': (u'\xc3\x86', u'\xC6'), 'html_entity': '&AElig;'},
    {'ansi_num': '&#199;', 'ansi_hex': (u'\xc3\x87', u'\xC7'), 'html_entity': '&Ccedil;'},
    {'ansi_num': '&#200;', 'ansi_hex': (u'\xc3\x88', u'\xC8'), 'html_entity': '&Egrave;'},
    {'ansi_num': '&#201;', 'ansi_hex': (u'\xc3\x89', u'\xC9'), 'html_entity': '&Eacute;'},
    {'ansi_num': '&#202;', 'ansi_hex': (u'\xc3\x8a', u'\xCA'), 'html_entity': '&Ecirc;'},
    {'ansi_num': '&#203;', 'ansi_hex': (u'\xc3\x8b', u'\xCB'), 'html_entity': '&Euml;'},
    {'ansi_num': '&#204;', 'ansi_hex': (u'\xc3\x8c', u'\xCC'), 'html_entity': '&Igrave;'},
    {'ansi_num': '&#205;', 'ansi_hex': (u'\xc3\x8d', u'\xCD'), 'html_entity': '&Iacute;'},
    {'ansi_num': '&#206;', 'ansi_hex': (u'\xc3\x8e', u'\xCE'), 'html_entity': '&Icirc;'},
    {'ansi_num': '&#207;', 'ansi_hex': (u'\xc3\x8f', u'\xCF'), 'html_entity': '&Iuml;'},
    {'ansi_num': '&#208;', 'ansi_hex': (u'\xc3\x90', u'\xD0'), 'html_entity': '&ETH;'},
    {'ansi_num': '&#209;', 'ansi_hex': (u'\xc3\x91', u'\xD1'), 'html_entity': '&Ntilde;'},
    {'ansi_num': '&#210;', 'ansi_hex': (u'\xc3\x92', u'\xD2'), 'html_entity': '&Ograve;'},
    {'ansi_num': '&#211;', 'ansi_hex': (u'\xc3\x93', u'\xD3'), 'html_entity': '&Oacute;'},
    {'ansi_num': '&#212;', 'ansi_hex': (u'\xc3\x94', u'\xD4'), 'html_entity': '&Ocirc;'},
    {'ansi_num': '&#213;', 'ansi_hex': (u'\xc3\x95', u'\xD5'), 'html_entity': '&Otilde;'},
    {'ansi_num': '&#214;', 'ansi_hex': (u'\xc3\x96', u'\xD6'), 'html_entity': '&Ouml;'},
    {'ansi_num': '&#215;', 'ansi_hex': (u'\xc3\x97', u'\xD7'), 'html_entity': '&times;'},
    {'ansi_num': '&#216;', 'ansi_hex': (u'\xc3\x98', u'\xD8'), 'html_entity': '&Oslash;'},
    {'ansi_num': '&#217;', 'ansi_hex': (u'\xc3\x99', u'\xD9'), 'html_entity': '&Ugrave;'},
    {'ansi_num': '&#218;', 'ansi_hex': (u'\xc3\x9a', u'\xDA'), 'html_entity': '&Uacute;'},
    {'ansi_num': '&#219;', 'ansi_hex': (u'\xc3\x9b', u'\xDB'), 'html_entity': '&Ucirc;'},
    {'ansi_num': '&#220;', 'ansi_hex': (u'\xc3\x9c', u'\xDC'), 'html_entity': '&Uuml;'},
    {'ansi_num': '&#221;', 'ansi_hex': (u'\xc3\x9d', u'\xDD'), 'html_entity': '&Yacute;'},
    {'ansi_num': '&#222;', 'ansi_hex': (u'\xc3\x9e', u'\xDE'), 'html_entity': '&THORN;'},
    {'ansi_num': '&#223;', 'ansi_hex': (u'\xc3\x9f', u'\xDF'), 'html_entity': '&szlig;'},
    {'ansi_num': ('&#224;', '&#24;'), 'ansi_hex': (u'\xc3\xa0', u'\xE0'), 'html_entity': '&agrave;'},
    {'ansi_num': ('&#225;', '&#25;'), 'ansi_hex': (u'\xc3\xa1', u'\xE1'), 'html_entity': '&aacute;'},
    {'ansi_num': '&#226;', 'ansi_hex': (u'\xc3\xa2', u'\xE2'), 'html_entity': '&acirc;'},
    {'ansi_num': '&#227;', 'ansi_hex': (u'\xc3\xa3', u'\xE3'), 'html_entity': '&atilde;'},
    {'ansi_num': '&#228;', 'ansi_hex': (u'\xc3\xa4', u'\xE4'), 'html_entity': '&auml;'},
    {'ansi_num': '&#229;', 'ansi_hex': (u'\xc3\xa5', u'\xE5'), 'html_entity': '&aring;'},
    {'ansi_num': '&#230;', 'ansi_hex': (u'\xc3\xa6', u'\xE6'), 'html_entity': '&aelig;'},
    {'ansi_num': '&#231;', 'ansi_hex': (u'\xc3\xa7', u'\xE7'), 'html_entity': '&ccedil;'},
    {'ansi_num': '&#232;', 'ansi_hex': (u'\xc3\xa8', u'\xE8'), 'html_entity': '&egrave;'},
    {'ansi_num': '&#233;', 'ansi_hex': (u'\xc3\xa9', u'\xE9'), 'html_entity': '&eacute;'},
    {'ansi_num': '&#234;', 'ansi_hex': (u'\xc3\xaa', u'\xEA'), 'html_entity': '&ecirc;'},
    {'ansi_num': '&#235;', 'ansi_hex': (u'\xc3\xab', u'\xEB'), 'html_entity': '&euml;'},
    {'ansi_num': '&#236;', 'ansi_hex': (u'\xc3\xac', u'\xEC'), 'html_entity': '&igrave;'},
    {'ansi_num': '&#237;', 'ansi_hex': (u'\xc3\xad', u'\xED'), 'html_entity': '&iacute;'},
    {'ansi_num': '&#238;', 'ansi_hex': (u'\xc3\xae', u'\xEE'), 'html_entity': '&icirc;'},
    {'ansi_num': '&#239;', 'ansi_hex': (u'\xc3\xaf', u'\xEF'), 'html_entity': '&iuml;'},
    {'ansi_num': '&#240;', 'ansi_hex': (u'\xc3\xb0', u'\xF0'), 'html_entity': '&eth;'},
    {'ansi_num': '&#241;', 'ansi_hex': (u'\xc3\xb1', u'\xF1'), 'html_entity': '&ntilde;'},
    {'ansi_num': '&#242;', 'ansi_hex': (u'\xc3\xb2', u'\xF2'), 'html_entity': '&ograve;'},
    {'ansi_num': '&#243;', 'ansi_hex': (u'\xc3\xb3', u'\xF3'), 'html_entity': '&oacute;'},
    {'ansi_num': '&#244;', 'ansi_hex': (u'\xc3\xb4', u'\xF4', u'\xf4'), 'html_entity': '&ocirc;'},
    {'ansi_num': '&#245;', 'ansi_hex': (u'\xc3\xb5', u'\xF5'), 'html_entity': '&otilde;'},
    {'ansi_num': '&#246;', 'ansi_hex': (u'\xc3\xb6', u'\xF6'), 'html_entity': '&ouml;'},
    {'ansi_num': '&#247;', 'ansi_hex': (u'\xc3\xb7', u'\xF7'), 'html_entity': '&divide;'},
    {'ansi_num': '&#248;', 'ansi_hex': (u'\xc3\xb8', u'\xF8'), 'html_entity': '&oslash;'},
    {'ansi_num': '&#249;', 'ansi_hex': (u'\xc3\xb9', u'\xF9'), 'html_entity': '&ugrave;'},
    {'ansi_num': '&#250;', 'ansi_hex': (u'\xc3\xba', u'\xFA'), 'html_entity': '&uacute;'},
    {'ansi_num': '&#251;', 'ansi_hex': (u'\xc3\xbb', u'\xFB'), 'html_entity': '&ucirc;'},
    {'ansi_num': '&#252;', 'ansi_hex': (u'\xc3\xbc', u'\xFC'), 'html_entity': '&uuml;'},
    {'ansi_num': '&#253;', 'ansi_hex': (u'\xc3\xbd', u'\xFD'), 'html_entity': '&yacute;'},
    {'ansi_num': '&#254;', 'ansi_hex': (u'\xc3\xbe', u'\xFE'), 'html_entity': '&thorn;'},
    {'ansi_num': '&#255;', 'ansi_hex': (u'\xc3\xbf', u'\xFF'), 'html_entity': '&yuml;'},

    {'ansi_num': '&#338;', 'ansi_hex': (u'\xc5\x92', u'\x8C'), 'html_entity': '&OElig;'},
    {'ansi_num': '&#339;', 'ansi_hex': (u'\xc5\x93', u'\x9C'), 'html_entity': '&oelig;'},
    {'ansi_num': '&#352;', 'ansi_hex': (u'\xc5\xa0', u'\x8A'), 'html_entity': '&Scaron;'},
    {'ansi_num': '&#353;', 'ansi_hex': (u'\xc5\xa1', u'\x9A'), 'html_entity': '&scaron;'},
    {'ansi_num': '&#376;', 'ansi_hex': (u'\xc5\xb8', u'\x9F'), 'html_entity': '&Yuml;'},
    {'ansi_num': '&#381;', 'ansi_hex': u'\x8E'},
    {'ansi_num': '&#382;', 'ansi_hex': u'\x9E'},
    {'ansi_num': '&#402;', 'ansi_hex': (u'\xc6\x92', u'\x83'), 'html_entity': '&fnof;'},
    
    {'ansi_num': '&#710;', 'ansi_hex': (u'\xcb\x86', u'\x88'), 'html_entity': '&circ;'},
    {'ansi_num': '&#732;', 'ansi_hex': (u'\xcb\x9c', u'\x98'), 'html_entity': '&tilde;'},
    
    {'ansi_num': "&#913;", 'ansi_hex': u'\xce\x91', 'html_entity': "&Alpha;"},
    {'ansi_num': "&#914;", 'ansi_hex': u'\xce\x92', 'html_entity': "&Beta;"},
    {'ansi_num': "&#915;", 'ansi_hex': u'\xce\x93', 'html_entity': "&Gamma;"},
    {'ansi_num': "&#916;", 'ansi_hex': u'\xe2\x88\x86', 'html_entity': "&Delta;"},
    {'ansi_num': "&#917;", 'ansi_hex': u'\xce\x95', 'html_entity': "&Epsilon;"},
    {'ansi_num': "&#918;", 'ansi_hex': u'\xce\x96', 'html_entity': "&Zeta;"},
    {'ansi_num': "&#919;", 'ansi_hex': u'\xce\x97', 'html_entity': "&Eta;"},
    {'ansi_num': "&#920;", 'ansi_hex': u'\xce\x98', 'html_entity': "&Theta;"},
    {'ansi_num': "&#921;", 'ansi_hex': u'\xce\x99', 'html_entity': "&Iota;"},
    {'ansi_num': "&#922;", 'ansi_hex': u'\xce\x9a', 'html_entity': "&Kappa;"},
    {'ansi_num': "&#923;", 'ansi_hex': u'\xce\x9b', 'html_entity': "&Lambda;"},
    {'ansi_num': "&#924;", 'ansi_hex': u'\xce\x9c', 'html_entity': "&Mu;"},
    {'ansi_num': "&#925;", 'ansi_hex': u'\xce\x9d', 'html_entity': "&Nu;"},
    {'ansi_num': "&#926;", 'ansi_hex': u'\xce\x9e', 'html_entity': "&Xi;"},
    {'ansi_num': "&#927;", 'ansi_hex': u'\xce\x9f', 'html_entity': "&Omicron;"},
    {'ansi_num': "&#928;", 'ansi_hex': u'\xce\xa0', 'html_entity': "&Pi;"},
    {'ansi_num': "&#929;", 'ansi_hex': u'\xce\xa1', 'html_entity': "&Rho;"},
    {'ansi_num': "&#931;", 'ansi_hex': u'\xce\xa3', 'html_entity': "&Sigma;"},
    {'ansi_num': "&#932;", 'ansi_hex': u'\xce\xa4', 'html_entity': "&Tau;"},
    {'ansi_num': "&#933;", 'ansi_hex': u'\xce\xa5', 'html_entity': "&Upsilon;"},
    {'ansi_num': "&#934;", 'ansi_hex': u'\xce\xa6', 'html_entity': "&Phi;"},
    {'ansi_num': "&#935;", 'html_entity': "&Chi;"},
    {'ansi_num': "&#936;", 'html_entity': "&Psi;"},
    {'ansi_num': "&#937;", 'ansi_hex': u'\xe2\x84\xa6', 'html_entity': "&Omega;"},
    {'ansi_num': "&#945;", 'ansi_hex': u'\xce\xb1', 'html_entity': "&alpha;"},
    {'ansi_num': "&#946;", 'ansi_hex': u'\xce\xb2', 'html_entity': "&beta;"},
    {'ansi_num': "&#947;", 'ansi_hex': u'\xce\xb3', 'html_entity': "&gamma;"},
    {'ansi_num': "&#948;", 'ansi_hex': u'\xce\xb4', 'html_entity': "&delta;"},
    {'ansi_num': "&#949;", 'ansi_hex': u'\xce\xb5', 'html_entity': "&epsilon;"},
    {'ansi_num': "&#950;", 'ansi_hex': u'\xce\xb6', 'html_entity': "&zeta;"},
    {'ansi_num': "&#951;", 'ansi_hex': u'\xce\xb7', 'html_entity': "&eta;"},
    {'ansi_num': "&#952;", 'ansi_hex': u'\xce\xb8', 'html_entity': "&theta;"},
    {'ansi_num': "&#953;", 'ansi_hex': u'\xce\xb9', 'html_entity': "&iota;"},
    {'ansi_num': "&#954;", 'ansi_hex': u'\xce\xba', 'html_entity': "&kappa;"},
    {'ansi_num': "&#955;", 'ansi_hex': u'\xce\xbb', 'html_entity': "&lambda;"},
    {'ansi_num': "&#956;", 'html_entity': "&mu;"},
    {'ansi_num': "&#957;", 'ansi_hex': u'\xce\xbd', 'html_entity': "&nu;"},
    {'ansi_num': "&#958;", 'ansi_hex': u'\xce\xbe', 'html_entity': "&xi;"},
    {'ansi_num': "&#959;", 'ansi_hex': u'\xce\xbf', 'html_entity': "&omicron;"},
    {'ansi_num': "&#960;", 'ansi_hex': u'\xcf\x80', 'html_entity': "&pi;"},
    {'ansi_num': "&#961;", 'ansi_hex': u'\xcf\x81', 'html_entity': "&rho;"},
    {'ansi_num': "&#962;", 'ansi_hex': u'\xcf\x82', 'html_entity': "&sigmaf;"},
    {'ansi_num': "&#963;", 'ansi_hex': u'\xcf\x83', 'html_entity': "&sigma;"},
    {'ansi_num': "&#964;", 'ansi_hex': u'\xcf\x84', 'html_entity': "&tau;"},
    {'ansi_num': "&#965;", 'ansi_hex': u'\xcf\x85', 'html_entity': "&upsilon;"},
    {'ansi_num': "&#966;", 'ansi_hex': u'\xcf\x95', 'html_entity': "&phi;"},
    {'ansi_num': "&#967;", 'ansi_hex': u'\xcf\x87', 'html_entity': "&chi;"},
    {'ansi_num': "&#968;", 'ansi_hex': u'\xcf\x88', 'html_entity': "&psi;"},
    {'ansi_num': "&#969;", 'ansi_hex': u'\xcf\x89', 'html_entity': "&omega;"},
    {'ansi_num': "&#977;", 'ansi_hex': u'\xcf\x91', 'html_entity': "&thetasym;"},
    {'ansi_num': "&#978;", 'ansi_hex': u'\xcf\x92', 'html_entity': "&upsih;"},
    {'ansi_num': "&#982;", 'ansi_hex': u'\xcf\x96', 'html_entity': "&piv;"},
    
    {'ansi_num': "&#8194;", 'ansi_hex': u'\xe2\x80\x82', 'html_entity': "&ensp;"},
    {'ansi_num': "&#8195;", 'ansi_hex': u'\xe2\x80\x83', 'html_entity': "&emsp;"},
    {'ansi_num': "&#8201;", 'ansi_hex': u'\xe2\x80\x89', 'html_entity': "&thinsp;"},
    {'ansi_num': "&#8204;", 'ansi_hex': u'\xe2\x80\x8c', 'html_entity': "&zwnj;"},
    {'ansi_num': "&#8205;", 'ansi_hex': u'\xe2\x80\x8d', 'html_entity': "&zwj;"},
    {'ansi_num': "&#8206;", 'ansi_hex': u'\xe2\x80\x8e', 'html_entity': "&lrm;"},
    {'ansi_num': "&#8207;", 'ansi_hex': u'\xe2\x80\x8f', 'html_entity': "&rlm;"},
    {'ansi_num': "&#8211;", 'ansi_hex': (u'\xe2\x80\x93', u'\x96'), 'html_entity': "&ndash;"},
    {'ansi_num': '&#8212;', 'ansi_hex': (u'\xe2\x80\x94', u'\x97'), 'html_entity': '&mdash;'},
    {'ansi_num': '&#8216;', 'ansi_hex': (u'\xe2\x80\x98', u'\x91'), 'html_entity': '&lsquo;'},
    {'ansi_num': '&#8217;', 'ansi_hex': (u'\xe2\x80\x99', u'\x92'), 'html_entity': '&rsquo;'},
    {'ansi_num': '&#8218;', 'ansi_hex': (u'\xe2\x80\x9a', u'\x82'), 'html_entity': '&sbquo;'},
    {'ansi_num': '&#8220;', 'ansi_hex': (u'\xe2\x80\x9c', u'\x93'), 'html_entity': '&ldquo;'},
    {'ansi_num': '&#8221;', 'ansi_hex': (u'\xe2\x80\x9d', u'\x94'), 'html_entity': '&rdquo;'},
    {'ansi_num': '&#8222;', 'ansi_hex': (u'\xe2\x80\x9e', u'\x84'), 'html_entity': '&bdquo;'},
    {'ansi_num': '&#8224;', 'ansi_hex': (u'\xe2\x80\xa0', u'\x86'), 'html_entity': '&dagger;'},
    {'ansi_num': '&#8225;', 'ansi_hex': (u'\xe2\x80\xa1', u'\x87'), 'html_entity': '&Dagger;'},
    {'ansi_num': '&#8226;', 'ansi_hex': (u'\xe2\x80\xa2', u'\x95'), 'html_entity': '&bull;'},
    {'ansi_num': '&#8230;', 'ansi_hex': (u'\xe2\x80\xa6', u'\x85'), 'html_entity': '&hellip;'},
    {'ansi_num': '&#8240;', 'ansi_hex': (u'\xe2\x80\xb0', u'\x89'), 'html_entity': '&permil;'},
    {'ansi_num': "&#8242;", 'ansi_hex': u'\xe2\x80\xb2', 'html_entity': "&prime;"},
    {'ansi_num': "&#8243;", 'ansi_hex': u'\xe2\x80\xb3', 'html_entity': "&Prime;"},
    {'ansi_num': '&#8249;', 'ansi_hex': (u'\xe2\x80\xb9', u'\x8B'), 'html_entity': '&lsaquo;'},
    {'ansi_num': '&#8250;', 'ansi_hex': (u'\xe2\x80\xba', u'\x9B'), 'html_entity': '&rsaquo;'},
    {'ansi_num': "&#8254;", 'ansi_hex': u'\xef\xa3\xa5', 'html_entity': "&oline;"},
    {'ansi_num': "&#8260;", 'ansi_hex': u'\xe2\x81\x84', 'html_entity': "&frasl;"},

    {'ansi_num': '&#8364;', 'ansi_hex': (u'\xe2\x82\xac', u'\x80'), 'html_entity': '&euro;'},
    {'ansi_num': '&#8482;', 'ansi_hex': u'\x99', 'html_entity': '&trade;'},

    {'ansi_num': "&#8465;", 'ansi_hex': u'\xe2\x84\x91', 'html_entity': "&image;"},
    {'ansi_num': "&#8472;", 'ansi_hex': u'\xe2\x84\x98', 'html_entity': "&weierp;"},
    {'ansi_num': "&#8476;", 'ansi_hex': u'\xe2\x84\x9c', 'html_entity': "&real;"},
    {'ansi_num': "&#8482;", 'ansi_hex': u'\xef\xa3\xaa', 'html_entity': "&trade;"},

    {'ansi_num': "&#8501;", 'ansi_hex': u'\xe2\x84\xb5', 'html_entity': "&alefsym;"},
    {'ansi_num': "&#8592;", 'ansi_hex': u'\xe2\x86\x90', 'html_entity': "&larr;"},
    {'ansi_num': "&#8593;", 'ansi_hex': u'\xe2\x86\x91', 'html_entity': "&uarr;"},
    {'ansi_num': "&#8594;", 'ansi_hex': u'\xe2\x86\x92', 'html_entity': "&rarr;"},
    {'ansi_num': "&#8595;", 'ansi_hex': u'\xe2\x86\x93', 'html_entity': "&darr;"},
    {'ansi_num': "&#8596;", 'ansi_hex': u'\xe2\x86\x94', 'html_entity': "&harr;"},

    {'ansi_num': "&#8629;", 'ansi_hex': u'\xe2\x86\xb5', 'html_entity': "&crarr;"},
    {'ansi_num': "&#8656;", 'ansi_hex': u'\xe2\x87\x90', 'html_entity': "&lArr;"},
    {'ansi_num': "&#8657;", 'ansi_hex': u'\xe2\x87\x91', 'html_entity': "&uArr;"},
    {'ansi_num': "&#8658;", 'ansi_hex': u'\xe2\x87\x92', 'html_entity': "&rArr;"},
    {'ansi_num': "&#8659;", 'ansi_hex': u'\xe2\x87\x93', 'html_entity': "&dArr;"},
    {'ansi_num': "&#8660;", 'ansi_hex': u'\xe2\x87\x94', 'html_entity': "&hArr;"},

    {'ansi_num': "&#8704;", 'ansi_hex': u'\xe2\x88\x80', 'html_entity': "&forall;"},
    {'ansi_num': "&#8706;", 'ansi_hex': u'\xe2\x88\x82', 'html_entity': "&part;"},
    {'ansi_num': "&#8707;", 'ansi_hex': u'\xe2\x88\x83', 'html_entity': "&exist;"},
    {'ansi_num': "&#8709;", 'ansi_hex': u'\xe2\x88\x85', 'html_entity': "&empty;"},
    {'ansi_num': "&#8711;", 'ansi_hex': u'\xe2\x88\x87', 'html_entity': "&nabla;"},
    {'ansi_num': "&#8712;", 'ansi_hex': u'\xe2\x88\x88', 'html_entity': "&isin;"},
    {'ansi_num': "&#8713;", 'ansi_hex': u'\xe2\x88\x89', 'html_entity': "&notin;"},
    {'ansi_num': "&#8715;", 'ansi_hex': u'\xe2\x88\x8b', 'html_entity': "&ni;"},
    {'ansi_num': "&#8719;", 'ansi_hex': u'\xe2\x88\x8f', 'html_entity': "&prod;"},
    {'ansi_num': "&#8721;", 'ansi_hex': u'\xe2\x88\x91', 'html_entity': "&sum;"},
    {'ansi_num': "&#8722;", 'ansi_hex': u'\xe2\x88\x92', 'html_entity': "&minus;"},
    {'ansi_num': "&#8727;", 'ansi_hex': u'\xe2\x88\x97', 'html_entity': "&lowast;"},
    {'ansi_num': "&#8730;", 'ansi_hex': u'\xe2\x88\x9a', 'html_entity': "&radic;"},
    {'ansi_num': "&#8733;", 'ansi_hex': u'\xe2\x88\x9d', 'html_entity': "&prop;"},
    {'ansi_num': "&#8734;", 'ansi_hex': u'\xe2\x88\x9e', 'html_entity': "&infin;"},
    {'ansi_num': "&#8736;", 'ansi_hex': u'\xe2\x88\xa0', 'html_entity': "&ang;"},
    {'ansi_num': "&#8743;", 'ansi_hex': u'\xe2\x88\xa7', 'html_entity': "&and;"},
    {'ansi_num': "&#8744;", 'ansi_hex': u'\xe2\x88\xa8', 'html_entity': "&or;"},
    {'ansi_num': "&#8745;", 'ansi_hex': u'\xe2\x88\xa9', 'html_entity': "&cap;"},
    {'ansi_num': "&#8746;", 'ansi_hex': u'\xe2\x88\xaa', 'html_entity': "&cup;"},
    {'ansi_num': "&#8747;", 'ansi_hex': u'\xe2\x88\xab', 'html_entity': "&int;"},
    {'ansi_num': "&#8756;", 'ansi_hex': u'\xe2\x88\xb4', 'html_entity': "&there4;"},
    {'ansi_num': "&#8764;", 'ansi_hex': u'\xe2\x88\xbc', 'html_entity': "&sim;"},
    {'ansi_num': "&#8773;", 'ansi_hex': u'\xe2\x89\x85', 'html_entity': "&cong;"},
    {'ansi_num': "&#8776;", 'ansi_hex': u'\xe2\x89\x88', 'html_entity': "&asymp;"},

    {'ansi_num': "&#8800;", 'ansi_hex': u'\xe2\x89\xa0', 'html_entity': "&ne;"},
    {'ansi_num': "&#8801;", 'ansi_hex': u'\xe2\x89\xa1', 'html_entity': "&equiv;"},
    {'ansi_num': "&#8804;", 'ansi_hex': u'\xe2\x89\xa4', 'html_entity': "&le;"},
    {'ansi_num': "&#8805;", 'ansi_hex': u'\xe2\x89\xa5', 'html_entity': "&ge;"},
    {'ansi_num': "&#8834;", 'ansi_hex': u'\xe2\x8a\x82', 'html_entity': "&sub;"},
    {'ansi_num': "&#8835;", 'ansi_hex': u'\xe2\x8a\x83', 'html_entity': "&sup;"},
    {'ansi_num': "&#8836;", 'ansi_hex': u'\xe2\x8a\x84', 'html_entity': "&nsub;"},
    {'ansi_num': "&#8838;", 'ansi_hex': u'\xe2\x8a\x86', 'html_entity': "&sube;"},
    {'ansi_num': "&#8839;", 'ansi_hex': u'\xe2\x8a\x87', 'html_entity': "&supe;"},
    {'ansi_num': "&#8853;", 'ansi_hex': u'\xe2\x8a\x95', 'html_entity': "&oplus;"},
    {'ansi_num': "&#8855;", 'ansi_hex': u'\xe2\x8a\x97', 'html_entity': "&otimes;"},
    {'ansi_num': "&#8869;", 'ansi_hex': u'\xe2\x8a\xa5', 'html_entity': "&perp;"},

    {'ansi_num': "&#8901;", 'ansi_hex': u'\xe2\x8b\x85', 'html_entity': "&sdot;"},
    {'ansi_num': "&#8968;", 'ansi_hex': u'\xef\xa3\xae', 'html_entity': "&lceil;"},
    {'ansi_num': "&#8969;", 'ansi_hex': u'\xef\xa3\xb9', 'html_entity': "&rceil;"},
    {'ansi_num': "&#8970;", 'ansi_hex': u'\xef\xa3\xb0', 'html_entity': "&lfloor;"},
    {'ansi_num': "&#8971;", 'ansi_hex': u'\xef\xa3\xbb', 'html_entity': "&rfloor;"},

    {'ansi_num': "&#9001;", 'ansi_hex': u'\xe2\x8c\xa9', 'html_entity': "&lang;"},
    {'ansi_num': "&#9002;", 'ansi_hex': u'\xe2\x8c\xaa', 'html_entity': "&rang;"},

    {'ansi_num': "&#9674;", 'ansi_hex': u'\xe2\x97\x8a', 'html_entity': "&loz;"},

    {'ansi_num': "&#9824;", 'ansi_hex': u'\xe2\x99\xa0', 'html_entity': "&spades;"},
    {'ansi_num': "&#9827;", 'ansi_hex': u'\xe2\x99\xa3', 'html_entity': "&clubs;"},
    {'ansi_num': "&#9829;", 'ansi_hex': u'\xe2\x99\xa5', 'html_entity': "&hearts;"},
    {'ansi_num': "&#9830;", 'ansi_hex': u'\xe2\x99\xa6', 'html_entity': "&diams;"},
  
    {'ansi_hex': u'\xcf\x86', 'html_entity': '&phis;'},
    {'ansi_hex': u'\xce\xb5', 'html_entity': '&epsiv;'},
    {'ansi_hex': u'\xcf\x82', 'html_entity': '&sigmav;'},
    {'ansi_hex': u'\xcf\x91', 'html_entity': '&thetav;'},
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

def replace_by_mapping(s, from_type, to_type):
    s = cast.to_unicode(s)

    # print(u'replace_by_mapping(s="{s}", from_type="{ft}", to_type="{tt}"'.format(s=s, ft=from_type, tt=to_type))

    def _get_values_for_key(k, mapping, default=None):
        # print('_get_values_for_key(k={k}, mapping={m}, default={d})'.format(k=k, m=mapping, d=default))

        if k in mapping:
            # Ultimately, we're trying to get a list of elements
            val = mapping[k]

            if isinstance(val, (str, unicode)):
                # Create a list from a single element
                # print('    -> casting to a list and returning val')
                return [val]

            elif isinstance(val, (tuple, list)):
                # Just keep the list
                # print('    -> returning val')
                return val

            # else:
                # print('    -> WTF! val: {v} is of type: {t}'.format(v=val, t=type(val)))

        # else:
            # print('    -> NO KEY; returning {d}'.format(d=default))

        return default

    for mapping in ascii_map:
        from_entities = _get_values_for_key(from_type, mapping)

        if not from_entities:
            continue

        # print(u'  using from_entities: {l}'.format(l=from_entities))
        
        to_entities = _get_values_for_key(to_type, mapping, default=None)

        if to_entities is not None:
            # print('  using to_entities: {l}'.format(l=to_entities))

            for k in from_entities:
                # print(u'  "{s}".replace("{k}", "{v}")'.format(s=s, k=k, v=to_entities[0]))

                s = s.replace(k, to_entities[0])

                # print(u'  s -> {s}'.format(s=s))

        # else:
            # print('  SKIP')

    return s
 
def sub_greeks(s):
    """
    >>> sub_greeks('hi there')
    u'hi there'

    >>> sub_greeks(u'hi\xc2\xa0there')
    u'hi&nbsp;there'

    """
    s = replace_by_mapping(s, 'ansi_hex', 'html_entity')

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
        u'\u2026': '...',
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

    s = re.sub(r'/\*.*\*/', '', s)

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
