import json
import xbmcgui
import apilogin
import cache
import classes
import dlfunc
import files
import path
import var

def get_epg_cache(dayDateString):
    #Check if epg day is cached in variable
    for epgCache in var.CacheEpgDaysArray:
        try:
            if epgCache.dayDateString == dayDateString:
                return epgCache
        except:
            continue
    return None

def download(dayDateTime, forceUpdate=False, cleanupCache=True):
    try:
        #Cleanup downloaded cache files
        if cleanupCache == True and cache.cache_cleanup_epg() == True:
            var.CacheEpgDaysArray = []

        #Convert datetime to datestring
        dayDateString = dayDateTime.strftime('%Y-%m-%d')

        if forceUpdate == False:
            #Check if already cached in variable
            variableCache = get_epg_cache(dayDateString)
            if variableCache != None:
                return variableCache.dataJson

            #Check if already cached in files
            filePath = path.addonstoragecache('epg' + dayDateString + '.js')
            fileCache = files.openFile(filePath)
            if fileCache != None:
                fileCacheJson = json.loads(fileCache)

                #Update variable cache
                classAdd = classes.Class_CacheEpgDays()
                classAdd.dayDateString = dayDateString
                classAdd.dataJson = fileCacheJson
                var.CacheEpgDaysArray.append(classAdd)
                return fileCacheJson

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
            xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return None

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.epg_day(dayDateTime))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        #Update variable cache
        classAdd = classes.Class_CacheEpgDays()
        classAdd.dayDateString = dayDateString
        classAdd.dataJson = DownloadDataJson
        var.CacheEpgDaysArray.append(classAdd)

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
        xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt.', notificationIcon, 2500, False)
        return None
