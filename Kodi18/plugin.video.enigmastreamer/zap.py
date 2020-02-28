from datetime import datetime, timedelta
from threading import Thread
import enigma
import func
import television
import var
import xbmc
import xbmcgui

def check_remote_number(_self, controlId, actionId, selectMode, clickOnSelection):
    var.ZapControlId = controlId
    if actionId == var.ACTION_SELECT_ITEM and var.thread_zap_wait_timer != None:
        var.ZapTimerForce = True
        return True
    elif actionId == var.REMOTE_0:
        set_remote_number(_self, '0', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_1:
        set_remote_number(_self, '1', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_2 or actionId == var.ACTION_JUMP_SMS2:
        set_remote_number(_self, '2', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_3 or actionId == var.ACTION_JUMP_SMS3:
        set_remote_number(_self, '3', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_4 or actionId == var.ACTION_JUMP_SMS4:
        set_remote_number(_self, '4', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_5 or actionId == var.ACTION_JUMP_SMS5:
        set_remote_number(_self, '5', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_6 or actionId == var.ACTION_JUMP_SMS6:
        set_remote_number(_self, '6', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_7 or actionId == var.ACTION_JUMP_SMS7:
        set_remote_number(_self, '7', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_8 or actionId == var.ACTION_JUMP_SMS8:
        set_remote_number(_self, '8', selectMode, clickOnSelection)
        return True
    elif actionId == var.REMOTE_9 or actionId == var.ACTION_JUMP_SMS9:
        set_remote_number(_self, '9', selectMode, clickOnSelection)
        return True
    return False

def set_remote_number(_self, ZapNumberPress, selectMode, clickOnSelection):
    var.ZapDelayDateTime = datetime.now()
    var.ZapNumber += str(ZapNumberPress)
    func.updateLabelText(_self, 7001, str(var.ZapNumber))
    _self.setProperty('ZapVisible', 'true')

    if var.thread_zap_wait_timer == None:
        var.thread_zap_wait_timer = Thread(target=thread_zap_wait_timer, args=(_self, selectMode, clickOnSelection))
        var.thread_zap_wait_timer.start()

def select_remote_number(_self, clickOnSelection):
    listcontainer = _self.getControl(var.ZapControlId)
    _self.setFocus(listcontainer)
    xbmc.sleep(200)
    itemnum = func.search_channelnumber_listcontainer(listcontainer, str(var.ZapNumber))
    if itemnum == None:
        notificationIcon = func.path_resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Channel ' + str(var.ZapNumber) + ' not found.', notificationIcon, 2500, False)
        return

    listcontainer.selectItem(itemnum)
    xbmc.sleep(200)
    if clickOnSelection:
        xbmc.executebuiltin('Action(Select)')

def zap_remote_number(_self):
    listcontainer = _self.getControl(var.ZapControlId)
    itemnum = func.search_channelnumber_listcontainer(listcontainer, str(var.ZapNumber))
    if itemnum == None:
        notificationIcon = func.path_resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Channel ' + str(var.ZapNumber) + ' not found.', notificationIcon, 2500, False)
        return

    listItemSelected = listcontainer.getListItem(itemnum)
    enigma.enigma_stream(listItemSelected)

def thread_zap_wait_timer(_self, selectMode, clickOnSelection):
    while var.thread_zap_wait_timer != None and var.addonmonitor.abortRequested() == False:
        xbmc.sleep(200)
        lastinteractseconds = int((datetime.now() - var.ZapDelayDateTime).total_seconds())
        if (var.ZapTimerForce or lastinteractseconds >= 3 or len(var.ZapNumber) == 4) and func.string_isnullorempty(var.ZapNumber) == False:
            #Handle remote action
            if selectMode: select_remote_number(_self, clickOnSelection)
            else: zap_remote_number(_self)

            #Reset remote variables
            var.ZapControlId = 0
            var.ZapNumber = ''
            var.ZapTimerForce = False
            var.thread_zap_wait_timer = None

            #Hide remote number popup
            _self.setProperty('ZapVisible', 'false')
            func.updateLabelText(_self, 7001, '')
