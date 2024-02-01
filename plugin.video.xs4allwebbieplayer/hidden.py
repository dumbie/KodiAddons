import json
import kids
import lihidden
import xbmc
import xbmcgui
import files
import func
import path
import var

def hidden_television_json_load():
    try:
        if var.HiddenTelevisionJson == [] and files.existFile('HiddenTelevision.js') == True:
            HiddenJsonString = files.openFile('HiddenTelevision.js')
            var.HiddenTelevisionJson = json.loads(HiddenJsonString)
    except:
        var.HiddenTelevisionJson = []

def hidden_radio_json_load():
    try:
        if var.HiddenRadioJson == [] and files.existFile('HiddenRadio.js') == True:
            HiddenJsonString = files.openFile('HiddenRadio.js')
            var.HiddenRadioJson = json.loads(HiddenJsonString)
    except:
        var.HiddenRadioJson = []

def hidden_check(ChannelId, hiddenJsonFile):
    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        hiddenTargetJson = var.HiddenTelevisionJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioJson
    return ChannelId in hiddenTargetJson

def hidden_add(listItem, hiddenJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        hiddenTargetJson = var.HiddenTelevisionJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioJson

    #Append the new hidden to Json
    hiddenTargetJson.append(ChannelId)

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(hiddenTargetJson).encode('ascii')
    files.saveFile(hiddenJsonFile, JsonDumpBytes)

    #Hidden has been set notification
    notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender is verborgen.', notificationIcon, 2500, False)
    return True

def hidden_remove(listItem, hiddenJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        hiddenTargetJson = var.HiddenTelevisionJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioJson

    hiddenRemoved = False
    for hidden in hiddenTargetJson:
        try:
            if hidden == ChannelId:
                hiddenTargetJson.remove(hidden)
                hiddenRemoved = True
                break
        except:
            continue

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(hiddenTargetJson).encode('ascii')
    files.saveFile(hiddenJsonFile, JsonDumpBytes)

    #Hidden has been removed notification
    notificationIcon = path.resources('resources/skins/default/media/common/vodyes.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender niet meer verborgen.', notificationIcon, 2500, False)
    return hiddenRemoved

def switch_to_page(hiddenMode='HiddenTelevision.js'):
    #Check kids hidden lock
    if kids.lock_check_hidden() == False:
        notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
        xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
        return False

    #Update hidden mode variable
    var.HiddenChannelMode = hiddenMode

    #Show hidden channel overlay
    if var.guiHidden == None:
        var.guiHidden = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiHidden.show()

def close_the_page():
    if var.guiHidden != None:
        #Refresh television channels on change
        if var.guiTelevision != None and var.HiddenChannelChanged == True:
            var.guiTelevision.refresh_programs(False)
            var.HiddenChannelChanged = False

        #Refresh radio channels on change
        if var.guiRadio != None and var.HiddenChannelChanged == True:
            var.guiRadio.load_channels(True)
            var.HiddenChannelChanged = False

        #Close the shown window
        var.guiHidden.close()
        var.guiHidden = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        func.updateLabelText(self, 3000, 'Verborgen Zenders')
        func.updateVisibility(self, 4001, False)

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
            hiddenRemoved = hidden_remove(listItemSelected, var.HiddenChannelMode)
            if hiddenRemoved == True:
                #Remove item from the list
                removeListItemId = clickedControl.getSelectedPosition()
                clickedControl.removeItem(removeListItemId)
                xbmc.sleep(100)
                clickedControl.selectItem(removeListItemId)
                xbmc.sleep(100)

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
        listContainer.reset()

        #Add items to sort list
        listContainerSort = []
        lihidden.list_load(listContainerSort, var.HiddenChannelMode)

        #Sort and add items to container
        listContainer.addItems(listContainerSort)

        #Update the status
        self.count_hidden_channels(True)

    #Update the status
    def count_hidden_channels(self, resetSelect=False):
        listContainer = self.getControl(1000)
        if var.HiddenChannelMode == 'HiddenTelevision.js':
            channelcount = len(var.HiddenTelevisionJson)
        else:
            channelcount = len(var.HiddenRadioJson)
        if channelcount > 0:
            func.updateLabelText(self, 3000, 'Verborgen Zenders (' + str(channelcount) + ')')
            func.updateLabelText(self, 3001, 'Huidige verborgen zenders, u kunt een zender weer laten verschijnen in de zenderlijst door er op te klikken.')
            if resetSelect == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 3000, 'Verborgen Zenders (0)')
            func.updateLabelText(self, 3001, 'Er zijn geen verborgen zenders, u kunt een zender verbergen in de zenderlijst.')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
