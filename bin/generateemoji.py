#!/usr/bin/env python3

import unicodedata
import emoji
import re
from itertools import chain

for e, a in chain(emoji.UNICODE_EMOJI.items(), emoji.UNICODE_EMOJI_ALIAS.items()):
    try:
        a = a.replace('_', '')
        keys = [*a];
        comment = ""
        print(comment, 'Mk {0} : "{1}" U{2} # {3}'.format(' '.join(keys), e, format(ord(e), 'x').upper(), unicodedata.name(e)))
    except Exception as e:
        continue

for e, a in emoji.UNICODE_EMOJI_ALIAS.items():
    try:
        if (re.search('skin_tone', a) or re.search('[0-9]', a)):
            continue
        a = a.replace('_', '').replace(':', '')
        keys = [*a];
        if len(keys) <= 2 or len(keys) >= 7:
            comment = "#"
        else:
            comment = ""
        print(comment, 'Mk Mk {0} : "{1}" U{2} # {3}'.format(' '.join(keys), e, format(ord(e), 'x').upper(), unicodedata.name(e)))
    except Exception as e:
        continue
