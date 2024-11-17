import dlmovies
import func
import getset
import lifunc
import metadatacombine
import metadatainfo
import path
import var

def list_load_combined(listContainer=None):
    try:
        #Download movies
        downloadResultVod = dlmovies.download_vod()
        downloadResultProgram = dlmovies.download_program()
        if downloadResultVod == False or downloadResultProgram == False:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_program_append(listContainerSort, remoteMode)
        list_load_vod_append(listContainerSort, remoteMode)

        #Sort items in list
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_vod_append(listContainer, remoteMode=False):
    for program in var.MoviesVodDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Check if program is already added
            ProgramYear = metadatainfo.programyear_from_json_metadata(program, False)
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramName').lower() == ProgramName.lower() and x[1].getProperty('ProgramYear') == ProgramYear)
            if duplicateProgram == True: continue

            #Check if program playback is allowed
            if metadatainfo.check_vod_playback_allowed_from_json_metadata(program) == False: continue

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, False, False, True)

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_vod(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Set item icons
            iconDefault = path.icon_vod(PictureUrl)
            iconFanart = path.icon_fanart()
            iconStreamType = path.icon_addon('vod')

            #Set item details
            jsonItem = {
                'StreamAssetId': StreamAssetId,
                'ProgramId': ProgramId,
                "ProgramName": ProgramName,
                "ProgramYear": ProgramYear,
                "ProgramDetails": ProgramDetails,
                "ProgramAvailability": ProgramAvailability,
                "ProgramDescription": ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart, 'image1': iconStreamType},
                'ItemAction': 'play_stream_vod'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer, remoteMode=False):
    for program in var.MoviesProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.episodetitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramName').lower() == ProgramName.lower())
            if duplicateProgram == True: continue

            #Check if program playback is allowed
            if metadatainfo.check_program_playback_allowed_from_json_metadata(program) == False: continue

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, False, False, True)

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_program(program)
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Set item icons
            iconDefault = path.icon_epg(PictureUrl)
            iconFanart = path.icon_fanart()
            iconStreamType = path.icon_addon('calendarweek')
            iconChannel = path.icon_television(ExternalId)

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'ChannelId': ChannelId,
                'ProgramId': ProgramId,
                "ProgramTimeStartDateTime": str(ProgramTimeStartDateTime),
                "ProgramName": ProgramName,
                "ProgramWeek": 'true',
                "ProgramDetails": ProgramDetails,
                "ProgramAvailability": ProgramAvailability,
                "ProgramDescription": ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart, 'image1': iconStreamType, 'image2': iconChannel},
                'ItemAction': 'play_stream_program'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
