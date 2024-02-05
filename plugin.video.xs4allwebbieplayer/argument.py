import var
import xbmcaddon
import widevine
import default
import func
import hybrid
import var
import limain
import lichannelradio
import lichanneltelevision
import limovies
import liseriesprogram
import liseriesepisode
import likidsprogram
import likidsepisode
import lisport
import livod
import lirecorded
import streamswitch
import sys

def set_launch_argument_source():
    try:
        var.LaunchUrl = str(sys.argv[0])
        var.LaunchHandle = int(sys.argv[1])
        var.LaunchArgument = hybrid.urllib_unquote(str(sys.argv[2]))
        return True
    except:
        return False

def handle_launch_argument_source():
    try:
        #Handle settings
        if var.LaunchArgument == "?InputAdaptiveSettings":
            xbmcaddon.Addon('inputstream.adaptive').openSettings()
        elif var.LaunchArgument == "?UpdateWidevineFiles":
            widevine.enable_widevine_support(True)
        elif var.LaunchArgument == "?ResetUserdata":
            default.reset_userdata()
        elif var.LaunchArgument == "?ResetThumbnails":
            default.reset_thumbnails()

        #List items
        elif func.string_isnullorempty(var.LaunchArgument):
            limain.list_load_combined()
        elif var.LaunchArgument == "?page_television":
            lichanneltelevision.list_load_combined()
        elif var.LaunchArgument == "?page_radio":
            lichannelradio.list_load_combined()
        elif var.LaunchArgument == "?page_movies":
            limovies.list_load_combined()
        elif var.LaunchArgument == "?page_series":
            liseriesprogram.list_load_combined()
        elif var.LaunchArgument == "?page_kids":
            likidsprogram.list_load_combined()
        elif var.LaunchArgument == "?page_sport":
            lisport.list_load_combined()
        elif var.LaunchArgument == "?page_vod":
            livod.list_load_combined()
        elif var.LaunchArgument == "?page_recorded":
            lirecorded.list_load_combined()
        elif var.LaunchArgument.startswith("?load_series_episodes_program="):
            actionSplit = var.LaunchArgument.replace('?load_series_episodes_program=', '').split(var.splitchar)
            liseriesepisode.list_load_program_combined(actionSplit[1], actionSplit[2])
        elif var.LaunchArgument.startswith("?load_series_episodes_vod="):
            actionSplit = var.LaunchArgument.replace('?load_series_episodes_vod=', '').split(var.splitchar)
            liseriesepisode.list_load_vod_combined(actionSplit[0], actionSplit[2])
        elif var.LaunchArgument.startswith("?load_kids_episodes_program="):
            actionSplit = var.LaunchArgument.replace('?load_kids_episodes_program=', '').split(var.splitchar)
            likidsepisode.list_load_program_combined(actionSplit[1], actionSplit[2])
        elif var.LaunchArgument.startswith("?load_kids_episodes_vod="):
            actionSplit = var.LaunchArgument.replace('?load_kids_episodes_vod=', '').split(var.splitchar)
            likidsepisode.list_load_vod_combined(actionSplit[0], actionSplit[2])

        #Play streams
        elif var.LaunchArgument.startswith("?play_stream_tv="):
            actionSplit = var.LaunchArgument.replace('?play_stream_tv=', '').split(var.splitchar)
            streamswitch.switch_tv_id(actionSplit[0], ShowInformation=True)
        elif var.LaunchArgument.startswith("?play_stream_radio="):
            actionSplit = var.LaunchArgument.replace('?play_stream_radio=', '').split(var.splitchar)
            streamswitch.switch_radio_id(actionSplit[0], Windowed=False)
        elif var.LaunchArgument.startswith("?play_stream_program="):
            actionSplit = var.LaunchArgument.replace('?play_stream_program=', '').split(var.splitchar)
            streamswitch.switch_program_id(actionSplit[0])
        elif var.LaunchArgument.startswith("?play_stream_vod="):
            actionSplit = var.LaunchArgument.replace('?play_stream_vod=', '').split(var.splitchar)
            streamswitch.switch_vod_id(actionSplit[0])
        elif var.LaunchArgument.startswith("?play_stream_recorded="):
            actionSplit = var.LaunchArgument.replace('?play_stream_recorded=', '').split(var.splitchar)
            streamswitch.switch_recorded_id(actionSplit[0], actionSplit[1])
        return True
    except:
        return True
