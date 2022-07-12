import os
import re
import time
from datetime import datetime, date, timedelta
from threading import Thread
import _strptime
import xbmc
import xbmcgui
import dialog
import hybrid
import metadatainfo
import var

#Run this add-on
def run_addon(forceLaunch=False):
    if var.addon.getSetting('RunAddonOnKodiLaunch') == 'true' or forceLaunch:
        xbmcgui.Dialog().notification(var.addonname, 'Webbie Player wordt gestart.', var.addonicon, 2500, False)
        xbmc.executebuiltin('RunScript(plugin.video.xs4allwebbieplayer)')

#Get provider color string
def get_provider_color_string():
    return '[COLOR FF009900]'

#Search filter string
def search_filter_string(searchString):
    searchFilterTerm = searchString.lower()
    searchFilterTerm = hybrid.string_remove_accents(searchFilterTerm)
    return searchFilterTerm

#Search for ChannelId in json epg
def search_channelid_jsonepg(jsonEpg, searchChannelId):
    if jsonEpg == []: return None
    for Epg in jsonEpg["resultObj"]["containers"]:
        try:
            if metadatainfo.channelId_from_json_metadata(Epg) == searchChannelId:
                return Epg
        except:
            continue
    return None

#Get ProgramIndex for airing program in json epg
def get_programindex_airingtime_jsonepg(jsonEpg, targetTime):
    if jsonEpg == []: return None
    programIndex = 0
    for Program in jsonEpg['containers']:
        try:
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(Program)
            if ProgramTimeEndDateTime < targetTime:
                programIndex += 1
            else:
                return programIndex
        except:
            continue
    return None

#Search for ChannelId in json recording event
def search_channelid_jsonrecording_event(searchChannelId, filterTime=False):
    if var.ChannelsDataJsonRecordingEvent == []: return None
    for Record in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
        try:
            if filterTime == True:
                ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(Record)
                if datetime.now() > ProgramTimeEndDateTime: continue
            if metadatainfo.channelId_from_json_metadata(Record) == searchChannelId:
                return Record
        except:
            continue
    return None

#Search for ChannelId in json recording series
def search_channelid_jsonrecording_series(searchChannelId):
    if var.ChannelsDataJsonRecordingSeries == []: return None
    for Record in var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"]:
        try:
            if metadatainfo.channelId_from_json_metadata(Record) == searchChannelId:
                return Record
        except:
            continue
    return None

#Search for ProgramId in json recording event
def search_programid_jsonrecording_event(searchProgramId):
    if var.ChannelsDataJsonRecordingEvent == []: return None
    for Record in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
        try:
            if metadatainfo.contentId_from_json_metadata(Record) == searchProgramId:
                return Record
            if metadatainfo.contentIdLive_from_json_metadata(Record) == searchProgramId:
                return Record
        except:
            continue
    return None

#Search for SeriesId in json recording event
def search_seriesid_jsonrecording_event(searchSeriesId):
    if var.ChannelsDataJsonRecordingEvent == []: return None
    for Record in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
        try:
            if metadatainfo.seriesId_from_json_metadata(Record) == searchSeriesId:
                return Record
            if metadatainfo.seriesIdLive_from_json_metadata(Record) == searchSeriesId:
                return Record
        except:
            continue
    return None

#Search for SeriesId in json recording series
def search_seriesid_jsonrecording_series(searchSeriesId):
    if var.ChannelsDataJsonRecordingSeries == []: return None
    for Record in var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"]:
        try:
            if metadatainfo.seriesId_from_json_metadata(Record) == searchSeriesId:
                return Record
            if metadatainfo.seriesIdLive_from_json_metadata(Record) == searchSeriesId:
                return Record
        except:
            continue
    return None

#Search for ChannelId in json television
def search_channelid_jsontelevision(searchChannelId):
    if var.ChannelsDataJsonTelevision == []: return None
    for Channel in var.ChannelsDataJsonTelevision["resultObj"]["containers"]:
        try:
            if metadatainfo.channelId_from_json_metadata(Channel) == searchChannelId:
                return Channel
        except:
            continue
    return None

#Search for ProgramName in list array
def search_programname_listarray(listArray, searchProgramName):
    for Program in listArray:
        try:
            checkProgram1 = searchProgramName.lower()
            checkProgram2 = Program.getProperty('ProgramName').lower()
            if checkProgram1 == checkProgram2:
                return Program
        except:
            continue
    return None

#Search for ChannelId in container
def search_channelid_listcontainer(listcontainer, searchChannelId):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            ChannelId = listcontainer.getListItem(itemNum).getProperty('ChannelId')
            if ChannelId == searchChannelId:
                return itemNum
        except:
            continue
    return None

#Search for ChannelName in container
def search_channelname_listcontainer(listcontainer, searchChannelName):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            ChannelName = listcontainer.getListItem(itemNum).getProperty('ChannelName')
            if ChannelName == searchChannelName:
                return itemNum
        except:
            continue
    return None

#Search for ChannelNumber in container
def search_channelnumber_listcontainer(listcontainer, searchChannelNumber):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            ChannelNumber = listcontainer.getListItem(itemNum).getProperty('ChannelNumber')
            if ChannelNumber == searchChannelNumber:
                return itemNum
        except:
            continue
    return None

#Search for label in container
def search_label_listcontainer(listcontainer, searchLabel):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            listItem = listcontainer.getListItem(itemNum)
            if str(listItem.getLabel()).startswith(searchLabel):
                return listItem
        except:
            continue
    return None

#Focus on the list
def focus_on_channel_list(_self, controlId, defaultNum, forceFocus, channelId):
    listcontainer = _self.getControl(controlId)
    if forceFocus:
        _self.setFocus(listcontainer)
        xbmc.sleep(100)
    if string_isnullorempty(channelId) == False:
        itemNum = search_channelid_listcontainer(listcontainer, channelId)
        if itemNum == None:
            listcontainer.selectItem(defaultNum)
        else:
            listcontainer.selectItem(itemNum)
    else:
        listcontainer.selectItem(defaultNum)
    xbmc.sleep(100)

#Update controls
def updateImage(_self, controlId, ImagePath):
    _self.getControl(controlId).setImage(ImagePath)
def updateVisibility(_self, controlId, visible):
    _self.getControl(controlId).setVisible(visible)
def updateLabelText(_self, controlId, string):
    _self.getControl(controlId).setLabel(string)
def updateTextBoxText(_self, controlId, string):
    _self.getControl(controlId).setText(string)
def updateProgressbarPercent(_self, controlId, percent):
    _self.getControl(controlId).setPercent(float(percent))

#Check if an addon is running
def check_addon_running():
    try:
        currentWindowId = xbmcgui.getCurrentWindowId()
        if str(currentWindowId).startswith('130') or currentWindowId == var.WINDOW_FULLSCREEN_VIDEO or currentWindowId == var.WINDOW_VISUALISATION:
            return True
        else:
            return False
    except:
        return False

#Open a window by id
def open_window_id(windowId):
    xbmc.executebuiltin('ActivateWindow(' + str(windowId) + ')')

#Close a window by id
def close_window_id(windowId):
    #Improve: find way to directly close the window
    currentWindowId = xbmcgui.getCurrentWindowId()
    if currentWindowId == windowId:
        xbmc.executebuiltin('Action(Close)')

#String replace regex
def string_replace_regex(regex, new, text):
    pattern = re.compile(regex, re.IGNORECASE|re.MULTILINE)
    return pattern.sub(new, text)

#String replace case insensitive
def string_replace_insensitive(old, new, text):
    pattern = re.compile(old, re.IGNORECASE|re.MULTILINE)
    return pattern.sub(new, text)

#Check if string is empty
def string_isnullorempty(string):
    if string and string.strip():
        return False
    else:
        return True

#Shorten string to certain length
def string_shorten(string, length, ending):
    if len(string) > length:
        return string[:length].rstrip() + ending
    else:
        return string

#Convert number to single string
def number_to_single_string(number):
    return str(int(number))

#Convert datetime to string
def datetime_to_string(date_time, date_format):
    return date_time.strftime(date_format)

#Convert string to datetime
def datetime_from_string(date_string, date_format):
    return datetime(*(time.strptime(date_string, date_format)[0:6]))

#Convert epoch ticks to datetime
def datetime_from_ticks(ticks):
    return datetime.fromtimestamp(int(ticks) / 1000)

#Convert datetime to epoch ticks
def datetime_to_ticks(dateTime, utcCorrection=False):
    if utcCorrection:
        timeOffsetUtcSeconds = (datetime.now() - datetime.utcnow()).total_seconds()
    else:
        timeOffsetUtcSeconds = 0
    return int((dateTime - datetime(1970,1,1)).total_seconds() - timeOffsetUtcSeconds) * 1000

#Remove seconds from datetime
def datetime_remove_seconds(datetimeFull):
    DateTimeString = datetimeFull.strftime('%Y-%m-%d %H:%M')
    return datetime_from_string(DateTimeString, '%Y-%m-%d %H:%M')

#Get datetime midnight
def datetime_to_midnight(datetimeFull):
    DateTimeString = datetimeFull.strftime('%Y-%m-%d')
    return datetime_from_string(DateTimeString, '%Y-%m-%d')

#Get days in current year
def days_in_year():
    TodayYear = datetime.today().year
    LastYear = date(TodayYear - 1, 1, 1)
    CurrentYear = date(TodayYear, 1, 1)
    return (CurrentYear - LastYear).days

#Check if certain time is between
def date_time_between(betweenTime, startTime, endTime):
    if startTime < endTime:
        return betweenTime >= startTime and betweenTime <= endTime
    else:
        return betweenTime >= startTime or betweenTime <= endTime

#Round integer to base
def round_integer_base(integer, base=5):
    return int(base * round(float(integer) / base))

#Shutdown Kodi
def close_kodi_force():
    xbmc.shutdown()

#Shutdown device with dialog
def device_shutdown_dialog():
    dialogAnswers = ['Ja', 'Nee']
    dialogHeader = 'Apparaat uitschakelen?'
    dialogSummary = 'Weet u zeker dat u dit apparaat wilt uitschakelen?'
    dialogFooter = ''

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == 'Ja':
        xbmc.executebuiltin('Powerdown')

#Shutdown device forced
def device_shutdown_force():
    xbmc.executebuiltin('Powerdown')

#Reboot device with dialog
def device_reboot_dialog():
    dialogAnswers = ['Ja', 'Nee']
    dialogHeader = 'Apparaat herstarten?'
    dialogSummary = 'Weet u zeker dat u dit apparaat wilt herstarten?'
    dialogFooter = ''

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == 'Ja':
        xbmc.executebuiltin('Reboot')
