sanity
======

Hacks and utilities for cleaning, parsing, and transforming text

This library has evolved over the past decade to maintain my sanity while working with various text input and files.  Some of the techniques may be dated (and there may be better solutions that have found their way into the standard library), but the functions within solved a problem when another solution wasn't easily found.  Perhaps they'll help you in a jam as well.

## abbr.py ##
Used to expand/contract abbreviations.  Currently only handles US State names (ex., 'Texas' -> 'TX' and back.)  This is helpful when normalizing addresses.

## cast.py ##
Functions to cast data from one format to another. The most-used is probably `to_ascii`, but `to_int` and `to_bool` are helpful when normalizing form input. (Ex., `to_bool` can deal with 'yes', 'no', 'on', 'off', etc.)

## extract.py ##
For when you need to extract a substring or piece of data from a larger context.  Dates, numbers, prices, email addresses, etc. There's also a handy function for extracting text based on a regex pattern, provided the text doesn't match a supplied 'blacklist' pattern.  Use this when look-ahead/behind patterns won't cut it.

## find.py ##
Probably the wrong name. These functions are simliar to those in `extract.py`, in that they isolate sub-strings, but they also return the parent string with the isolated text removed.  You'll have to look at the doctests to see what I mean.

## fmt.py ##
This is the big daddy. There are all kinds of formatting functions in here. Use this to convert unicode characters to HTML encodings; strip HTML; create slugs; convert numbers to words (ie., 10 -> 'ten'); and in general, normalize text into whatever format you need. Most functions were written to deal with Word docs copy-pasted into HTML forms, sadly enough.

## identify.py ##
These are `is_` functions, like `is_numeric` and `is_whitespace`.

## numeraltable.py ##
This contains the numbers 0 to 100 spelled out (e.g., zero to one hundred.) It is used by `fmt.py` when converting numbers to numerals.

## shell.py ##
For when you want to run something in the shell rather than Python. This is really just so I don't have to keep looking up the subprocess syntax whenever this need comes up.

## split.py ##
Split strings based on patterns, or by things that look like taxonomy 'tags'.

## uniasciitable.py ##
Used by `fmt.py` to convert unicode text into HTML/XML-safe ascii, this is a big table that maps HTML encodings to unicode characters to ascii representations to HTML entities.  If you have '&amp;gt;' and want '&amp;#62;' or '>', you can look it up here.  There's over a thousand mappings in here, and yes, I did most by hand out of neccesity.

## util.py ##
Currently all it knows how to do is find non-ascii characters in files.  I needed it at some point when generating large quantities of XML that needed to be read by an ascii-only parser.


----

Copyright 2009-2016 Erik Smartt

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
