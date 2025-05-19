import os
import var

#Update controls
def setLabelText(_self, controlId, string):
    _self.getControl(controlId).setLabel(string)

def getLabelText(_self, controlId):
    return _self.getControl(controlId).getLabel()

def setTextBoxText(_self, controlId, string):
    _self.getControl(controlId).setText(string)

def getTextBoxText(_self, controlId):
    return _self.getControl(controlId).getText()

def setTextBoxScroll(_self, controlId, position):
    _self.getControl(controlId).scroll(position)

def setVisible(_self, controlId, value):
    _self.getControl(controlId).setVisible(value)

#Check if string is empty
def string_isnullorempty(string):
    if string and string.strip():
        return False
    else:
        return True

#Get add-on resource path
def path_resources(iconName):
    return os.path.join(var.addonpath, iconName)
