#!/usr/bin/env python
# -*- coding: utf-8 -*-


__license__ = "MIT"
__version__ = "0.1"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."


def find_nonascii_line_in_file(file_name):
    count = 0
    error_count = 0
    with open(file_name, 'r') as fp:
        for line in fp.readlines():
            try:
                s = str(line)
            except:
                print("Error on line: {c}".format(c=count))
                error_count += 1
            else:
                count += 1


    print("Read: {c} lines".format(c=count))
    print("Found: {c} errors".format(c=error_count))


# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:", ['file=', 'nonascii'])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    infile = None
    mode_find_nonascii = False

    for o, a in opts:
        if o in ['-f', '--file']:
            infile = a

        if o in ['--nonascii']:
            mode_find_nonascii = True

    if infile:
        if mode_find_nonascii:
            find_nonascii_line_in_file(file_name=infile)

