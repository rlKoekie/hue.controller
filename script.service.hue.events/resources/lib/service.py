# -*- coding: utf-8 -*-

from resources.lib import kodiutils
from resources.lib import kodilogging
import logging
import time
import xbmc
import xbmcaddon
import json


import huecontroller


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
myloglevel=xbmc.LOGDEBUG

HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')

debug = HueControllerADDON.getSetting('debug')
if debug:
    myloglevel = xbmc.LOGNOTICE

bridge=huecontroller.getBridge()

def changeScene(setting_name):
    setting = HueControllerADDON.getSetting(setting_name)
    if setting:
        try:
            room, scene = setting.split('//')
        except:
            xbmc.log("Failed to get room/scene from %s settings, possibly incorrectly formatted? setting=%s" %(setting_name, setting), level=myloglevel)
        else:
            xbmc.log("Applying scene %s to room %s" %(scene, room), level=myloglevel)
            huecontroller.runScene(bridge, room, scene)

class XBMCPlayer( xbmc.Player ):
    def __init__( self, *args ):
        # super(XBMCPlayer, self).__init__()
        self.lastplayingtype = ''

    def onPlayBackStarted( self ):
        count = 0
        self.lastplayingtype = 'Unknown'
        # We loop here because if playback takes some time to start, then the isPlayingAudio/Video functions will return 'false'
        while count < 15 and self.lastplayingtype == 'Unknown':
            if self.isPlayingAudio():
                self.lastplayingtype = 'Audio'
                xbmc.log( "Playback started, Audio type detected", level=myloglevel )
                if HueControllerADDON.getSetting('video_only') == "true": return
            elif self.isPlayingVideo():
                self.lastplayingtype = 'Video'
                xbmc.log( "Playback started, Video type detected", level=myloglevel )
            else:
                self.lastplayingtype = 'Unknown'
                xbmc.log( "Playback started, but type Unknown. Sleeping and then trying again. Count=%s" %(count), level=myloglevel )
                xbmc.sleep(1000)
        changeScene("playback_start")

    def onPlayBackPaused( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Paused", level=myloglevel )
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Paused", level=myloglevel )
        changeScene("playback_paused")

    def onPlayBackResumed( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Resumed", level=myloglevel )
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Resumed", level=myloglevel )
        changeScene("playback_start")

    def onPlayBackEnded( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Ended", level=myloglevel )
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Ended", level=myloglevel )
        changeScene("playback_end")

    def onPlayBackStopped( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Stopped", level=myloglevel )
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Stopped", level=myloglevel )
        changeScene("playback_end")


def run():
    monitor = xbmc.Monitor()
    
    player = XBMCPlayer()
    
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        # xbmc.log("hello from service.py! %s lastplayingtype= %s" %( time.time(), player.lastplayingtype), level=myloglevel)
        xbmc.log("video_only setting value: %s" %(HueControllerADDON.getSetting("video_only")), level=myloglevel)
        pass
