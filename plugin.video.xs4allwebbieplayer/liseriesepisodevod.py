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
            listItem = xbmcgui.ListItem()
            listItem.setProperty('Action', 'play_episode_vod')
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_vod(selectedPictureUrl), 'icon': path.icon_vod(selectedPictureUrl)})
            listContainer.append(listItem)
        except:
            continue
