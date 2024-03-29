import xbmcgui
import apilogin
import dlfunc
import path
import var
import files
import json

def download(searchTerm, forceUpdate=False):
    try:
        #Set cache file path
        filePath = path.addonstoragecache('searchprogram.js')

        if forceUpdate == False:
            #Check if already cached in variables
            if var.SearchProgramDataJson != []:
                return var.SearchProgramDataJson

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.SearchProgramDataJson = json.loads(fileCache)
                return var.SearchProgramDataJson

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/search.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_search(searchTerm))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/search.png')
                xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.SearchProgramDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/search.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt.', notificationIcon, 2500, False)
        return False
