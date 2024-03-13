import json
import xbmcgui
import apilogin
import cache
import dlfunc
import files
import path
import var

def download(forceUpdate=False):
    try:
        #Check if user has recording access
        if var.RecordingAccess() == False:
            return True

        #Cleanup downloaded cache files
        filePath = path.addonstoragecache('recordingevent.js')
        if cache.cache_cleanup_file(filePath, var.CacheCleanTimeOther()) == True:
            var.RecordingEventDataJson = []

        if forceUpdate == False:
            #Check if already cached in variables
            if var.RecordingEventDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.RecordingEventDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_event())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.RecordingEventDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt.', notificationIcon, 2500, False)
        return False
