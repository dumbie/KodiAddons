import func
import var
import xbmc
import xbmcgui

def show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, selectIndex=0):
    if var.guiDialog == None:
        var.guiDialog = Gui('dialog.xml', var.addonpath, 'default', '720p')
        var.guiDialog.show()

        var.guiDialog.update_dialogSize(dialogFooter, dialogAnswers)
        var.guiDialog.update_dialogHeader(dialogHeader)
        var.guiDialog.update_dialogSummary(dialogSummary)
        var.guiDialog.update_dialogFooter(dialogFooter)
        var.guiDialog.update_dialogAnswers(dialogAnswers, selectIndex)

        var.DialogResult = None
        while var.DialogResult == None:
            xbmc.sleep(100)

        return var.DialogResult

def close_dialog(setDialogResult):
    if var.guiDialog != None:
        #Set the dialog chosen result
        var.DialogResult = setDialogResult

        #Close the shown window
        var.guiDialog.close()
        var.guiDialog = None

class Gui(xbmcgui.WindowXMLDialog):
    def update_dialogSize(self, dialogFooter, dialogAnswers):
        #Check if maximum answers reached
        dialogAnswerCount = len(dialogAnswers)
        if dialogAnswerCount > 8:
            dialogAnswerCount = 8

        #Calculate the dialog height
        dialogHeight = 130
        dialogHeight += (dialogAnswerCount * 45) + 5

        #Check if maximum height reached
        if dialogHeight > 600:
            dialogHeight = 600

        #Update the dialog panel height
        dialogControl = self.getControl(4000)
        dialogControl.setHeight(dialogHeight)
        dialogControl = self.getControl(1000)
        dialogControl.setHeight(dialogHeight - 130)

        #Set the footer text position
        if func.string_isnullorempty(dialogFooter) == False:
            dialogControl = self.getControl(3002)
            dialogControl.setPosition(10, dialogHeight)
            dialogHeight += 40

        #Update the dialog background height
        dialogControl = self.getControl(5000)
        dialogControl.setHeight(dialogHeight)

        #Update the dialog border height
        dialogControl = self.getControl(5001)
        dialogControl.setHeight(dialogHeight + 3)

    def update_dialogHeader(self, dialogHeader):
        func.updateLabelText(self, 3000, dialogHeader)

    def update_dialogSummary(self, dialogSummary):
        func.updateTextBoxText(self, 3001, dialogSummary)

    def update_dialogFooter(self, dialogFooter):
        func.updateLabelText(self, 3002, dialogFooter)

    def update_dialogAnswers(self, dialogAnswers, selectIndex=0):
        #Get and check the button list container
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return True

        for string in dialogAnswers:
            listitem = xbmcgui.ListItem(string)
            listcontainer.addItem(listitem)

        #Focus on the list
        self.setFocus(listcontainer)
        xbmc.sleep(100)
        listcontainer.selectItem(selectIndex)
        xbmc.sleep(100)

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_dialog('DialogCancel')

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            close_dialog(listItemSelected.getLabel())
        elif clickId == 4001:
            close_dialog('DialogCancel')
