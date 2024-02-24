import xbmcgui
import download
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
        downloadResult = download.download_vod_series_season(selectedProgramId)
        if downloadResult == None:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, "Afleveringen downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_vod_append(listContainerSort, downloadResult, selectedPictureUrl)

        #Sort list items
        listContainerSort.sort(key=lambda x: (int(x[1].getProperty('ProgramSeasonInt')), int(x[1].getProperty('ProgramEpisodeInt'))))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_program_combined(selectedProgramName, selectedPictureUrl, listContainer=None):
    try:
        #Download episodes
        downloadResult = download.download_search_kids()
        if downloadResult == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, "Afleveringen downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_program_append(listContainerSort, selectedProgramName, selectedPictureUrl)

        #Sort list items
        listContainerSort.sort(key=lambda x: (int(x[1].getProperty('ProgramSeasonInt')), int(x[1].getProperty('ProgramEpisodeInt'))))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_vod_append(listContainer, downloadedSeason, selectedPictureUrl):
    for program in downloadedSeason["resultObj"]["containers"]:
        try:
            #Load program basics
            TechnicalPackageIds = metadatainfo.technicalPackageIds_from_json_metadata(program)
            ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
            ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)

            #Check if content is pay to play
            if metadatainfo.program_check_paytoplay(TechnicalPackageIds): continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramSeasonInt') == ProgramSeasonInt and x[1].getProperty('ProgramEpisodeInt') == ProgramEpisodeInt)
            if duplicateProgram == True: continue

            #Load program details
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            EpisodeTitleRaw = metadatainfo.episodetitle_from_json_metadata(program)
            ProgramTitleRaw = metadatainfo.programtitle_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_vod(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)

            #Set item icons
            iconDefault = path.icon_vod(selectedPictureUrl)

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
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramTitleRaw, 'Tagline': ProgramDetails, 'Title': EpisodeTitleRaw, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_vod'
            }
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer, selectedProgramName, selectedPictureUrl):
    for program in var.KidsProgramDataJson["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramTitleRaw = metadatainfo.programtitle_from_json_metadata(program)
            ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
            ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)

            #Check if program matches serie
            checkSerie1 = ProgramTitleRaw.lower()
            checkSerie2 = selectedProgramName.lower()
            if checkSerie1 != checkSerie2: continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramSeasonInt') == ProgramSeasonInt and x[1].getProperty('ProgramEpisodeInt') == ProgramEpisodeInt)
            if duplicateProgram == True: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            EpisodeTitleRaw = metadatainfo.episodetitle_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_program(program)
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)

            #Set item icons
            iconDefault = path.icon_epg(selectedPictureUrl)

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
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramTitleRaw, 'Tagline': ProgramDetails, 'Title': EpisodeTitleRaw, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_program'
            }
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
