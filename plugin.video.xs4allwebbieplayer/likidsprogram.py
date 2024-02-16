import download
import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load_combined(listContainer=None, forceUpdate=False):
    try:
        #Download programs
        downloadResultVod = download.download_vod_kids(forceUpdate)
        downloadResultProgram = download.download_search_kids(forceUpdate)
        if downloadResultVod == False or downloadResultProgram == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, "Kids downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_program_append(listContainerSort)
        list_load_vod_append(listContainerSort)

        #Sort items in list
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_vod_append(listContainer):
    for program in var.KidsVodDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
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
                'ItemInfo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'image1': iconStreamType, 'image2': iconProgramType},
                'ItemAction': 'load_kids_episodes_vod'
            }
            dirIsfolder = True
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer):
    for program in var.KidsProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Check if program is already added
            duplicateProgram = any(True for x in listContainer if x[1].getProperty('ProgramName').lower() == ProgramName.lower())
            if duplicateProgram == True: continue

            #Check if program is serie or movie
            ContentSubtype = metadatainfo.contentSubtype_from_json_metadata(program)
            if ContentSubtype == "VOD":
                listAction = 'play_stream_program'
                dirIsfolder = False
                iconProgramType = path.icon_addon('movies')
                ProgramDuration = True
                ProgramDescription = metadatacombine.program_description_extended(program)
                ProgramAvailability = metadatainfo.available_time_program(program)
                StartOffset = str(int(func.setting_get('PlayerSeekOffsetStartMinutes')) * 60)
            else:
                listAction = 'load_kids_episodes_program'
                dirIsfolder = True
                iconProgramType = path.icon_addon('series')
                ProgramDuration = False
                ProgramDescription = ""
                ProgramAvailability = ""
                StartOffset = ""

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, ProgramDuration, True, False, False, False, True)

            #Set item icons
            iconDefault = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            iconStreamType = path.icon_addon('calendarweek')

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'PictureUrl': PictureUrl,
                'SeriesId': SeriesId,
                'ProgramId': ProgramId,
                "ProgramName": ProgramName,
                "ProgramWeek": 'true',
                'ProgramDetails': ProgramDetails,
                "ProgramAvailability": ProgramAvailability,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'image1': iconStreamType, 'image2': iconProgramType, 'image3': iconChannel},
                'ItemAction': listAction
            }
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
