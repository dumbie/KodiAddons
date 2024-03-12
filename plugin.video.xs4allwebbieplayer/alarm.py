from datetime import datetime, timedelta
import json
import xbmc
import xbmcgui
import dialog
import files
import func
import guifunc
import lialarm
import path
import var

def switch_to_page():
    if var.guiAlarm == None:
        var.guiAlarm = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiAlarm.setProperty('WebbiePlayerPage', 'Open')
        var.guiAlarm.show()

def close_the_page():
    if var.guiAlarm != None:
        #Close the shown window
        var.guiAlarm.close()
        var.guiAlarm = None

def alarm_json_load(forceLoad=False):
    try:
        if var.AlarmDataJson == [] or forceLoad == True:
            if files.existFileUser('AlarmDataString1.js') == True:
                AlarmJsonString = files.openFileUser('AlarmDataString1.js')
                var.AlarmDataJson = json.loads(AlarmJsonString)
    except:
        var.AlarmDataJson = []

def alarm_clean_expired(delayed=False):
    #Delay expired alarm cleaning
    if delayed == True:
        xbmc.sleep(2000)

    #Check if alarm has already passed
    for alarm in var.AlarmDataJson:
        try:
            ProgramTimeStartDateTime = func.datetime_from_string(alarm['starttime'], '%Y-%m-%d %H:%M:%S')

            #Remove the alarm if it has passed
            if datetime.now() >= ProgramTimeStartDateTime:
                var.AlarmDataJson.remove(alarm)
        except:
            continue

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.AlarmDataJson).encode('ascii')
    files.saveFileUser('AlarmDataString1.js', JsonDumpBytes)

    #Update the main page count
    if var.guiMain != None:
        var.guiMain.count_alarm()

    #Update the alarm window count
    if var.guiAlarm != None:
        var.guiAlarm.count_alarm()

    return True

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
    notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')

    #Check if alarm start time already exists
    if removeDuplicate == True and alarm_duplicate_program_check(ProgramTimeStartDateTime, ChannelId):
        alarm_remove(ProgramTimeStartDateTime)
        return 'Remove'
    elif alarm_duplicate_time_check(ProgramTimeStartDateTime):
        xbmcgui.Dialog().notification(var.addonname, 'Er is al een alarm voor dit tijdstip.', notificationIcon, 2500, False)
        return False

    #Check if program is more than 3 minutes away
    ProgramTimeLeft = int((ProgramTimeStartDateTime - datetime.now()).total_seconds())
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

    #Update the main page count
    if var.guiMain != None:
        var.guiMain.count_alarm()

    #Update the alarm window count
    if var.guiAlarm != None:
        var.guiAlarm.count_alarm()

    return True

def alarm_remove(ProgramTimeStart):
    #Check if the alarm start exists
    for alarm in var.AlarmDataJson:
        try:
            if str(ProgramTimeStart) == alarm['starttime']:
                var.AlarmDataJson.remove(alarm)
        except:
            continue

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.AlarmDataJson).encode('ascii')
    files.saveFileUser('AlarmDataString1.js', JsonDumpBytes)

    #Alarm has been removed notification
    notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
    xbmcgui.Dialog().notification(var.addonname, 'Programma alarm is geannuleerd.', notificationIcon, 2500, False)

    #Update the main page count
    if var.guiMain != None:
        var.guiMain.count_alarm()

    #Update the alarm window count
    if var.guiAlarm != None:
        var.guiAlarm.count_alarm()

    return True

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

            #Update the main page count
            if var.guiMain != None:
                var.guiMain.count_alarm()

            #Update the alarm window count
            if var.guiAlarm != None:
                var.guiAlarm.count_alarm()

            return True
    else:
        notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
        xbmcgui.Dialog().notification(var.addonname, 'Er zijn geen alarmen gezet.', notificationIcon, 2500, False)
    return False

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        guifunc.updateLabelText(self, 3000, 'Geplande Alarmen')
        guifunc.updateLabelText(self, 4001, 'Alle alarmen annuleren')
        guifunc.updateLabelText(self, 3002, '* Programma alarm werkt alleen als Kodi geopend is.')
        guifunc.updateVisibility(self, 4001, True)

        #Update the schedule panel height
        dialogControl = self.getControl(8000)
        dialogControl.setHeight(590)
        dialogControl = self.getControl(8001)
        dialogControl.setHeight(592)

        #Clear expired alarms from Json
        alarm_clean_expired()

        #Load all current set alarms
        self.load_alarm()

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            ProgramTimeStart = listItemSelected.getProperty('ProgramTimeStart')
            alarmRemoved = alarm_remove(ProgramTimeStart)
            if alarmRemoved == True:
                #Remove item from the list
                removeListItemIndex = clickedControl.getSelectedPosition()
                guifunc.listRemoveItem(clickedControl, removeListItemIndex)
                guifunc.listSelectIndex(clickedControl, removeListItemIndex)
        elif clickId == 4000:
            close_the_page()
        elif clickId == 4001:
            if alarm_remove_all():
                close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()

    def load_alarm(self):
        #Get and check the list container
        listContainer = self.getControl(1000)
        guifunc.listReset(listContainer)

        #Add items to list container
        lialarm.list_load_combined(listContainer)

        #Update the status
        self.count_alarm(True)

    #Update the status
    def count_alarm(self, resetSelect=False):
        listContainer = self.getControl(1000)
        alarmCount = len(var.AlarmDataJson)
        if alarmCount > 0:
            guifunc.updateLabelText(self, 3000, 'Geplande Alarmen (' + str(alarmCount) + ')')
            guifunc.updateLabelText(self, 3001, 'Huidig geplande programma alarmen, u kunt een alarm annuleren door er op te klikken.')
            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectIndex(listContainer, 0)
        else:
            guifunc.updateLabelText(self, 3000, 'Geplande Alarmen (0)')
            guifunc.updateLabelText(self, 3001, 'Er zijn geen programma alarmen gezet, u kunt een nieuw alarm zetten in de tv gids, op de televisie pagina of tijdens het tv kijken.')
            closeButton = self.getControl(4000)
            guifunc.controlFocus(self, closeButton)
