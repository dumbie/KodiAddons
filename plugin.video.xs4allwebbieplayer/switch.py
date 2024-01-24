import xbmcgui
import download
import func
import stream
import path
import var

#Stream television by channel identifier
def stream_tv_channelid(ChannelId, ExternalId='', ChannelName='', ChannelGenre='', Windowed=False, ShowInformation=False, SeekOffset=0):
    if func.string_isnullorempty(ChannelId):
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
        return

    #Check stream details
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

    download.download_channels_tv(False)
    stream.play_stream_tv(listItem, Windowed, ShowInformation, SeekOffset)

#Stream radio by channel identifier
def stream_radio_channelid(ChannelId, StreamUrl='', ChannelName='', ChannelGenre='', Windowed=True):
    if func.string_isnullorempty(ChannelId):
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
        return

    #Check stream details
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

    download.download_channels_radio(False)
    stream.play_stream_radio(listItem, Windowed)

#Stream program by identifier
def stream_program_id(ProgramId, ProgramName='', ProgramGenre='', Windowed=False):
    if func.string_isnullorempty(ProgramId):
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige programma informatie.', notificationIcon, 2500, False)
        return

    #Check stream details
    if func.string_isnullorempty(ProgramName):
        ProgramName = 'Onbekende programma'

    if func.string_isnullorempty(ProgramGenre):
        ProgramGenre = 'Onbekend'

    #Generate list item
    listItem = xbmcgui.ListItem(ProgramName)
    listItem.setProperty('ProgramId', ProgramId)
    listItem.setProperty('ProgramName', ProgramName)
    listItem.setInfo('video', {'Genre': ProgramGenre})

    stream.play_stream_program(listItem, Windowed)

#Stream vod by identifier
def stream_vod_id(ProgramId, ProgramName='', ProgramGenre='', Windowed=False):
    if func.string_isnullorempty(ProgramId):
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige programma informatie.', notificationIcon, 2500, False)
        return

    #Check stream details
    if func.string_isnullorempty(ProgramName):
        ProgramName = 'Onbekende programma'

    if func.string_isnullorempty(ProgramGenre):
        ProgramGenre = 'Onbekend'

    #Generate list item
    listItem = xbmcgui.ListItem(ProgramName)
    listItem.setProperty('ProgramId', ProgramId)
    listItem.setProperty('ProgramName', ProgramName)
    listItem.setInfo('video', {'Genre': ProgramGenre})

    stream.play_stream_vod(listItem, Windowed)

#Stream recorded by identifier
def stream_recorded_id(ProgramAssetId, ProgramRecordEventId, ProgramName='', ProgramGenre='', Windowed=False):
    if func.string_isnullorempty(ProgramAssetId) or func.string_isnullorempty(ProgramRecordEventId):
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige opname informatie.', notificationIcon, 2500, False)
        return

    #Check stream details
    if func.string_isnullorempty(ProgramName):
        ProgramName = 'Onbekende programma'

    if func.string_isnullorempty(ProgramGenre):
        ProgramGenre = 'Onbekend'

    #Generate list item
    listItem = xbmcgui.ListItem(ProgramName)
    listItem.setProperty('ProgramAssetId', ProgramAssetId)
    listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
    listItem.setProperty('ProgramName', ProgramName)
    listItem.setInfo('video', {'Genre': ProgramGenre})

    stream.play_stream_recorded(listItem, Windowed)
