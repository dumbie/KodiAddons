import xbmc
import func

#Search for ProgramName in list array
def search_programname_listarray(listArray, searchProgramName):
    for Program in listArray:
        try:
            checkProgram1 = searchProgramName.lower()
            checkProgram2 = Program.getProperty('ProgramName').lower()
            if checkProgram1 == checkProgram2:
                return Program
        except:
            continue
    return None

#Search for ChannelId in container
def search_channelid_listcontainer(listcontainer, searchChannelId):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            ChannelId = listcontainer.getListItem(itemNum).getProperty('ChannelId')
            if ChannelId == searchChannelId:
                return itemNum
        except:
            continue
    return None

#Search for ChannelName in container
def search_channelname_listcontainer(listcontainer, searchChannelName):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            ChannelName = listcontainer.getListItem(itemNum).getProperty('ChannelName')
            if ChannelName == searchChannelName:
                return itemNum
        except:
            continue
    return None

#Search for ChannelNumber in container
def search_channelnumber_listcontainer(listcontainer, searchChannelNumber):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            ChannelNumber = listcontainer.getListItem(itemNum).getProperty('ChannelNumber')
            if ChannelNumber == searchChannelNumber:
                return itemNum
        except:
            continue
    return None

#Search for label in container
def search_label_listcontainer(listcontainer, searchLabel):
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            listItem = listcontainer.getListItem(itemNum)
            if str(listItem.getLabel()).startswith(searchLabel):
                return listItem
        except:
            continue
    return None

#Focus on channel in list
def focus_on_channelid_in_list(_self, controlId, defaultNum, forceFocus, channelId):
    listcontainer = _self.getControl(controlId)
    if forceFocus:
        _self.setFocus(listcontainer)
        xbmc.sleep(100)
    if func.string_isnullorempty(channelId) == False:
        itemNum = search_channelid_listcontainer(listcontainer, channelId)
        if itemNum == None:
            listcontainer.selectItem(defaultNum)
        else:
            listcontainer.selectItem(itemNum)
    else:
        listcontainer.selectItem(defaultNum)
    xbmc.sleep(100)
