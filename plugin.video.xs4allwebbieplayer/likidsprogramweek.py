import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.KidsSearchDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

            #Check if serie is already added
            if lifunc.search_programname_listarray(listContainer, ProgramName) != None: continue

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Check if program is serie or movie
            ContentSubtype = metadatainfo.contentSubtype_from_json_metadata(program)
            if ContentSubtype == "VOD":
                ProgramAction = 'play_stream_program'
                iconProgramType = "common/movies.png"
                ProgramDuration = True
                ProgramDescription = metadatacombine.program_description_extended(program)
                ProgramAvailability = metadatainfo.vod_week_available_time(program)
            else:
                ProgramAction = 'load_kids_episodes_week'
                iconProgramType = "common/series.png"
                ProgramDuration = False
                ProgramDescription = ""
                ProgramAvailability = ""

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, ProgramDuration, True, False, False, False, True)
            ProgramTitle = ProgramName + " " + ProgramDetails

            #Add week program
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', ProgramAction)
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('SeriesId', SeriesId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Kids', 'Plot': ProgramDescription})
            iconStreamType = "common/calendarweek.png"
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType, 'image3': iconChannel})
            listContainer.append(listItem)
        except:
            continue
