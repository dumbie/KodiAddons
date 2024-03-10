import xbmcgui
import dlchanneltelevision
import dlrecordingseries
import lifunc
import metadatacombine
import metadatafunc
import metadatainfo
import path
import recordingfunc
import var

def list_load_combined(listContainer=None):
    try:
        #Download record series
        downloadResultChannels = dlchanneltelevision.download()
        downloadResultSeries = dlrecordingseries.download()
        if downloadResultChannels == False or downloadResultSeries == False:
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Sort list items
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    for program in var.RecordingSeriesDataJson["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            ProgramSeriesId = metadatainfo.seriesId_from_json_metadata(program)

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

            #Set item details
            listItem = xbmcgui.ListItem()
            listItem.setProperty('ProgramSeriesId', ProgramSeriesId)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramDescription', ChannelName)
            listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon, 'poster': ChannelIcon})
            listContainer.append(listItem)
        except:
            continue
