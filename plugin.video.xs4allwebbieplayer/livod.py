from datetime import datetime, timedelta
import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in var.VodDayDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)
            EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch1 = func.search_filter_string(ProgramNameRaw)
                searchMatch2 = func.search_filter_string(EpisodeTitle)
                searchResultFound = var.SearchChannelTerm in searchMatch1 or var.SearchChannelTerm in searchMatch2
                if searchResultFound == False: continue

            #Check if program has finished airing and processing
            if dateTimeNow < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

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
            ProgramNameList = ProgramNameRaw + ' [COLOR gray]' + ProgramDetails + '[/COLOR]'
            ProgramNameDesc = ProgramNameRaw + '\n' + ProgramDetails

            #Add program
            listAction = 'play_stream_program'
            listItem = xbmcgui.ListItem(ProgramNameRaw)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listItem.setProperty("ProgramName", ProgramNameList)
            listItem.setProperty("ProgramNameDesc", ProgramNameDesc)
            listItem.setProperty("ProgramNameRaw", ProgramNameRaw)
            listItem.setProperty("ProgramDetails", ProgramTiming)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramNameRaw, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            lifunc.auto_add_item(listItem, listContainer, dirUrl=listAction+'='+ProgramId)
        except:
            continue
    lifunc.auto_end_items()
