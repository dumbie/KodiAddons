import json
import xbmcgui
import files
import path
import var

def hidden_television_json_load(forceLoad=False):
    try:
        if var.HiddenTelevisionJson == [] or forceLoad == True:
            if files.existFileUser('HiddenTelevision.js') == True:
                HiddenJsonString = files.openFileUser('HiddenTelevision.js')
                var.HiddenTelevisionJson = json.loads(HiddenJsonString)
    except:
        var.HiddenTelevisionJson = []

def hidden_radio_json_load(forceLoad=False):
    try:
        if var.HiddenRadioJson == [] or forceLoad == True: 
            if files.existFileUser('HiddenRadio.js') == True:
                HiddenJsonString = files.openFileUser('HiddenRadio.js')
                var.HiddenRadioJson = json.loads(HiddenJsonString)
    except:
        var.HiddenRadioJson = []

def hidden_target_variable(hiddenJsonFile):
    #Set Json target list variable
    if hiddenJsonFile == 'HiddenTelevision.js':
        return var.HiddenTelevisionJson
    elif hiddenJsonFile == 'HiddenRadio.js':
        return var.HiddenRadioJson

def hidden_check_channel(ChannelId, hiddenJsonFile):
    #Set Json target list variable
    hiddenTargetJson = hidden_target_variable(hiddenJsonFile)
    return ChannelId in hiddenTargetJson

def hidden_add_channel(listItem, hiddenJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    hiddenTargetJson = hidden_target_variable(hiddenJsonFile)

    #Append the new hidden to Json
    hiddenTargetJson.append(ChannelId)

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(hiddenTargetJson).encode('ascii')
    files.saveFileUser(hiddenJsonFile, JsonDumpBytes)

    #Hidden has been set notification
    notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender is verborgen.', notificationIcon, 2500, False)
    return True

def hidden_remove_channel(listItem, hiddenJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    hiddenTargetJson = hidden_target_variable(hiddenJsonFile)

    hiddenRemoved = False
    for hidden in hiddenTargetJson[:]:
        try:
            if hidden == ChannelId:
                hiddenTargetJson.remove(hidden)
                hiddenRemoved = True
        except:
            continue

    if hiddenRemoved == True:
        #Save the raw json data to storage
        JsonDumpBytes = json.dumps(hiddenTargetJson).encode('ascii')
        files.saveFileUser(hiddenJsonFile, JsonDumpBytes)

        #Hidden has been removed notification
        notificationIcon = path.resources('resources/skins/default/media/common/vodyes.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zender niet meer verborgen.', notificationIcon, 2500, False)
    return hiddenRemoved
