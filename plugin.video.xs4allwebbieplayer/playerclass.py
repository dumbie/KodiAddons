import xbmc
import xbmcgui
import getset
import path
import player
import playergui
import var

class Class_PlayerCustom(xbmc.Player):
    def onAVStarted(self):
        xbmc.sleep(100)

        #Check if player is playing
        if xbmc.Player().isPlaying() == True:
            #Switch to full screen player
            player.Fullscreen()

        #Check if video is playing
        if xbmc.Player().isPlayingVideo() == True:
            #Player seek stream from ending
            PlayerSeekOffsetSecEnd = player.PlayerSeekOffsetSecEnd()
            if PlayerSeekOffsetSecEnd != 0:
                xbmc.executebuiltin('Seek(-' + str(PlayerSeekOffsetSecEnd) + ')')

            #Enable or disable subtitles
            if getset.setting_get('PlayerSubtitlesOff') == 'true':
                xbmc.Player().showSubtitles(False)
            else:
                xbmc.Player().showSubtitles(True)

        #Refresh the main page media buttons
        if var.guiMain != None:
            var.guiMain.buttons_add_media(False)

    def onPlayBackSeek(self, seekTime, seekOffset):
        xbmc.sleep(100)

        #Check current stream type
        if xbmc.Player().isPlayingVideo() == True:
            #Show custom player information
            if var.guiPlayer != None:
                var.guiPlayer.show_epg(True, False, True, False)

    def onPlayBackStopped(self):
        xbmc.sleep(100)

        #Check if player is playing
        if xbmc.Player().isPlaying() == False:
            #Reset custom player variables
            player.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackEnded(self):
        xbmc.sleep(100)

        #Check if player is playing
        if xbmc.Player().isPlaying() == False:
            #Reset custom player variables
            player.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

    def onPlayBackError(self):
        xbmc.sleep(100)

        #Check if player is playing
        if xbmc.Player().isPlaying() == False:
            #Reset custom player variables
            player.ResetVariables()

            #Close the gui video player window
            playergui.close_the_page()

            #Refresh the main page media buttons
            if var.guiMain != None:
                var.guiMain.buttons_add_media(True)

            #Show playback error notification
            notificationIcon = path.icon_addon('error')
            xbmcgui.Dialog().notification(var.addonname, 'Er ging iets mis tijdens het afspelen.', notificationIcon, 2500, False)
