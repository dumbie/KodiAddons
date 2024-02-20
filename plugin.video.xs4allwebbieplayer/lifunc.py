import xbmc
import xbmcplugin
import xbmcgui
import func
import var

#Convert JsonItem to ListItem
def jsonitem_to_listitem(jsonItem):
    try:
        listItem = xbmcgui.ListItem()
        for name, value in jsonItem.items():
            if name == 'ItemLabel':
                listItem.setLabel(value)
            elif name == 'ItemInfoVideo':
                listItem.setInfo('video', value)
            elif name == 'ItemInfoMusic':
                listItem.setInfo('music', value)
            elif name == 'ItemArt':
                listItem.setArt(value)
            else:
                listItem.setProperty(name, value)
        return listItem
    except:
        return None

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
                    tupleContainer = [x[1] for x in listItems]
                    listContainer.addItems(tupleContainer)
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
