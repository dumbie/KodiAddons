import xbmc
import xbmcgui
import download
import favorite
import hidden
import func
import lifunc
import metadatainfo
import path
import var

def list_load_combined(listContainer=None, forceUpdate=False):
    try:
        #Download recordings
        downloadResultRecordingEvent = download.download_recording_event(forceUpdate)
        downloadResultRecordingSeries = download.download_recording_series(forceUpdate)

        #Download channels
        downloadResultChannels = download.download_channels_tv(forceUpdate)
        if downloadResultRecordingEvent == False or downloadResultRecordingSeries == False or downloadResultChannels == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, "Zenders downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Load favorite and hidden channels
        favorite.favorite_television_json_load()
        hidden.hidden_television_json_load()

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    var.TelevisionChannelIdsPlayable = []
    for channel in var.TelevisionChannelsDataJson['resultObj']['containers']:
        try:
            #Load channel basics
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(channel)
            ChannelId = metadatainfo.channelId_from_json_metadata(channel)
            ChannelName = metadatainfo.channelName_from_json_metadata(channel)
            ChannelIsAdult = metadatainfo.isAdult_from_json_metadata(channel)

            #Check if channel is streamable
            if func.string_isnullorempty(StreamAssetId): continue

            #Check if channel is hidden
            if hidden.hidden_check(ChannelId, 'HiddenTelevision.js'): continue

            #Add channelId to playable id list
            var.TelevisionChannelIdsPlayable.append(ChannelId)

            #Check if channel is filtered
            if var.addon.getSetting('TelevisionChannelNoErotic') == 'true' and ChannelIsAdult == True: continue

            #Check if there are search results
            if var.SearchTermCurrent != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Check if channel is marked as favorite or epg navigate
            if favorite.favorite_check(ChannelId, 'FavoriteTelevision.js'):
                ChannelFavorite = 'true'
            elif ChannelId == var.addon.getSetting('CurrentChannelId') and xbmc.Player().isPlayingVideo():
                ChannelFavorite = 'false'
            elif ChannelId == var.EpgCurrentChannelId and func.string_isnullorempty(var.EpgNavigateProgramId) == False:
                ChannelFavorite = 'false'
            elif var.addon.getSetting('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchTermCurrent):
                continue
            else:
                ChannelFavorite = 'false'

            #Load channel details
            ExternalId = metadatainfo.externalId_from_json_metadata(channel)
            ChannelNumberString = metadatainfo.orderId_from_json_metadata(channel)
            ChannelNumberAccent = func.get_provider_color_string() + ChannelNumberString + '[/COLOR]'
            ChannelRecordEvent = 'false'
            ChannelRecordSeries = 'false'
            ChannelAlarm = 'false'
            ProgramNowName = 'Informatie wordt geladen'
            ProgramNextName = 'Informatie wordt geladen'
            ProgramDescription = 'Programmabeschrijving wordt geladen.'
            ProgramProgressPercent = '100'

            #Set item details
            listAction = 'play_stream_tv'
            listItem = xbmcgui.ListItem(ChannelName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('StreamAssetId', StreamAssetId)
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ChannelNumber', ChannelNumberString)
            listItem.setProperty('ChannelNumberAccent', ChannelNumberAccent)
            listItem.setProperty('ChannelFavorite', ChannelFavorite)
            listItem.setProperty('ExternalId', ExternalId)
            listItem.setProperty('ChannelName', ChannelName)
            listItem.setProperty('ChannelRecordEvent', ChannelRecordEvent)
            listItem.setProperty('ChannelRecordSeries', ChannelRecordSeries)
            listItem.setProperty('ChannelAlarm', ChannelAlarm)
            listItem.setProperty("ProgramNowName", ProgramNowName)
            listItem.setProperty("ProgramNextName", ProgramNextName)
            listItem.setProperty("ProgramDescription", ProgramDescription)
            listItem.setProperty("ProgramProgressPercent", ProgramProgressPercent)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': 'Televisie', 'Tagline': ChannelNumberString, 'Title': ChannelName})
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + ChannelId
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
