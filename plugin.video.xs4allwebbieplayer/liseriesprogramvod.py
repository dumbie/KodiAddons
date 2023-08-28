from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.ChannelsDataJsonSeries['resultObj']['containers']:
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
            listItem = xbmcgui.ListItem()
            listItem.setProperty('Action', 'load_episodes_vod')
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setInfo('video', {'Genre': 'Series', 'Plot': ProgramDetails})
            iconStreamType = "common/vod.png"
            iconProgram = path.icon_vod(PictureUrl)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType})
            listContainer.append(listItem)
        except:
            continue
