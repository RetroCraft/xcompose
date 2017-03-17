#!/usr/bin/env python3

import unicodedata
import emoji

for e in emoji.unicode_codes.UNICODE_EMOJI:
    try:
        print('#Mk :                 : "{0}" U{1} # {2}'.format(e, format(ord(e), 'x').upper(), unicodedata.name(e)))
    except Exception as e:
        continue
