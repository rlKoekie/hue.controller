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

import huecontroller

bridge = huecontroller.getBridge()

bridge.connect()


@plugin.route('/')
def index():
    for group in bridge.groups:
        addDirectoryItem(plugin.handle, plugin.url_for(show_group, group.name), ListItem(group.name), True)
    endOfDirectory(plugin.handle)

@plugin.route('/group/<group_name>')
def show_group(group_name):
    # on/off button
    addDirectoryItem(plugin.handle, plugin.url_for(toggle_group, group_name), ListItem("Toggle %s on/off" %group_name))
    # applicable scenes
    for scene in bridge.scenes:
        if scene.group == str(bridge.get_group_id_by_name(group_name)):
            addDirectoryItem(plugin.handle, plugin.url_for(scene_group, group_name, scene.name), ListItem("Set scene %s" %scene.name))

    endOfDirectory(plugin.handle)

@plugin.route('/group/<group_name>/toggle')
def toggle_group(group_name):
    huecontroller.toggleGroup(bridge, group_name)

@plugin.route('/group/<group_name>/scene-<scene_name>')
def scene_group(group_name, scene_name):
    # transition_time = ADDON.getSetting("transition_time") # seems not to work in phue
    huecontroller.runScene(bridge, group_name, scene_name)

def run():
    plugin.run()

