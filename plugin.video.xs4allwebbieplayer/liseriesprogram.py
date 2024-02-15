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
        downloadResultVod = download.download_vod_series(forceUpdate)
        downloadResultProgram = download.download_search_series(forceUpdate)
        if downloadResultVod == False or downloadResultProgram == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, "Series downloaden mislukt.", notificationIcon, 2500, False)
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
    for program in var.SeriesVodDataJson['resultObj']['containers']:
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
            iconStreamType = path.icon_addon('vod')

            #Set item details
            jsonItem = {
                'PictureUrl': PictureUrl,
                'ProgramId': ProgramId,
                "ProgramName": ProgramName,
                'ProgramDetails': ProgramDetails,
                'ItemLabel': ProgramName,
                'ItemInfo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'image1': iconStreamType},
                'ItemAction': 'load_series_episodes_vod'
            }
            dirIsfolder = True
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer):
    for program in var.SeriesProgramDataJson['resultObj']['containers']:
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
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Set item icons
            iconDefault = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            iconStreamType = path.icon_addon('calendarweek')

            #Set item details
            jsonItem = {
                'PictureUrl': PictureUrl,
                'SeriesId': SeriesId,
                'ProgramId': ProgramId,
                "ProgramName": ProgramName,
                "ProgramWeek": 'true',
                'ProgramDetails': ProgramDetails,
                'ItemLabel': ProgramName,
                'ItemInfo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'image1': iconStreamType, 'image2': iconChannel},
                'ItemAction': 'load_series_episodes_program'
            }
            dirIsfolder = True
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
