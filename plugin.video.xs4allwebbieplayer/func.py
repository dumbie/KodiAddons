import re
import time
import pickle
import codecs
from datetime import datetime, date, timedelta
import xbmc
import xbmcgui
import dialog
import hybrid
import var

#Run this add-on
def run_addon(forceLaunch=False):
    if var.addon.getSetting('RunAddonOnKodiLaunch') == 'true' or forceLaunch:
        xbmcgui.Dialog().notification(var.addonname, 'Webbie Player wordt gestart.', var.addonicon, 2500, False)
        xbmc.executebuiltin('RunScript(plugin.video.xs4allwebbieplayer)')

#Get provider color string
def get_provider_color_string():
    currentProvider = var.addon.getSetting('AddonAccent').lower()
    if currentProvider == 'geel':
        return '[COLOR FFF5AF00]'
    elif currentProvider == 'blauw':
        return '[COLOR FF2F41B7]'
    elif currentProvider == 'groen':
        return '[COLOR FF009900]'
    elif currentProvider == 'grijs':
        return '[COLOR FF888888]'

#Search filter string
def search_filter_string(searchString):
    searchFilterTerm = searchString.lower()
    searchFilterTerm = hybrid.string_remove_accents(searchFilterTerm)
    return searchFilterTerm

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
    #Fix: find way to directly close the window
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

#Day offset from datetime
def day_offset_from_datetime(dayDateTime):
    return (datetime.now().date() - dayDateTime.date()).days

#Datetime from day offset
def datetime_from_day_offset(numberDayOffset):
    return datetime.now() + timedelta(days=numberDayOffset)

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

#Convert epoch ticks to seconds
def ticks_to_seconds(ticks):
    return int(ticks) / 100000 * 60

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
    dialogHeader = 'Kodi afsluiten?'
    dialogSummary = 'Weet u zeker dat u Kodi wilt afsluiten?'
    dialogFooter = ''

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == 'Ja':
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

#Set global variable
def globalvar_set(varName, varObject, varHead='Webbie'):
    try:
        pickleString = object_to_picklestring(varObject)
        var.windowHome.setProperty(varHead + varName, pickleString)
        return True
    except:
        return False

#Get global variable
def globalvar_get(varName, defaultObject=None, varHead='Webbie'):
    try:
        pickleString = var.windowHome.getProperty(varHead + varName)
        return picklestring_to_object(pickleString)
    except:
        return defaultObject

#Convert object to pickle string
def object_to_picklestring(object):
    return codecs.encode(pickle.dumps(object), "base64").decode()

#Convert pickle string to object
def picklestring_to_object(picklestring):
    return pickle.loads(codecs.decode(picklestring.encode(), "base64"))
