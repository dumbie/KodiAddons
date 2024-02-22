import sys
import xbmc
import func
import playerclass
import playergui
import var

#Custom player variables
PlayerCustom = playerclass.Class_PlayerCustom()

def PlayerWindowed(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return func.globalvar_get(varName, False)
    else:
         return func.globalvar_set(varName, setObject)

def PlayerOpenOverlay(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return func.globalvar_get(varName, False)
    else:
         return func.globalvar_set(varName, setObject)

def PlayerShowInformation(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return func.globalvar_get(varName, False)
    else:
         return func.globalvar_set(varName, setObject)

def PlayerSeekOffsetSecEnd(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return func.globalvar_get(varName, 0)
    else:
         return func.globalvar_set(varName, setObject)

def ResetVariables():
    PlayerWindowed(False)
    PlayerOpenOverlay(False)
    PlayerShowInformation(False)
    PlayerSeekOffsetSecEnd(0)

#Custom player functions
def PlayCustom(streamUrl, listItem, Windowed=False, OpenOverlay=False, ShowInformation=False, SeekOffsetSecEnd=0):
    #Update custom player variables
    PlayerWindowed(Windowed)
    PlayerOpenOverlay(OpenOverlay)
    PlayerShowInformation(ShowInformation)
    PlayerSeekOffsetSecEnd(SeekOffsetSecEnd)

    #Start playing list item media
    xbmc.Player().play(streamUrl, listItem, Windowed)

def Fullscreen(forceFullscreen=False, forceOpenOverlay=False, forceShowInformation=False):
    #Check if player is playing
    if xbmc.Player().isPlayingVideo() == True:
        #Open fullscreen player interface
        if forceFullscreen == True or PlayerWindowed() == False:
            func.open_window_id(var.WINDOW_FULLSCREEN_VIDEO)
            xbmc.sleep(100)

        #Open or close custom player overlay
        if forceOpenOverlay == True or PlayerOpenOverlay() == True:
            playergui.switch_to_page()
            xbmc.sleep(100)
        else:
            playergui.close_the_page(False)
            xbmc.sleep(100)

        #Show custom player information
        if forceShowInformation == True or PlayerShowInformation() == True:
            if var.guiPlayer != None:
                var.guiPlayer.show_epg(True, False, True, True)
    elif xbmc.Player().isPlayingAudio() == True:
        #Close custom player overlay
        playergui.close_the_page()
        xbmc.sleep(100)

        #Open fullscreen player interface
        if forceFullscreen == True or PlayerWindowed() == False:
            func.open_window_id(var.WINDOW_VISUALISATION)
            xbmc.sleep(100)
