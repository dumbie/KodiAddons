from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.VodCurrentDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch1 = func.search_filter_string(ProgramName)
                searchMatch2 = func.search_filter_string(EpisodeTitle)
                searchResultFound = var.SearchFilterTerm in searchMatch1 or var.SearchFilterTerm in searchMatch2
                if searchResultFound == False: continue

            #Check if program has finished airing and processing
            if datetime.now() < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

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
            ProgramNameList = ProgramName + ' ' + ProgramDetails
            ProgramNameDesc = ProgramName + '\n' + ProgramDetails

            #Add program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_stream')
            listitem.setProperty('ChannelId', ChannelId)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listitem.setProperty("ProgramName", ProgramNameList)
            listitem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listitem.setProperty("ProgramNameRaw", ProgramName)
            listitem.setProperty("ProgramDetails", ProgramTiming)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Genre': 'Programma Gemist', 'Plot': ProgramDescription})
            listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.addItem(listitem)
        except:
            continue
