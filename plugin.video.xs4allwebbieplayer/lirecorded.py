from datetime import datetime, timedelta
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
        downloadResultProfile = download.download_recording_profile(forceUpdate)
        downloadResultEvent = download.download_recording_event(forceUpdate)
        if downloadResultProfile == False or downloadResultEvent == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, "Opnames downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Sort list items
        listContainerSort.sort(key=lambda x: int(x[1].getProperty('ProgramTimeStart')), reverse=True)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in var.RecordingEventDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

            #Check if there are search results
            if var.SearchTermCurrent != '':
                searchMatch = func.search_filter_string(ProgramNameRaw)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Check if program has finished airing and processing
            if dateTimeNow < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

            #Check if program is available for streaming
            AssetsLength = len(program['assets'])
            if AssetsLength > 0:
                AssetsStatus = str(program['assets'][0]['status'])
                if AssetsStatus == 'RecordFailed':
                    ProgramNameRaw = '(Opname mislukt) ' + ProgramNameRaw
                elif AssetsStatus == 'ScheduleSuccess':
                    ProgramNameRaw = '(Geplande opname) ' + ProgramNameRaw    
            else:
                ProgramNameRaw = '(Niet speelbaar) ' + ProgramNameRaw

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.available_time_recording(program)

            #Load program timing
            ProgramTimeStart = str(metadatainfo.programstarttime_from_json_metadata(program))
            ProgramDeltaTimeStart = str(metadatainfo.programstartdeltatime_from_json_metadata(program))

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

            #Add program
            listAction = 'play_stream_recorded'
            listItem = xbmcgui.ListItem(ProgramNameRaw)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('StreamAssetId', StreamAssetId)
            listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
            listItem.setProperty('ProgramTimeStart', ProgramTimeStart)
            listItem.setProperty('ProgramDeltaTimeStart', ProgramDeltaTimeStart)
            listItem.setProperty("ProgramName", ProgramNameList)
            listItem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listItem.setProperty("ProgramNameRaw", ProgramNameRaw)
            listItem.setProperty("ProgramDetails", ProgramTiming)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramNameRaw, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + StreamAssetId + var.splitchar + ProgramRecordEventId + var.splitchar + ProgramDeltaTimeStart
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
