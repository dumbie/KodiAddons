from datetime import datetime, timedelta
import func
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
            ProgramYear = metadatainfo.programyear_from_json_metadata(program)
            ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
            ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
            ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
            ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
            ProgramAvailability = metadatainfo.vod_ondemand_available_time(program)

            #Combine program details
            stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisode, ProgramDuration ]
            ProgramDetails = ' '.join(filter(None, stringJoin))
            if func.string_isnullorempty(ProgramDetails):
                ProgramDetails = '(?)'
            ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
            ProgramTitle = ProgramName + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

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
