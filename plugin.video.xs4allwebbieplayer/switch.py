import xbmcgui
import func
import stream
import path
import var
import playergui

#Switch to new television channel by listitem
def channel_tv_listitem(listitem, Windowed=False, ShowInformation=False, SeekOffset=0):
    stream.play_stream_television(listitem, Windowed, SeekOffset)

    if ShowInformation == True:
        if var.guiPlayer != None:
            var.guiPlayer.show_epg(True)

#Switch to new television channel by id
def channel_tv_channelid(ChannelId, ExternalId='', ChannelName='Onbekende zender', ChannelGenre='Onbekend', Windowed=False, ShowInformation=False, SeekOffset=0):
    if func.string_isnullorempty(ChannelId):
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
        return

    if func.string_isnullorempty(ChannelName):
        ChannelName = 'Onbekende zender'

    if func.string_isnullorempty(ChannelGenre):
        ChannelGenre = 'Onbekend'

    #Generate list item
    listItem = xbmcgui.ListItem(ChannelName)
    listItem.setProperty('ChannelId', ChannelId)
    listItem.setProperty('ChannelName', ChannelName)
    listItem.setInfo('video', {'Genre': ChannelGenre})

    if func.string_isnullorempty(ExternalId) == False:
        listItem.setProperty('ExternalId', ExternalId)
        listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})

    stream.play_stream_television(listItem, Windowed, SeekOffset)

    if ShowInformation == True:
        if var.guiPlayer != None:
            var.guiPlayer.show_epg(True)

#Switch to new radio channel by id
def channel_radio_channelid(ChannelId, StreamUrl='', ChannelName='Onbekende zender', ChannelGenre='Onbekend'):
    if func.string_isnullorempty(ChannelId):
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
        return

    if func.string_isnullorempty(ChannelName):
        ChannelName = 'Onbekende zender'

    if func.string_isnullorempty(ChannelGenre):
        ChannelGenre = 'Onbekend'

    #Generate list item
    listItem = xbmcgui.ListItem(ChannelName)
    listItem.setProperty('ChannelId', ChannelId)
    listItem.setProperty('ChannelName', ChannelName)
    listItem.setProperty('StreamUrl', StreamUrl)
    listItem.setInfo('video', {'Genre': ChannelGenre})
    listItem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})

    stream.play_stream_radio(listItem)
