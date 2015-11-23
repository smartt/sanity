#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def ip_for_hostname(s):
    """Yeah, this is a one-line function.

    >>> ip_for_hostname(None)

    >>> import identify
    >>> ip = ip_for_hostname('google.com')
    >>> identify.is_ip_address(ip)
    True

    """
    try:
        return socket.gethostbyname(s)
    except:
        return None


# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import doctest
    print("[net.py] Testing...")
    doctest.testmod()
    print("Done.")
