from datetime import datetime, timedelta
import dlchanneltelevision
import dlepg
import func
import lichanneltelevision
import lifunc
import metadatacombine
import metadatafunc
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

        #Set epg days
        for x in range(var.VodDayOffsetPast + var.EpgDaysOffsetFuture):
            try:
                #Set day string
                dateTime = func.datetime_from_day_offset(var.EpgDaysOffsetFuture - x)
                dayString = func.day_string_from_datetime(dateTime)

                #Set item details
                jsonItem = {
                    'DateTime': str(dateTime),
                    'ItemLabel': dayString,
                    'ItemInfoVideo': {'Title': dayString},
                    'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                    'ItemAction': 'load_epg_channels'
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

def list_load_channels(dateTime):
    try:
        #Update epg variables
        var.EpgCurrentLoadDateTime = func.datetime_from_string(dateTime, '%Y-%m-%d %H:%M:%S')

        #Load and add channels
        return lichanneltelevision.list_load_combined(epgMode=True)
    except:
        return False

def list_load_combined(listContainer=None, channelId=''):
    try:
        #Update variables
        if func.string_isnullorempty(channelId) == False:
            var.EpgCurrentChannelId = channelId

        #Download channels
        downloadResultChannels = dlchanneltelevision.download()
        if downloadResultChannels == False:
            return False

        #Download epg day
        downloadResultEpg = dlepg.download(var.EpgCurrentLoadDateTime)
        if downloadResultEpg == None:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        if func.string_isnullorempty(var.SearchTermResult):
            #Load programs for current channel on set day
            jsonEpgChannel = metadatafunc.search_channelid_jsonepg(downloadResultEpg, var.EpgCurrentChannelId)
            if jsonEpgChannel != None:
                list_load_append(listContainerSort, jsonEpgChannel, remoteMode)
        else:
            #Load programs for search term from all channels on set day
            for jsonEpgChannel in downloadResultEpg["resultObj"]["containers"]:
                list_load_append(listContainerSort, jsonEpgChannel, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStart'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, jsonEpgChannel, remoteMode=False):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in jsonEpgChannel['containers']:
        try:
            #Load program basics
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)

            #Check if program is starting or ending on target day
            if ProgramTimeStartDateTime.date() != var.EpgCurrentLoadDateTime.date() and ProgramTimeEndDateTime.date() != var.EpgCurrentLoadDateTime.date(): continue

            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ProgramNameRaw)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Load channel basics
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ChannelExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ChannelName = metadatainfo.channelName_from_json_metadata(program)

            #Load program details
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))
            ProgramDurationSeconds = metadatainfo.programdurationint_from_json_metadata(program) * 60
            ProgramDurationString = metadatainfo.programdurationstring_from_json_metadata(program, False, False, True)
            ProgramDescriptionDesc = 'Programmabeschrijving wordt geladen.'
            ProgramEpgList = 'Programmaduur wordt geladen'

            #Combine program description extended
            ProgramDescriptionRaw = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Check if the program is part of series
            ProgramSeriesId = metadatainfo.seriesId_from_json_metadata(program)

            #Check if current program is a rerun
            programRerunName = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramNameRaw.lower())
            programRerunDescription = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramDescriptionRaw.lower())
            if programRerunName or programRerunDescription:
                ProgramRerun = 'true'
            else:
                ProgramRerun = 'false'

            #Check if program vod playback is allowed
            contentOptionsArray = metadatainfo.contentOptions_from_json_metadata(program)
            if 'CATCHUP' in contentOptionsArray:
                ProgramIsCatchup = 'true'
            else:
                ProgramIsCatchup = 'false'

            #Check if program finished airing
            if ProgramProgressPercent >= 100:
                ProgramIsAvailable = ProgramIsCatchup
            else:
                ProgramIsAvailable = 'false'

            #Check if program is still to come
            if ProgramProgressPercent <= 0:
                ProgramIsUpcoming = 'true'
            else:
                ProgramIsUpcoming = 'false'

            #Check if program is currently airing
            if ProgramProgressPercent > 0 and ProgramProgressPercent < 100:
                ProgramIsAiring = 'true'
            else:
                ProgramIsAiring = 'false'

            if remoteMode == True:
                ProgramNameRaw = '[COLOR FF888888](' + ProgramTimeStartDateTime.strftime('%H:%M') + ')[/COLOR] ' + ProgramNameRaw

            #Set item icons
            iconDefault = path.icon_television(ChannelExternalId)

            #Set item details
            jsonItem = {
                'ExternalId': ChannelExternalId,
                'ChannelId': ChannelId,
                "ChannelName": ChannelName,
                "ProgramId": ProgramId,
                "ProgramName": ProgramNameRaw,
                "ProgramRerun": ProgramRerun,
                "ProgramIsCatchup": ProgramIsCatchup,
                "ProgramIsAvailable": ProgramIsAvailable,
                "ProgramIsUpcoming": ProgramIsUpcoming,
                "ProgramIsAiring": ProgramIsAiring,
                'ProgramDuration': ProgramDurationString,
                'ProgramSeriesId': ProgramSeriesId,
                "ProgramDescriptionRaw": ProgramDescriptionRaw,
                "ProgramDescriptionDesc": ProgramDescriptionDesc,
                "ProgramEpgList": ProgramEpgList,
                "ProgramDetails": ProgramDetails,
                "ProgramTimeStart": str(ProgramTimeStartDateTime),
                "ProgramTimeEnd": str(ProgramTimeEndDateTime),
                'ItemLabel': ProgramNameRaw,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Title': ProgramNameRaw, 'Plot': ProgramDescriptionRaw, 'Duration': ProgramDurationSeconds},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'action_epg'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
