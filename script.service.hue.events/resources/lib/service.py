# -*- coding: utf-8 -*-

from resources.lib import kodiutils
from resources.lib import kodilogging
import logging
import time
import xbmc
import xbmcaddon
import json
import datetime


import huecontroller


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
myloglevel=xbmc.LOGDEBUG


bridge=huecontroller.getBridge()


class XBMCPlayer( xbmc.Player ):
    def __init__( self, *args ):
        # super(XBMCPlayer, self).__init__()
        self.lastplayingtype = ''
        self.lightswereon = True
        self.loglevel = xbmc.LOGDEBUG

    def changeScene(self, setting_name):
        # we have to get the HueControllerADDON every time we need a settings value, otherwise we don't see changes made to the settings
        HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
        setting = HueControllerADDON.getSetting(setting_name)
        if setting:
            try:
                room, scene = setting.split('//')
            except:
                xbmc.log("Failed to get room//scene from %s setting, possibly incorrectly formatted? setting=%s" %(setting_name, setting), level=self.loglevel)
            else:
                xbmc.log("Applying scene %s to room %s" %(scene, room), level=self.loglevel)
                huecontroller.runScene(bridge, room, scene)

    def onPlayBackStarted( self ):
        HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
        if HueControllerADDON.getSetting('excl_time_on') == "true":
            excltimestart = HueControllerADDON.getSetting('excl_time_start')
            excltimeend = HueControllerADDON.getSetting('excl_time_end')
            # the times from settings are type string and formatted "03:00"   !
            try:
                # convert it to integers
                exclstartlist = excltimestart.split(":")
                exclendlist = excltimeend.split(":")
                excltimestartint = int(exclstartlist[0])*100 + int(exclstartlist[1])
                excltimeendint = int(exclendlist[0])*100 + int(exclendlist[1])
            except Exception as err:
                xbmc.log("Failed to split and convert the times to an integer value.\n excl_time_start: %s\n excl_time_end: %s.\n Error message: %s" %(excltimestart,excltimeend, err), level=xbmc.LOGNOTICE)
            else:
                # get the current time
                currenttime = datetime.datetime.now().hour * 100 + datetime.datetime.now().minute
                if currenttime >= excltimestartint and currenttime < excltimeendint:
                    xbmc.log("We are inside the excluded time slot. Not chaning scenes. currenttime: %s, excltimestartint: %s, excltimeendint: %s" %(currenttime, excltimestartint, excltimeendint), level=self.loglevel)
                    self.lightswereon = False
                    return
        if HueControllerADDON.getSetting('lights_already_on') == "true":
            roomscenestring = HueControllerADDON.getSetting('playback_start')
            if roomscenestring:
                try:
                    room, scene = roomscenestring.split('//')
                except:
                    xbmc.log("Failed to get room from playback_start setting, possibly incorrectly formatted? roomscenestring=%s" %(roomscenestring), level=self.loglevel)
                else:
                    roomIsOn = huecontroller.lightsAreOn(bridge, room)
                    xbmc.log('Lights in room %s are on? %s' %(room, roomIsOn), level=self.loglevel)
                    self.lightswereon = roomIsOn
        if self.lightswereon == False:
            xbmc.log("Lights were off when playback started, or we were in the excluded time slot! Not changing scenes.", level=self.loglevel)
            return
        count = 0
        self.lastplayingtype = 'Unknown'
        # We loop here because if playback takes some time to start, then the isPlayingAudio/Video functions will return 'false'
        while count < 15 and self.lastplayingtype == 'Unknown':
            if self.isPlayingAudio():
                self.lastplayingtype = 'Audio'
                xbmc.log( "Playback started, Audio type detected", level=self.loglevel )
                HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
                if HueControllerADDON.getSetting('video_only') == "true": return
            elif self.isPlayingVideo():
                self.lastplayingtype = 'Video'
                xbmc.log( "Playback started, Video type detected", level=self.loglevel )
            else:
                self.lastplayingtype = 'Unknown'
                xbmc.log( "Playback started, but type Unknown. Sleeping and then trying again. Count=%s" %(count), level=self.loglevel )
                xbmc.sleep(1000)
        self.changeScene("playback_start")

    def onPlayBackPaused( self ):
        if self.lightswereon == False:
            xbmc.log("Lights were off when playback started! Not changing scenes.", level=self.loglevel)
            return
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Paused", level=self.loglevel )
            HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Paused", level=self.loglevel )
        self.changeScene("playback_paused")

    def onPlayBackResumed( self ):
        if self.lightswereon == False:
            xbmc.log("Lights were off when playback started! Not changing scenes.", level=self.loglevel)
            return
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Resumed", level=self.loglevel )
            HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Resumed", level=self.loglevel )
        self.changeScene("playback_start")

    def onPlayBackEnded( self ):
        if self.lightswereon == False:
            xbmc.log("Lights were off when playback started! Not changing scenes.", level=self.loglevel)
            return
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Ended", level=self.loglevel )
            HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Ended", level=self.loglevel )
        self.changeScene("playback_end")

    def onPlayBackStopped( self ):
        if self.lightswereon == False:
            xbmc.log("Lights were off when playback started! Not changing scenes.", level=self.loglevel)
            return
        if self.lastplayingtype == 'Audio':
            xbmc.log( "Audio Playback Stopped", level=self.loglevel )
            HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
            if HueControllerADDON.getSetting('video_only') == "true": return
        xbmc.log( "Playback Stopped", level=self.loglevel )
        self.changeScene("playback_end")


def run():
    monitor = xbmc.Monitor()
    
    player = XBMCPlayer()
    
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
        debug = HueControllerADDON.getSetting('debug')
        if debug == "true":
            player.loglevel = xbmc.LOGNOTICE
        else:
            player.loglevel = xbmc.LOGDEBUG
        # xbmc.log("%s lastplayingtype= %s lightswereon= %s loglevel=%s" %( time.time(), player.lastplayingtype, player.lightswereon, player.loglevel), level=xbmc.LOGNOTICE)
        # HueControllerADDON = xbmcaddon.Addon(id='plugin.program.hue.controller')
        # xbmc.log("lights_already_on setting value: %s" %(HueControllerADDON.getSetting("lights_already_on")), level=myloglevel)
        # xbmc.log("video_only setting value: %s" %(HueControllerADDON.getSetting("video_only")), level=myloglevel)
        pass
