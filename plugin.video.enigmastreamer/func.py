import os
import var

#Update controls
def updateLabelText(_self, controlId, string):
    _self.getControl(controlId).setLabel(string)

#Check if string is empty
def string_isnullorempty(string):
    if string and string.strip():
        return False
    else:
        return True

#String decode
def string_decode(string):
    if string and string.strip():
        return False
    else:
        return True

#String remove after char
def string_remove_after_char(string, char, nth):
    return char.join(string.split(char)[:nth])

#Convert number to single string
def number_to_single_string(number):
    return str(int(number))

#Search for ChannelNumber in container
def search_channelnumber_listcontainer(listcontainer, searchChannelNumber):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        ChannelId = listcontainer.getListItem(itemNum).getProperty('ChannelNumber')
        if ChannelId == searchChannelNumber: return itemNum
    return None

#Get add-on resource path
def path_resources(iconName):
    return os.path.join(var.addonpath, iconName)
