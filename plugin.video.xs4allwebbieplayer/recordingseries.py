import xbmc
import xbmcgui
import dialog
import download
import func
import lirecordingseries
import var

def switch_to_page():
    if var.guiRecordingSeries == None:
        var.guiRecordingSeries = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiRecordingSeries.show()

def close_the_page():
    if var.guiRecordingSeries != None:
        #Close the shown window
        var.guiRecordingSeries.close()
        var.guiRecordingSeries = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        func.updateLabelText(self, 3000, 'Geplande Series')
        func.updateLabelText(self, 4001, 'Series vernieuwen')
        func.updateVisibility(self, 4001, True)

        #Load all current set recording
        self.load_recording(False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            SeriesId = listItemSelected.getProperty('SeriesId')

            #Ask user to remove recordings
            dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
            dialogHeader = 'Serie opnames verwijderen'
            dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
            dialogFooter = ''
            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult == 'Opnames verwijderen':
                KeepRecording = False
            elif dialogResult == 'Opnames houden': 
                KeepRecording = True
            else:
                return

            #Remove record series
            recordingRemoved = download.record_series_remove(SeriesId, KeepRecording)
            if recordingRemoved == True:
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
        listcontainer = self.getControl(1000)
        listcontainer.reset()

        #Download the tv channels
        func.updateLabelText(self, 3001, 'Televisie zenders worden gedownload.')
        download.download_channels_tv(False)

        #Download the recording programs
        func.updateLabelText(self, 3001, "Geplande series worden gedownload.")
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 3001, 'Geplande series zijn niet beschikbaar')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 3001, "Geplande series worden geladen.")

        #Add items to sort list
        listcontainersort = []
        lirecordingseries.list_load(listcontainersort)

        #Sort and add items to container
        listcontainersort.sort(key=lambda x: x.getProperty('ProgramName'))
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_recording(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recording_series()

    #Update the status
    def count_recording(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateLabelText(self, 3000, 'Geplande Series (' + str(listcontainer.size()) + ')')
            func.updateLabelText(self, 3001, 'U kunt een serie seizoen annuleren door er op te klikken.')
            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 3000, 'Geplande Series (0)')
            func.updateLabelText(self, 3001, 'Er zijn geen serie seizoen opnames gepland, u kunt een nieuwe serie seizoen opnemen vanuit de TV Gids.')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
