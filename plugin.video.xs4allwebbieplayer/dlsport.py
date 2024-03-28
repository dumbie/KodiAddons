import json
import xbmcgui
import apilogin
import dlfunc
import files
import path
import var

def download(forceUpdate=False):
    try:
        #Set cache file path
        filePath = path.addonstoragecache('sportprogram.js')

        if forceUpdate == False:
            #Check if already cached in variables
            if var.SportProgramDataJson != []:
                return var.SportProgramDataJson

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.SportProgramDataJson = json.loads(fileCache)
                return var.SportProgramDataJson

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
            xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_sport())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
                xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.SportProgramDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return var.SportProgramDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
        xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt.', notificationIcon, 2500, False)
        return False
