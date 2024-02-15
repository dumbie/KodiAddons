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
        #Download movies
        downloadResultVod = download.download_vod_movies(forceUpdate)
        downloadResultProgram = download.download_search_movies(forceUpdate)
        if downloadResultVod == False or downloadResultProgram == False:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, "Films downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_program(listContainerSort)
        list_load_vod(listContainerSort)

        #Sort items in list
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, "Films downloaden mislukt.", notificationIcon, 2500, False)
        return False

def list_load_vod(listContainer):
    for program in var.MoviesVodDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Check if content is pay to play
            TechnicalPackageIds = metadatainfo.technicalPackageIds_from_json_metadata(program)
            if metadatainfo.program_check_paytoplay(TechnicalPackageIds): continue

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, False, False, True)

            #Check if movie is already added
            tupleContainer = [x[1] for x in listContainer]
            if lifunc.search_program_namedetails_listarray(tupleContainer, ProgramName, ProgramDetails) != None: continue

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_vod(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Set item icons
            iconDefault = path.icon_vod(PictureUrl)
            iconStreamType = path.icon_addon('vod')

            #Set item details
            jsonItem = {
                'StreamAssetId': StreamAssetId,
                'ProgramId': ProgramId,
                "ProgramName": ProgramName,
                "ProgramDetails": ProgramDetails,
                "ProgramAvailability": ProgramAvailability,
                "ProgramDescription": ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'image1': iconStreamType},
                'ItemAction': 'play_stream_vod'
            }
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + func.object_to_picklestring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program(listContainer):
    for program in var.MoviesProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.episodetitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, False, False, True)

            #Check if movie is already added
            tupleContainer = [x[1] for x in listContainer]
            if lifunc.search_program_namedetails_listarray(tupleContainer, ProgramName, ProgramDetails) != None: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramAvailability = metadatainfo.available_time_program(program)
            StartOffset = str(int(var.addon.getSetting('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Set item icons
            iconDefault = path.icon_epg(PictureUrl)
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
                'ItemInfo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDescription},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'image1': iconStreamType, 'image2': iconChannel},
                'ItemAction': 'play_stream_program'
            }
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + func.object_to_picklestring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
