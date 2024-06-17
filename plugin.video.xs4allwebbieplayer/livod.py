from datetime import datetime, timedelta
import dlchannelweb
import dlepg
import favoritefunc
import func
import getset
import hiddenfunc
import lifunc
import metadatacombine
import metadatainfo
import path
import var

def list_load_days(listContainer=None):
    try:
        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None

        #Set item icons
        iconDefault = path.resources('resources/skins/default/media/common/calendar.png')
        iconFanart = path.icon_fanart()

        #Set epg days
        for x in range(var.VodDayOffsetPast):
            try:
                #Set day string
                dateTime = func.datetime_from_day_offset(-x)
                dayString = func.day_string_from_datetime(dateTime)

                #Set item details
                jsonItem = {
                    'DateTime': str(dateTime),
                    'ItemLabel': dayString,
                    'ItemInfoVideo': {'Title': dayString},
                    'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart},
                    'ItemAction': 'load_vod_programs'
                }
                dirIsfolder = True
                dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
                listItem = lifunc.jsonitem_to_listitem(jsonItem)
                listContainerSort.append((dirUrl, listItem, dirIsfolder))
            except:
                continue

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_combined(listContainer=None, dateTime=''):
    try:
        #Update variables
        if func.string_isnullorempty(dateTime) == False:
            var.VodDayLoadDateTime = func.datetime_from_string(dateTime, '%Y-%m-%d %H:%M:%S')

        #Download channels
        downloadResultChannels = dlchannelweb.download()
        if downloadResultChannels == False:
            return False

        #Download programs
        downloadResult = dlepg.download(var.VodDayLoadDateTime)
        if downloadResult == None:
            return False

        #Load favorite and hidden channels
        favoritefunc.favorite_television_json_load()
        hiddenfunc.hidden_television_json_load()

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, downloadResult, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStartDateTime'), reverse=True)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, downloadResult, remoteMode=False):
    for channel in downloadResult['resultObj']['containers']:
        list_load_append_program(listContainer, channel, remoteMode)

def list_load_append_program(listContainer, downloadResult, remoteMode=False):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in downloadResult['containers']:
        try:
            #Load program basics
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)
            EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True)

            if func.string_isnullorempty(var.SearchTermResult) == False:
                #Check if there are search results
                searchMatch1 = func.search_filter_string(ProgramNameRaw)
                searchMatch2 = func.search_filter_string(EpisodeTitle)
                searchResultFound = var.SearchTermResult in searchMatch1 or var.SearchTermResult in searchMatch2
                if searchResultFound == False: continue
            else:
                #Check if channel is marked as favorite
                if getset.setting_get('LoadChannelFavoritesOnly') == 'true' and favoritefunc.favorite_check_channel(ChannelId, 'FavoriteTelevision.js') == False: continue

            #Check if channel is hidden
            if hiddenfunc.hidden_check_channel(ChannelId, 'HiddenTelevision.js'): continue

            #Check if program vod playback is allowed
            contentOptionsArray = metadatainfo.contentOptions_from_json_metadata(program)
            if ('CATCHUP' in contentOptionsArray) == False: continue
            if ('TV_PREMIERE' in contentOptionsArray) == False: continue

            #Check if program has finished airing and processing
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)
            if dateTimeNow < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

            #Check if program is starting or ending on target day
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            if ProgramTimeStartDateTime.date() != var.VodDayLoadDateTime.date() and ProgramTimeEndDateTime.date() != var.VodDayLoadDateTime.date(): continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Load program timing
            ProgramDurationMinutes = int(metadatainfo.programdurationstring_from_json_metadata(program, False, False, False))
            ProgramDurationSeconds = ProgramDurationMinutes * 60

            #Combine program timing
            ProgramTiming = metadatacombine.program_timing_vod(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Update program name string
            ProgramNameList = ProgramNameRaw + ' ' + ProgramDetails
            ProgramNameDesc = ProgramNameRaw + '\n' + ProgramDetails

            #Set item icons
            iconDefault = path.icon_television(ExternalId)
            iconFanart = path.icon_fanart()

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'ChannelId': ChannelId,
                'ProgramId': ProgramId,
                "ProgramTimeStartDateTime": str(ProgramTimeStartDateTime),
                "ProgramName": ProgramNameList,
                "ProgramNameDesc": ProgramNameDesc,
                "ProgramNameRaw": ProgramNameRaw,
                "ProgramDetails": ProgramTiming,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': ProgramNameRaw,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramTiming, 'Title': ProgramNameRaw, 'Plot': ProgramDescription, 'Duration': ProgramDurationSeconds},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart},
                'ItemAction': 'play_stream_program'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
