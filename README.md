Hue Controller
==============

This is a set of kodi add-ons for basic control of Philips hue lights. It uses the phue (https://github.com/studioimaginaire/phue) python module to do the actual work.
It has basic uPnP discovery to find the hue bridge in the network, based on the code from discoverhue (https://github.com/Overboard/discoverhue).

Supported platforms: So far the add-ons have only been tested on Linux, but there is a good chance they work on OSX/Windows as well :-)

script.module.hue.tools:
------------------------
This plugin contains code for dealing with Hue lights, and is the shared repo

plugin.program.hue.controller:
------------------------------
This is the actual plugin, which currently is capable of detecting, connecting & controlling your Hue setup.
After connecting, it shows your configured Hue rooms (groups), and upon selecting one of them you can toggle the lights or apply a scene. Scenes need to be set up in some another way, e.g. through the Philips Hue app, or Hue Essentals.

script.service.hue.events:
--------------------------
This is a service plugin, needed for monitoring playback start/stop events. Currently this is not yet doing anything useful, but in the near future this will take care of selecting scenes whenever you start/stop/pause a video in Kodi.


How to install
==============
1. git clone the repo
2. cd $HOME/.kodi/addons
3. ln -s /path/to/the/repo/script.module.hue.tools
4. ln -s /path/to/the/repo/plugin.program.hue.controller
5. ln -s /path/to/the/repo/script.service.hue.events # this can be skipped for now!
6. Start Kodi, go to my add-ons, and enable the add-ons under programs and service
7. Go to the program add-ons, select Hue Controller, and follow the on-screen instructions



Simple feature requests are welcome!

