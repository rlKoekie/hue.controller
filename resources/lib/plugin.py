# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
import xbmcplugin
import xbmcgui
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
from urlparse import urlsplit

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
addon_name = ADDON.getAddonInfo('name')
kodilogging.config()
plugin = routing.Plugin()

from phue import Bridge, PhueRegistrationException

bridgeIP = ADDON.getSetting("bridge_ip")
try:
    # try to connect to the bridge without supplying info. 
    # This works after the first successful connect from phue by reading the data from $HOME/.python_hue
    if bridgeIP:
        b=Bridge(bridgeIP)
    else:
        b=Bridge()
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
                b=Bridge(bridgelocation)
            except PhueRegistrationException:
                xbmcgui.Dialog().ok(addon_name, 'We need to authenticate with the Hue bridge to continue.\nPlease press the button on the Hue bridge, and then close this message within 30 seconds.')
                b=Bridge(bridgelocation)
            if bridgeIP:
                answer2 = xbmcgui.Dialog().yesno(addon_name, 'remove the faulty brdige IP from the plugin setings?')
                if answer2 == True: ADDON.setSetting("bridge_ip", "")
        else:
            xbmcgui.Dialog().ok(addon_name, 'Sorry, we failed to locate the Hue bridge...')

def toggleGroup(group_name):
    if b.get_group(group_name, 'on'):
        b.set_group(group_name, 'on', False)
    else:
        b.set_group(group_name, 'on', True)

b.connect()

@plugin.route('/')
def index():
    for group in b.groups:
        addDirectoryItem(plugin.handle, plugin.url_for(show_group, group.name), ListItem(group.name), True)
    endOfDirectory(plugin.handle)

@plugin.route('/group/<group_name>')
def show_group(group_name):
    # on/off button
    addDirectoryItem(plugin.handle, plugin.url_for(toggle_group, group_name), ListItem("Toggle %s on/off" %group_name))
    # applicable scenes
    for scene in b.scenes:
        if scene.group == str(b.get_group_id_by_name(group_name)):
            addDirectoryItem(plugin.handle, plugin.url_for(scene_group, group_name, scene.scene_id), ListItem("Set scene %s" %scene.name))

    endOfDirectory(plugin.handle)

@plugin.route('/group/<group_name>/toggle')
def toggle_group(group_name):
    toggleGroup(group_name)

@plugin.route('/group/<group_name>/scene-<scene_id>')
def scene_group(group_name, scene_id):
    b.activate_scene(b.get_group_id_by_name(group_name),scene_id)

def run():
    plugin.run()
