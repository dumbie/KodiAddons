import json
import xbmcgui
import apilogin
import cache
import dlfunc
import files
import func
import metadatainfo
import path
import var

def update_playable_channel_identifiers():
    var.TelevisionChannelIdsPlayableArray = []
    for channel in var.TelevisionChannelsDataJson['resultObj']['containers']:
        try:
            #Load channel basics
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(channel)
            ChannelId = metadatainfo.channelId_from_json_metadata(channel)

            #Check if channel is streamable
            if func.string_isnullorempty(StreamAssetId) == False:
                #Add channelId to playable id list
                var.TelevisionChannelIdsPlayableArray.append(ChannelId)
        except:
            pass

    #Convert playable identifiers to string
    var.TelevisionChannelIdsPlayableString = ','.join(filter(None, var.TelevisionChannelIdsPlayableArray))

def download(forceUpdate=False):
    try:
        #Cleanup downloaded cache files
        filePath = path.addonstoragecache('television.js')
        if cache.cache_cleanup_file(filePath, var.CacheCleanTimeChannels) == True:
            var.TelevisionChannelsDataJson = []

        if forceUpdate == False:
            #Check if already cached in variables
            if var.TelevisionChannelsDataJson != []:
                return True

            #Check if already cached in files
            fileCache = files.openFile(filePath)
            if fileCache != None:
                #Update variable cache
                var.TelevisionChannelsDataJson = json.loads(fileCache)

                #Update playable channel identifiers
                update_playable_channel_identifiers()
                return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.channels_list_tv())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/television.png')
                xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.TelevisionChannelsDataJson = DownloadDataJson

        #Update playable channel identifiers
        update_playable_channel_identifiers()

        #Update file cache
        JsonDumpBytes = json.dumps(DownloadDataJson).encode('ascii')
        files.saveFile(filePath, JsonDumpBytes)

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt.', notificationIcon, 2500, False)
        return False
