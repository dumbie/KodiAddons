import json
import xbmcgui
import apilogin
import dlfunc
import files
import path
import var

def download_vod(forceUpdate=False):
    try:
        if forceUpdate == False:
            #Check if already cached in variables
            if var.SeriesVodDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(path.addonstoragecache('seriesvod.js'))
            if fileCache != None:
                var.SeriesVodDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.vod_series())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.SeriesVodDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(path.addonstoragecache('seriesvod.js'), JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt.', notificationIcon, 2500, False)
        return False

def download_program(forceUpdate=False):
    try:
        if forceUpdate == False:
            #Check if already cached in variables
            if var.SeriesProgramDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(path.addonstoragecache('seriesprogram.js'))
            if fileCache != None:
                var.SeriesProgramDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_series())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.SeriesProgramDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(path.addonstoragecache('seriesprogram.js'), JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt.', notificationIcon, 2500, False)
        return False
