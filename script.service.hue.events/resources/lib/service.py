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

HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')

bridge=huecontroller.getBridge()

class XBMCPlayer( xbmc.Player ):
    def __init__( self, *args ):
        # super(XBMCPlayer, self).__init__()
        self.lastplayingtype = ''


    def onPlayBackStarted( self ):
        # TODO: make a while loop with shorter sleep, we need this if playback startup takes a long time
        # examples: video playback takes slightly longer to start, so that needs a small amount of sleep
        # can probably take a lot longer with disk spinup time. So just while loop with max count 15 or something like that if we keep getting Unknown type
        xbmc.sleep(1000)
        if self.isPlayingAudio():
            self.lastplayingtype = 'Audio'
            xbmc.log( "LED Status: Audio Playback Started, LED ON", level=xbmc.LOGNOTICE )
            return
        elif self.isPlayingVideo():
            self.lastplayingtype = 'Video'
            xbmc.log( "LED Status: Video Playback Started, LED ON", level=xbmc.LOGNOTICE )
            setting = HueControllerADDON.getSetting("playback_start")
        else:
            self.lastplayingtype = 'Unknown'
            xbmc.log( "LED Status: Unknown Playback Started, LED ON", level=xbmc.LOGNOTICE )
            return
        if setting:
            try:
                room, scene = setting.split('//')
            except:
                xbmc.log("hue.events service: Failed to get room/scene from playback_start settings, possibly incorrectly formatted: %s" %(setting), level=xbmc.LOGNOTICE)
            else:
                huecontroller.runScene(bridge, room, scene)

    def onPlayBackPaused( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Paused", level=xbmc.LOGNOTICE )
            return
        xbmc.log( "LED Status: Playback Paused, LED OFF", level=xbmc.LOGNOTICE )
        setting = HueControllerADDON.getSetting("playback_paused")
        if setting:
            try:
                room, scene = setting.split('//')
            except:
                xbmc.log("hue.events service: Failed to get room/scene from playback_paused settings, possibly incorrectly formatted: %s" %(setting), level=xbmc.LOGNOTICE)
            else:
                huecontroller.runScene(bridge, room, scene)

    def onPlayBackResumed( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Resumed", level=xbmc.LOGNOTICE )
            return
        xbmc.log( "LED Status: Playback Resumed, LED OFF", level=xbmc.LOGNOTICE )
        setting = HueControllerADDON.getSetting("playback_start")
        if setting:
            try:
                room, scene = setting.split('//')
            except:
                xbmc.log("hue.events service: Failed to get room/scene from playback_start settings, possibly incorrectly formatted: %s" %(setting), level=xbmc.LOGNOTICE)
            else:
                huecontroller.runScene(bridge, room, scene)

    def onPlayBackEnded( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Ended", level=xbmc.LOGNOTICE )
            return
        xbmc.log( "LED Status: Playback Ended, LED OFF", level=xbmc.LOGNOTICE )
        setting = HueControllerADDON.getSetting("playback_end")
        if setting:
            try:
                room, scene = setting.split('//')
            except:
                xbmc.log("hue.events service: Failed to get room/scene from playback_end settings, possibly incorrectly formatted: %s" %(setting), level=xbmc.LOGNOTICE)
            else:
                huecontroller.runScene(bridge, room, scene)

    def onPlayBackStopped( self ):
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Stopped", level=xbmc.LOGNOTICE )
            return
        xbmc.log( "LED Status: Playback Stopped, LED OFF", level=xbmc.LOGNOTICE )
        setting = HueControllerADDON.getSetting("playback_end")
        if setting:
            try:
                room, scene = setting.split('//')
            except:
                xbmc.log("hue.events service: Failed to get room/scene from playback_end settings, possibly incorrectly formatted: %s" %(setting), level=xbmc.LOGNOTICE)
            else:
                huecontroller.runScene(bridge, room, scene)




def run():
    # monitor = XBMCMonitor()
    monitor = xbmc.Monitor()
    
    player = XBMCPlayer()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("hello from service.py! %s lastplayingtype= %s" %( time.time(), player.lastplayingtype), level=xbmc.LOGINFO)
        
