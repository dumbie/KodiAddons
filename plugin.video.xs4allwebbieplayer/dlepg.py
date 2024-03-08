import json
import xbmcgui
import apilogin
import classes
import dlfunc
import files
import path
import var

def get_cache_variable_class(dayDateString):
    #Check if epg day is cached in variable
    for epgCache in var.EpgCacheArrayDataJson:
        try:
            if epgCache.dayDateString == dayDateString:
                return epgCache
        except:
            continue
    return None

def download(dayDateTime, forceUpdate=False):
    try:
        #Convert datetime to datestring
        dayDateString = dayDateTime.strftime('%Y-%m-%d')

        #Get cache from variable
        variableCache = get_cache_variable_class(dayDateString)

        if forceUpdate == False:
            #Check if already cached in variable
            if variableCache != None:
                return variableCache.epgJson

            #Check if already cached in files
            fileCache = files.openFile(path.addonstoragecache('epg' + dayDateString + '.js'))
            if fileCache != None:
                fileCacheJson = json.loads(fileCache)

                #Update variable cache
                classAdd = classes.Class_CacheEpgDays()
                classAdd.dayDateString = dayDateString
                classAdd.epgJson = fileCacheJson
                var.EpgCacheArrayDataJson.append(classAdd)

                #Return epg json
                return fileCacheJson

        #Remove cache from variable
        if variableCache != None:
            var.EpgCacheArrayDataJson.remove(variableCache)

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
        classAdd.epgJson = DownloadDataJson
        var.EpgCacheArrayDataJson.append(classAdd)

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(path.addonstoragecache('epg' + dayDateString + '.js'), JsonDumpBytes)

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
        xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt.', notificationIcon, 2500, False)
        return None
