import xbmc
import xbmcgui
import func
import path
import playergui
import var

class PlayerCustom(xbmc.Player):
    PlayerWindowed = False
    PlayerOpenOverlay = False
    PlayerShowInformation = False
    PlayerSeekOffsetSecEnd = 0
    PlayerStreamType = 'video'

    def PlayCustom(self, streamUrl, listItem, Windowed=False, OpenOverlay=False, ShowInformation=False, SeekOffsetSecEnd=0, StreamType='video'):
        #Update custom player variables
        self.PlayerWindowed = Windowed
        self.PlayerOpenOverlay = OpenOverlay
        self.PlayerShowInformation = ShowInformation
        self.PlayerSeekOffsetSecEnd = SeekOffsetSecEnd
        self.PlayerStreamType = StreamType

        #Start playing list item media
        self.play(streamUrl, listItem, True)

    def Fullscreen(self, forceFullscreen=False, forceOpenOverlay=False, forceShowInformation=False):
        xbmc.sleep(100)

        #Check variables instance name
        if var.VariablesName != 'WebbiePlayerScript':
            return

        #Check if player is playing
        if xbmc.Player().isPlaying() == True:
            if self.PlayerStreamType == 'audio':
                #Close media player windows
                func.close_window_id(var.WINDOW_HOME)
                func.close_window_id(var.WINDOW_SLIDESHOW)
                func.close_window_id(var.WINDOW_FULLSCREEN_VIDEO)
                xbmc.sleep(100)

                #Close custom player overlay
                playergui.close_the_page()
                xbmc.sleep(100)

                #Open fullscreen player interface
                if forceFullscreen == True or self.PlayerWindowed == False:
                    func.open_window_id(var.WINDOW_VISUALISATION)
                    xbmc.sleep(100)
            elif self.PlayerStreamType == 'video':
                #Close media player windows
                func.close_window_id(var.WINDOW_HOME)
                func.close_window_id(var.WINDOW_SLIDESHOW)
                func.close_window_id(var.WINDOW_VISUALISATION)
                xbmc.sleep(100)

                #Open fullscreen player interface
                if forceFullscreen == True or self.PlayerWindowed == False:
                    func.open_window_id(var.WINDOW_FULLSCREEN_VIDEO)
                    xbmc.sleep(100)

                if forceOpenOverlay == True or self.PlayerOpenOverlay == True:
                    #Open custom player overlay
                    playergui.switch_to_page()
                    xbmc.sleep(100)
                else:
                    #Close custom player overlay
                    playergui.close_the_page()
                    xbmc.sleep(100)

                #Show custom player information
                if forceShowInformation == True or self.PlayerShowInformation == True:
                    if var.guiPlayer != None:
                        var.guiPlayer.show_epg(True, False, True)

    def onAVStarted(self):
        xbmc.sleep(100)

        #Check variables instance name
        if var.VariablesName != 'WebbiePlayerScript':
            return

        #Check if player is playing
        if xbmc.Player().isPlaying() == True:
            #Switch to full screen player
            self.Fullscreen()

        #Check if video is playing
        if self.PlayerStreamType == 'video':
            #Player seek stream from ending
            if self.PlayerSeekOffsetSecEnd != 0:
                xbmc.executebuiltin('Seek(-' + str(self.PlayerSeekOffsetSecEnd) + ')')

            #Enable or disable subtitles
            if func.setting_get('PlayerSubtitlesOff') == 'true':
                xbmc.Player().showSubtitles(False)
            else:
                xbmc.Player().showSubtitles(True)

        #Refresh the main page media buttons
        if var.guiMain != None:
            var.guiMain.buttons_add_media(False)

    def onPlayBackSeek(self, seekTime, seekOffset):
        xbmc.sleep(100)

        #Check variables instance name
        if var.VariablesName != 'WebbiePlayerScript':
            return

        #Check current stream type
        if self.PlayerStreamType == 'video':
            #Show custom player information
            if var.guiPlayer != None:
                var.guiPlayer.show_epg(True, False, True)

    def onPlayBackStopped(self):
        xbmc.sleep(100)

        #Check variables instance name
        if var.VariablesName != 'WebbiePlayerScript':
            return

        #Check if player is playing
        if xbmc.Player().isPlaying() == False:
            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackEnded(self):
        xbmc.sleep(100)

        #Check variables instance name
        if var.VariablesName != 'WebbiePlayerScript':
            return

        #Check if player is playing
        if xbmc.Player().isPlaying() == False:
            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackError(self):
        xbmc.sleep(100)

        #Check variables instance name
        if var.VariablesName != 'WebbiePlayerScript':
            return

        #Check if player is playing
        if xbmc.Player().isPlaying() == False:
            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

            #Show playback error notification
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Er ging iets mis tijdens het afspelen.', notificationIcon, 2500, False)
