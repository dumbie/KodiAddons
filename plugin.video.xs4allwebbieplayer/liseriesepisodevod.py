import lifunc
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
            listAction = 'play_stream_vod'
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_vod(selectedPictureUrl), 'icon': path.icon_vod(selectedPictureUrl)})
            lifunc.auto_add_item(listItem, listContainer, dirUrl=listAction+'='+ProgramId)
        except:
            continue
    lifunc.auto_end_items()
