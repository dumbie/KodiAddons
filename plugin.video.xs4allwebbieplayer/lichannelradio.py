import accent
import dlchannelstb
import favoritefunc
import func
import getset
import hiddenfunc
import lifunc
import metadatainfo
import path
import var

def list_load_combined(listContainer=None):
    try:
        #Download channels
        downloadResult = dlchannelstb.download()
        if downloadResult == False:
            return False

        #Load favorite and hidden channels
        favoritefunc.favorite_radio_json_load()
        hiddenfunc.hidden_radio_json_load()

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: func.to_type(int, x[1].getProperty('ChannelNumber'), 0))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
    for channel in var.StbChannelsDataJson['resultObj']['containers']:
        try:
            #Load channel basics
            ChannelId = metadatainfo.channelId_from_json_metadata(channel)
            ChannelName = metadatainfo.channelName_from_json_metadata(channel)

            #Check radio channel start number
            ChannelNumberInt = int(metadatainfo.orderId_from_json_metadata(channel))
            if ChannelNumberInt < 800: continue
            elif ChannelNumberInt > 8000: continue

            #Check if channel is radio type
            ChannelType = metadatainfo.type_from_json_metadata(channel)
            if ChannelType != "MUSIC": continue

            #Check if channel is hidden
            if hiddenfunc.hidden_check_channel(ChannelId, 'HiddenRadio.js'): continue

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Load channel details
            ChannelStream = metadatainfo.stream_multicast_url(channel)
            ExternalId = metadatainfo.externalId_from_json_metadata(channel)
            ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + str(ChannelNumberInt) + '[/COLOR][/B]'

            #Check if channel is marked as favorite
            if favoritefunc.favorite_check_channel(ChannelId, 'FavoriteRadio.js'):
                ChannelFavorite = 'true'
            elif getset.setting_get('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchTermResult):
                continue
            else:
                ChannelFavorite = 'false'

            #Set item icons
            iconDefault = path.icon_television(ExternalId)
            ProgramGenre = 'Radio'

            #Set item details
            jsonItem = {
                'ChannelId': ChannelId,
                'ChannelName': ChannelName,
                'ChannelNumber': str(ChannelNumberInt),
                'ChannelNumberAccent': ChannelNumberAccent,
                'ChannelFavorite': ChannelFavorite,
                'StreamUrl': ChannelStream,
                'ItemLabel': ChannelName,
                'ItemInfoMusic': {'MediaType': 'music', 'Genre': ProgramGenre, 'TrackNumber': str(ChannelNumberInt)},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_radio'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
