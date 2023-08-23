from datetime import datetime, timedelta
from threading import Thread
import alarm
import xbmc
import xbmcgui
import func
import path
import var

def alarm_notification():
    for alarm in var.AlarmDataJson:
        try:
            #Load alarm details
            #ChannelId = alarm['channelid']
            ExternalId = alarm['externalid']
            #ChannelName = alarm['channelname']
            ProgramName = alarm['programname']
            StartTime = alarm['starttime']

            #Calculate alarm times
            DateTimeNowDateTime = datetime.now()
            DateTimeNowString = DateTimeNowDateTime.strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartDateTime = func.datetime_from_string(StartTime, '%Y-%m-%d %H:%M:%S')
            ProgramTimeStartPlusThreeDateTime = (ProgramTimeStartDateTime + timedelta(minutes=3))
            ProgramTimeStartMinOneString = (ProgramTimeStartDateTime - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinThreeString = (ProgramTimeStartDateTime - timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinFiveString = (ProgramTimeStartDateTime - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinTenString = (ProgramTimeStartDateTime - timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M')

            #Check alarm times
            if DateTimeNowDateTime >= ProgramTimeStartDateTime and DateTimeNowDateTime < ProgramTimeStartPlusThreeDateTime:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' is begonnen.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinOneString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 1 minuut.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinThreeString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 3 minuten.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinFiveString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 5 minuten.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinTenString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 10 minuten.', path.icon_television(ExternalId), 5000, True)
        except:
            continue

def thread_alarm_timer():
    threadLastTime = ''
    while var.thread_alarm_timer != None and var.addonmonitor.abortRequested() == False: #Service thread no need to check addon running
        threadCurrentTime = datetime.now().strftime('%H:%M')
        if threadLastTime != threadCurrentTime:
            threadLastTime = threadCurrentTime
            alarm.alarm_json_load(True)
            alarm_notification()
            alarm.alarm_clean_expired(True)
        else:
            xbmc.sleep(1000)

def start_alarm_check():
    if var.thread_alarm_timer == None:
        var.thread_alarm_timer = Thread(target=thread_alarm_timer)
        var.thread_alarm_timer.start()

def stop_alarm_check():
    if var.thread_alarm_timer != None:
        var.thread_alarm_timer = None