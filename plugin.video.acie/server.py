import os
import var
import getpass
import xbmc
import xbmcgui

def install_server():
    try:
        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Installing docker", var.addonicon, 2500, False)

        #Manually: Add-ons > Install from repository > LibreELEC Add-ons > Services > Docker > Install
        #service.system.docker

        #Linux install docker
        aceCommand = ""
        runResult = os.system(aceCommand)

        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Installing ace stream server", var.addonicon, 2500, False)

        #Linux RPI ARM ace stream server
        aceCommand = "docker pull futebas/acestream-engine-arm:3.2.7.6"
        runResult = os.system(aceCommand)

        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Installed ace stream server, reboot device", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed installing ace stream server", var.addonicon, 2500, False)

def run_server():
    try:
        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Running ace stream server", var.addonicon, 2500, False)

        #Get username
        userName = getpass.getuser()

        #Fix check if already running
        #Fix check operating system

        #Android
        #Fix find way to avoid error message
        aceCommand = 'StartAndroidActivity("","org.acestream.action.start_content","","")'
        runResult = xbmc.executebuiltin(aceCommand)

        #Windows
        aceCommand = "start C:\\Users\\" + userName + "\\AppData\\Roaming\\ACEStream\\engine\\ace_engine.exe"
        runResult = os.system(aceCommand)

        #Linux RPI ARM docker
        aceCommand = "docker run --tty --privileged --detach --publish 6878:6878 futebas/acestream-engine-arm:3.2.7.6"
        runResult = os.system(aceCommand)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed running ace stream server", var.addonicon, 2500, False)