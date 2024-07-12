#!/usr/bin/env python3

# First attempt: bad = "00".split()
# We start the program with Immunity Debugger
# !mona bytearray -b "\x00"
# We make it crash and we compare with ESP or direct address
# !mona compare -f C:\mona\oscp\bytearray.bin -a esp 

"""
This script generates a list of non-bad characters in hexadecimal format and prints
them in a format suitable for various debugging and exploit development tools. It 
also prints the list of bad characters for use with Mona, a plugin for Immunity Debugger.

Usage:
    python3 badchars.py "00 a9 cd d4"

Arguments:
    bad_chars (str): A space-separated string of bad characters in hexadecimal format.
"""

import sys

def generate_non_badchars(bad_chars):
    """
    Generates a string of non-bad characters in hexadecimal format.

    Args:
        bad_chars (str): A space-separated string of bad characters in hexadecimal format.

    Returns:
        str: A string of non-bad characters formatted as \\xHH.
    """
    bad = bad_chars.split()
    non_badchars = ""
    for x in range(1, 256):
        if "{:02x}".format(x) not in bad:
            non_badchars += "\\x" + "{:02x}".format(x)
    return non_badchars

def print_mona_format(bad_chars):
    """
    Prints the bad characters in a format suitable for Mona.

    Args:
        bad_chars (str): A space-separated string of bad characters in hexadecimal format.
    """
    bad = bad_chars.split()
    for byte in bad:
        print("\\x{}".format(byte), end='')
    print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 badchars.py \"00 a9 cd d4\"")
        sys.exit(1)

    bad_chars = sys.argv[1]
    non_badchars = generate_non_badchars(bad_chars)

    print("badchars = ", end='')
    print(non_badchars)
    print("\n\nFor mona")
    print_mona_format(bad_chars)
