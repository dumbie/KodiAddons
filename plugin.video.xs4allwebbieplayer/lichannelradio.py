import accent
import dlchannelradio
import favorite
import func
import getset
import hidden
import lifunc
import path
import var

def list_load_combined(listContainer=None):
    try:
        #Download channels
        downloadResult = dlchannelradio.download()
        if downloadResult == False:
            return False

        #Load favorite and hidden channels
        favorite.favorite_radio_json_load()
        hidden.hidden_radio_json_load()

        #Check if there are favorites set
        favorite.favorite_check_set('FavoriteRadio.js')

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: int(x[1].getProperty('ChannelNumber')))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
    for channel in var.RadioChannelsDataJson['radios']:
        try:
            #Load channel basics
            ChannelId = channel['id']
            ChannelName = channel['name']

            #Check if channel is hidden
            if hidden.hidden_check(ChannelId, 'HiddenRadio.js'): continue

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermResult) == False:
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchTermResult in searchMatch
                if searchResultFound == False: continue

            #Load channel details
            ChannelStream = channel['stream']

            #Check if channel is marked as favorite
            if favorite.favorite_check_channel(ChannelId, 'FavoriteRadio.js'):
                ChannelFavorite = 'true'
            elif getset.setting_get('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchTermResult):
                continue
            else:
                ChannelFavorite = 'false'

            #Update channel number
            ChannelNumberInt = str(ChannelId)
            ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + ChannelNumberInt + '[/COLOR][/B]'

            #Set item icons
            iconDefault = path.icon_radio(ChannelId)

            #Set item details
            jsonItem = {
                'ChannelId': ChannelId,
                'ChannelName': ChannelName,
                'ChannelNumber': ChannelNumberInt,
                'ChannelNumberAccent': ChannelNumberAccent,
                'ChannelFavorite': ChannelFavorite,
                'StreamUrl': ChannelStream,
                'ItemLabel': ChannelName,
                'ItemInfoMusic': {'MediaType': 'music', 'Genre': 'Radio', 'TrackNumber': ChannelNumberInt},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'play_stream_radio'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
