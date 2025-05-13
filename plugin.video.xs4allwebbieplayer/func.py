from datetime import date, datetime, time, timedelta
import base64
import json
import pickle
import re
import time
import xbmc
import xbmcgui
import dialog
import getset
import hybrid
import var

#Run this add-on
def run_addon(showNotification=True):
    if showNotification == True:
        xbmcgui.Dialog().notification(var.addonname, 'Webbie Player wordt gestart.', var.addonicon, 2500, False)
    xbmc.executebuiltin('RunScript(plugin.video.xs4allwebbieplayer)')

#Check if add-on is running
def check_addon_running():
    return getset.get_addon_windowId_bottom() != 0

#Check for add-on updates
def check_addon_updates(showNotification=True):
    if showNotification == True:
        xbmcgui.Dialog().notification(var.addonname, 'Controleren add-on updates gestart.', var.addonicon, 2500, False)
    xbmc.executebuiltin('UpdateAddonRepos')

#Check if loop is allowed
def check_loop_allowed():
    try:
        return var.addonmonitor.abortRequested() == False
    except:
        return False

#Check if current window is add-on
def check_currentwindow_is_addon():
    return xbmcgui.getCurrentWindowId() == getset.get_addon_windowId_top()

#Stop currently playing media
def stop_playing_media():
    if xbmc.Player().isPlaying():
        xbmc.executebuiltin('PlayerControl(Stop)')

#Search filter string
def search_filter_string(searchString):
    searchFilterTerm = searchString.lower()
    searchFilterTerm = hybrid.string_remove_accents(searchFilterTerm)
    return searchFilterTerm

#Open a window by id
def open_window_id(windowId):
    try:
        xbmc.executebuiltin('ActivateWindow(' + str(windowId) + ')')
    except:
        pass

#Close a window by id
def close_window_id(windowId):
    #Fix: find way to directly close the window
    try:
        currentWindowId = xbmcgui.getCurrentWindowId()
        if currentWindowId == windowId:
            xbmc.executebuiltin('Action(Close)')
    except:
        pass

#Convert object to type with backup value
def to_type(convertType, convertObject, defaultValue=None):
    try:
        return convertType(convertObject)
    except:
        return defaultValue

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

#Day offset from datetime
def day_offset_from_datetime(dayDateTime):
    return (datetime.now().date() - dayDateTime.date()).days

#Datetime from day offset
def datetime_from_day_offset(numberDayOffset):
    return datetime_remove_seconds(datetime.now() + timedelta(days=numberDayOffset))

#Day description from datetime
def day_string_from_datetime(dayDateTime, includeYear=True):
    todayDateTime = datetime.now().date()
    dayDateTime = dayDateTime.date()
    if includeYear:
        dayString = dayDateTime.strftime('%a, %d %B %Y')
    else:
        dayString = dayDateTime.strftime('%a, %d %B')

    if dayDateTime == todayDateTime + timedelta(days=2):
        dayString += ' (Overmorgen)'
    elif dayDateTime == todayDateTime + timedelta(days=1):
        dayString += ' (Morgen)'
    elif dayDateTime == todayDateTime:
        dayString += ' (Vandaag)'
    elif dayDateTime == todayDateTime + timedelta(days=-1):
        dayString += ' (Gisteren)'
    elif dayDateTime == todayDateTime + timedelta(days=-2):
        dayString += ' (Eergister)'
    return dayString

#Day description from day offset
def day_string_from_day_offset(numberDayOffset, includeYear=True):
    todayDateTime = datetime.now().date()
    dayDateTime = todayDateTime + timedelta(days=numberDayOffset)
    if includeYear:
        dayString = dayDateTime.strftime('%a, %d %B %Y')
    else:
        dayString = dayDateTime.strftime('%a, %d %B')

    if dayDateTime == todayDateTime + timedelta(days=2):
        dayString += ' (Overmorgen)'
    elif dayDateTime == todayDateTime + timedelta(days=1):
        dayString += ' (Morgen)'
    elif dayDateTime == todayDateTime:
        dayString += ' (Vandaag)'
    elif dayDateTime == todayDateTime + timedelta(days=-1):
        dayString += ' (Gisteren)'
    elif dayDateTime == todayDateTime + timedelta(days=-2):
        dayString += ' (Eergister)'
    return dayString

#Convert number to single string
def number_to_single_string(number):
    return str(int(number))

#Convert datetime to string
def datetime_to_string(date_time, date_format):
    return date_time.strftime(date_format)

#Convert string to datetime
def datetime_from_string(date_string, date_format):
    return datetime(*(time.strptime(date_string, date_format)[0:6]))

#Get current time in epoch ticks
def ticks_current_time():
    return time.time()

#Convert epoch ticks to seconds
def ticks_to_seconds(ticks):
    return float(ticks) / 100000 * 60

#Convert epoch ticks to datetime
def datetime_from_ticks(ticks):
    return datetime.fromtimestamp(float(ticks) / 1000)

#Convert datetime to epoch ticks
def datetime_to_ticks(dateTime, utcCorrection=False):
    if utcCorrection:
        timeOffsetUtcSeconds = (datetime.now() - datetime.utcnow()).total_seconds()
    else:
        timeOffsetUtcSeconds = 0
    return int((dateTime - datetime(1970,1,1)).total_seconds() - timeOffsetUtcSeconds) * 1000

#Remove seconds from datetime
def datetime_remove_seconds(datetime):
    return datetime.replace(second=0, microsecond=0)

#Get datetime midnight
def datetime_to_midnight(datetime):
    return datetime.replace(hour=0, minute=0, second=0, microsecond=0)

#Get days in current year
def days_in_year():
    TodayYear = datetime.now().year
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

#Shutdown Kodi with dialog
def close_kodi_dialog():
    dialogAnswers = ['Ja', 'Nee']
    dialogHeader = 'Kodi afsluiten'
    dialogSummary = 'Weet u zeker dat u Kodi wilt afsluiten?'
    dialogFooter = ''

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == 'Ja':
        xbmc.shutdown()

#Shutdown device with dialog
def device_shutdown_dialog():
    dialogAnswers = ['Ja', 'Nee']
    dialogHeader = 'Apparaat uitschakelen'
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
    dialogHeader = 'Apparaat herstarten'
    dialogSummary = 'Weet u zeker dat u dit apparaat wilt herstarten?'
    dialogFooter = ''

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == 'Ja':
        xbmc.executebuiltin('Reboot')

#Convert object to pickle string
def object_to_picklestring(object, useBase64=True):
    if useBase64:
        return base64.urlsafe_b64encode(pickle.dumps(object))
    else:
        return pickle.dumps(object)

#Convert pickle string to object
def picklestring_to_object(picklestring, useBase64=True):
    if useBase64:
        return pickle.loads(base64.urlsafe_b64decode(picklestring))
    else:
        return pickle.loads(picklestring)

#Convert dictionary to json string
def dictionary_to_jsonstring(dictionary, useBase64=True):
    if useBase64:
        return base64.urlsafe_b64encode(json.dumps(dictionary).encode("ascii")).decode("ascii")
    else:
        return json.dumps(dictionary)

#Convert json string to dictionary
def jsonstring_to_dictionary(jsonString, useBase64=True):
    if useBase64:
        return json.loads(base64.urlsafe_b64decode(jsonString.encode("ascii")).decode("ascii"))
    else:
        return json.loads(jsonString)
