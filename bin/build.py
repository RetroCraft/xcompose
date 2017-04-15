#!/usr/bin/env python3

import re, glob, os, unicodedata, itertools, argparse
from keycodes import keycodes
from subprocess import call

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--locale', help='locale to base xcompose conflicts on (default en_US.UTF-8)',
                    default='en_US.UTF-8')
parser.add_argument('-o', '--output', help='output file to build to (default xcompose)',
                    default='xcompose')
args = parser.parse_args()

print(bcolors.UNDERLINE + bcolors.HEADER + "Begin build" + bcolors.ENDC)
out = open(args.output, 'w+')
out.write('include "/usr/share/X11/locale/' + args.locale + '/Compose"\n')
os.chdir("src")
for file in glob.glob("*.xcompose"):
    print("Building file", file)
    with open(file) as f:
        for line in f.readlines():
            # If line is nonexistant, comment, or blank, skip
            if not line or line[0] == '#' or not line.strip():
                continue
            # If line is following new parsing rules
            if line[0] != '%':
                out_line = ''
                m1 = re.match(r'\s*(.+)\s*:\s*(.*)', line)
                if not m1 or not m1.group(1) or not m1.group(2):
                    print(bcolors.FAIL + 'Error parsing line', line.strip() + bcolors.ENDC)
                    continue
                m = re.match(r'"?(\S+)"?\s*(\S+)?\s*#?(.*)?', m1.group(2))
                if not m or not m.group(1):
                    print(bcolors.FAIL + 'Error parsing value', line.strip() + bcolors.ENDC)
                    continue
                keys = m1.group(1).strip().split(' ')
                # if (len(keys) > 14):
                #     continue
                # if (len(keys) > 9):
                #     print(bcolors.WARNING + 'Line too long', keys, bcolors.ENDC)
                val = m.group(1).strip('"')
                if not m.group(2):
                    code = ''
                else:
                    code = m.group(2)
                if not m.group(3):
                    comment = ''
                else:
                    comment = m.group(3).strip()
                # Generate keys
                for key in keys:
                    if key in keycodes:
                        out_line += '<' + keycodes[key] + '> '
                    else:
                        out_line += '<' + key + '> '
                # If using Unicode code
                m = re.match(r'U([A-F0-9]+)', code)
                fail = ''
                if m and m.group(1) and len(val) == 1:
                    if m.group(1) != format(ord(val), 'x').upper():
                        fail = 'Unicode'
                    desc = re.match(r'([^(*]*).*', comment)
                    if desc.group(1).strip() != unicodedata.name(val) and not re.search('⋮', desc.group(0)):
                        fail = 'Description'
                    if fail != '':
                        print(bcolors.FAIL + 'Unicode parse error: ' + fail + '\n' +
                              '\tShould be: "' + val + '" U' +
                              format(ord(val), 'x').upper() + ' # ' +
                              unicodedata.name(val) + '\n' +
                              '\tGot      : "' + val + '" U' +
                              m.group(1) + ' # ' +
                              desc.group(1) + bcolors.ENDC)
                        continue
                out_line += ': "' + val + '" '
                out_line += code + ' '
                out_line += '# ' + comment
                out_line += '\n'
                out.write(out_line)
            else:
                out.write(line)
print(bcolors.UNDERLINE + bcolors.HEADER + "Finish build" + bcolors.ENDC)

locale = open('/usr/share/X11/locale/' + args.locale + '/Compose', 'r')
print(bcolors.UNDERLINE + bcolors.HEADER + "Begin conflict check" + bcolors.ENDC)
os.chdir("..")
out.seek(0)
listing = {}
conflict = False
for line in itertools.chain(locale.readlines(), out.readlines()):
    startpos = 0
    name = ''
    dupsfound = []
    while True:
        m = re.match(r'\s*<(\w+)>', line[startpos:])
        if not m:
            break
        word = m.group(1)
        name += ' ' + word
        startpos += m.end()
    if startpos <= 0:
        continue
    m = re.match(r'[^"]*"(.+)"',line)
    if not m:
        # shouldn't happen, but just in case
        val = '???'
        print(bcolors.FAIL + "Parsing error:", line, bcolors.ENDC)
    else:
        val = m.group(1)
    if name in listing and not re.search('INTENTIONAL CONFLICT', line):
        conflict = True
        if val != listing[name]:
            print(bcolors.FAIL + "Exact conflict found: ("+name+" )["+listing[name]+"]["+val+"]" + bcolors.ENDC)
        # else:
        #     print(bcolors.WARNING + "Redundant definition: ("+name+" )["+val+"]" + bcolors.ENDC)
    else:
        listing[name] = val
if not conflict:
    print(bcolors.OKBLUE + "No conflicts found" + bcolors.ENDC)
print(bcolors.UNDERLINE + bcolors.HEADER + "End conflict check" + bcolors.ENDC)

print(bcolors.UNDERLINE + bcolors.HEADER + "Begin prefix check" + bcolors.ENDC)
conflict = False
for key in listing.keys():
    pref=''
    # Careful when splitting.  The key always starts with a space.
    for word in key.split(" ")[:-1]: # chop the last one; that'll always match.
        # Skip the empty first entry
        if not word:
            continue
        pref+=" "+word
        if pref in listing:
            conflict = True
            print(bcolors.FAIL + "Prefix conflict found: ("+pref+")["+listing[pref]+"] vs ("+key+")["+listing[key]+"]", bcolors.ENDC)
if not conflict:
    print(bcolors.OKBLUE + "No prefix conflicts found" + bcolors.ENDC)
print(bcolors.UNDERLINE + bcolors.HEADER + "End prefix check" + bcolors.ENDC)

num_lines = sum(1 for line in open(args.output)) - 1

print(bcolors.OKGREEN + "Final xcompose file has" + bcolors.BOLD, num_lines, "definitions" + bcolors.ENDC)

call('sort -u xcompose | tee xcompose | wc -l', shell=True)
