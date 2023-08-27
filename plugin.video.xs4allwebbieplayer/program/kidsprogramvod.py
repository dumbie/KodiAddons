from datetime import datetime, timedelta
import func
import metadatacombine
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

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Add vod program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'load_episodes_vod')
            listitem.setProperty('PictureUrl', PictureUrl)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty('ProgramDetails', ProgramDetails)
            listitem.setInfo('video', {'Genre': 'Kids', 'Plot': ProgramDetails})
            iconProgramType = "common/series.png"
            iconStreamType = "common/vod.png"
            iconProgram = path.icon_vod(PictureUrl)
            listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType})
            listContainer.append(listitem)
        except:
            continue
