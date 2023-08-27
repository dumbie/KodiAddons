from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.ChannelsDataJsonMovies['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            TechnicalPackageIds = metadatainfo.technicalPackageIds_from_json_metadata(program)

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False: continue

            #Check if content is pay to play
            if metadatainfo.program_check_paytoplay(TechnicalPackageIds): continue

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramAvailability = metadatainfo.vod_ondemand_available_time(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, False, False, True)
            ProgramTitle = ProgramName + " " + ProgramDetails

            #Add vod program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_stream_vod')
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty("ProgramDetails", ProgramDetails)
            listitem.setProperty("ProgramAvailability", ProgramAvailability)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Films', 'Plot': ProgramDescription})
            iconStreamType = "common/vod.png"
            iconProgram = path.icon_vod(PictureUrl)
            listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType})
            listContainer.append(listitem)
        except:
            continue
