import metadatainfo
import metadatacombine
import metadatafunc
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
            RecordingEventMetaData = metadatafunc.search_seriesid_jsonrecording_event(ProgramSeriesId)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(RecordingEventMetaData, True, False, True, True, False, False, False)

            #Combine recorded episodes count
            ProgramDetails += ' [COLOR gray]' + ProgramEpisodeCount + '[/COLOR]'

            #Update program name string
            ProgramName += ' ' + ProgramDetails

            #Get channel basics
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ChannelName = 'Onbekende zender'
            ChannelIcon = path.resources('resources/skins/default/media/common/unknown.png')
            ChannelDetails = metadatafunc.search_channelid_jsontelevision(ChannelId)
            if ChannelDetails:
                ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                ChannelName = metadatainfo.channelName_from_json_metadata(ChannelDetails)
                ChannelIcon = path.icon_television(ExternalId)

            #Add recording series to the list
            listItem = xbmcgui.ListItem()
            listItem.setProperty('SeriesId', ProgramSeriesId)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramDescription', ChannelName)
            listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon})
            listContainer.append(listItem)
        except:
            continue
