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
        if var.HiddenTelevisionDataJson == [] and files.existFile('HiddenTelevision.js') == True:
            HiddenJsonString = files.openFile('HiddenTelevision.js')
            var.HiddenTelevisionDataJson = json.loads(HiddenJsonString)
    except:
        var.HiddenTelevisionDataJson = []

def hidden_radio_json_load():
    try:
        if var.HiddenRadioDataJson == [] and files.existFile('HiddenRadio.js') == True:
            HiddenJsonString = files.openFile('HiddenRadio.js')
            var.HiddenRadioDataJson = json.loads(HiddenJsonString)
    except:
        var.HiddenRadioDataJson = []

def hidden_check(ChannelId, hiddenJsonFile):
    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        hiddenTargetJson = var.HiddenTelevisionDataJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioDataJson
    return ChannelId in hiddenTargetJson

def hidden_add(listItem, hiddenJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        hiddenTargetJson = var.HiddenTelevisionDataJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioDataJson

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
        hiddenTargetJson = var.HiddenTelevisionDataJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        hiddenTargetJson = var.HiddenRadioDataJson

    HiddenRemoved = False
    for hidden in hiddenTargetJson:
        try:
            if hidden == ChannelId:
                hiddenTargetJson.remove(hidden)
                HiddenRemoved = True
                break
        except:
            continue

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(hiddenTargetJson).encode('ascii')
    files.saveFile(hiddenJsonFile, JsonDumpBytes)

    #Hidden has been removed notification
    notificationIcon = path.resources('resources/skins/default/media/common/vodyes.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender niet meer verborgen.', notificationIcon, 2500, False)
    return HiddenRemoved

def switch_to_page():
    #Check kids hidden lock
    if kids.lock_check_hidden() == False:
        notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
        xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
        return False

    if var.guiHidden == None:
        var.guiHidden = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiHidden.show()

def close_the_page():
    if var.guiHidden != None:
        #Refresh channels on change
        if var.guiTelevision != None and var.HiddenChannelChanged == True:
            var.guiTelevision.refresh_programs(False)
            var.HiddenChannelChanged = False

        #Close the shown window
        var.guiHidden.close()
        var.guiHidden = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        func.updateLabelText(self, 3000, 'Verborgen Zenders')
        func.updateVisibility(self, 4001, False)

        #Update the alarm panel height
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
            hiddenRemoved = hidden_remove(listItemSelected, 'HiddenTelevision.js')
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
        listcontainer = self.getControl(1000)
        listcontainer.reset()

        #Add items to sort list
        listcontainersort = []
        lihidden.list_load(listcontainersort, 'HiddenTelevision.js')

        #Sort and add items to container
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_hidden_channels(True)

    #Update the status
    def count_hidden_channels(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        channelcount = len(var.HiddenTelevisionDataJson)
        if channelcount > 0:
            func.updateLabelText(self, 3000, 'Verborgen Zenders (' + str(channelcount) + ')')
            func.updateLabelText(self, 3001, 'Huidige verborgen zenders, u kunt een zender weer laten verschijnen in de zenderlijst door er op te klikken.')
            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 3000, 'Verborgen Zenders (0)')
            func.updateLabelText(self, 3001, 'Er zijn geen verborgen zenders, u kunt een zender verbergen in de zenderlijst.')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
