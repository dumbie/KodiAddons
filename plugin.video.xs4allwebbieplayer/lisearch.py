import xbmcgui
import dlsearch
import func
import getset
import lifunc
import metadatacombine
import metadatainfo
import path
import var

def list_load_combined(listContainer=None, forceUpdate=True):
    try:
        #Download search programs
        downloadResult = dlsearch.download(var.SearchTermDownload, forceUpdate)
        if downloadResult == False:
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Sort list items
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramTimeStartDateTime'), reverse=True)

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
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch1 = func.search_filter_string(ProgramName)
                searchMatch2 = func.search_filter_string(EpisodeTitle)
                searchResultFound = var.SearchTermResult in searchMatch1 or var.SearchTermResult in searchMatch2
                if searchResultFound == False: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_program(program)

            #Load program timing
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program timing
            ProgramTiming = metadatacombine.program_timing_vod(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Update program name string
            ProgramNameList = ProgramName + ' ' + ProgramDetails
            ProgramNameDesc = ProgramName + '\n' + ProgramDetails

            #Update program availability
            ProgramNameDesc += '\n' + ProgramAvailability

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            listItem = xbmcgui.ListItem()
            listItem.setProperty('StartOffset', StartOffset)
            listItem.setProperty('ItemAction', 'play_stream_program')
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listItem.setProperty("ProgramName", ProgramNameList)
            listItem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listItem.setProperty("ProgramNameRaw", ProgramName)
            listItem.setProperty("ProgramDetails", ProgramTiming)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramTiming, 'Title': ProgramName, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault})
            listContainer.append(listItem)
        except:
            continue
