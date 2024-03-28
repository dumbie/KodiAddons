from datetime import datetime, timedelta
import json
import xbmc
import xbmcgui
import dialog
import files
import path
import var

def alarm_json_load(forceLoad=False):
    try:
        if var.AlarmDataJson == [] or forceLoad == True:
            if files.existFileUser('AlarmDataString1.js') == True:
                AlarmJsonString = files.openFileUser('AlarmDataString1.js')
                var.AlarmDataJson = json.loads(AlarmJsonString)
    except:
        var.AlarmDataJson = []

def alarm_get_count():
    #Load set program alarms
    alarm_json_load()

    #Return program alarms count
    return len(var.AlarmDataJson)

def alarm_update_interface():
    #Update the main page count
    if var.guiMain != None:
        var.guiMain.count_alarm()

    #Update the alarm window count
    if var.guiAlarm != None:
        var.guiAlarm.count_alarm()

def alarm_duplicate_time_check(ProgramTimeStart):
    for alarm in var.AlarmDataJson:
        try:
            if alarm['starttime'] == str(ProgramTimeStart):
                return True
        except:
            continue
    return False

def alarm_duplicate_program_check(ProgramTimeStart, ChannelId):
    for alarm in var.AlarmDataJson:
        try:
            if alarm['starttime'] == str(ProgramTimeStart) and alarm['channelid'] == ChannelId:
                return True
        except:
            continue
    return False

def alarm_duplicate_channel_check(ChannelId):
    for alarm in var.AlarmDataJson:
        try:
            if alarm['channelid'] == ChannelId:
                return True
        except:
            continue
    return False

def alarm_add(ProgramTimeStartDateTime, ChannelId, ExternalId, ChannelName, ProgramName, removeDuplicate=False):
    #Load set program alarms
    alarm_json_load()

    notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
    dateTimeNow = datetime.now()

    #Check if alarm start time already exists
    if removeDuplicate == True and alarm_duplicate_program_check(ProgramTimeStartDateTime, ChannelId):
        alarm_remove(ProgramTimeStartDateTime)
        return 'Remove'
    elif alarm_duplicate_time_check(ProgramTimeStartDateTime):
        xbmcgui.Dialog().notification(var.addonname, 'Er is al een alarm voor dit tijdstip.', notificationIcon, 2500, False)
        return False

    #Check if program time is valid
    if ProgramTimeStartDateTime == datetime(1970,1,1):
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldig programma begin tijd.', notificationIcon, 2500, False)
        return False

    #Check if program time is in future
    if dateTimeNow > ProgramTimeStartDateTime:
        xbmcgui.Dialog().notification(var.addonname, 'Programma is al afgelopen.', notificationIcon, 2500, False)
        return False

    #Check if program time is atleast 3 minutes away
    ProgramTimeLeft = int((ProgramTimeStartDateTime - dateTimeNow).total_seconds())
    if ProgramTimeLeft <= 180:
        xbmcgui.Dialog().notification(var.addonname, 'Programma begint binnen 3 minuten.', notificationIcon, 2500, False)
        return False

    #Append the new alarm to Json
    var.AlarmDataJson.append({"starttime": str(ProgramTimeStartDateTime), "channelid": ChannelId, "externalid": ExternalId, "channelname": ChannelName, "programname": ProgramName})

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.AlarmDataJson).encode('ascii')
    files.saveFileUser('AlarmDataString1.js', JsonDumpBytes)

    #Alarm has been set notification
    xbmcgui.Dialog().notification(var.addonname, 'Alarm gezet: ' + ProgramName + ' (' + ChannelName + ')', notificationIcon, 2500, False)

    #Update interface information
    alarm_update_interface()

    return True

def alarm_remove(ProgramTimeStart, remoteMode=False):
    #Load set program alarms
    alarm_json_load()

    #Check if the alarm start exists
    alarmRemoved = False
    for alarm in var.AlarmDataJson[:]:
        try:
            if str(ProgramTimeStart) == alarm['starttime']:
                var.AlarmDataJson.remove(alarm)
                alarmRemoved = True
        except:
            continue

    if alarmRemoved == True:
        #Save the raw json data to storage
        JsonDumpBytes = json.dumps(var.AlarmDataJson).encode('ascii')
        files.saveFileUser('AlarmDataString1.js', JsonDumpBytes)

        #Alarm has been removed notification
        notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma alarm is geannuleerd.', notificationIcon, 2500, False)

        if remoteMode == False:
            #Update interface information
            alarm_update_interface()
        else:
            #Notify to reload alarms
            xbmc.executebuiltin('NotifyAll(WebbiePlayer, alarm_reload)')

    return alarmRemoved

def alarm_remove_all():
    if len(var.AlarmDataJson) > 0:
        dialogAnswers = ['Alle alarmen annuleren']
        dialogHeader = 'Alle alarmen annuleren'
        dialogSummary = 'Weet u zeker dat u alle geplande alarmen wilt annuleren?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Alle alarmen annuleren':
            #Remove all the set alarms
            var.AlarmDataJson = []

            #Save the raw json data to storage
            JsonDumpBytes = json.dumps(var.AlarmDataJson).encode('ascii')
            files.saveFileUser('AlarmDataString1.js', JsonDumpBytes)

            #Alarm has been removed notification
            notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
            xbmcgui.Dialog().notification(var.addonname, 'Alle alarmen zijn geannuleerd.', notificationIcon, 2500, False)

            #Update interface information
            alarm_update_interface()

            return True
    else:
        notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
        xbmcgui.Dialog().notification(var.addonname, 'Er zijn geen alarmen gezet.', notificationIcon, 2500, False)
    return False
