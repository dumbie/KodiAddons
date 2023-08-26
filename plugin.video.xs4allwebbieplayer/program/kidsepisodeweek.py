from datetime import datetime, timedelta
import func
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer, selectedSeriesName, selectedPictureUrl):
    for program in var.KidsSearchDataJson["resultObj"]["containers"]:
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
            ProgramYear = metadatainfo.programyear_from_json_metadata(program)
            ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
            ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
            ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
            ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
            ProgramAvailability = metadatainfo.vod_week_available_time(program)

            #Combine program details
            stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisode, ProgramDuration ]
            ProgramDetails = ' '.join(filter(None, stringJoin))
            if func.string_isnullorempty(ProgramDetails):
                ProgramDetails = '(?)'
            ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
            ProgramTitle = EpisodeTitle + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

            #Add vod program
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_episode_week')
            listitem.setProperty('ChannelId', ChannelId)
            listitem.setProperty('ProgramId', ProgramId)
            listitem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listitem.setProperty("ProgramName", EpisodeTitle)
            listitem.setProperty("ProgramSeasonInt", ProgramSeasonInt)
            listitem.setProperty("ProgramEpisodeInt", ProgramEpisodeInt)
            listitem.setProperty("ProgramWeek", 'true')
            listitem.setProperty('ProgramDetails', ProgramDetails)
            listitem.setProperty("ProgramAvailability", ProgramAvailability)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
            listitem.setArt({'thumb': path.icon_epg(selectedPictureUrl), 'icon': path.icon_epg(selectedPictureUrl)})
            listContainer.append(listitem)
        except:
            continue
