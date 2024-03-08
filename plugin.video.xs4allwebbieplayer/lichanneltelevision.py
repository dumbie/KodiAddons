from datetime import date, datetime, timedelta
import xbmc
import accent
import dlchanneltelevision
import dlepg
import dlrecordingevent
import dlrecordingseries
import favorite
import func
import getset
import hidden
import lifunc
import metadatafunc
import metadatainfo
import path
import var

def list_load_combined(listContainer=None, downloadRecordings=True, downloadEpg=False, forceUpdate=False):
    try:
        #Download channels
        downloadResultChannels = dlchanneltelevision.download(forceUpdate)
        if downloadResultChannels == False:
            return False

        #Download recordings
        if downloadRecordings == True:
            downloadResultRecordingEvent = dlrecordingevent.download(forceUpdate)
            downloadResultRecordingSeries = dlrecordingseries.download(forceUpdate)
            if downloadResultRecordingEvent == False or downloadResultRecordingSeries == False:
                return False

        #Download epg day
        if downloadEpg == True:
            downloadResultEpg = dlepg.download(datetime.now(), forceUpdate)
            if downloadResultEpg == None:
                return False
        else:
            downloadResultEpg = None

        #Load favorite and hidden channels
        favorite.favorite_television_json_load()
        hidden.hidden_television_json_load()

        #Check if there are favorites set
        favorite.favorite_check_set('FavoriteTelevision.js')

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, downloadResultEpg, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: int(x[1].getProperty('ChannelNumber')))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, downloadResultEpg, remoteMode=False):
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

            #Add channelId to playable id list
            var.TelevisionChannelIdsPlayable.append(ChannelId)

            #Check if channel is hidden
            if hidden.hidden_check(ChannelId, 'HiddenTelevision.js'): continue

            #Check if channel is filtered
            if getset.setting_get('TelevisionChannelNoErotic') == 'true' and ChannelIsAdult == True: continue

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Check if channel is marked as favorite or epg navigate
            if favorite.favorite_check_channel(ChannelId, 'FavoriteTelevision.js'):
                ChannelFavorite = 'true'
            elif ChannelId == getset.setting_get('CurrentChannelId') and xbmc.Player().isPlayingVideo():
                ChannelFavorite = 'false'
            elif ChannelId == var.EpgCurrentChannelId and func.string_isnullorempty(var.EpgNavigateProgramId) == False:
                ChannelFavorite = 'false'
            elif getset.setting_get('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchTermResult):
                continue
            else:
                ChannelFavorite = 'false'

            #Load channel details
            ExternalId = metadatainfo.externalId_from_json_metadata(channel)
            ChannelNumberString = metadatainfo.orderId_from_json_metadata(channel)
            ChannelNumberAccent = accent.get_accent_color_string() + ChannelNumberString + '[/COLOR]'
            ChannelRecordEvent = 'false'
            ChannelRecordSeries = 'false'
            ChannelAlarm = 'false'
            ProgramNowName = 'Informatie wordt geladen'
            ProgramNextName = 'Informatie wordt geladen'
            ProgramDescription = 'Programmabeschrijving wordt geladen.'
            ProgramProgressPercent = '100'
            ProgramGenre = 'Televisie'
            ProgramDuration = ''

            if remoteMode == True:
                #Get json epg for channel identifier
                channelEpg = metadatafunc.search_channelid_jsonepg(downloadResultEpg, ChannelId)

                #Look for current airing program index
                metaData = metadatafunc.search_program_airingtime_jsonepg(channelEpg, datetime.now())

                #Get the current program information
                ProgramDuration = metadatainfo.programdurationint_from_json_metadata(metaData) * 60
                ProgramStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
                ProgramStartString = ProgramStartDateTime.strftime('%H:%M')
                ProgramEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)
                ProgramEndString = ProgramEndDateTime.strftime('%H:%M')
                ProgramNowName = metadatainfo.programtitle_from_json_metadata(metaData)
                ProgramGenre = '(' + ProgramStartString + '/' + ProgramEndString + ') ' + ProgramNowName

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            jsonItem = {
                'StreamAssetId': StreamAssetId,
                'ExternalId': ExternalId,
                'ChannelId': ChannelId,
                'ChannelNumber': ChannelNumberString,
                'ChannelNumberAccent': ChannelNumberAccent,
                'ChannelFavorite': ChannelFavorite,
                'ChannelName': ChannelName,
                'ChannelRecordEvent': ChannelRecordEvent,
                'ChannelRecordSeries': ChannelRecordSeries,
                'ChannelAlarm': ChannelAlarm,
                "ProgramNowName": ProgramNowName,
                "ProgramNextName": ProgramNextName,
                "ProgramDescription": ProgramDescription,
                "ProgramProgressPercent": ProgramProgressPercent,
                'ItemLabel': ChannelName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramGenre, 'Tagline': ChannelNumberString, 'Title': ChannelName, 'TrackNumber': ChannelNumberString, 'Duration': ProgramDuration},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_tv'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
