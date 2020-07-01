import subprocess
import func
import var
import xbmcgui

#Moonlight list
def moonlight_list():
    #Check the current settings
    set_host = var.addon.getSetting('host')
    if set_host.endswith('.') or set_host.endswith('0') or not set_host[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/moonlight-list.sh']
    scriptVars = [set_host]

    process = subprocess.Popen(scriptRun + scriptCode + scriptVars, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    processOutput = process.communicate()
    process.wait()

    return processOutput[0] + processOutput[1]

#Moonlight pair
def moonlight_pair():
    #Check the current settings
    set_host = var.addon.getSetting('host')
    if set_host.endswith('.') or set_host.endswith('0') or not set_host[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/moonlight-pair.sh']
    scriptVars = [set_host]

    process = subprocess.Popen(scriptRun + scriptCode + scriptVars)
    process.wait()

#Moonlight install
def moonlight_install():
    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/moonlight-install.sh']

    process = subprocess.Popen(scriptRun + scriptCode)
    process.wait()

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

    #Launch the moonlight stream
    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/moonlight-stream.sh']
    scriptVars = [set_host, appName, setwidth, setheight, setbitrate, setfps, setlocalaudio, setsurroundsound]

    process = subprocess.Popen(scriptRun + scriptCode + scriptVars)
    process.wait()
