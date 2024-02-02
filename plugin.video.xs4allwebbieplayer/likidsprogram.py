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
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Add vod program
            listAction = 'load_kids_episodes_vod'
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails})
            iconProgramType = path.icon_addon('series')
            iconStreamType = path.icon_addon('vod')
            iconProgram = path.icon_vod(PictureUrl)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType})
            dirIsfolder = True
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + ProgramId + var.splitchar + ProgramName + var.splitchar + PictureUrl
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer):
    for program in var.KidsProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if serie is already added
            tupleContainer = [x[1] for x in listContainer]
            if lifunc.search_programname_listarray(tupleContainer, ProgramName) != None: continue

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Check if program is serie or movie
            ContentSubtype = metadatainfo.contentSubtype_from_json_metadata(program)
            if ContentSubtype == "VOD":
                listAction = 'play_stream_program'
                dirIsfolder = False
                iconProgramType = path.icon_addon('movies')
                ProgramDuration = True
                ProgramDescription = metadatacombine.program_description_extended(program)
                ProgramAvailability = metadatainfo.available_time_program(program)
            else:
                listAction = 'load_kids_episodes_program'
                dirIsfolder = True
                iconProgramType = path.icon_addon('series')
                ProgramDuration = False
                ProgramDescription = ""
                ProgramAvailability = ""

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, ProgramDuration, True, False, False, False, True)

            #Add week program
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('SeriesId', SeriesId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails})
            iconStreamType = path.icon_addon('calendarweek')
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType, 'image3': iconChannel})
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + ProgramId + var.splitchar + ProgramName + var.splitchar + PictureUrl
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
