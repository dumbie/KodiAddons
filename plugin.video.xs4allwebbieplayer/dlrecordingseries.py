import json
import xbmcgui
import apilogin
import dlfunc
import files
import path
import var

def download(forceUpdate=False):
    try:
        #Check if user has recording access
        if var.RecordingAccess() == False:
            return True

        if forceUpdate == False:
            #Check if already cached in variables
            if var.RecordingSeriesDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(path.addonstoragecache('recordingseries.js'))
            if fileCache != None:
                var.RecordingSeriesDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_series())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.RecordingSeriesDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(path.addonstoragecache('recordingseries.js'), JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt.', notificationIcon, 2500, False)
        return False
