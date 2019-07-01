Hue Controller
==============

This is a set of kodi add-ons for basic control of Philips hue lights. It uses the phue (https://github.com/studioimaginaire/phue) python module to communicate with the Hue bridge.
It has basic uPnP discovery to find the hue bridge in the network, based on the code from discoverhue (https://github.com/Overboard/discoverhue).

Supported platforms: I've tested the add-on on Linux, Windows and Android, and it probably works on MacOS as well :-)

plugin.program.hue.controller:
------------------------------
This is the actual plugin. It detects & connects to your Hue bridge, then shows your configured rooms (groups), and upon selecting one of them you can toggle the lights on/off or apply a scene. The scenes also have context menu options for selecting them as a Playback action!
Scenes are read from your Hue configuration, and cannot be configured from Kodi (That would be too complex and very remote-unfriendly). Just configure your scenes in some another way, e.g. through the Philips Hue app, or a third party app such as Hue Essentals.
The settings of this add-on also control the behaviour of the service add-on. It currently has the following options:
- Bridge IP: You can enter the ip address of your Hue bridge in here if there are problems connecting to it. In most cases this can just stay empty!
- Playback start/paused/stopped event actions: The service script add-on reads these values and applies them on the corresponding playback change. They take the format of "room//scene" (without the quotes), and are case sensitive. You could manually enter them, but it is easier to open the plugin, select a room, open the context menu on a scene, and then select the desired action.
- Video only: If this option is enabled, the add-on will not change the lighting configuration when playing audio files. If it is disabled, the add-on will respond to all media types.
- Change only if lights are on: If enabled the add-on will only change your room lighting on playback start/paused/stopped IF the lights were ON when playback started. When disabled it will also change the room lighting if the lights were originally off.

script.service.hue.events:
--------------------------
This is a service script add-on. It monitors playback start/pauze/stop events, and can act on them. If there are scenes configured for the playback started, playback paused and/or playback stopped events (see plugin.program.hue.controller), then the service script will set the room lighting to these scenes on the corresponding playback change.

script.module.hue.tools:
------------------------
This plugin is the shared code base for the service script and the program plugin. It contains code for dealing with Hue lights, the phue (https://github.com/studioimaginaire/phue) python module, and a stripped-down version of discoverhue (https://github.com/Overboard/discoverhue).

How to install
==============
* git clone the repo, or download the zip file
* Open your kodi add-ons folder, this is $HOME/.kodi/addons on linux
* Copy or symlink the following three folders into the add-ons folder: script.module.hue.tools , plugin.program.hue.controller , script.service.hue.events
* Start Kodi, go to my add-ons, and enable the add-ons under programs and service
* Go to the program add-ons, select Hue Controller, and follow the on-screen instructions


Simple feature requests are welcome!


TODO at some point:
-------------------
- change multiple rooms on playback events
- maybe support multiple hue bridges during detection
