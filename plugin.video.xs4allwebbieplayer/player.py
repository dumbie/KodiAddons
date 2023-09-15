import xbmc
import xbmcgui
import func
import path
import playergui
import var

class PlayerCustom(xbmc.Player):
    def PlayCustom(self, title='Onbekend', listitem=None, Windowed=False, Overlay=False, SeekOffset=0):
        #Check if audio is playing in visualization
        if xbmc.Player().isPlayingAudio():
            func.close_window_id(var.WINDOW_VISUALISATION)
            xbmc.sleep(100)

        #Update the video player settings
        var.PlayerWindowed = Windowed
        var.PlayerOverlay = Overlay
        var.PlayerSeekOffset = SeekOffset

        #Check which video player should be used for playback
        super(PlayerCustom, self).play(title, listitem, Windowed)

    def Fullscreen(self, ForceFullscreen=False, ForceOverlay=False):
        #Stop all epg update threads
        var.thread_update_television_program = None
        var.thread_update_epg_program = None
        var.thread_update_epg_channel = None

        #Switch to the desired video player window
        if xbmc.Player().isPlayingVideo():
            #Fullscreen the video player
            if ForceFullscreen == True or var.PlayerWindowed == False and xbmc.getCondVisibility('VideoPlayer.IsFullscreen') == False:
                xbmc.executebuiltin('Action(FullScreen)')
                xbmc.sleep(100)

            #Overlay the custom player gui
            if ForceOverlay == True or var.PlayerOverlay == True and xbmc.getCondVisibility('VideoPlayer.IsFullscreen') == True:
                playergui.switch_to_page()
            else:
                playergui.close_the_page()
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Televisie speelt niet.', notificationIcon, 2500, False)

    def onAVStarted(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlayingVideo():
            #Switch to full screen video player
            self.Fullscreen()

            #Player seek back stream
            if var.PlayerSeekOffset != 0:
                xbmc.executebuiltin('Seek(-' + str(var.PlayerSeekOffset) + ')')
                var.PlayerSeekOffset = 0

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
            #Reset the custom player variables
            var.PlayerWindowed = False
            var.PlayerOverlay = False

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackEnded(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Reset the custom player variables
            var.PlayerWindowed = False
            var.PlayerOverlay = False

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackError(self):
        xbmc.sleep(100)
        if xbmc.Player().isPlaying() == False:
            #Reset the custom player variables
            var.PlayerWindowed = False
            var.PlayerOverlay = False

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

            #Show playback error notification
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Er ging iets mis tijdens het afspelen.', notificationIcon, 2500, False)
