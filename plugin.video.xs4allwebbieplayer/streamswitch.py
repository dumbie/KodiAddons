import xbmcgui
import streamplay

#Switch television by channel identifier
def switch_tv_id(ChannelId, Windowed=False, OpenOverlay=True, ShowInformation=False, SeekOffsetEnd=0):
    try:
        listItem = xbmcgui.ListItem()
        listItem.setProperty('ChannelId', ChannelId)
        streamplay.play_tv(listItem, Windowed, OpenOverlay, ShowInformation, SeekOffsetEnd)
        return True
    except:
        return False

#Switch radio by channel identifier
def switch_radio_id(ChannelId, Windowed=False):
    try:
        listItem = xbmcgui.ListItem()
        listItem.setProperty('ChannelId', ChannelId)
        streamplay.play_radio(listItem, Windowed)
        return True
    except:
        return False

#Switch program by identifier
def switch_program_id(ProgramId, Windowed=False):
    try:
        listItem = xbmcgui.ListItem()
        listItem.setProperty('ProgramId', ProgramId)
        streamplay.play_program(listItem, Windowed)
        return True
    except:
        return False

#Switch vod by identifier
def switch_vod_id(ProgramId, Windowed=False):
    try:
        listItem = xbmcgui.ListItem()
        listItem.setProperty('ProgramId', ProgramId)
        streamplay.play_vod(listItem, Windowed)
        return True
    except:
        return False

#Switch recorded by identifier
def switch_recorded_id(StreamAssetId, ProgramRecordEventId, ProgramDeltaTimeStart, Windowed=False):
    try:
        listItem = xbmcgui.ListItem()
        listItem.setProperty('StreamAssetId', StreamAssetId)
        listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
        listItem.setProperty('ProgramDeltaTimeStart', str(ProgramDeltaTimeStart))
        streamplay.play_recorded(listItem, Windowed)
        return True
    except:
        return False
