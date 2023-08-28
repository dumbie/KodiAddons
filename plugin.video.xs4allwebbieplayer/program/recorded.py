from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.ChannelsDataJsonRecordingEvent['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False: continue

            #Check if program has finished airing and processing
            if datetime.now() < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

            #Check if program is available for streaming
            AssetsLength = len(program['assets'])
            if AssetsLength > 0:
                AssetsStatus = str(program['assets'][0]['status'])
                if AssetsStatus == 'RecordFailed':
                    ProgramName = '(Opname mislukt) ' + ProgramName
                elif AssetsStatus == 'ScheduleSuccess':
                    ProgramName = '(Geplande opname) ' + ProgramName    
            else:
                ProgramName = '(Niet speelbaar) ' + ProgramName

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramAssetId = metadatainfo.get_stream_assetid(program['assets'])
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.recording_available_time(program)

            #Load program timing
            ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(program))

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

            #Add program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_stream')
            listitem.setProperty('ProgramAssetId', ProgramAssetId)
            listitem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
            listitem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
            listitem.setProperty("ProgramName", ProgramNameList)
            listitem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listitem.setProperty("ProgramNameRaw", ProgramName)
            listitem.setProperty("ProgramDetails", ProgramTiming)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Genre': 'Opname', 'Plot': ProgramDescription})
            listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.addItem(listitem)
        except:
            continue
