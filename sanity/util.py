#!/usr/bin/env python
# -*- coding: utf-8 -*-


def find_nonascii_line_in_file(file_name):
    line_count = 1
    char_count = 0
    error_count = 0

    with open(file_name, 'r') as fp:
        for line in fp.readlines():
            try:
                char_count = 0
                for c in line:
                    if ord(c) > 128:
                        print("Error on line: {c}, char: {n}, ord: {d}".format(c=line_count, n=char_count, d=ord(c)))

                    char_count += 1

                s = str(line)

            except:
                print("Error on line: {c}".format(c=line_count))
                error_count += 1

            line_count += 1

    print("Read: {c} lines".format(c=line_count))
    print("Found: {c} errors".format(c=error_count))


# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:", ['file=', 'nonascii'])
    except getopt.GetoptError as err:
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

