#!/usr/bin/env python

import sys
import re


listing={}

try:
    print "Begin conflict check"
    while True:
        line=sys.stdin.next()
        # print "((%s))"%line
        startpos=0
        name=''
        dupsfound=[]
        while True:
            m=re.match("\s*<(\w+)>",line[startpos:])
            if not m:
                break
            word=m.group(1)
            name+=' '+word
            startpos+=m.end()
        if startpos<=0:
            continue
        m=re.match(r'[^"]*"(.+)"',line)
        if not m:
            # shouldn't happen, but just in case
            val='???'
            print "\tParsing error: "+line
        else:
            val=m.group(1)
        if listing.has_key(name) and not re.search(r'INTENTIONAL CONFLICT', line):
            if val != listing[name]:
                print "\tExact conflict found: (%s )[%s][%s]"%(name,
                                                             listing[name], val)
            else:
                print "\t\tRedundant definition: (%s )[%s]"%(name, val)
        else:
            listing[name]=val
except StopIteration:
    print "Finish conflict check"
# NOW check for prefix conflicts:
print "Begin prefix check"
for key in listing.keys():
    # print "Key: (%s)"%key
    pref=''
    # Careful when splitting.  The key always starts with a space.
    for word in key.split(" ")[:-1]: # chop the last one; that'll always match.
        # Skip the empty first entry
        if not word:
            continue
        pref+=" "+word
        # print "checking (%s)"%pref
        if listing.has_key(pref):
            print "\tPrefix conflict found: " \
                "(%s )[%s] vs (%s )[%s]"%(pref, listing[pref],
                                          key, listing[key])
print "Finish prefix check"
