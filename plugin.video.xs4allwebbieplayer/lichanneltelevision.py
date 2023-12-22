import xbmc
import xbmcgui
import favorite
import func
import metadatainfo
import path
import var

def list_load(listContainer):
    favorite.favorite_television_json_load()
    var.ChannelIdsPlayable = []
    for channel in var.ChannelsDataJsonTelevision['resultObj']['containers']:
        try:
            #Load channel basics
            AssetId = metadatainfo.stream_assetid_from_json_metadata(channel['assets'])
            ChannelId = metadatainfo.channelId_from_json_metadata(channel)
            ChannelName = metadatainfo.channelName_from_json_metadata(channel)
            ChannelIsAdult = metadatainfo.isAdult_from_json_metadata(channel)

            #Check if channel is streamable
            if func.string_isnullorempty(AssetId): continue

            #Add channelId to playable id list
            var.ChannelIdsPlayable.append(ChannelId)

            #Check if channel is filtered
            if var.addon.getSetting('TelevisionChannelNoErotic') == 'true' and ChannelIsAdult == True: continue

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Check if channel is marked as favorite or epg navigate
            if ChannelId in var.FavoriteTelevisionDataJson:
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
            ChannelNumber = metadatainfo.orderId_from_json_metadata(channel)
            ChannelNumberAccent = func.get_provider_color_string() + ChannelNumber + '[/COLOR]'
            ChannelRecordEvent = 'false'
            ChannelRecordSeries = 'false'
            ChannelAlarm = 'false'
            ProgramNowName = 'Informatie wordt geladen'
            ProgramNextName = 'Informatie wordt geladen'
            ProgramDescription = 'Programmabeschrijving wordt geladen.'
            ProgramProgressPercent = '100'

            #Add television channel
            listItem = xbmcgui.ListItem()
            listItem.setProperty('Action', 'play_stream')
            listItem.setProperty('AssetId', AssetId)
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ChannelNumber', ChannelNumber)
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
            listItem.setInfo('video', {'Genre': 'Televisie'})
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.append(listItem)
        except:
            continue
