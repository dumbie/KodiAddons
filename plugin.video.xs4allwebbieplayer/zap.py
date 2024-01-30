from datetime import datetime, timedelta
import xbmc
import func
import lifunc
import streamplay
import var

def check_remote_number(_self, controlId, actionId, selectMode, clickOnSelection):
    var.ZapControlId = controlId
    if actionId == var.ACTION_SELECT_ITEM and var.thread_zap_wait_timer.Running():
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
    listContainer = _self.getControl(var.ZapControlId)
    listItemCount = listContainer.size()
    for itemNum in range(0, listItemCount):
        try:
            channelNameProp = listContainer.getListItem(itemNum).getProperty('ChannelName')
            channelNumberProp = listContainer.getListItem(itemNum).getProperty('ChannelNumber')
            if channelNumberProp.startswith(var.ZapNumberString):
                channelNumberCut = channelNumberProp.replace(var.ZapNumberString, '', 1)
                var.ZapHintString += func.get_provider_color_string() + var.ZapNumberString + '[/COLOR][COLOR gray]' + channelNumberCut + '[/COLOR] ' + channelNameProp + ' '
        except:
            continue

    #Check if channel is found
    if func.string_isnullorempty(var.ZapHintString):
        var.ZapHintString = 'Zender ' + func.get_provider_color_string() + var.ZapNumberString + '[/COLOR] niet gevonden.'
        var.ZapNumberString = ''

    #Start zap wait thread
    var.thread_zap_wait_timer.Start(thread_zap_wait_timer, (_self, selectMode, clickOnSelection))

def select_remote_number(_self, clickOnSelection):
    listContainer = _self.getControl(var.ZapControlId)
    itemNum = lifunc.search_channelnumber_listcontainer(listContainer, var.ZapNumberString)
    if itemNum == None:
        return

    _self.setFocus(listContainer)
    xbmc.sleep(100)
    listContainer.selectItem(itemNum)
    xbmc.sleep(100)
    if clickOnSelection:
        xbmc.executebuiltin('Action(Select)')

def zap_remote_number(_self):
    listContainer = _self.getControl(var.ZapControlId)
    itemnum = lifunc.search_channelnumber_listcontainer(listContainer, var.ZapNumberString)
    if itemnum == None:
        return

    listItemSelected = listContainer.getListItem(itemnum)
    streamplay.play_tv(listItemSelected, False, True)

def thread_zap_wait_timer(_self, selectMode, clickOnSelection):
    while var.thread_zap_wait_timer.Allowed():
        xbmc.sleep(100)
        interactSecond = 3
        lastInteractSeconds = int((datetime.now() - var.ZapDelayDateTime).total_seconds())
        if var.ZapTimerForce or lastInteractSeconds >= interactSecond or len(var.ZapNumberString) == 4:
            #Handle remote action
            if selectMode:
                select_remote_number(_self, clickOnSelection)
            else:
                zap_remote_number(_self)

            #Hide remote number popup
            _self.setProperty('ZapVisible', 'false')
            func.updateLabelText(_self, 7001, '')

            #Reset remote variables
            var.ZapControlId = 0
            var.ZapNumberString = ''
            var.ZapHintString = ''
            var.ZapTimerForce = False
            var.thread_zap_wait_timer.Stop()
        else:
            #Countdown string
            zapCountInt = interactSecond - lastInteractSeconds
            zapCountString = '[COLOR gray]' + str(zapCountInt) + '[/COLOR]'

            #Show remote number popup
            func.updateLabelText(_self, 7001, zapCountString)
            func.updateLabelText(_self, 7002, var.ZapHintString)
            _self.setProperty('ZapVisible', 'true')
