import subprocess
import func
import var
import xbmcgui
import time
import console

#Moonlight list
def moonlight_list():
    #Check the current settings
    set_host = var.addon.getSetting('host')
    if set_host.endswith('.') or set_host.endswith('0') or not set_host[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    #List moonlight apps
    scriptRun = ['bash']
    scriptFile = [var.addonpath + '/scripts/moonlight-list.sh']
    scriptVars = [set_host]
    process = subprocess.Popen(scriptRun + scriptFile + scriptVars, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #Show and update console
    pollString = console.console_process_poll(process, 'Moonlight list')

    #Wait for completion
    process.wait()

    #Close console
    console.console_close()

    #Return app list
    return pollString

#Moonlight pair
def moonlight_pair():
    #Check the current settings
    set_host = var.addon.getSetting('host')
    if set_host.endswith('.') or set_host.endswith('0') or not set_host[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    #Pair with moonlight
    scriptRun = ['bash']
    scriptFile = [var.addonpath + '/scripts/moonlight-pair.sh']
    scriptVars = [set_host]
    process = subprocess.Popen(scriptRun + scriptFile + scriptVars, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #Show and update console
    console.console_process_poll(process, 'Moonlight pairing')

    #Wait for completion
    process.wait()

    #Close console
    time.sleep(3)
    console.console_close()

    #Fix refresh apps after pairing

#Moonlight install
def moonlight_install():
    #Install moonlight client
    scriptRun = ['bash']
    scriptFile = [var.addonpath + '/scripts/moonlight-install.sh']
    process = subprocess.Popen(scriptRun + scriptFile, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #Show and update console
    console.console_process_poll(process, 'Moonlight installation')

    #Wait for completion
    process.wait()

    #Close console
    time.sleep(3)
    console.console_close()

#Moonlight stream
def moonlight_stream(appName=''):
    #Check the current settings
    set_host = var.addon.getSetting('host')
    if set_host.endswith('.') or set_host.endswith('0') or not set_host[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return
    
    #Check the application name
    if func.string_isnullorempty(appName) == True:
        notificationIcon = func.path_resources('resources/skins/default/media/common/close.png')
        xbmcgui.Dialog().notification(var.addonname, 'Invalid launch application.', notificationIcon, 2500, False)
        return

    #Load the stream settings
    setwidth = var.addon.getSetting('width')
    setheight = var.addon.getSetting('height')
    setbitrate = var.addon.getSetting('bitrate')
    setfps = var.addon.getSetting('fps')
    if var.addon.getSetting('localaudio') == 'true':
        setlocalaudio = '-localaudio'
    else:
        setlocalaudio = '-unsupported'
    if var.addon.getSetting('surroundsound') == 'true':
        setsurroundsound = '-surround'
    else:
        setsurroundsound = '-unsupported'

    #Launch moonlight stream
    scriptRun = ['systemd-run', 'bash']
    scriptFile = [var.addonpath + '/scripts/moonlight-stream.sh']
    scriptVars = [set_host, appName, setwidth, setheight, setbitrate, setfps, setlocalaudio, setsurroundsound]
    process = subprocess.Popen(scriptRun + scriptFile + scriptVars, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #Wait for completion
    process.wait()
