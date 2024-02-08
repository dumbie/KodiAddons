import xbmc
import xbmcgui
import func
import path
import playergui
import var

class PlayerCustom(xbmc.Player):
    def PlayCustom(self, streamUrl, listItem=None, Windowed=False, OpenOverlay=False, ShowInformation=False, SeekOffsetStart=0, SeekOffsetEnd=0, StreamType='video'):
        #Update video player variables
        var.PlayerWindowed(Windowed)
        var.PlayerOpenOverlay(OpenOverlay)
        var.PlayerShowInformation(ShowInformation)
        var.PlayerSeekOffsetStart(SeekOffsetStart)
        var.PlayerSeekOffsetEnd(SeekOffsetEnd)
        var.PlayerStreamType(StreamType)

        #Set list item seek offset start
        if SeekOffsetStart != 0:
            listItem.setProperty('StartOffset', str(SeekOffsetStart))

        #Start playing list item media
        self.play(streamUrl, listItem, Windowed)

    def ResetVariables(self):
        #Reset video player variables
        var.PlayerWindowed(False)
        var.PlayerOpenOverlay(False)
        var.PlayerShowInformation(False)
        var.PlayerSeekOffsetStart(0)
        var.PlayerSeekOffsetEnd(0)
        var.PlayerStreamType('video')

    def Fullscreen(self, forceFullscreen=False, forceOverlay=False):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == True:
            if var.PlayerStreamType() == 'audio':
                #Close custom player overlay
                playergui.close_the_page()
                xbmc.sleep(100)

                #Open fullscreen player interface
                if forceFullscreen == True or var.PlayerWindowed() == False:
                    func.open_window_id(var.WINDOW_VISUALISATION)
                    xbmc.sleep(100)
            elif var.PlayerStreamType() == 'video':
                #Open fullscreen player interface
                if forceFullscreen == True or var.PlayerWindowed() == False:
                    func.open_window_id(var.WINDOW_FULLSCREEN_VIDEO)
                    xbmc.sleep(100)

                if forceOverlay == True or var.PlayerOpenOverlay() == True:
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
        if xbmc.Player().isPlaying() == True:
            #Switch to full screen player
            self.Fullscreen()

        if xbmc.Player().isPlayingVideo() == True:
            #Player seek stream from ending
            PlayerSeekOffsetEnd = var.PlayerSeekOffsetEnd()
            if PlayerSeekOffsetEnd != 0:
                xbmc.executebuiltin('Seek(-' + str(PlayerSeekOffsetEnd) + ')')

            #Enable or disable subtitles
            if var.addon.getSetting('PlayerSubtitlesOff') == 'true':
                self.showSubtitles(False)
            else:
                self.showSubtitles(True)

        #Refresh the main page media buttons
        if var.guiMain != None:
            var.guiMain.buttons_add_media(False)

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
