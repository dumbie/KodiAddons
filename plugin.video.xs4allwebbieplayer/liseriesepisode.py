import dlseriesepisode
import dlseriesprogram
import func
import getset
import lifunc
import metadatacombine
import metadatainfo
import path
import var

def list_load_vod_combined(selectedProgramId, selectedPictureUrl, listContainer=None):
    try:
        #Download episodes
        downloadResult = dlseriesepisode.download(selectedProgramId)
        if downloadResult == None:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_vod_append(listContainerSort, downloadResult, selectedPictureUrl, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: (func.to_type(int, x[1].getProperty('ProgramSeasonInt'), 0), func.to_type(int, x[1].getProperty('ProgramEpisodeInt'), 0)))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_vod_append(listContainer, downloadResult, selectedPictureUrl, remoteMode=False):
    for program in downloadResult["resultObj"]["containers"]:
        try:
            #Load program basics
            EpisodeTitleRaw = metadatainfo.episodetitle_from_json_metadata(program)
            ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
            ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramSeasonInt') == ProgramSeasonInt and x[1].getProperty('ProgramEpisodeInt') == ProgramEpisodeInt and x[1].getProperty('ProgramName').lower() == EpisodeTitleRaw.lower())
            if duplicateProgram == True: continue

            #Check if program playback is allowed
            if metadatainfo.check_vod_playback_allowed_from_json_metadata(program) == False: continue

            #Load program details
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTitleRaw = metadatainfo.programtitle_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_vod(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)

            #Set item icons
            iconDefault = path.icon_vod(selectedPictureUrl)
            iconFanart = path.icon_fanart()

            #Set item details
            jsonItem = {
                'StreamAssetId': StreamAssetId,
                'ProgramId': ProgramId,
                "ProgramName": EpisodeTitleRaw,
                'ProgramDetails': ProgramDetails,
                "ProgramSeasonInt": ProgramSeasonInt,
                "ProgramEpisodeInt": ProgramEpisodeInt,
                "ProgramAvailability": ProgramAvailability,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': EpisodeTitleRaw,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramTitleRaw, 'Title': EpisodeTitleRaw, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart},
                'ItemAction': 'play_stream_vod'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_combined(selectedProgramName, selectedPictureUrl, listContainer=None):
    try:
        #Download episodes
        downloadResult = dlseriesprogram.download_program()
        if downloadResult == False:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_program_append(listContainerSort, selectedProgramName, selectedPictureUrl, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: (func.to_type(int, x[1].getProperty('ProgramSeasonInt'), 0), func.to_type(int, x[1].getProperty('ProgramEpisodeInt'), 0)))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_program_append(listContainer, selectedProgramName, selectedPictureUrl, remoteMode=False):
    for program in var.SeriesProgramDataJson["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramTitleRaw = metadatainfo.programtitle_from_json_metadata(program)
            EpisodeTitleRaw = metadatainfo.episodetitle_from_json_metadata(program)
            ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
            ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)

            #Check if program matches serie
            checkSerie1 = ProgramTitleRaw.lower()
            checkSerie2 = selectedProgramName.lower()
            if checkSerie1 != checkSerie2: continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramSeasonInt') == ProgramSeasonInt and x[1].getProperty('ProgramEpisodeInt') == ProgramEpisodeInt and x[1].getProperty('ProgramName').lower() == EpisodeTitleRaw.lower())
            if duplicateProgram == True: continue

            #Check if program playback is allowed
            if metadatainfo.check_program_playback_allowed_from_json_metadata(program) == False: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_program(program)
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)

            #Set item icons
            iconDefault = path.icon_epg(selectedPictureUrl)
            iconFanart = path.icon_fanart()

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'ChannelId': ChannelId,
                'ProgramId': ProgramId,
                "ProgramTimeStartDateTime": str(ProgramTimeStartDateTime),
                "ProgramName": EpisodeTitleRaw,
                "ProgramSeasonInt": ProgramSeasonInt,
                "ProgramEpisodeInt": ProgramEpisodeInt,
                "ProgramWeek": 'true',
                'ProgramDetails': ProgramDetails,
                "ProgramAvailability": ProgramAvailability,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': EpisodeTitleRaw,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramTitleRaw, 'Title': EpisodeTitleRaw, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart},
                'ItemAction': 'play_stream_program'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
