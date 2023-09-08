import xbmcgui
import favorite
import func
import path
import var

def list_load(listContainer):
    favorite.favorite_json_load()
    ChannelNumberInt = 0
    for channel in var.ChannelsDataJsonRadio['radios']:
        try:
            #Load channel basics
            ChannelName = channel['name']

            #Check if there are search results
            if var.SearchChannelTerm != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchChannelTerm in searchMatch
                if searchResultFound == False: continue

            #Load channel details
            ChannelId = channel['id']
            ChannelStream = channel['stream']

            #Check if channel is marked as favorite
            if ChannelId in var.FavoriteRadioDataJson:
                ChannelFavorite = 'true'
            else:
                if var.LoadChannelFavoritesOnly == True and var.SearchChannelTerm == '': continue
                ChannelFavorite = 'false'

            #Update channel number
            ChannelNumberInt += 1
            ChannelNumberString = str(ChannelNumberInt)
            ChannelNumberAccent = func.get_provider_color_string() + ChannelNumberString + '[/COLOR]'

            #Add radio channel
            listItem = xbmcgui.ListItem()
            listItem.setProperty('Action', 'play_stream')
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ChannelName', ChannelName)
            listItem.setProperty('ChannelNumber', ChannelNumberString)
            listItem.setProperty('ChannelNumberAccent', ChannelNumberAccent)
            listItem.setProperty('ChannelFavorite', ChannelFavorite)
            listItem.setProperty('StreamUrl', ChannelStream)
            listItem.setInfo('video', {'Genre': 'Radio'})
            listItem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})
            listContainer.append(listItem)
        except:
            continue
