import xbmcgui
import favorite
import hidden
import func
import lifunc
import path
import var

def list_load(listContainer):
    favorite.favorite_radio_json_load()
    hidden.hidden_radio_json_load()
    ChannelNumberInt = 0
    for channel in var.RadioChannelsDataJson['radios']:
        try:
            #Load channel basics
            ChannelId = channel['id']
            ChannelName = channel['name']

            #Check if channel is hidden
            if hidden.hidden_check(ChannelId, 'HiddenRadio.js'): continue

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Load channel details
            ChannelStream = channel['stream']

            #Check if channel is marked as favorite
            if favorite.favorite_check(ChannelId, 'FavoriteRadio.js'):
                ChannelFavorite = 'true'
            elif var.addon.getSetting('LoadChannelFavoritesOnly') == 'true' and func.string_isnullorempty(var.SearchChannelTerm):
                continue
            else:
                ChannelFavorite = 'false'

            #Update channel number
            ChannelNumberInt += 1
            ChannelNumberString = str(ChannelNumberInt)
            ChannelNumberAccent = func.get_provider_color_string() + ChannelNumberString + '[/COLOR]'

            #Add radio channel
            listAction = 'play_stream_radio'
            listItem = xbmcgui.ListItem(ChannelName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ChannelName', ChannelName)
            listItem.setProperty('ChannelNumber', ChannelNumberString)
            listItem.setProperty('ChannelNumberAccent', ChannelNumberAccent)
            listItem.setProperty('ChannelFavorite', ChannelFavorite)
            listItem.setProperty('StreamUrl', ChannelStream)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': 'Radio', 'Tagline': ChannelNumberString, 'Title': ChannelName})
            listItem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})
            lifunc.auto_add_item(listItem, listContainer, dirUrl=listAction+'='+ChannelId)
        except:
            continue
    lifunc.auto_end_items()
