import metadatafunc
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer, hiddenJsonFile):
    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        hiddenTargetJson = var.HiddenTelevisionJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioJson

    for hiddenChannelId in hiddenTargetJson:
        try:
            ChannelId = hiddenChannelId
            ChannelDetails = metadatafunc.search_channelid_jsontelevision(ChannelId)
            if ChannelDetails:
                ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                ChannelNumber = metadatainfo.orderId_from_json_metadata(ChannelDetails)
                ChannelName = metadatainfo.channelName_from_json_metadata(ChannelDetails)
                ChannelIcon = path.icon_television(ExternalId)
            else:
                ExternalId = "0"
                ChannelNumber = "?"
                ChannelName = "Onbekende zender"
                ChannelIcon = path.resources('resources/skins/default/media/common/unknown.png')

            listItem = xbmcgui.ListItem()
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ProgramName', ChannelNumber)
            listItem.setProperty('ProgramDescription', ChannelName)
            listItem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon})
            listContainer.append(listItem)
        except:
            continue
