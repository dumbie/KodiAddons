from datetime import datetime, timedelta
import json
import xbmc
import xbmcgui
import alarmfunc
import files
import func
import path
import var

def alarm_notification():
    for alarm in var.AlarmDataJson:
        try:
            #Load alarm details
            ExternalId = alarm['externalid']
            ProgramName = alarm['programname']
            StartTime = alarm['starttime']

            #Calculate alarm times
            DateTimeNowDateTime = datetime.now()
            DateTimeNowString = DateTimeNowDateTime.strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartDateTime = func.datetime_from_string(StartTime, '%Y-%m-%d %H:%M:%S')
            ProgramTimeStartPlusThreeDateTime = (ProgramTimeStartDateTime + timedelta(minutes=3))
            ProgramTimeStartMinOneString = (ProgramTimeStartDateTime - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinTwoString = (ProgramTimeStartDateTime - timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinThreeString = (ProgramTimeStartDateTime - timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinFiveString = (ProgramTimeStartDateTime - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')
            ProgramTimeStartMinTenString = (ProgramTimeStartDateTime - timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M')

            #Check alarm times
            if DateTimeNowDateTime >= ProgramTimeStartDateTime and DateTimeNowDateTime < ProgramTimeStartPlusThreeDateTime:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' is begonnen.', path.icon_television(ExternalId), 10000, True)
            elif DateTimeNowString == ProgramTimeStartMinOneString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 1 minuut.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinTwoString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 2 minuten.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinThreeString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 3 minuten.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinFiveString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 5 minuten.', path.icon_television(ExternalId), 5000, True)
            elif DateTimeNowString == ProgramTimeStartMinTenString:
                xbmcgui.Dialog().notification(var.addonname, ProgramName + ' begint over 10 minuten.', path.icon_television(ExternalId), 5000, True)
        except:
            continue

def alarm_clean_expired():
    #Check if alarm has already passed
    alarmRemoved = False
    for alarm in var.AlarmDataJson[:]:
        try:
            ProgramTimeStartDateTime = func.datetime_from_string(alarm['starttime'], '%Y-%m-%d %H:%M:%S')

            #Remove the alarm if it has passed
            if datetime.now() >= ProgramTimeStartDateTime:
                var.AlarmDataJson.remove(alarm)
                alarmRemoved = True
        except:
            continue

    if alarmRemoved == True:
        #Save the raw json data to storage
        JsonDumpBytes = json.dumps(var.AlarmDataJson).encode('ascii')
        files.saveFileUser('AlarmDataString1.js', JsonDumpBytes)

        #Notify to reload alarms
        xbmc.executebuiltin('NotifyAll(WebbiePlayer, alarm_reload)')

    return alarmRemoved

def thread_alarm_timer():
    threadLastTime = ''
    while var.thread_alarm_timer.Allowed(sleepDelayMs=1000):
        try:
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime:
                threadLastTime = threadCurrentTime
                alarmfunc.alarm_json_load(True)
                alarm_notification()
                alarm_clean_expired()
        except:
            pass

def start_alarm_check():
    var.thread_alarm_timer.Start(thread_alarm_timer)

def stop_alarm_check():
    var.thread_alarm_timer.Stop()
