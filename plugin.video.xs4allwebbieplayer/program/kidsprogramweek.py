from datetime import datetime, timedelta
import func
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
            if func.search_programname_listarray(listContainer, ProgramName) != None: continue

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False: continue

            #Check if program is serie or movie
            ContentSubtype = metadatainfo.contentSubtype_from_json_metadata(program)
            if ContentSubtype == "VOD":
                ProgramAction = 'play_episode_week'
                iconProgramType = "common/movies.png"
                ProgramDuration = True
                ProgramDescription = metadatacombine.program_description_extended(program)
                ProgramAvailability = metadatainfo.vod_week_available_time(program)
            else:
                ProgramAction = 'load_episodes_week'
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
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', ProgramAction)
            listitem.setProperty('PictureUrl', PictureUrl)
            listitem.setProperty('SeriesId', SeriesId)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty("ProgramWeek", 'true')
            listitem.setProperty('ProgramDetails', ProgramDetails)
            listitem.setProperty("ProgramAvailability", ProgramAvailability)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Kids', 'Plot': ProgramDescription})
            iconStreamType = "common/calendarweek.png"
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType, 'image3': iconChannel})
            listContainer.append(listitem)
        except:
            continue
