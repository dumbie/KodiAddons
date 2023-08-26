from datetime import datetime, timedelta
import func
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.ChannelsDataJsonSeriesKids['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False: continue

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramYear = metadatainfo.programyear_from_json_metadata(program)
            ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
            ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)

            #Combine program details
            stringJoin = [ ProgramYear, ProgramStarRating, ProgramAgeRating ]
            ProgramDetails = ' '.join(filter(None, stringJoin))
            if func.string_isnullorempty(ProgramDetails):
                ProgramDetails = '(?)'
            ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'

            #Add vod program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'load_episodes_vod')
            listitem.setProperty('PictureUrl', PictureUrl)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty('ProgramDetails', ProgramDetails)
            listitem.setInfo('video', {'Genre': 'Series', 'Plot': ProgramDetails})
            iconProgramType = "common/series.png"
            iconStreamType = "common/vod.png"
            iconProgram = path.icon_vod(PictureUrl)
            listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType})
            listContainer.append(listitem)
        except:
            continue
