import var
import xbmcgui
import xbmcaddon
import widevine
import default
import func
import var
import limain
import lichannelradio
import lichanneltelevision
import download
import switch
import apilogin
import sys

def set_launch_argument_source():
    try:
        var.LaunchUrl = str(sys.argv[0])
        var.LaunchHandle = int(sys.argv[1])
        var.LaunchArgument = str(sys.argv[2])
        xbmcgui.Dialog().notification(var.addonname, "Launch argument source: " + var.LaunchArgument, var.addonicon, 2500, False)
        return True
    except:
        return False

def set_launch_argument_script():
    try:
        var.LaunchArgument = str(sys.argv[1])
        xbmcgui.Dialog().notification(var.addonname, "Launch argument script: " + var.LaunchArgument, var.addonicon, 2500, False)
        return True
    except:
        return False

def handle_launch_argument_script():
    try:
        if var.LaunchArgument == "InputAdaptiveSettings":
            xbmcaddon.Addon('inputstream.adaptive').openSettings()
            return False
        elif var.LaunchArgument == "UpdateWidevineFiles":
            widevine.enable_widevine_support(True)
            return False
        elif var.LaunchArgument == "ResetUserdata":
            default.reset_userdata()
            return False
        elif var.LaunchArgument == "ResetThumbnails":
            default.reset_thumbnails()
            return False
        return True
    except:
        return True

def handle_launch_argument_source():
    try:
        #Fix share variables every source request
        #Fix add listitem to dirurl string conversion
        if func.string_isnullorempty(var.LaunchArgument):
            apilogin.ApiLogin(True)
            limain.list_load(None)
        elif var.LaunchArgument == "?page_television":
            download.download_channels_tv(False)
            lichanneltelevision.list_load(None)
        elif var.LaunchArgument == "?page_radio":
            download.download_channels_radio(False)
            lichannelradio.list_load(None)
        elif var.LaunchArgument.startswith("?play_stream_tv="):
            channelId = var.LaunchArgument.replace('?play_stream_tv=', '')
            download.download_channels_tv(False)
            switch.channel_tv_channelid(channelId, ShowInformation=True)
        elif var.LaunchArgument.startswith("?play_stream_radio="):
            channelId = var.LaunchArgument.replace('?play_stream_radio=', '')
            download.download_channels_radio(False)
            switch.channel_radio_channelid(channelId)
        return True
    except:
        return True
