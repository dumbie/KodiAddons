import dlchanneltelevision
import lifunc
import metadatafunc
import metadatainfo
import path

def generate_listitem_tv(channelId):
    try:
        #Download channels
        if dlchanneltelevision.download() == False:
            return None

        #Get channel json
        channelJson = metadatafunc.search_channelid_jsontelevision(channelId)

        #Load channel basics
        StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(channelJson)
        ChannelId = metadatainfo.channelId_from_json_metadata(channelJson)
        ChannelName = metadatainfo.channelName_from_json_metadata(channelJson)
        ExternalId = metadatainfo.externalId_from_json_metadata(channelJson)
        ProgramGenre = 'Televisie'

        #Set item icons
        iconDefault = path.icon_television(ExternalId)

        #Set item details
        jsonItem = {
            'StreamAssetId': StreamAssetId,
            'ExternalId': ExternalId,
            'ChannelId': ChannelId,
            'ChannelName': ChannelName,
            'ItemLabel': ChannelName,
            'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramGenre, 'Title': ChannelName},
            'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
            'ItemAction': 'play_stream_tv'
        }
        return lifunc.jsonitem_to_listitem(jsonItem)
    except:
        return None
