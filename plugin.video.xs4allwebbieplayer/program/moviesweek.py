from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.MovieSearchDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchFilterTerm in searchMatch
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
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_stream_week')
            listitem.setProperty('ChannelId', ChannelId)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty("ProgramWeek", 'true')
            listitem.setProperty("ProgramDetails", ProgramDetails)
            listitem.setProperty("ProgramAvailability", ProgramAvailability)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Films', 'Plot': ProgramDescription})
            iconStreamType = "common/calendarweek.png"
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconChannel})
            listContainer.append(listitem)
        except:
            continue
