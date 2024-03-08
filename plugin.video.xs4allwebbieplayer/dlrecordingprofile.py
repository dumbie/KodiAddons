import xbmcgui
import apilogin
import dlfunc
import metadatainfo
import path
import var

def download(forceUpdate=False):
    try:
        #Check if already cached in variables
        if var.RecordingProfileLoaded() == True and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname profiel download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_profile())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opname profiel download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update recording variables
        var.RecordingProfileLoaded(True)
        var.RecordingAccess(metadatainfo.recording_access(DownloadDataJson))
        var.RecordingAvailableSpace(metadatainfo.recording_space(DownloadDataJson))
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname profiel download mislukt.', notificationIcon, 2500, False)
        return False
