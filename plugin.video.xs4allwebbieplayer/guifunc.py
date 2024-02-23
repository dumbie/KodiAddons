import xbmc

#Variables
InterfaceUpdateDelay = 50

#Control
def updateImage(_self, controlId, ImagePath):
    _self.getControl(controlId).setImage(ImagePath)

def updateVisibility(_self, controlId, visible):
    _self.getControl(controlId).setVisible(visible)

def updateLabelText(_self, controlId, string):
    _self.getControl(controlId).setLabel(string)

def updateTextBoxText(_self, controlId, string):
    _self.getControl(controlId).setText(string)

def updateProgressbarPercent(_self, controlId, percent):
    _self.getControl(controlId).setPercent(float(percent))

def controlFocus(_self, control):
    _self.setFocus(control)
    xbmc.sleep(InterfaceUpdateDelay)

#List container
def listSelectItem(listContainer, listItem):
    listContainer.selectItem(listItem)
    xbmc.sleep(InterfaceUpdateDelay)

def listAddItem(listContainer, listItem):
    listContainer.addItem(listItem)
    xbmc.sleep(InterfaceUpdateDelay)

def listRemoveItem(listContainer, listItem):
    listContainer.removeItem(listItem)
    xbmc.sleep(InterfaceUpdateDelay)

def listReset(listContainer):
    listContainer.reset()
    xbmc.sleep(InterfaceUpdateDelay)
