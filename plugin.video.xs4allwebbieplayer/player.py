import xbmc
import xbmcgui
import func
import path
import playergui
import var

class PlayerCustom(xbmc.Player):
    def PlayCustom(self, streamUrl, listItem, Windowed=False, OpenOverlay=False, ShowInformation=False, SeekOffsetSecEnd=0):
        #Update custom player variables
        var.PlayerWindowed(Windowed)
        var.PlayerOpenOverlay(OpenOverlay)
        var.PlayerShowInformation(ShowInformation)
        var.PlayerSeekOffsetSecEnd(SeekOffsetSecEnd)
        xbmc.sleep(100)

        #Start playing list item media
        self.play(streamUrl, listItem, True)

    def ResetVariables(self):
        #Reset custom player variables
        var.PlayerWindowed(False)
        var.PlayerOpenOverlay(False)
        var.PlayerShowInformation(False)
        var.PlayerSeekOffsetSecEnd(0)

    def Fullscreen(self, forceFullscreen=False, forceOpenOverlay=False, forceShowInformation=False):
        #Check if player is playing
        if self.isPlayingVideo() == True:
            #Open fullscreen player interface
            if forceFullscreen == True or var.PlayerWindowed() == False:
                func.open_window_id(var.WINDOW_FULLSCREEN_VIDEO)
                xbmc.sleep(100)

            #Open or close custom player overlay
            if forceOpenOverlay == True or var.PlayerOpenOverlay() == True:
                playergui.switch_to_page()
                xbmc.sleep(100)
            else:
                playergui.close_the_page()
                xbmc.sleep(100)

            #Show custom player information
            if forceShowInformation == True or var.PlayerShowInformation() == True:
                if var.guiPlayer != None:
                    var.guiPlayer.show_epg(True, False, True)
        elif self.isPlayingAudio() == True:
            #Close custom player overlay
            playergui.close_the_page()
            xbmc.sleep(100)

            #Open fullscreen player interface
            if forceFullscreen == True or var.PlayerWindowed() == False:
                func.open_window_id(var.WINDOW_VISUALISATION)
                xbmc.sleep(100)

    def onAVStarted(self):
        xbmc.sleep(100)

        #Check if player is playing
        if self.isPlaying() == True:
            #Switch to full screen player
            self.Fullscreen()

        #Check if video is playing
        if self.isPlayingVideo() == True:
            #Player seek stream from ending
            PlayerSeekOffsetSecEnd = var.PlayerSeekOffsetSecEnd()
            if PlayerSeekOffsetSecEnd != 0:
                xbmc.executebuiltin('Seek(-' + str(PlayerSeekOffsetSecEnd) + ')')

            #Enable or disable subtitles
            if func.setting_get('PlayerSubtitlesOff') == 'true':
                self.showSubtitles(False)
            else:
                self.showSubtitles(True)

        #Refresh the main page media buttons
        if var.guiMain != None:
            var.guiMain.buttons_add_media(False)

    def onPlayBackSeek(self, seekTime, seekOffset):
        xbmc.sleep(100)

        #Check current stream type
        if self.isPlayingVideo() == True:
            #Show custom player information
            if var.guiPlayer != None:
                var.guiPlayer.show_epg(True, False, True)

    def onPlayBackStopped(self):
        xbmc.sleep(100)

        #Check if player is playing
        if self.isPlaying() == False:
            #Reset custom player variables
            self.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackEnded(self):
        xbmc.sleep(100)

        #Check if player is playing
        if self.isPlaying() == False:
            #Reset custom player variables
            self.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackError(self):
        xbmc.sleep(100)

        #Check if player is playing
        if self.isPlaying() == False:
            #Reset custom player variables
            self.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

            #Show playback error notification
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Er ging iets mis tijdens het afspelen.', notificationIcon, 2500, False)
