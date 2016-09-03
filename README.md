All files in this distribution use UTF‐8 pointlessly.  Read them in a
font with good Unicode coverage — say, DejaVu Sans Mono or GNU unifont
(xfonts-unifont).

Introduction
============

Unicode has lots of cool characters.  I mean lots and lots of cool
characters.  Enough characters to annoy all your friends with useless
charactery.  Your keyboard doesn’t have nearly enough keys to input
all them.

In X — the GUI system used in Linux, BSD, Solaris &c. — there are a
number of different ways to input these extra characters.  Some are
suitable for occasional use: search for the character online or in a
character map program by name, then copy and paste it or enter its
number or name.  Some are suitable for frequent use: use a “3rd Level
Shift” (typically AltGr), dead keys, or input methods.  XCompose is an
intermediate solution: each character is typed using a mnemonic
combination of a few keystrokes.  It’s not fast enough to use in every
word, but it’s fairly easy to remember (or rediscover) for characters
you might use once a day or once a fortnight, and much less annoying
than having to search online that often.

Most Compose sequences begin with the Compose key, also known as
Multi_key (typically assigned to the Windows Menu key or equivalent).
Dead keys (where you press an accent key, then a letter, and an
accented letter is typed) are implemented with Compose too.  X comes
with many builtin mappings described in
/usr/share/X11/locale/*/Compose, and you can add your own in
~/.XCompose.  But what to add, and how?

Pointless‐XCompose provides a Compose file with thousands of extra
Compose mappings, compatible with the standard X US English Compose
file.  (I intend to make it compatible with *all* standard Compose
files.)


What’s included
===============

I also included a few other potentially interesting Compose‐related
stuff, such as a selection of standard X mappings, a script to
generate deadkey variants of Compose files, &c.

 * README.md:                 This.
 * src/*.xcompose:            All the abbreviations
 * bin/build.py:              Make an xcompose-usable file
 * doc/mnemonics.md:          Abbreviation starts
 * doc/license.txt:           “Public domain.”


Installation
============

1. Copy or git-clone this directory.

2. Run bin/build.py to create an xcompose file. 

3. Symlink xcompose to ~/.XCompose:

    ln -s /path/to/pointless-xcompose/xcompose ~/.XCompose


4. Check your Compose key setup: the command

    setxkbmap -print

   should mention “compose” in a line starting `xkb_symbols`, for example:

    xkb_symbols   { include "pc+us(altgr-intl)+gb:2+us:3+inet(evdev)+altwin(swap_alt_win)+level3(rwin_switch)+capslock(ctrl_modifier)+compose(ralt)"	};

   (near the end of the line; here it says Compose is the right Alt
   key).  If no Compose key is set up, you’ll need to configure one.
   Sadly, this works differently in different desktops, so I can’t
   give standard instructions.

   Once you have a Compose key configured, try it out: type “Compose +
   -” (i.e., the Compose key, then the plus key, then the minus key)
   and you should get “±”.

5. Restart your apps (and perhaps X the first time) — XCompose
   settings only apply for new windows.

6. In GNOME (or GTK applications, if you know what that means),
   XCompose configuration unfortunately won’t work by default; GTK
   defines its own static, compile‐time, non-configurable compose
   mechanism which overrides X.

   A workaround is to use the uim input method.  Sadly, how to install
   and configure it varies from system to system.  The package is
   probably called uim.  On Debian or Ubuntu, use im-config; on Fedora
   or RedHat, use ImChooser.


Usage
=====

Read the included xcompose files to see what’s included.  The system’s
mappings are in /usr/share/X11/locale/$LANG/Compose (if there’s no
such directory for your locale, look in
/usr/share/X11/locale/locale.dir; for example my locale, en_GB.UTF-8
is listed there under en_US.UTF-8):

  en_US.UTF-8/XLC_LOCALE                  en_GB.UTF-8


Adding your own Compose sequences
=================================

One Compose sequence cannot be a prefix of another.  Suppose you have
this sequence:

 * Compose . . =      → ·
 * Compose . . . =    → …

Now when you type «Compose . .», X won’t print anything because it’s
waiting for «Compose . . .» (IMHO it should print · and then change it
to … should you type another period, but I digress).  That means you
probably don’t want to make a Compose shortcut for U2A94 GREATER-THAN
ABOVE SLANTED EQUAL ABOVE LESS-THAN ABOVE SLANTED EQUAL (⪔).

All the mappings here have been compared against X.org 1.6.2’s en_US
Compose file for conflicts.  Several of my entries are present in X’s
Compose as another sequence, but I prefer one that’s more mnemonic.
The few entries that replace X mappings are marked “INTENTIONAL
CONFLICT”.

Conventions:

 * Follow patterns in system Compose files. For example:

 * Termination convention (copied from X):
    * A repeated character: Compose v v → ✓
    * Where that would conflict, a period:
       * Compose - .      → − (true hypen)
       * Compose - - .    → – (en‐bar)
       * Compose - - -    → — (em‐bar)
         (Side note: the difference between the above three characters is
         small in monospaced fonts, but large in proportionals).

 * Where we conflict with the system files, do so only for characters
   that have multiple definitions, and where multiple sequences follow
   the same pattern, only conflict with one pattern, so that users can
   use the remaining pattern(s) without being bothered with
   exceptions.

 * Avoid spelling out names (rather, use an input method that allows
   spelling out).
