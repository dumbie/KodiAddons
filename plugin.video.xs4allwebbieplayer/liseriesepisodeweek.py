from datetime import datetime, timedelta
import func
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer, selectedSeriesName, selectedPictureUrl):
    for program in var.SeriesSearchDataJson["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

            #Check if program matches serie
            checkSerie1 = ProgramName.lower()
            checkSerie2 = selectedSeriesName.lower()
            if checkSerie1 != checkSerie2: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
            ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)
            EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, False)
            ProgramAvailability = metadatainfo.vod_week_available_time(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)
            ProgramTitle = EpisodeTitle + " " + ProgramDetails

            #Add vod program
            listItem = xbmcgui.ListItem()
            listItem.setProperty('Action', 'play_episode_week')
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listItem.setProperty("ProgramName", EpisodeTitle)
            listItem.setProperty("ProgramSeasonInt", ProgramSeasonInt)
            listItem.setProperty("ProgramEpisodeInt", ProgramEpisodeInt)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_epg(selectedPictureUrl), 'icon': path.icon_epg(selectedPictureUrl)})
            listContainer.append(listItem)
        except:
            continue
