import dlchannelweb
import dlrecordingseries
import dlrecordingevent
import func
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
        downloadResultChannels = dlchannelweb.download()
        downloadResultRecordingSeries = dlrecordingseries.download()
        downloadResultRecordingEvent = dlrecordingevent.download()
        if downloadResultChannels == False or downloadResultRecordingSeries == False or downloadResultRecordingEvent == False:
            return False

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
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
            ProgramDetails += ' [COLOR FF888888]' + ProgramEpisodeCount + '[/COLOR]'

            #Get channel basics
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ChannelDetails = metadatafunc.search_channelid_json_web(ChannelId)
            if ChannelDetails != None:
                ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                ChannelIcon = path.icon_television(ExternalId)
            else:
                ChannelIcon = path.resources('resources/skins/default/media/common/unknown.png')

            #Set item icons
            iconFanart = path.icon_fanart()

            #Set item details
            jsonItem = {
                'ProgramSeriesId': ProgramSeriesId,
                'ProgramName': ProgramName,
                "ProgramDescription": ProgramDetails,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName},
                'ItemArt': {'thumb': ChannelIcon, 'icon': ChannelIcon, 'poster': ChannelIcon, 'fanart': iconFanart},
                'ItemAction': 'action_none'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
