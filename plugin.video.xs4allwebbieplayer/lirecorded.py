import dlrecordingevent
import func
import getset
import lifunc
import metadatacombine
import metadatainfo
import path
import recordingfunc
import var

def list_load_combined(listContainer=None, forceUpdate=False):
    try:
        #Download recordings
        downloadResult = dlrecordingevent.download(forceUpdate)
        if downloadResult == False:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStart'), reverse=True)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
    for program in var.RecordingEventDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)
            ProgramName = ProgramNameRaw

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ProgramNameRaw)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Load and check recording status
            recordingStatus = recordingfunc.get_status(program)
            if recordingStatus == 'ScheduleSuccess' or recordingStatus == 'RescheduleSuccess' or recordingStatus == 'NoAssets':
                continue
            elif recordingStatus == 'RecordFailed':
                ProgramName = '(Opname mislukt) ' + ProgramName

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_recording(program)

            #Load program timing
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramDurationMinutes = int(metadatainfo.programdurationstring_from_json_metadata(program, False, False, False))
            ProgramDurationSeconds = ProgramDurationMinutes * 60
            ProgramDeltaTimeStart = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
            StartOffset = str(int(getset.setting_get('PlayerSeekOffsetStartMinutes')) * 60)

            #Combine program timing
            ProgramTiming = metadatacombine.program_timing_vod(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Update program name string
            ProgramNameList = ProgramName + ' [COLOR gray]' + ProgramDetails + '[/COLOR]'
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
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramTiming, 'Title': ProgramName, 'Plot': ProgramDescription, 'Duration': ProgramDurationSeconds},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_recorded'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
