import func
import var
import xbmcgui
import time
import hybrid

def console_show(header, string, stringAdd=False):
    if var.guiConsole == None:
        var.guiConsole = Gui('console.xml', var.addonpath, 'default', '720p')
        var.guiConsole.show()
    var.guiConsole.console_update(header, string, stringAdd)

def console_close():
    if var.guiConsole != None:
        var.guiConsole.close()
        var.guiConsole = None

def console_process_poll(process, head_string):
    poll_string = ''
    console_show(head_string, poll_string)
    while process.poll() == None:
        poll_string += hybrid.string_decode_utf8(process.stdout.readline())
        console_show(head_string, poll_string)
    return poll_string

class Gui(xbmcgui.WindowXMLDialog):
    def console_update(self, header, string, stringAdd=False):
        func.setLabelText(self, 3000, header)
        if stringAdd:
            stringNew = func.getTextBoxText(self, 3001) + "[CR]" + string
            func.setTextBoxText(self, 3001, stringNew)
        else:
            func.setTextBoxText(self, 3001, string)
        time.sleep(0.100)
        func.setTextBoxScroll(self, 3001, -1)
