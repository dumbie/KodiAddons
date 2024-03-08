import xbmcgui
import apilogin
import dlfunc
import path
import var

def download(parentId):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, 'Afleveringen download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return None

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.vod_episodes(parentId))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Afleveringen download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Afleveringen download mislukt.', notificationIcon, 2500, False)
        return None
