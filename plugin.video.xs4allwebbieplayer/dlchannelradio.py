import json
import xbmcgui
import cache
import dlfunc
import files
import path
import var

def update_playable_channel_identifiers():
    var.RadioChannelIdsPlayableArray = []
    for channel in var.RadioChannelsDataJson['radios']:
        try:
            #Load channel basics
            ChannelId = channel['id']

            #Add channelId to playable id list
            var.RadioChannelIdsPlayableArray.append(ChannelId)
        except:
            pass

    #Convert playable identifiers to string
    var.RadioChannelIdsPlayableString = ','.join(filter(None, var.RadioChannelIdsPlayableArray))

def download(forceUpdate=False):
    try:
        #Cleanup downloaded cache files
        filePath = path.addonstoragecache('radio.js')
        if cache.cache_cleanup_file(filePath, var.CacheCleanTimeChannels) == True:
            var.RadioChannelsDataJson = []

        if forceUpdate == False:
            #Check if already cached in variables
            if var.RadioChannelsDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                #Update variable cache
                var.RadioChannelsDataJson = json.loads(fileCache)

                #Update playable channel identifiers
                update_playable_channel_identifiers()
                return True

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.channels_list_radio())

        #Check if connection is successful
        if DownloadDataJson == []:
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Radio download mislukt.', notificationIcon, 2500, False)
            return False

        #Update variable cache
        var.RadioChannelsDataJson = DownloadDataJson

        #Update playable channel identifiers
        update_playable_channel_identifiers()

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Radio download mislukt.', notificationIcon, 2500, False)
        return False
