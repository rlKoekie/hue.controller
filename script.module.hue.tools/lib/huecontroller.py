# -*- coding: utf-8 -*-

import logging
import xbmcaddon
import xbmcplugin
import xbmcgui
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
from urlparse import urlsplit
from phue import Bridge, PhueRegistrationException

ADDON = xbmcaddon.Addon()
HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')

logger = logging.getLogger(ADDON.getAddonInfo('id'))
addon_name = ADDON.getAddonInfo('name')
kodilogging.config()


def getBridge():
    bridgeIP = HueControllerADDON.getSetting("bridge_ip")
    myBridge=None
    try:
        # try to connect to the bridge without supplying info. 
        # This works after the first successful connect from phue by reading the data from $HOME/.python_hue
        if bridgeIP:
            myBridge=Bridge(bridgeIP)
        else:
            myBridge=Bridge()
    except:
        # if it fails, we can try a upnp scan for the bridge
        if bridgeIP:
            messagetext = 'Failed to connect to the bridge on IP %s.\nWould you like to autodiscover the bridge with uPnP?' %(bridgeIP)
        else:
            messagetext = 'Failed to connect to the bridge.\nWould you like to autodiscover the bridge with uPnP?'
        answer = xbmcgui.Dialog().yesno(addon_name, messagetext)
        if answer == True:
            from discoverhue import discoverhue
            bridges = discoverhue.via_upnp()
            if bridges:
                # TODO: present a list to the user if we find more than one bridge!
                # xbmcgui.Dialog().ok(addon_name, 'found the following bridges: %s' %(str(bridges)))
                bridgelocation=urlsplit(bridges[0].location).netloc
                try:
                    myBridge=Bridge(bridgelocation)
                except PhueRegistrationException:
                    xbmcgui.Dialog().ok(addon_name, 'We need to authenticate with the Hue bridge to continue.\nPlease press the button on the Hue bridge, and then close this message within 30 seconds.')
                    myBridge=Bridge(bridgelocation)
                if bridgeIP:
                    answer2 = xbmcgui.Dialog().yesno(addon_name, 'remove the faulty bridge IP from the plugin setings?')
                    if answer2 == True: HueControllerADDON.setSetting("bridge_ip", "")
            else:
                xbmcgui.Dialog().ok(addon_name, 'Sorry, we failed to locate the Hue bridge...')
    return myBridge

def toggleGroup(bridge, group_name):
    if bridge.get_group(group_name, 'on'):
        bridge.set_group(group_name, 'on', False)
    else:
        bridge.set_group(group_name, 'on', True)

def lightsAreOn(bridge, group_name):
    return bridge.get_group(group_name, 'on')

def turnLightsOff(bridge, group_name):
    bridge.set_group(group_name, 'on', False)

def turnLightsOn(bridge, group_name):
    bridge.set_group(group_name, 'on', True)

# inconvinient way of setting a scene, needs the group_id and scene_id
def applyScene(bridge, group_name, scene_id):
    bridge.activate_scene(bridge.get_group_id_by_name(group_name),scene_id)

# easy way of setting a scene, just uses human readable names
def runScene(bridge, group_name, scene_name, transition_time=4):
    # note: transition_time does not seem to work in phue
    bridge.run_scene(group_name, scene_name, transition_time)