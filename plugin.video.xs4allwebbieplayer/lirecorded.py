from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in var.RecordingEventDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ProgramNameRaw)
                searchResultFound = var.SearchChannelTerm in searchMatch
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
            ProgramAssetId = metadatainfo.stream_assetid_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.recording_available_time(program)

            #Load program timing
            ProgramStartTime = str(metadatainfo.programstarttime_from_json_metadata(program))
            ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(program))

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
            listItem = xbmcgui.ListItem(ProgramNameRaw)
            listItem.setProperty('Action', 'play_stream_recorded')
            listItem.setProperty('ProgramAssetId', ProgramAssetId)
            listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
            listItem.setProperty('ProgramStartTime', ProgramStartTime)
            listItem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
            listItem.setProperty("ProgramName", ProgramNameList)
            listItem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listItem.setProperty("ProgramNameRaw", ProgramNameRaw)
            listItem.setProperty("ProgramDetails", ProgramTiming)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramNameRaw, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.append(listItem)
        except:
            continue
