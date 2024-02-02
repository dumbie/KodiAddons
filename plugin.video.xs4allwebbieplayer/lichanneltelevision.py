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
        #Download channels
        downloadResult = download.download_channels_tv(forceUpdate)
        if downloadResult == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, "Zenders downloaden mislukt.", notificationIcon, 2500, False)
            return False

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
    favorite.favorite_television_json_load()
    hidden.hidden_television_json_load()
    var.TelevisionChannelIdsPlayable = []
    for channel in var.TelevisionChannelsDataJson['resultObj']['containers']:
        try:
            #Load channel basics
            AssetId = metadatainfo.stream_assetid_from_json_metadata(channel)
            ChannelId = metadatainfo.channelId_from_json_metadata(channel)
            ChannelName = metadatainfo.channelName_from_json_metadata(channel)
            ChannelIsAdult = metadatainfo.isAdult_from_json_metadata(channel)

            #Check if channel is streamable
            if func.string_isnullorempty(AssetId): continue

            #Check if channel is hidden
            if hidden.hidden_check(ChannelId, 'HiddenTelevision.js'): continue

            #Add channelId to playable id list
            var.TelevisionChannelIdsPlayable.append(ChannelId)

            #Check if channel is filtered
            if var.addon.getSetting('TelevisionChannelNoErotic') == 'true' and ChannelIsAdult == True: continue

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Check if channel is marked as favorite or epg navigate
            if favorite.favorite_check(ChannelId, 'FavoriteTelevision.js'):
                ChannelFavorite = 'true'
            elif ChannelId == var.addon.getSetting('CurrentChannelId') and xbmc.Player().isPlayingVideo():
                ChannelFavorite = 'false'
            elif ChannelId == var.EpgCurrentChannelId and func.string_isnullorempty(var.EpgNavigateProgramId) == False:
                ChannelFavorite = 'false'
            elif var.addon.getSetting('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchChannelTerm):
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
            listItem.setProperty('AssetId', AssetId)
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
