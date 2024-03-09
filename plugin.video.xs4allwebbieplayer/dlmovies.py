import json
import xbmcgui
import apilogin
import cache
import dlfunc
import files
import path
import var

def download_vod(forceUpdate=False):
    try:
        #Cleanup downloaded cache files
        filePath = path.addonstoragecache('moviesvod.js')
        if cache.cache_cleanup_file(filePath, var.CacheCleanTimeOther) == True:
            var.MoviesVodDataJson = []

        if forceUpdate == False:
            #Check if already cached in variables
            if var.MoviesVodDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.MoviesVodDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.vod_movies())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
                xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.MoviesVodDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt.', notificationIcon, 2500, False)
        return False

def download_program(forceUpdate=False):
    try:
        #Cleanup downloaded cache files
        filePath = path.addonstoragecache('moviesprogram.js')
        if cache.cache_cleanup_file(filePath, var.CacheCleanTimeOther) == True:
            var.MoviesProgramDataJson = []

        if forceUpdate == False:
            #Check if already cached in variables
            if var.MoviesProgramDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                var.MoviesProgramDataJson = json.loads(fileCache)
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_movies())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.MoviesProgramDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt.', notificationIcon, 2500, False)
        return False
