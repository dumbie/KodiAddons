import accent
import dlchannelradio
import dlchanneltelevision
import func
import hidden
import lifunc
import metadatafunc
import metadatainfo
import path
import var

def list_load_combined(listContainer, hiddenJsonFile):
    try:
        if hiddenJsonFile == 'HiddenTelevision.js':
            #Download channels
            downloadResultChannels = dlchanneltelevision.download()
            if downloadResultChannels == False:
                return False

            #Load hidden channels
            hidden.hidden_television_json_load()
        else:
            #Download channels
            downloadResultChannels = dlchannelradio.download()
            if downloadResultChannels == False:
                return False

            #Load hidden channels
            hidden.hidden_radio_json_load()

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, hiddenJsonFile, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, hiddenJsonFile, remoteMode=False):
    if hiddenJsonFile == 'HiddenTelevision.js':
        for hiddenChannelId in var.HiddenTelevisionJson:
            try:
                ChannelId = hiddenChannelId
                ChannelDetails = metadatafunc.search_channelid_jsontelevision(ChannelId)
                if ChannelDetails != None:
                    ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                    ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + metadatainfo.orderId_from_json_metadata(ChannelDetails) + '[/COLOR][/B]'
                    ChannelName = metadatainfo.channelName_from_json_metadata(ChannelDetails)
                    ChannelIcon = path.icon_television(ExternalId)
                else:
                    ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + '?[/COLOR][/B]'
                    ChannelName = "Onbekende zender"
                    ChannelIcon = path.icon_addon('unknown')

                #Set item icons
                iconFanart = path.icon_fanart()

                #Set item details
                jsonItem = {
                    'ChannelId': ChannelId,
                    'ProgramName': ChannelName,
                    'ProgramDescription': ChannelNumberAccent,
                    'ItemLabel': ChannelName,
                    'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ChannelNumberAccent, 'Tagline': ChannelNumberAccent, 'Title': ChannelName},
                    'ItemArt': {'thumb': ChannelIcon, 'icon': ChannelIcon, 'poster': ChannelIcon, 'fanart': iconFanart},
                    'ItemAction': 'action_none'
                }
                dirIsfolder = False
                dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
                listItem = lifunc.jsonitem_to_listitem(jsonItem)
                listContainer.append((dirUrl, listItem, dirIsfolder))
            except:
                continue
    elif hiddenJsonFile == 'HiddenRadio.js':
        for hiddenChannelId in var.HiddenRadioJson:
            try:
                ChannelId = hiddenChannelId
                ChannelDetails = metadatafunc.search_channelid_jsonradio(ChannelId)
                if ChannelDetails != None:
                    ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + ChannelDetails['id'] + '[/COLOR][/B]'
                    ChannelName = ChannelDetails['name']
                    ChannelIcon = path.icon_radio(ChannelId)
                else:
                    ChannelNumberAccent = '[B]' + accent.get_accent_color_string() + '?[/COLOR][/B]'
                    ChannelName = "Onbekende zender"
                    ChannelIcon = path.icon_addon('unknown')

                #Set item icons
                iconFanart = path.icon_fanart()

                #Set item details
                jsonItem = {
                    'ChannelId': ChannelId,
                    'ProgramName': ChannelName,
                    'ProgramDescription': ChannelNumberAccent,
                    'ItemLabel': ChannelName,
                    'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ChannelNumberAccent, 'Tagline': ChannelNumberAccent, 'Title': ChannelName},
                    'ItemArt': {'thumb': ChannelIcon, 'icon': ChannelIcon, 'poster': ChannelIcon, 'fanart': iconFanart},
                    'ItemAction': 'action_none'
                }
                dirIsfolder = False
                dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
                listItem = lifunc.jsonitem_to_listitem(jsonItem)
                listContainer.append((dirUrl, listItem, dirIsfolder))
            except:
                continue
