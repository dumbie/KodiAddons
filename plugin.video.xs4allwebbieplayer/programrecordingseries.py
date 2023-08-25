from datetime import datetime, timedelta
import func
import metadatainfo
import recordingfunc
import xbmcgui
import path
import var

def list_load(listContainer):
    for program in var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramSeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check recorded episodes count
            ProgramEpisodeCount = recordingfunc.count_recorded_series_id(ProgramSeriesId)

            #Get first recording event
            RecordingEvent = func.search_seriesid_jsonrecording_event(ProgramSeriesId)

            #Load program details
            ProgramYear = metadatainfo.programyear_from_json_metadata(RecordingEvent)
            ProgramSeason = metadatainfo.programseason_from_json_metadata(RecordingEvent)

            #Combine program details
            stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisodeCount ]
            ProgramDetails = ' '.join(filter(None, stringJoin))
            if func.string_isnullorempty(ProgramDetails):
                ProgramDetails = '(?)'

            #Update program name string
            ProgramName += ' [COLOR gray]' + ProgramDetails + '[/COLOR]'

            #Get channel basics
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ChannelName = 'Onbekende zender'
            ChannelIcon = path.resources('resources/skins/default/media/common/unknown.png')
            ChannelDetails = func.search_channelid_jsontelevision(ChannelId)
            if ChannelDetails:
                ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                ChannelName = metadatainfo.channelName_from_json_metadata(ChannelDetails)
                ChannelIcon = path.icon_television(ExternalId)

            #Add recording series to the list
            listitem = xbmcgui.ListItem()
            listitem.setProperty('SeriesId', ProgramSeriesId)
            listitem.setProperty('ProgramName', ProgramName)
            listitem.setProperty('ProgramDescription', ChannelName)
            listitem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon})
            listContainer.addItem(listitem)
        except:
            continue
