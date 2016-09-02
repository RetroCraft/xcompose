#!/usr/bin/env python3

import unicodedata
from itertools import chain

for i in chain(range(0x1f600, 0x1f650), range(0x1f680, 0x1f700), range(0x1f900, 0x1fa00)):
    try:
        print('#<Multi_key> <colon>                 : "{0}" U{1} # {2}'.format(chr(i), format(i, 'x').upper(), unicodedata.name(chr(i))))
    except Exception as e:
        continue
