import json
import xbmcgui
import apilogin
import dlfunc
import files
import path
import var

def download_vod(forceUpdate=False):
    try:
        #Set cache file path
        filePath = path.addonstoragecache('kidsvod.js')

        if forceUpdate == False:
            #Check if already cached in variables
            if var.KidsVodDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.KidsVodDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.vod_kids())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
                xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.KidsVodDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
        xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt.', notificationIcon, 2500, False)
        return False

def download_program(forceUpdate=False):
    try:
        #Set cache file path
        filePath = path.addonstoragecache('kidsprogram.js')

        if forceUpdate == False:
            #Check if already cached in variables
            if var.KidsProgramDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.KidsProgramDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, 'Week kids download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_kids())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week kids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.KidsProgramDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week kids download mislukt.', notificationIcon, 2500, False)
        return False
