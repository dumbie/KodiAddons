import json
import xbmcgui
import apilogin
import dlfunc
import files
import path
import var

def download(forceUpdate=False):
    try:
        if forceUpdate == False:
            #Check if already cached in variables
            if var.TelevisionChannelsDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(path.addonstoragecache('television.js'))
            if fileCache != None:
                var.TelevisionChannelsDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.channels_list_tv())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/television.png')
                xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.TelevisionChannelsDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(path.addonstoragecache('television.js'), JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt.', notificationIcon, 2500, False)
        return False
