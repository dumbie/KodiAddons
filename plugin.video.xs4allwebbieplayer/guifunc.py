import xbmc

#Variables
InterfaceUpdateDelay = 50

#Control
def updateImage(_self, controlId, ImagePath):
    try:
        _self.getControl(controlId).setImage(ImagePath)
        return True
    except:
        return False

def updateVisibility(_self, controlId, visible):
    try:
        _self.getControl(controlId).setVisible(visible)
        return True
    except:
        return False

def updateLabelText(_self, controlId, string):
    try:
        _self.getControl(controlId).setLabel(string)
        return True
    except:
        return False

def updateTextBoxText(_self, controlId, string):
    try:
        _self.getControl(controlId).setText(string)
        return True
    except:
        return False

def updateProgressbarPercent(_self, controlId, percent):
    try:
        _self.getControl(controlId).setPercent(float(percent))
        return True
    except:
        return False

def controlFocus(_self, control):
    try:
        _self.setFocus(control)
        xbmc.sleep(InterfaceUpdateDelay)
        return True
    except:
        return False

#List container
def listSelectIndex(listContainer, listIndex):
    try:
        listContainer.selectItem(listIndex)
        xbmc.sleep(InterfaceUpdateDelay)
        return True
    except:
        return False

def listAddItem(listContainer, listItem):
    try:
        listContainer.addItem(listItem)
        xbmc.sleep(InterfaceUpdateDelay)
        return True
    except:
        return False

def listRemoveItem(listContainer, listItem):
    try:
        listContainer.removeItem(listItem)
        xbmc.sleep(InterfaceUpdateDelay)
        return True
    except:
        return False

def listReset(listContainer):
    try:
        listContainer.reset()
        xbmc.sleep(InterfaceUpdateDelay)
        return True
    except:
        return False
