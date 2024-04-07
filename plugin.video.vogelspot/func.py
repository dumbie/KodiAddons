#Update controls
def updateLabelText(_self, controlId, string):
    _self.getControl(controlId).setLabel(string)

#Check if string is empty
def string_isnullorempty(string):
    if string and string.strip():
        return False
    else:
        return True
