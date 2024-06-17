import json
import xbmcgui
import dlfunc
import files
import path
import var

def download(forceUpdate=False):
    try:
        #Set cache file path
        filePath = path.addonstoragecache('stb.js')

        if forceUpdate == False:
            #Check if already cached in variables
            if var.StbChannelsDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                #Update variable cache
                var.StbChannelsDataJson = json.loads(fileCache)
                return True

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json_nocookie(path.channels_list_stb())

        #Check if connection is successful
        if DownloadDataJson == []:
            notificationIcon = path.resources('resources/skins/default/media/common/stb.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ontvanger download mislukt.', notificationIcon, 2500, False)
            return False

        #Update variable cache
        var.StbChannelsDataJson = DownloadDataJson

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/stb.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ontvanger download mislukt.', notificationIcon, 2500, False)
        return False
