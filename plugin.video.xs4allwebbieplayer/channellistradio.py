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
            listitem = xbmcgui.ListItem()
            listitem.setProperty('Action', 'play_stream')
            listitem.setProperty('ChannelId', ChannelId)
            listitem.setProperty('ChannelName', ChannelName)
            listitem.setProperty('ChannelNumber', ChannelNumberString)
            listitem.setProperty('ChannelNumberAccent', ChannelNumberAccent)
            listitem.setProperty('StreamUrl', ChannelStream)
            listitem.setInfo('music', {'Genre': 'Radio'})
            listitem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})
            listContainer.addItem(listitem)
        except:
            continue
