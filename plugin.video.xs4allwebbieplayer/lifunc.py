import xbmc
import xbmcplugin
import func
import var

#Add item to container or directory
def auto_add_item(listItem, listContainer, dirUrl='', dirFolder=False):
    try:
        if listContainer == None:
            if type(listItem) == tuple:
                xbmcplugin.addDirectoryItem(handle=var.LaunchHandle,listitem=listItem[1],url=listItem[0],isFolder=listItem[2])
            else:
                xbmcplugin.addDirectoryItem(handle=var.LaunchHandle,listitem=listItem,url=dirUrl,isFolder=dirFolder)
        else:
            if type(listContainer) == list:
                listContainer.append(listItem)
            else:
                if type(listItem) == tuple:
                    listContainer.addItem(listItem[1])
                else:
                    listContainer.addItem(listItem)
        return True
    except:
        return False

#Add items to container or directory
def auto_add_items(listItems, listContainer):
    try:
        if listContainer == None:
            xbmcplugin.addDirectoryItems(handle=var.LaunchHandle,items=listItems)
        else:
            if type(listContainer) == list:
                listContainer.append(listItems)
            else:
                if type(listItems[0]) == tuple:
                    listItemsTuple = [x[1] for x in listItems]
                    listContainer.addItems(listItemsTuple)
                else:
                    listContainer.addItems(listItems)
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

#Search for Program by Episode and Season in list array
def search_program_episodeseason_listarray(listArray, searchProgramEpisode, searchProgramSeason):
    for Program in listArray:
        try:
            checkProgramSeason = Program.getProperty('ProgramSeasonInt')
            checkProgramEpisode = Program.getProperty('ProgramEpisodeInt')
            if searchProgramEpisode == checkProgramSeason and searchProgramSeason == checkProgramEpisode:
                return Program
        except:
            continue
    return None

#Search for Program by Name and Details in list array
def search_program_namedetails_listarray(listArray, searchProgramName, searchProgramDetails):
    for Program in listArray:
        try:
            checkProgramName = Program.getProperty('ProgramName')
            checkProgramDetails = Program.getProperty('ProgramDetails')
            if searchProgramName == checkProgramName and searchProgramDetails == checkProgramDetails:
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

#Focus on channel in list container
def focus_on_channelid_in_list(_self, controlId, defaultNum, forceFocus, channelId):
    #Check if list container has items
    listContainer = _self.getControl(controlId)
    listItemCount = listContainer.size()
    if listItemCount > 0:
        #Focus on list container 
        if forceFocus:
            _self.setFocus(listContainer)
            xbmc.sleep(100)

        #Select list item
        if func.string_isnullorempty(channelId) == False:
            itemNum = search_channelid_listcontainer(listContainer, channelId)
            if itemNum == None:
                listContainer.selectItem(defaultNum)
            else:
                listContainer.selectItem(itemNum)
        else:
            listContainer.selectItem(defaultNum)
        xbmc.sleep(100)
