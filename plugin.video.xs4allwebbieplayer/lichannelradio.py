import download
import xbmcgui
import favorite
import hidden
import func
import lifunc
import path
import var

def list_load_combined(listContainer=None, forceUpdate=False):
    try:
        #Download channels
        downloadResult = download.download_channels_radio(forceUpdate)
        if downloadResult == False:
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, "Zenders downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
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

            #Set item details
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
            dirIsfolder = False
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + ChannelId
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
