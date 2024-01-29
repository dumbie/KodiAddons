import xbmcgui
import func
import streamplay
import path
import var

#Switch television by channel identifier
def switch_tv_id(ChannelId, Windowed=False, ShowInformation=False, SeekOffsetEnd=0):
    try:
        if func.string_isnullorempty(ChannelId):
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
            return

        #Generate list item
        listItem = xbmcgui.ListItem()
        listItem.setProperty('ChannelId', ChannelId)

        streamplay.play_tv(listItem, Windowed, ShowInformation, SeekOffsetEnd)
        return True
    except:
        return False

#Switch radio by channel identifier
def switch_radio_id(ChannelId, Windowed=True):
    try:
        if func.string_isnullorempty(ChannelId):
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
            return

        #Generate list item
        listItem = xbmcgui.ListItem()
        listItem.setProperty('ChannelId', ChannelId)

        streamplay.play_radio(listItem, Windowed)
        return True
    except:
        return False

#Switch program by identifier
def switch_program_id(ProgramId, ProgramName='', Genre='', Windowed=False):
    try:
        if func.string_isnullorempty(ProgramId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige programma informatie.', notificationIcon, 2500, False)
            return

        #Check stream details
        if func.string_isnullorempty(ProgramName):
            ProgramName = 'Onbekende programma'

        if func.string_isnullorempty(Genre):
            Genre = 'Onbekend'

        #Generate list item
        listItem = xbmcgui.ListItem(ProgramName)
        listItem.setProperty('ProgramId', ProgramId)
        listItem.setProperty('ProgramName', ProgramName)
        listItem.setInfo('video', {'Genre': Genre})

        streamplay.play_program(listItem, Windowed)
        return True
    except:
        return False

#Switch vod by identifier
def switch_vod_id(ProgramId, ProgramName='', Genre='', Windowed=False):
    try:
        if func.string_isnullorempty(ProgramId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige vod informatie.', notificationIcon, 2500, False)
            return

        #Check stream details
        if func.string_isnullorempty(ProgramName):
            ProgramName = 'Onbekende vod'

        if func.string_isnullorempty(Genre):
            Genre = 'Onbekend'

        #Generate list item
        listItem = xbmcgui.ListItem(ProgramName)
        listItem.setProperty('ProgramId', ProgramId)
        listItem.setProperty('ProgramName', ProgramName)
        listItem.setInfo('video', {'Genre': Genre})

        streamplay.play_vod(listItem, Windowed)
        return True
    except:
        return False

#Switch recorded by identifier
def switch_recorded_id(ProgramAssetId, ProgramRecordEventId, ProgramName='', Genre='', Windowed=False):
    try:
        if func.string_isnullorempty(ProgramAssetId) or func.string_isnullorempty(ProgramRecordEventId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige opname informatie.', notificationIcon, 2500, False)
            return

        #Check stream details
        if func.string_isnullorempty(ProgramName):
            ProgramName = 'Onbekende opname'

        if func.string_isnullorempty(Genre):
            Genre = 'Onbekend'

        #Generate list item
        listItem = xbmcgui.ListItem(ProgramName)
        listItem.setProperty('ProgramAssetId', ProgramAssetId)
        listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
        listItem.setProperty('ProgramName', ProgramName)
        listItem.setInfo('video', {'Genre': Genre})

        streamplay.play_recorded(listItem, Windowed)
        return True
    except:
        return False
