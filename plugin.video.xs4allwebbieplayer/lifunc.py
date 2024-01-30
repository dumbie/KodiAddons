import xbmc
import xbmcplugin
import func
import var

#Add item to container or directory
def auto_add_item(listItem, listContainer, dirUrl='', dirFolder=False):
    try:
        if listContainer == None:
            if func.string_isnullorempty(dirUrl) == False:
                dirUrl = var.LaunchUrl + '?' + dirUrl
            xbmcplugin.addDirectoryItem(listitem=listItem,handle=var.LaunchHandle,url=dirUrl,isFolder=dirFolder)
        else:
            if type(listContainer) == list:
                listContainer.append(listItem)
            else:
                listContainer.addItem(listItem)
        return True
    except:
        return False

#End adding items to directory
def auto_end_items():
    try:
        xbmcplugin.endOfDirectory(var.LaunchHandle)
        return True
    except:
        return False

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

#Search for SeriesId in list array
def search_seriesid_listarray(listArray, searchSeriesId):
    for Program in listArray:
        try:
            checkProgram1 = searchSeriesId.lower()
            checkProgram2 = Program.getProperty('SeriesId').lower()
            if checkProgram1 == checkProgram2:
                return Program
        except:
            continue
    return None

#Search for ChannelId in container
def search_channelid_listcontainer(listContainer, searchChannelId):
    listItemCount = listContainer.size()
    for itemNum in range(0, listItemCount):
        try:
            ChannelId = listContainer.getListItem(itemNum).getProperty('ChannelId')
            if ChannelId == searchChannelId:
                return itemNum
        except:
            continue
    return None

#Search for ChannelName in container
def search_channelname_listcontainer(listContainer, searchChannelName):
    listItemCount = listContainer.size()
    for itemNum in range(0, listItemCount):
        try:
            ChannelName = listContainer.getListItem(itemNum).getProperty('ChannelName')
            if ChannelName == searchChannelName:
                return itemNum
        except:
            continue
    return None

#Search for ChannelNumber in container
def search_channelnumber_listcontainer(listContainer, searchChannelNumber):
    listItemCount = listContainer.size()
    for itemNum in range(0, listItemCount):
        try:
            ChannelNumber = listContainer.getListItem(itemNum).getProperty('ChannelNumber')
            if ChannelNumber == searchChannelNumber:
                return itemNum
        except:
            continue
    return None

#Search for label in container
def search_label_listcontainer(listContainer, searchLabel):
    listItemCount = listContainer.size()
    for itemNum in range(0, listItemCount):
        try:
            listItem = listContainer.getListItem(itemNum)
            if str(listItem.getLabel()).startswith(searchLabel):
                return listItem
        except:
            continue
    return None

#Focus on channel in list
def focus_on_channelid_in_list(_self, controlId, defaultNum, forceFocus, channelId):
    listContainer = _self.getControl(controlId)
    if forceFocus:
        _self.setFocus(listContainer)
        xbmc.sleep(100)
    if func.string_isnullorempty(channelId) == False:
        itemNum = search_channelid_listcontainer(listContainer, channelId)
        if itemNum == None:
            listContainer.selectItem(defaultNum)
        else:
            listContainer.selectItem(itemNum)
    else:
        listContainer.selectItem(defaultNum)
    xbmc.sleep(100)
