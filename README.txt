
=======
UXB Gtk
=======

An implementation of the well-known 'Mines' game in Python, using the Gtk+ 
graphics library. This is derived from the author's 'Danger UXB' game, 
but includes some additional features (notably a periodic boundary option) that
were developed for this version. (Periodic boundaries have now been back-ported 
to 'Danger UXB').

There are no instructions on how to play. If it isn't self-evident from the UI
then I have failed. Please email me (see below) to tell me how to make it 
better.

There is no written language in the game, so there is no translation.

There are also no timers, clocks, or high-score charts. That way, every time you 
finish is an achievement. The emphasis is on the fun of playing the game rather 
than 'winning'.

The most recent change (v1.1) introduces saving and restoring the game 
configuration (but not the game itself) between sessions.

Installation
============

For Version 1.1 the only supported platform is Linux, although *in theory* this
game should play equally well on Windows or Mac. I would like to hear from
anyone who can help with porting.

System Requirements:
--------------------

    *   Python 3
    *   Gtk
    *   Python Gtk+ bindings 3.4.2

Installation (Linux):
---------------------

    1.  Unzip the tar.gz somewhere.

    2.  In a console window navigate to the UXBgtk-1.1 directory and run the
        following command as root (on Ubuntu/Debian use sudo):

            ``[sudo] python3 setup.py install``

    3.  On Ubuntu a desktop launcher is installed, which you should be able to
        find in the Dash and drag to the launcher bar.

Design Notes and Plans
======================

It took me a while to get to grips with Gtk+, but here it is.

This version of the game includes a periodic boundary option. Hopefully it is 
fairly obvious from the button icons, but in any case some tinkering as you 
play should help you work out what does what. Certainly, if you are feeling a 
little jaded with the 'normal' game, you will find periodic boundary conditions 
add a little extra challenge...

I found a bug in the introspected bindings, where the 
``Gtk.Grid.get_child_at()`` method is not mapped. I am assured this has been 
fixed in later versions of the bindings, and that the python3-gi package in 
Ubuntu 12.10 will include the fix. Meanwhile, a workaround has been 
implemented. It is planned to remove the workaround in later versions. 

Please note, if you wish to use the workaround elsewhere, many of the methods 
needed for a full workaround have not been implemented in my fix.

Author:
=======

Bob Bowles <bobjohnbowles@gmail.com>

