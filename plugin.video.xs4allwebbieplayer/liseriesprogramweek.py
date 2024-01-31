import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.SeriesProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if serie is already added
            if lifunc.search_programname_listarray(listContainer, ProgramName) != None: continue

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Add week program
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', 'load_series_episodes_week')
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('SeriesId', SeriesId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setInfo('video', {'Genre': 'Series', 'Plot': ProgramDetails})
            iconStreamType = path.icon_addon('calendarweek')
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconChannel})
            listContainer.append(listItem)
        except:
            continue
