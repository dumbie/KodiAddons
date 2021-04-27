from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import dialog
import func
import path
import var

def dialog_sleep():
    #Set default sleep times
    dialogAnswers = ['15 minuten', '30 minuten', '45 minuten', '60 minuten', '90 minuten', '120 minuten', '180 minuten']

    if var.thread_sleep_timer != None:
        dialogAnswers.append('Zet slaap timer uit')

    dialogHeader = 'Slaap Timer'

    if var.addon.getSetting('SleepTimerCloseKodi') == 'true':
        dialogSummary = 'Selecteer hier hoe lang u nog wilt kijken of luisteren voordat Kodi zich zelf automatisch zal afsluiten*'
    else:
        dialogSummary = 'Selecteer hier hoe lang u nog wilt kijken of luisteren voordat uw apparaat zich automatisch zal uitschakelen*'

    if var.thread_sleep_timer != None and var.SleepEndingMinutes > 0:
        dialogFooter = '* Huidige slaap timer loopt af in ' + str(var.SleepEndingMinutes) + ' minuten.'
    else:
        dialogFooter = '* Slaap timer werkt alleen als Webbie Player geopend is.'

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == '15 minuten':
        sleep_timerset(15)
    elif dialogResult == '30 minuten':
        sleep_timerset(30)
    elif dialogResult == '45 minuten':
        sleep_timerset(45)
    elif dialogResult == '60 minuten':
        sleep_timerset(60)
    elif dialogResult == '90 minuten':
        sleep_timerset(90)
    elif dialogResult == '120 minuten':
        sleep_timerset(120)
    elif dialogResult == '180 minuten':
        sleep_timerset(180)
    elif dialogResult == 'Zet slaap timer uit':
        sleep_timeroff(True)

def thread_sleep_timer():
    threadLastTime = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
    while var.thread_sleep_timer != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
        threadCurrentTime = datetime.now().strftime('%H:%M')
        if threadLastTime != threadCurrentTime:
            threadLastTime = threadCurrentTime
            var.SleepEndingMinutes -= 1
            sleep_notification()
        else:
            xbmc.sleep(1000)

def sleep_notification():
    #Check sleep times
    if var.SleepEndingMinutes <= 0:
        sleep_close()
    elif var.SleepEndingMinutes == 1:
        notificationIcon = path.resources('resources/skins/default/media/common/sleep.png')
        xbmcgui.Dialog().notification(var.addonname, 'Slaap timer in 1 minuut', notificationIcon, 5000, False)
    elif var.SleepEndingMinutes == 3:
        notificationIcon = path.resources('resources/skins/default/media/common/sleep.png')
        xbmcgui.Dialog().notification(var.addonname, 'Slaap timer in 3 minuten', notificationIcon, 5000, False)
    elif var.SleepEndingMinutes == 5:
        notificationIcon = path.resources('resources/skins/default/media/common/sleep.png')
        xbmcgui.Dialog().notification(var.addonname, 'Slaap timer in 5 minuten', notificationIcon, 5000, False)

def sleep_close():
    notificationIcon = path.resources('resources/skins/default/media/common/sleep.png')
    xbmcgui.Dialog().notification(var.addonname, 'Tot ziens', notificationIcon, 5000, False)
    sleep_timeroff(False)

    #Close Kodi or device
    if var.addon.getSetting('SleepTimerCloseKodi') == 'true':
        func.close_kodi()
    else:
        func.close_device()

def sleep_timeroff(showDialog):
    var.thread_sleep_timer = None
    var.SleepEndingMinutes = 9999
    var.windowHome.clearProperty('WebbiePlayerSleepTimer')
    if showDialog:
        notificationIcon = path.resources('resources/skins/default/media/common/sleep.png')
        xbmcgui.Dialog().notification(var.addonname, 'Slaap timer is uitgezet.', notificationIcon, 2500, False)

def sleep_timerset(minutes):
    var.SleepEndingMinutes = minutes
    var.windowHome.setProperty('WebbiePlayerSleepTimer', 'True')

    if var.thread_sleep_timer == None:
        var.thread_sleep_timer = Thread(target=thread_sleep_timer)
        var.thread_sleep_timer.start()

    notificationIcon = path.resources('resources/skins/default/media/common/sleep.png')
    xbmcgui.Dialog().notification(var.addonname, 'Slaap timer voor ' + str(minutes) + ' min is gezet.', notificationIcon, 2500, False)
