import subprocess
import func
import var
import xbmcgui

#Parsec connect
def parsec_connect():
    #Check the current settings
    set_server_id = var.addon.getSetting('server_id')
    if len(set_server_id) < 10:
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the host peer id.', notificationIcon, 2500, False)
        return

    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/parsec-connect.sh']

    #Get Parsec connection arguments
    set_client_audio_buffer = var.addon.getSetting('client_audio_buffer')
    connectArguments = 'peer_id=' + set_server_id + ':client_audio_max_buffer_ms=' + set_client_audio_buffer + ':client_overlay=0:client_immersive=1'
    scriptVars = [connectArguments]

    process = subprocess.Popen(scriptRun + scriptCode + scriptVars)
    process.wait()

#Parsec login
def parsec_login():
    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/parsec-login.sh']

    process = subprocess.Popen(scriptRun + scriptCode)
    process.wait()

#Parsec install
def parsec_install():
    scriptRun = [var.addonpath + '/scripts/script-run.sh']
    scriptCode = [var.addonpath + '/scripts/parsec-install.sh']

    process = subprocess.Popen(scriptRun + scriptCode)
    process.wait()
