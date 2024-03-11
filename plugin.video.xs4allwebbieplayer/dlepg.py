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
    for epgCache in var.EpgCacheDaysArray:
        try:
            if epgCache.dayDateString == dayDateString:
                return epgCache
        except:
            continue
    return None

def download(dayDateTime, forceUpdate=False, cleanupCache=True):
    try:
        #Convert datetime to datestring
        dayDateString = dayDateTime.strftime('%Y-%m-%d')

        #Cleanup downloaded cache files
        filePath = path.addonstoragecache('epg' + dayDateString + '.js')
        if cleanupCache == True and cache.cache_cleanup_days('epg', var.CacheCleanTimeEpg) == True:
            var.EpgCacheDaysArray = []

        if forceUpdate == False:
            #Check if already cached in variables
            variableCache = get_epg_cache(dayDateString)
            if variableCache != None:
                return variableCache.dataJson

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                fileCacheJson = json.loads(fileCache)

                #Update variable cache
                classAdd = classes.Class_CacheDays()
                classAdd.dayDateString = dayDateString
                classAdd.dataJson = fileCacheJson
                var.EpgCacheDaysArray.append(classAdd)
                return fileCacheJson
        else:
            var.EpgCacheDaysArray = []

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
        classAdd = classes.Class_CacheDays()
        classAdd.dayDateString = dayDateString
        classAdd.dataJson = DownloadDataJson
        var.EpgCacheDaysArray.append(classAdd)

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
        xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt.', notificationIcon, 2500, False)
        return None
