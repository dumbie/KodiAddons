from datetime import datetime, timedelta
import func
import var
import xbmc
import xbmcgui

class Player(xbmc.Player):
    def onAVStarted(self):
        #Stop the television epg update thread
        var.thread_refresh_epgtv = None

    def onPlayBackStarted(self):
        #Set the tuner in use check time
        var.PlayerTunerCheck = datetime.now()

    def onPlayBackStopped(self):
        if int((datetime.now() - var.PlayerTunerCheck).total_seconds()) < 2:
            notificationIcon = func.path_resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Tuner already in use?', notificationIcon, 2500, False)
