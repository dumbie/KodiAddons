import xbmc
import xbmcgui
import func
import path
import playergui
import var

class PlayerCustom(xbmc.Player):
    def PlayCustom(self, streamUrl, listItem=None, Windowed=False, OpenOverlay=False, ShowInformation=False, SeekOffsetSecEnd=0):
        #Update video player variables
        var.PlayBackStartTriggered(False)
        var.PlayerOpenOverlay(OpenOverlay)
        var.PlayerShowInformation(ShowInformation)
        var.PlayerSeekOffsetSecEnd(SeekOffsetSecEnd)

        #Start playing list item media
        self.play(streamUrl, listItem, Windowed)

    def ResetVariables(self):
        #Reset video player variables
        var.PlayBackStartTriggered(False)
        var.PlayerOpenOverlay(False)
        var.PlayerShowInformation(False)
        var.PlayerSeekOffsetSecEnd(0)

    def Fullscreen(self, forceOverlay=False):
        xbmc.sleep(100)
        if xbmc.Player().isPlayingVideo() == True:
            if forceOverlay == True or var.PlayerOpenOverlay() == True:
                #Open fullscreen video player
                func.open_window_id(var.WINDOW_FULLSCREEN_VIDEO)
                xbmc.sleep(100)

                #Open custom player overlay
                playergui.switch_to_page()
                xbmc.sleep(100)
            else:
                #Close custom player overlay
                playergui.close_the_page()
                xbmc.sleep(100)

            #Show custom player information
            if var.PlayerShowInformation() == True:
                if var.guiPlayer != None:
                    var.guiPlayer.show_epg(True, False, True)

    def onAVStarted(self):
        xbmc.sleep(100)

        #Check if triggered twice
        if var.PlayBackStartTriggered() == False:
            var.PlayBackStartTriggered(True)
        else:
            return

        #Check if video is playing
        if xbmc.Player().isPlayingVideo() == True:
            #Switch to full screen player
            self.Fullscreen()

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
        if xbmc.Player().isPlayingVideo() == True:
            #Show custom player information
                if var.guiPlayer != None:
                    var.guiPlayer.show_epg(True, False, True)

    def onPlayBackStopped(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Reset video player variables
            self.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackEnded(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Reset video player variables
            self.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackError(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Reset video player variables
            self.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

            #Show playback error notification
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Er ging iets mis tijdens het afspelen.', notificationIcon, 2500, False)
