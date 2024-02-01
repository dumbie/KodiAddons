import metadatafunc
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer, hiddenJsonFile):
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
                listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon})
                listContainer.append(listItem)
            except:
                continue
    elif hiddenJsonFile == 'HiddenRadio.js':
        for hiddenChannelId in var.HiddenRadioJson:
            try:
                ChannelId = hiddenChannelId
                ChannelDetails = metadatafunc.search_channelid_jsonradio(ChannelId)
                if ChannelDetails:
                    ChannelName = ChannelDetails['name']
                    ChannelIcon = path.icon_radio(ChannelId)
                else:
                    ChannelName = "Onbekende zender"
                    ChannelIcon = path.icon_addon('unknown')

                listItem = xbmcgui.ListItem()
                listItem.setProperty('ChannelId', ChannelId)
                listItem.setProperty('ProgramName', ChannelName)
                listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon})
                listContainer.append(listItem)
            except:
                continue
