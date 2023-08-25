from datetime import datetime, timedelta
import func
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
            ProgramYear = metadatainfo.programyear_from_json_metadata(program)
            ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
            ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
            ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)
            ProgramActors = metadatainfo.programactors_from_json_metadata(program)
            ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
            ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
            ProgramAvailability = metadatainfo.vod_ondemand_available_time(program)

            #Combine program details
            stringJoin = [ ProgramYear, ProgramSeason, ProgramStarRating, ProgramAgeRating, ProgramDuration ]
            ProgramDetails = ' '.join(filter(None, stringJoin))
            if func.string_isnullorempty(ProgramDetails):
                ProgramDetails = '(?)'
            ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
            ProgramTitle = ProgramName + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

            #Combine program actors
            if func.string_isnullorempty(ProgramActors) == False:
                ProgramDescription += "\n\n[COLOR gray]" + ProgramActors + "[/COLOR]"

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
