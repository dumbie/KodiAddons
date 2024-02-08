import download
import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load_combined(listContainer=None, forceUpdate=True):
    try:
        #Download search programs
        downloadResult = download.download_search_program(var.SearchDownloadSearchTerm, forceUpdate)
        if downloadResult == False:
            notificationIcon = path.resources('resources/skins/default/media/common/search.png')
            xbmcgui.Dialog().notification(var.addonname, "Zoek downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    for program in var.SearchProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True)

            #Check if there are search results
            if var.SearchTermCurrent != '':
                searchMatch1 = func.search_filter_string(ProgramName)
                searchMatch2 = func.search_filter_string(EpisodeTitle)
                searchResultFound = var.SearchTermCurrent in searchMatch1 or var.SearchTermCurrent in searchMatch2
                if searchResultFound == False: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_program(program)

            #Load program timing
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)

            #Combine program timing
            ProgramTiming = metadatacombine.program_timing_vod(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Update program name string
            ProgramNameList = ProgramName + ' [COLOR gray]' + ProgramDetails + '[/COLOR]'
            ProgramNameDesc = ProgramName + '\n' + ProgramDetails

            #Update program availability
            ProgramNameDesc += '\n' + ProgramAvailability

            #Add program
            listItem = xbmcgui.ListItem()
            listItem.setProperty('Action', 'play_stream')
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listItem.setProperty("ProgramName", ProgramNameList)
            listItem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listItem.setProperty("ProgramNameRaw", ProgramName)
            listItem.setProperty("ProgramDetails", ProgramTiming)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'Genre': 'Zoeken', 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.append(listItem)
        except:
            continue
