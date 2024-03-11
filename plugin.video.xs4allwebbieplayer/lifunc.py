import xbmcplugin
import xbmcgui
import func
import guifunc
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

#Search for property in listcontainer index
def search_listcontainer_property_listindex(listContainer, searchProperty, searchValue):
    try:
        listItemCount = listContainer.size()
        for itemNum in range(0, listItemCount):
            try:
                listItem = listContainer.getListItem(itemNum)
                if str(listItem.getProperty(searchProperty)) == searchValue:
                    return itemNum
            except:
                continue
        return None
    except:
        return None

#Search for property in listcontainer listitem
def search_listcontainer_property_listitem(listContainer, searchProperty, searchValue):
    try:
        listItemCount = listContainer.size()
        for itemNum in range(0, listItemCount):
            try:
                listItem = listContainer.getListItem(itemNum)
                if str(listItem.getProperty(searchProperty)) == searchValue:
                    return listItem
            except:
                continue
        return None
    except:
        return None

#Search for label in listcontainer listitem
def search_listcontainer_label_listitem(listContainer, searchLabel):
    try:
        listItemCount = listContainer.size()
        for itemNum in range(0, listItemCount):
            try:
                listItem = listContainer.getListItem(itemNum)
                if str(listItem.getLabel()).startswith(searchLabel):
                    return listItem
            except:
                continue
        return None
    except:
        return None

#Focus on value in listcontainer
def focus_listcontainer_value(_self, controlId, defaultIndex, forceFocus, searchProperty, searchValue):
    try:
        #Check if listcontainer has items
        listContainer = _self.getControl(controlId)
        listItemCount = listContainer.size()
        if listItemCount > 0:
            #Focus on listcontainer
            if forceFocus:
                guifunc.controlFocus(_self, listContainer)

            #Select listitem
            if func.string_isnullorempty(searchValue) == False:
                listIndex = search_listcontainer_property_listindex(listContainer, searchProperty, searchValue)
                if listIndex == None:
                    guifunc.listSelectIndex(listContainer, defaultIndex)
                else:
                    guifunc.listSelectIndex(listContainer, listIndex)
            else:
                guifunc.listSelectIndex(listContainer, defaultIndex)
    except:
        pass
