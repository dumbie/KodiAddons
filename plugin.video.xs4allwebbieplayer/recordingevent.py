import xbmc
import xbmcgui
import download
import func
import lirecordingevent
import var

def switch_to_page():
    if var.guiRecordingEvent == None:
        var.guiRecordingEvent = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiRecordingEvent.show()

def close_the_page():
    if var.guiRecordingEvent != None:
        #Close the shown window
        var.guiRecordingEvent.close()
        var.guiRecordingEvent = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        func.updateLabelText(self, 3000, 'Geplande Opnames')
        func.updateLabelText(self, 4001, 'Opnames vernieuwen')
        func.updateVisibility(self, 4001, True)

        #Load all current set recording
        self.load_recording(False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            ProgramRecordEventId = listItemSelected.getProperty("ProgramRecordEventId")
            ProgramStartDeltaTime = listItemSelected.getProperty("ProgramStartDeltaTime")
            recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
            if recordRemove == True:
                #Remove item from the list
                removeListItemId = clickedControl.getSelectedPosition()
                clickedControl.removeItem(removeListItemId)
                xbmc.sleep(100)
                clickedControl.selectItem(removeListItemId)
                xbmc.sleep(100)

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
        listContainer = self.getControl(1000)
        listContainer.reset()

        #Download the recording programs
        func.updateLabelText(self, 3001, "Geplande opnames worden gedownload.")
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 3001, 'Geplande opnames zijn niet beschikbaar')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 3001, "Geplande opnames worden geladen.")

        #Add items to sort list
        listContainerSort = []
        lirecordingevent.list_load(listContainerSort)

        #Sort and add items to container
        listContainerSort.sort(key=lambda x: int(x.getProperty('ProgramStartTime')))
        listContainer.addItems(listContainerSort)

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
            func.updateLabelText(self, 3000, 'Geplande Opnames (' + str(listContainer.size()) + ')')
            func.updateLabelText(self, 3001, 'Huidig geplande programma opnames, u kunt een opname annuleren door er op te klikken.')
            if resetSelect == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 3000, 'Geplande Opnames (0)')
            func.updateLabelText(self, 3001, 'Er zijn geen programma opnames gepland, u kunt een nieuwe opname plannen in de TV Gids of op de Televisie pagina.')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
