Auto Avrdude
------------

An extremely rudimentary python wrapper around the AVRDUDE executable.
Using Popen, so it involves a lot of ugly stream parsing.

This can be used to automate the flashing of AVR microprocessors.  For
example, a script to automatically detect when a powered host has been
connected to an AVRISP, and to automatically write to fuses and flash
memory.
