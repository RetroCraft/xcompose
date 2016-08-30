#!/usr/bin/env python3

from unicodedata import name
import re
import sys

print("Begin Unicode check")
for line in sys.stdin:
  line=line.strip()
  if not line or line[0]=="#":
    continue
  match=re.match(r'\s*(.*):\s*"(.*?)"\s*(\S*)\s*(#.*)?', line)
  if not match:
    continue
  if re.search("MULTIPLE CHARS", line):
    continue
  (keystrokes, char, num, comments)=match.groups()
  nummatch=re.match(r'U([0-9A-Fa-f]+)', num)
  if not nummatch:
    wordmatch=re.match(r'([0-9A-Za-z]+)', num)
    if not wordmatch:
        print("\tMissing Unicode number/descriptor: {0}".format(line))
    continue
  x=int(nummatch.group(1),0x10)
  c=chr(x)
  try:
    if c != char:
      print(line)
      print("\t\tLine's char: {0} ({1})".format(char, name(char)))
      print("\t\tLine's number: {0:X}".format(x))
      print("\t\tChar gives number: {0:X}".format(ord(char)))
      print("\t\tNumber gives character: {0} ({1})".format(c, name(c)))
  except Exception as e:
    print("{0}\n\t{1}".format(line, e))
print("Finish Unicode check")
