import xbmc
import xbmcgui
import func
import path
import playergui
import var

class PlayerCustom(xbmc.Player):
    def PlayCustom(self, title='Onbekend', listItem=None, Windowed=False, OpenOverlay=False, ShowInformation=False, SeekOffsetStart=0, SeekOffsetEnd=0):
        #Check if audio is playing in visualization
        if xbmc.Player().isPlayingAudio():
            func.close_window_id(var.WINDOW_VISUALISATION)
            xbmc.sleep(100)

        #Update video player variables
        var.PlayerWindowed(Windowed)
        var.PlayerOpenOverlay(OpenOverlay)
        var.PlayerShowInformation(ShowInformation)
        var.PlayerSeekOffsetStart(SeekOffsetStart)
        var.PlayerSeekOffsetEnd(SeekOffsetEnd)

        #Start playing list item media
        self.play(title, listItem, Windowed)

    def Fullscreen(self, ForceFullscreen=False, ForceOverlay=False):
        xbmc.sleep(100)
        if xbmc.Player().isPlayingVideo():
            #Fullscreen video player
            if ForceFullscreen == True or var.PlayerWindowed() == False and xbmc.getCondVisibility('VideoPlayer.IsFullscreen') == False:
                xbmc.executebuiltin('Action(FullScreen)')
                xbmc.sleep(100)

            #Open or close custom player gui
            if ForceOverlay == True or var.PlayerOpenOverlay() == True and xbmc.getCondVisibility('VideoPlayer.IsFullscreen') == True:
                playergui.switch_to_page()
                xbmc.sleep(100)
            else:
                playergui.close_the_page()
                xbmc.sleep(100)       

            #Show custom player gui
            if var.PlayerShowInformation() == True and var.guiPlayer != None:
                var.guiPlayer.show_epg(True)
                xbmc.sleep(100)

    def onAVStarted(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlayingVideo():
            #Switch to full screen player
            self.Fullscreen()

            #Player seek stream from start
            PlayerSeekOffsetStart = var.PlayerSeekOffsetStart()
            if PlayerSeekOffsetStart != 0:
                xbmc.executebuiltin('Seek(' + str(PlayerSeekOffsetStart) + ')')
                var.PlayerSeekOffsetStart(0)

            #Player seek stream from ending
            PlayerSeekOffsetEnd = var.PlayerSeekOffsetEnd()
            if PlayerSeekOffsetEnd != 0:
                xbmc.executebuiltin('Seek(-' + str(PlayerSeekOffsetEnd) + ')')
                var.PlayerSeekOffsetEnd(0)

            #Enable or disable the subtitles
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
            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackEnded(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackError(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

            #Show playback error notification
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Er ging iets mis tijdens het afspelen.', notificationIcon, 2500, False)
