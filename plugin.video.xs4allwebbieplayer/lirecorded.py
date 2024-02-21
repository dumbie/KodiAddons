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
        #Download recordings
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, "Opnames downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStart'), reverse=True)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    for program in var.RecordingEventDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramNameRaw)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Load and check recording status
            assetsArray = metadatainfo.stream_assets_array_from_json_metadata(program)
            if assetsArray != []:
                assetStatus = metadatainfo.stream_assetstatus_from_assets_array(assetsArray)
                if assetStatus == 'ScheduleSuccess' or assetStatus == 'RescheduleSuccess':
                    continue
                elif assetStatus == 'RecordFailed':
                    ProgramNameRaw = '(Opname mislukt) ' + ProgramNameRaw
            else:
                ProgramNameRaw = '(Niet speelbaar) ' + ProgramNameRaw

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_recording(program)

            #Load program timing
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramTimeStartMinutes = (ProgramTimeStartDateTime.hour * 60) + ProgramTimeStartDateTime.minute
            ProgramDurationMinutes = metadatainfo.programdurationstring_from_json_metadata(program, False, False, False)
            ProgramDeltaTimeStart = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
            StartOffset = str(int(func.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program timing
            ProgramTiming = metadatacombine.program_timing_vod(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, False, True)

            #Update program name string
            ProgramNameList = ProgramNameRaw + ' [COLOR gray]' + ProgramDetails + '[/COLOR]'
            ProgramNameDesc = ProgramNameRaw + '\n' + ProgramDetails

            #Update program availability
            ProgramNameDesc += '\n' + ProgramAvailability

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            jsonItem = {
                'StartOffset': StartOffset,
                'StreamAssetId': StreamAssetId,
                'ProgramRecordEventId': ProgramRecordEventId,
                'ProgramTimeStart': str(ProgramTimeStartDateTime),
                'ProgramDeltaTimeStart': ProgramDeltaTimeStart,
                "ProgramName": ProgramNameList,
                "ProgramNameDesc": ProgramNameDesc,
                "ProgramNameRaw": ProgramNameRaw,
                "ProgramDetails": ProgramTiming,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': ProgramNameRaw,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramNameRaw, 'Plot': ProgramDescription, 'Size': ProgramDurationMinutes, 'Duration': ProgramTimeStartMinutes},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_recorded'
            }
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
