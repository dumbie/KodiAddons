import xbmcgui
import download
import guifunc
import lirecordingevent
import var

def switch_to_page():
    if var.guiRecordingEvent == None:
        var.guiRecordingEvent = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiRecordingEvent.setProperty('WebbiePlayerPage', 'Open')
        var.guiRecordingEvent.show()

def close_the_page():
    if var.guiRecordingEvent != None:
        #Close the shown window
        var.guiRecordingEvent.close()
        var.guiRecordingEvent = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        guifunc.updateLabelText(self, 3000, 'Geplande Opnames')
        guifunc.updateLabelText(self, 4001, 'Opnames vernieuwen')
        guifunc.updateVisibility(self, 4001, True)

        #Load all current set recording
        self.load_recording(False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            #Remove record event
            listItemSelected = clickedControl.getSelectedItem()
            ProgramRecordEventId = listItemSelected.getProperty("ProgramRecordEventId")
            ProgramDeltaTimeStart = listItemSelected.getProperty("ProgramDeltaTimeStart")
            recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramDeltaTimeStart)
            if recordRemove == True:
                #Remove item from the list
                removeListItemId = clickedControl.getSelectedPosition()
                guifunc.listRemoveItem(clickedControl, removeListItemId)
                guifunc.listSelectItem(clickedControl, removeListItemId)

                #Update the status
                self.count_recording(False)
        elif clickId == 4000:
            close_the_page()
        elif clickId == 4001:
            self.load_recording(True)

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()

    def load_recording(self, forceUpdate=False):
        #Get and check the list container
        listContainer = self.getControl(1000)
        guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 3001, "Geplande opnames worden geladen.")
        if lirecordingevent.list_load_combined(listContainer, forceUpdate) == False:
            guifunc.updateLabelText(self, 3001, 'Geplande opnames zijn niet beschikbaar')
            closeButton = self.getControl(4000)
            guifunc.controlFocus(self, closeButton)
            return False

        #Update the status
        self.count_recording(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

    #Update the status
    def count_recording(self, resetSelect=False):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            guifunc.updateLabelText(self, 3000, 'Geplande Opnames (' + str(listContainer.size()) + ')')
            guifunc.updateLabelText(self, 3001, 'Huidig geplande programma opnames, u kunt een opname annuleren door er op te klikken.')
            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectItem(listContainer, 0)
        else:
            guifunc.updateLabelText(self, 3000, 'Geplande Opnames (0)')
            guifunc.updateLabelText(self, 3001, 'Er zijn geen programma opnames gepland, u kunt een nieuwe opname plannen in de TV Gids of op de Televisie pagina.')
            closeButton = self.getControl(4000)
            guifunc.controlFocus(self, closeButton)
