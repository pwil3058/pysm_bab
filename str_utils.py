#  Copyright 2017 Peter Williams <pwil3058@gmail.com>
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License only.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to:
#  The Free Software Foundation, Inc., 51 Franklin Street,
#  Fifth Floor, Boston, MA 02110-1301 USA

"""Utility functions for working with strings
"""

import string
import bisect

__all__ = []
__author__ = "Peter Williams <pwil3058@gmail.com>"

# Allow possessives and hyphenated words
DELIMITERS = string.whitespace + string.punctuation.replace("'", '').replace('-', '')

def find_start_last_word(text, before=None):
    index = before if before is not None and before < len(text) else len(text)
    while index > 0:
        index -= 1
        if text[index] in DELIMITERS:
            return index + 1
    return index

def replace_last_word(text, new_word, before=None):
    """
    Return a new string with the last word replaced by the new word.
    """
    index = find_start_last_word(text=text, before=before)
    tail = text[before:] if before is not None else ''
    return text[:index] + new_word + tail

def extract_words(text):
    words = []
    index = 0
    inword = False
    start = None
    while index < len(text):
        if inword:
            if text[index] in DELIMITERS:
                words.append(text[start:index])
                start = None
                inword = False
        elif text[index] not in DELIMITERS:
            inword = True
            start = index
        index += 1
    if start is not None:
        words.append(text[start:])
    return words

def contains(somelist, arg):
    index = bisect.bisect_left(somelist, arg)
    return index != len(somelist) and somelist[index] == arg
