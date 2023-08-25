import xbmcgui
import alarm
import func
import metadatainfo
import path
import var

def list_load(listContainer, checkStatus=False):
    var.ChannelIdsPlayable = []
    for channel in var.ChannelsDataJsonTelevision['resultObj']['containers']:
        try:
            #Load channel basics
            AssetId = metadatainfo.get_stream_assetid(channel['assets'])
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
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False: continue

            #Check if channel is marked as favorite
            if ChannelId in var.FavoriteTelevisionDataJson:
                ChannelFavorite = 'true'
            else:
                if var.LoadChannelFavoritesOnly == True and var.SearchFilterTerm == '': continue
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

            if checkStatus == True:
                #Check if channel has active recording
                if func.search_channelid_jsonrecording_event(ChannelId, True):
                    ChannelRecordEvent = 'true'

                #Check if channel has active recording series
                if func.search_channelid_jsonrecording_series(ChannelId):
                    ChannelRecordSeries = 'true'

                #Check if channel has active alarm
                if alarm.alarm_duplicate_channel_check(ChannelId) == True:
                    ChannelAlarm = 'true'

            #Add normal channel
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_stream')
            listitem.setProperty('AssetId', AssetId)
            listitem.setProperty('ChannelId', ChannelId)
            listitem.setProperty('ChannelNumber', ChannelNumber)
            listitem.setProperty('ChannelNumberAccent', ChannelNumberAccent)
            listitem.setProperty('ChannelFavorite', ChannelFavorite)
            listitem.setProperty('ExternalId', ExternalId)
            listitem.setProperty('ChannelName', ChannelName)
            listitem.setProperty('ChannelRecordEvent', ChannelRecordEvent)
            listitem.setProperty('ChannelRecordSeries', ChannelRecordSeries)
            listitem.setProperty('ChannelAlarm', ChannelAlarm)
            listitem.setProperty("ProgramNowName", ProgramNowName)
            listitem.setProperty("ProgramNextName", ProgramNextName)
            listitem.setProperty("ProgramDescription", ProgramDescription)
            listitem.setProperty("ProgramProgressPercent", ProgramProgressPercent)
            listitem.setInfo('video', {'Genre': 'Televisie'})
            listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.addItem(listitem)
        except:
            continue
