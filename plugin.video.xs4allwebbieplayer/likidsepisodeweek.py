import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer, selectedSeriesName, selectedPictureUrl):
    for program in var.KidsProgramDataJson["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramNameRaw = metadatainfo.programtitle_from_json_metadata(program)

            #Check if program matches serie
            checkSerie1 = ProgramNameRaw.lower()
            checkSerie2 = selectedSeriesName.lower()
            if checkSerie1 != checkSerie2: continue

            #Load program details
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
            ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)
            EpisodeTitleRaw = metadatainfo.episodetitle_from_json_metadata(program)
            ProgramAvailability = metadatainfo.vod_week_available_time(program)

            #Combine program description extended
            ProgramDescription = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, True, True, True, True, False, False)

            #Add vod program
            listAction = 'play_stream_program'
            listItem = xbmcgui.ListItem(EpisodeTitleRaw)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
            listItem.setProperty("ProgramName", EpisodeTitleRaw)
            listItem.setProperty("ProgramSeasonInt", ProgramSeasonInt)
            listItem.setProperty("ProgramEpisodeInt", ProgramEpisodeInt)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty("ProgramAvailability", ProgramAvailability)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': selectedSeriesName, 'Tagline': ProgramDetails, 'Title': EpisodeTitleRaw, 'Plot': ProgramDescription})
            listItem.setArt({'thumb': path.icon_epg(selectedPictureUrl), 'icon': path.icon_epg(selectedPictureUrl)})
            lifunc.auto_add_item(listItem, listContainer, dirUrl=listAction+'='+ProgramId)
        except:
            continue
    lifunc.auto_end_items()
