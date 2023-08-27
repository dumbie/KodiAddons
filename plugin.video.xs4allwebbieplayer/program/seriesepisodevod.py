from datetime import datetime, timedelta
import metadatacombine
import metadatainfo
import xbmcgui
import path

def list_load(listContainer, seasonDownloaded, selectedSeriesName, selectedPictureUrl):
    for program in seasonDownloaded["resultObj"]["containers"]:
        try:
            #Load program basics
            TechnicalPackageIds = metadatainfo.technicalPackageIds_from_json_metadata(program)

            #Check if content is pay to play
            if metadatainfo.program_check_paytoplay(TechnicalPackageIds): continue

            #Load program details
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            ProgramAvailability = metadatainfo.vod_ondemand_available_time(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)
            ProgramTitle = ProgramName + " " + ProgramDetails

            #Add vod program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_episode_vod')
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramName", ProgramName)
            listitem.setProperty('ProgramDetails', ProgramDetails)
            listitem.setProperty("ProgramAvailability", ProgramAvailability)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
            listitem.setArt({'thumb': path.icon_vod(selectedPictureUrl), 'icon': path.icon_vod(selectedPictureUrl)})
            listContainer.addItem(listitem)
        except:
            continue
