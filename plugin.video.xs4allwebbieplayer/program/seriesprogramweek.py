from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.SeriesSearchDataJson['resultObj']['containers']:
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

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Add week program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'load_episodes_week')
            listitem.setProperty('PictureUrl', PictureUrl)
            listitem.setProperty('SeriesId', SeriesId)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty("ProgramWeek", 'true')
            listitem.setProperty('ProgramDetails', ProgramDetails)
            listitem.setInfo('video', {'Genre': 'Series', 'Plot': ProgramDetails})
            iconStreamType = "common/calendarweek.png"
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconChannel})
            listContainer.append(listitem)
        except:
            continue
