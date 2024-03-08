import json
import xbmcgui
import apilogin
import dlfunc
import files
import path
import var

def download(dayDateTime, forceUpdate=False):
    try:
        if forceUpdate == False:
            #Check if already cached in variables
            if var.VodDayDataJson != []:
                return var.VodDayDataJson

            #Check if already cached in files
            fileCache = files.openFile(path.addonstoragecache('vod.js'))
            if fileCache != None:
                var.VodDayDataJson = json.loads(fileCache)
                return var.VodDayDataJson

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
            xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_vod(dayDateTime))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
                xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.VodDayDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(path.addonstoragecache('vod.js'), JsonDumpBytes)

        return var.VodDayDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt.', notificationIcon, 2500, False)
        return False
