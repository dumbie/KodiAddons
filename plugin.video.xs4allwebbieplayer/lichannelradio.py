import xbmcgui
import func
import path
import var

def list_load(listContainer):
    ChannelNumberInt = 0
    for channel in var.ChannelsDataJsonRadio['radios']:
        try:
            #Load channel basics
            ChannelName = channel['name']

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ChannelName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False: continue

            #Load channel details
            ChannelId = channel['id']
            ChannelStream = channel['stream']

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
            listItem.setProperty('StreamUrl', ChannelStream)
            listItem.setInfo('music', {'Genre': 'Radio'})
            listItem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})
            listContainer.addItem(listItem)
        except:
            continue
