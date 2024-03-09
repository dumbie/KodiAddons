import lifunc
import hidden
import metadatafunc
import metadatainfo
import xbmcgui
import path
import var

def list_load_combined(listContainer, hiddenJsonFile):
    try:
        #Load hidden channels
        if hiddenJsonFile == 'HiddenTelevision.js':
            hidden.hidden_television_json_load()
        else:
            hidden.hidden_radio_json_load()

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort, hiddenJsonFile)

        #Sort list items
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, hiddenJsonFile):
    if hiddenJsonFile == 'HiddenTelevision.js':
        for hiddenChannelId in var.HiddenTelevisionJson:
            try:
                ChannelId = hiddenChannelId
                ChannelDetails = metadatafunc.search_channelid_jsontelevision(ChannelId)
                if ChannelDetails:
                    ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                    ChannelNumber = metadatainfo.orderId_from_json_metadata(ChannelDetails)
                    ChannelName = metadatainfo.channelName_from_json_metadata(ChannelDetails)
                    ChannelIcon = path.icon_television(ExternalId)
                else:
                    ChannelNumber = "?"
                    ChannelName = "Onbekende zender"
                    ChannelIcon = path.icon_addon('unknown')

                listItem = xbmcgui.ListItem()
                listItem.setProperty('ChannelId', ChannelId)
                listItem.setProperty('ProgramName', ChannelName)
                listItem.setProperty('ProgramDescription', ChannelNumber)
                listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon, 'poster': ChannelIcon})
                listContainer.append(listItem)
            except:
                continue
    elif hiddenJsonFile == 'HiddenRadio.js':
        for hiddenChannelId in var.HiddenRadioJson:
            try:
                ChannelId = hiddenChannelId
                ChannelDetails = metadatafunc.search_channelid_jsonradio(ChannelId)
                if ChannelDetails:
                    ChannelNumber = ChannelDetails['id']
                    ChannelName = ChannelDetails['name']
                    ChannelIcon = path.icon_radio(ChannelId)
                else:
                    ChannelNumber = "?"
                    ChannelName = "Onbekende zender"
                    ChannelIcon = path.icon_addon('unknown')

                listItem = xbmcgui.ListItem()
                listItem.setProperty('ChannelId', ChannelId)
                listItem.setProperty('ProgramName', ChannelName)
                listItem.setProperty('ProgramDescription', ChannelNumber)
                listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon, 'poster': ChannelIcon})
                listContainer.append(listItem)
            except:
                continue
