import var
import files
import hybrid
import os
import sys

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

#Check user folders
def check_user_folders():
    files.createDirectory(var.addonstorageuser)

#Get addon path
def path_addon(fileName):
    return os.path.join(var.addonpath, fileName)

#Generate addon url
def generate_addon_url(**kwargs):
    LaunchUrl = str(sys.argv[0])
    return LaunchUrl + "?" + hybrid.urlencode(kwargs)

#Check if string is empty
def string_isnullorempty(string):
    if string and string.strip():
        return False
    else:
        return True