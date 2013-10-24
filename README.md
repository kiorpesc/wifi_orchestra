wifi_orchestra
==============

A python script that generates music from characteristics of nearby wifi networks.

This was intended to be used on a Raspberry Pi while wandering around, seeing how the music evolves as new networks are encountered and old ones lost.

Currently this creates a very basic sort of drone in C maj, with a random melody that sort of wanders through the notes of the C maj scale.
...Not very much variation.  I hope to change this.


Normal, secured networks create the drone.
Unsecured networks create the melody/melodies.
Volume is determined by signal strength.
Voice (instrument) is determined by the wifi channel.

This is all built in python using rtmidi to send midi commands to a timidity server.

It sounds pretty choppy unless modifications are made to the timidy config files in /etc/timidity.

It's still not all that good.

Next step is to look into ChucK.
