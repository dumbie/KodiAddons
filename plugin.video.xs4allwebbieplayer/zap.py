from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import func
import path
import stream
import var

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
    var.ZapNumberString += ZapNumberPress
    var.ZapHintString = ''

    #Set channel string
    listcontainer = _self.getControl(var.ZapControlId)
    listitemcount = listcontainer.size()
    for itemNum in range(0, listitemcount):
        try:
            channelNameProp = listcontainer.getListItem(itemNum).getProperty('ChannelName')
            channelNumberProp = listcontainer.getListItem(itemNum).getProperty('ChannelNumber')
            if channelNumberProp.startswith(var.ZapNumberString):
                var.ZapHintString += func.get_provider_color_string() + channelNumberProp + '[/COLOR] [COLOR white]' + channelNameProp + '[/COLOR] '
        except:
            continue

    #Check if channel is found
    if func.string_isnullorempty(var.ZapHintString):
        var.ZapHintString = 'Zender ' + var.ZapNumberString + ' niet gevonden.'
        var.ZapTimerForce = True

    #Start zap wait thread
    if var.thread_zap_wait_timer == None:
        var.thread_zap_wait_timer = Thread(target=thread_zap_wait_timer, args=(_self, selectMode, clickOnSelection))
        var.thread_zap_wait_timer.start()

def select_remote_number(_self, clickOnSelection):
    listcontainer = _self.getControl(var.ZapControlId)
    itemnum = func.search_channelnumber_listcontainer(listcontainer, var.ZapNumberString)
    if itemnum == None:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zender ' + var.ZapNumberString + ' niet gevonden.', notificationIcon, 2500, False)
        return

    _self.setFocus(listcontainer)
    xbmc.sleep(100)
    listcontainer.selectItem(itemnum)
    xbmc.sleep(100)
    if clickOnSelection:
        xbmc.executebuiltin('Action(Select)')

def zap_remote_number(_self):
    listcontainer = _self.getControl(var.ZapControlId)
    itemnum = func.search_channelnumber_listcontainer(listcontainer, var.ZapNumberString)
    if itemnum == None:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zender ' + var.ZapNumberString + ' niet gevonden.', notificationIcon, 2500, False)
        return

    listItemSelected = listcontainer.getListItem(itemnum)
    stream.switch_channel_tv_listitem(listItemSelected, False, True)

def thread_zap_wait_timer(_self, selectMode, clickOnSelection):
    while var.thread_zap_wait_timer != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
        xbmc.sleep(100)
        interactSecond = 3
        lastInteractSeconds = int((datetime.now() - var.ZapDelayDateTime).total_seconds())
        if (var.ZapTimerForce or lastInteractSeconds >= interactSecond or len(var.ZapNumberString) == 4) and func.string_isnullorempty(var.ZapNumberString) == False:
            #Handle remote action
            if selectMode:
                select_remote_number(_self, clickOnSelection)
            else:
                zap_remote_number(_self)

            #Reset remote variables
            var.ZapControlId = 0
            var.ZapNumberString = ''
            var.ZapTimerForce = False
            var.thread_zap_wait_timer = None

            #Hide remote number popup
            _self.setProperty('ZapVisible', 'false')
            func.updateLabelText(_self, 7001, '')
        else:
            #Countdown string
            ZapCountInt = interactSecond - lastInteractSeconds
            ZapCountDownString = '[COLOR gray]' + str(ZapCountInt) + '[/COLOR] '

            #Show remote number popup
            func.updateLabelText(_self, 7001, ZapCountDownString + var.ZapHintString)
            _self.setProperty('ZapVisible', 'true')
