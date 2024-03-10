import dlkidsprogram
import func
import getset
import lifunc
import metadatacombine
import metadatainfo
import path
import var

def list_load_combined(listContainer=None):
    try:
        #Download programs
        downloadResultVod = dlkidsprogram.download_vod()
        downloadResultProgram = dlkidsprogram.download_program()
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
    for program in var.KidsVodDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramName').lower() == ProgramName.lower())
            if duplicateProgram == True: continue

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Set item icons
            iconDefault = path.icon_vod(PictureUrl)
            iconProgramType = path.icon_addon('series')
            iconStreamType = path.icon_addon('vod')

            #Set item details
            jsonItem = {
                'PictureUrl': PictureUrl,
                'ProgramId': ProgramId,
                "ProgramName": ProgramName,
                'ProgramDetails': ProgramDetails,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'tvshow', 'Genre': ProgramDetails},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'image1': iconStreamType, 'image2': iconProgramType},
                'ItemAction': 'load_kids_episodes_vod'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer, remoteMode=False):
    for program in var.KidsProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramName').lower() == ProgramName.lower())
            if duplicateProgram == True: continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramSeriesId = metadatainfo.seriesId_from_json_metadata(program)

            #Check if program is serie or movie
            ContentSubtype = metadatainfo.contentSubtype_from_json_metadata(program)
            if ContentSubtype == "VOD":
                ProgramDetails = metadatacombine.program_details(program, True, True, True, False, False, False, True)
                ProgramDescription = metadatacombine.program_description_extended(program)
                ProgramAvailability = metadatainfo.available_time_program(program)
                ItemAction = 'play_stream_program'
                ItemInfoVideo = {'MediaType': 'movie', 'Genre': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDescription}
                dirIsfolder = False
                iconProgramType = path.icon_addon('movies')
                StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)
            else:
                ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)
                ProgramDescription = ""
                ProgramAvailability = ""
                ItemAction = 'load_kids_episodes_program'
                ItemInfoVideo = {'MediaType': 'tvshow', 'Genre': ProgramDetails}
                dirIsfolder = True
                iconProgramType = path.icon_addon('series')
                StartOffset = ""

            #Set item icons
            iconDefault = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            iconStreamType = path.icon_addon('calendarweek')

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'PictureUrl': PictureUrl,
                'ProgramId': ProgramId,
                'ProgramSeriesId': ProgramSeriesId,
                "ProgramName": ProgramName,
                "ProgramWeek": 'true',
                'ProgramDetails': ProgramDetails,
                "ProgramAvailability": ProgramAvailability,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': ItemInfoVideo,
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'image1': iconStreamType, 'image2': iconProgramType, 'image3': iconChannel},
                'ItemAction': ItemAction
            }
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
