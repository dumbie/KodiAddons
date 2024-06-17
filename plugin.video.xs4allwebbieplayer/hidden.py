import xbmcgui
import guifunc
import hiddenfunc
import kids
import lihidden
import path
import var

def switch_to_page(hiddenMode='HiddenTelevision.js'):
    #Check kids lock
    if kids.lock_check() == False:
        return

    #Update hidden mode variable
    var.HiddenChannelMode = hiddenMode

    #Check if there are hidden tv channels
    if var.HiddenChannelMode == 'HiddenTelevision.js' and var.HiddenTelevisionJson == []:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Geen verborgen zenders.', notificationIcon, 2500, False)
        return

    #Check if there are hidden radio channels
    if var.HiddenChannelMode == 'HiddenRadio.js' and var.HiddenRadioJson == []:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Geen verborgen zenders.', notificationIcon, 2500, False)
        return

    #Show hidden channel overlay
    if var.guiHidden == None:
        var.guiHidden = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiHidden.setProperty('WebbiePlayerPage', 'Open')
        var.guiHidden.show()

def close_the_page():
    if var.guiHidden != None:
        #Refresh television channels on change
        if var.guiTelevision != None and var.HiddenChannelChanged == True:
            var.guiTelevision.load_channels(True)
            var.HiddenChannelChanged = False

        #Refresh radio channels on change
        if var.guiRadio != None and var.HiddenChannelChanged == True:
            var.guiRadio.load_channels(True)
            var.HiddenChannelChanged = False

        #Refresh stb channels on change
        if var.guiStb != None and var.HiddenChannelChanged == True:
            var.guiStb.load_channels(True)
            var.HiddenChannelChanged = False

        #Close the shown window
        var.guiHidden.close()
        var.guiHidden = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        guifunc.updateLabelText(self, 3000, 'Verborgen Zenders')
        guifunc.updateVisibility(self, 4001, False)

        #Update the schedule panel height
        dialogControl = self.getControl(8000)
        dialogControl.setHeight(590)
        dialogControl = self.getControl(8001)
        dialogControl.setHeight(592)

        #Load current hidden channels
        self.load_hidden_channels()

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            hiddenRemoved = hiddenfunc.hidden_remove_channel(listItemSelected, var.HiddenChannelMode)
            if hiddenRemoved == True:
                #Remove item from the list
                removeListItemIndex = clickedControl.getSelectedPosition()
                guifunc.listRemoveItem(clickedControl, removeListItemIndex)
                guifunc.listSelectIndex(clickedControl, removeListItemIndex)

                #Update changed variable
                var.HiddenChannelChanged = True

                #Update channel count
                self.count_hidden_channels(False)
        elif clickId == 4000:
            close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()

    def load_hidden_channels(self):
        #Get and check the list container
        listContainer = self.getControl(1000)
        guifunc.listReset(listContainer)

        #Add items to list container
        lihidden.list_load_combined(listContainer, var.HiddenChannelMode)

        #Update the status
        self.count_hidden_channels(True)

    #Update the status
    def count_hidden_channels(self, resetSelect=False):
        listContainer = self.getControl(1000)
        if var.HiddenChannelMode == 'HiddenTelevision.js':
            channelcount = len(var.HiddenTelevisionJson)
        elif var.HiddenChannelMode == 'HiddenRadio.js':
            channelcount = len(var.HiddenRadioJson)

        if channelcount > 0:
            guifunc.updateLabelText(self, 3000, 'Verborgen Zenders (' + str(channelcount) + ')')
            guifunc.updateLabelText(self, 3001, 'Huidige verborgen zenders, u kunt een zender weer laten verschijnen in de zenderlijst door er op te klikken.')
            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectIndex(listContainer, 0)
        else:
            guifunc.updateLabelText(self, 3000, 'Verborgen Zenders (0)')
            guifunc.updateLabelText(self, 3001, 'Er zijn geen verborgen zenders, u kunt een zender verbergen in de zenderlijst.')
            closeButton = self.getControl(4000)
            guifunc.controlFocus(self, closeButton)
