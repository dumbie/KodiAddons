from datetime import date, datetime, timedelta
import xbmc
import accent
import dlchannelweb
import dlepg
import dlrecordingevent
import dlrecordingseries
import favoritefunc
import func
import getset
import hiddenfunc
import lifunc
import metadatafunc
import metadatainfo
import path
import var

def list_load_combined(listContainer=None, downloadRecordings=False, downloadEpg=False, epgMode=False):
    try:
        #Download channels
        downloadResultChannels = dlchannelweb.download()
        if downloadResultChannels == False:
            return False

        #Download recordings
        if downloadRecordings == True:
            downloadResultRecordingEvent = dlrecordingevent.download()
            downloadResultRecordingSeries = dlrecordingseries.download()
            if downloadResultRecordingEvent == False or downloadResultRecordingSeries == False:
                return False

        #Download epg day
        if downloadEpg == True:
            downloadResultEpg = dlepg.download(datetime.now())
            if downloadResultEpg == None:
                return False
        else:
            downloadResultEpg = None

        #Load favorite and hidden channels
        favoritefunc.favorite_television_json_load()
        hiddenfunc.hidden_television_json_load()

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, downloadResultEpg, remoteMode, epgMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: func.to_type(int, x[1].getProperty('ChannelNumber'), 0))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, jsonEpg, remoteMode=False, epgMode=False):
    for channel in var.WebChannelsDataJson['resultObj']['containers']:
        try:
            #Load channel basics
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(channel)
            ChannelId = metadatainfo.channelId_from_json_metadata(channel)
            ChannelName = metadatainfo.channelName_from_json_metadata(channel)

            #Check if channel is streamable
            if func.string_isnullorempty(StreamAssetId): continue

            #Check if channel is hidden
            if hiddenfunc.hidden_check_channel(ChannelId, 'HiddenTelevision.js'): continue

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Check if channel is marked as favorite or epg navigate
            if favoritefunc.favorite_check_channel(ChannelId, 'FavoriteTelevision.js'):
                ChannelFavorite = 'true'
            elif ChannelId == getset.setting_get('CurrentChannelId') and xbmc.Player().isPlayingVideo():
                ChannelFavorite = 'false'
            elif ChannelId == var.EpgCurrentChannelId and func.string_isnullorempty(var.EpgNavigateIdentifier) == False:
                ChannelFavorite = 'false'
            elif getset.setting_get('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchTermResult):
                continue
            else:
                ChannelFavorite = 'false'

            #Load channel details
            ExternalId = metadatainfo.externalId_from_json_metadata(channel)
            ChannelNumberInt = metadatainfo.orderId_from_json_metadata(channel)
            ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + ChannelNumberInt + '[/COLOR][/B]'
            ChannelRecordEvent = 'false'
            ChannelRecordSeries = 'false'
            ChannelAlarm = 'false'
            ProgramNowNameRaw = 'Informatie wordt geladen'
            ProgramNextNameRaw = 'Informatie wordt geladen'
            ProgramDescription = 'Programmabeschrijving wordt geladen.'
            ProgramProgressPercent = '100'
            ProgramDurationSeconds = ''

            if remoteMode == True and epgMode == False:
                #Get json epg for channel identifier
                jsonEpgChannel = metadatafunc.search_channelid_jsonepg(jsonEpg, ChannelId)

                #Look for current airing program index
                metaData = metadatafunc.search_program_airingtime_jsonepg(jsonEpgChannel, datetime.now())

                #Get the current program information
                ProgramNowNameRaw = metadatainfo.programtitle_from_json_metadata(metaData)
                ProgramDurationSeconds = metadatainfo.programdurationint_from_json_metadata(metaData) * 60
                ProgramStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
                ProgramEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)

                #Combine program timing
                if ProgramStartDateTime != datetime(1970,1,1) and ProgramEndDateTime != datetime(1970,1,1):
                    ProgramStartString = ProgramStartDateTime.strftime('%H:%M')
                    ProgramEndString = ProgramEndDateTime.strftime('%H:%M')
                    ProgramTimingString = ProgramStartString + '/' + ProgramEndString
                else:
                    ProgramTimingString = '?'

                #Combine program name
                ProgramGenre = '[COLOR FF888888](' + ProgramTimingString + ') ' + ProgramNowNameRaw + '[/COLOR]'
            elif epgMode == True:
                ProgramGenre = 'TV Gids'
            else:
                ProgramGenre = 'Televisie'

            if epgMode == True:
                dirIsfolder = True
                ItemAction = 'load_epg_days'
                ItemInfoVideo = {'MediaType': 'tvshow', 'Genre': ProgramGenre, 'Tagline': ProgramGenre, 'Title': ChannelName, 'TrackNumber': ChannelNumberInt}
            else:
                dirIsfolder = False
                ItemAction = 'play_stream_tv'
                ItemInfoVideo = {'MediaType': 'movie', 'Genre': ProgramGenre, 'Tagline': ProgramGenre, 'Title': ChannelName, 'TrackNumber': ChannelNumberInt, 'Duration': ProgramDurationSeconds}

            #Set item icons
            iconDefault = path.icon_television(ExternalId)
            iconFanart = path.icon_fanart()

            #Set item details
            jsonItem = {
                'StreamAssetId': StreamAssetId,
                'ExternalId': ExternalId,
                'ChannelId': ChannelId,
                'ChannelNumber': ChannelNumberInt,
                'ChannelNumberAccent': ChannelNumberAccent,
                'ChannelFavorite': ChannelFavorite,
                'ChannelName': ChannelName,
                'ChannelRecordEvent': ChannelRecordEvent,
                'ChannelRecordSeries': ChannelRecordSeries,
                'ChannelAlarm': ChannelAlarm,
                "ProgramNowNameRaw": ProgramNowNameRaw,
                "ProgramNextNameRaw": ProgramNextNameRaw,
                "ProgramDescription": ProgramDescription,
                "ProgramProgressPercent": ProgramProgressPercent,
                'ItemLabel': ChannelName,
                'ItemInfoVideo': ItemInfoVideo,
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart},
                'ItemAction': ItemAction
            }
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
