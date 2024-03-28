import xbmcgui
import alarmfunc
import guifunc
import lialarm
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
        dialogControl.setHeight(593)

        #Load all current set alarms
        self.load_alarm()

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            ProgramTimeStart = listItemSelected.getProperty('ProgramTimeStart')
            if alarmfunc.alarm_remove(ProgramTimeStart) == True:
                #Remove item from the list
                removeListItemIndex = clickedControl.getSelectedPosition()
                guifunc.listRemoveItem(clickedControl, removeListItemIndex)
                guifunc.listSelectIndex(clickedControl, removeListItemIndex)
        elif clickId == 4000:
            close_the_page()
        elif clickId == 4001:
            if alarmfunc.alarm_remove_all() == True:
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
