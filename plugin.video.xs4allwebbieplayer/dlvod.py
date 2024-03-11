import json
import xbmcgui
import apilogin
import cache
import classes
import dlfunc
import files
import path
import var

def get_vod_cache(dayDateString):
    for vodCache in var.VodCacheDaysArray:
        try:
            if vodCache.dayDateString == dayDateString:
                return vodCache
        except:
            continue
    return None

def download(dayDateTime, forceUpdate=False):
    try:
        #Cleanup downloaded cache files
        if cache.cache_cleanup_days('vod', var.CacheCleanTimeOther) == True:
            var.VodCacheDaysArray = []

        #Convert datetime to datestring
        dayDateString = dayDateTime.strftime('%Y-%m-%d')

        if forceUpdate == False:
            #Check if already cached in variables
            variableCache = get_vod_cache(dayDateString)
            if variableCache != None:
                return variableCache.dataJson

            #Check if already cached in files
            filePath = path.addonstoragecache('vod' + dayDateString + '.js')
            fileCache = files.openFile(filePath)
            if fileCache != None:
                fileCacheJson = json.loads(fileCache)

                #Update variable cache
                classAdd = classes.Class_CacheDays()
                classAdd.dayDateString = dayDateString
                classAdd.dataJson = fileCacheJson
                var.VodCacheDaysArray.append(classAdd)
                return fileCacheJson
        else:
            var.VodCacheDaysArray = []

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
            xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return None

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
                return None

        #Update variable cache
        classAdd = classes.Class_CacheDays()
        classAdd.dayDateString = dayDateString
        classAdd.dataJson = DownloadDataJson
        var.VodCacheDaysArray.append(classAdd)

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt.', notificationIcon, 2500, False)
        return None
