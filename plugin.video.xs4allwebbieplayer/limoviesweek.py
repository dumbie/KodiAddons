import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.MoviesProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramAvailability = metadatainfo.vod_week_available_time(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, False, False, True)
            ProgramTitle = ProgramName + " " + ProgramDetails

            #Add week program
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', 'play_stream_program')
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty("ProgramDetails", ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Films', 'Plot': ProgramDescription})
            iconStreamType = "common/calendarweek.png"
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconChannel})
            listContainer.append(listItem)
        except:
            continue
