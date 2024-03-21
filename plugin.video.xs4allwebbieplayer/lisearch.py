import xbmcgui
import dlsearch
import func
import getset
import lifunc
import metadatacombine
import metadatainfo
import path
import searchdialog
import var

def list_load_remote():
    #Show search dialog
    searchDialogTerm = searchdialog.search_keyboard('')

    #Check search term
    if searchDialogTerm.cancelled == True:
        return

    #Check search term
    if func.string_isnullorempty(searchDialogTerm.string) == True:
        notificationIcon = path.resources('resources/skins/default/media/common/search.png')
        xbmcgui.Dialog().notification(var.addonname, 'Leeg zoek term', notificationIcon, 2500, False)
        return

    #Update search term
    var.SearchTermDownload = searchDialogTerm.string

    #List search items
    list_load_combined()

def list_load_combined(listContainer=None, forceUpdate=True):
    try:
        #Download search programs
        downloadResult = dlsearch.download(var.SearchTermDownload, forceUpdate)
        if downloadResult == False:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStartDateTime'), reverse=True)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
    for program in var.SearchProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)
            EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch1 = func.search_filter_string(ProgramNameRaw)
                searchMatch2 = func.search_filter_string(EpisodeTitle)
                searchResultFound = var.SearchTermResult in searchMatch1 or var.SearchTermResult in searchMatch2
                if searchResultFound == False: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_program(program)

            #Load program timing
            ProgramDurationMinutes = int(metadatainfo.programdurationstring_from_json_metadata(program, False, False, False))
            ProgramDurationSeconds = ProgramDurationMinutes * 60
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program timing
            ProgramTiming = metadatacombine.program_timing_vod(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Update program name string
            ProgramNameList = ProgramNameRaw + ' ' + ProgramDetails
            ProgramNameDesc = ProgramNameRaw + '\n' + ProgramDetails

            #Update program availability
            ProgramNameDesc += '\n' + ProgramAvailability

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'ChannelId': ChannelId,
                "ProgramId": ProgramId,
                "ProgramTimeStartDateTime": str(ProgramTimeStartDateTime),
                "ProgramName": ProgramNameList,
                "ProgramNameDesc": ProgramNameDesc,
                "ProgramNameRaw": ProgramNameRaw,
                "ProgramDetails": ProgramTiming,
                "ProgramDescription": ProgramDescription,
                'ItemLabel': ProgramNameRaw,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramTiming, 'Title': ProgramNameRaw, 'Plot': ProgramDescription, 'Duration': ProgramDurationSeconds},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_program'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
