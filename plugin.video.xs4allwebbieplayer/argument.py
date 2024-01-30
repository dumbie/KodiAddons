import var
import xbmcaddon
import widevine
import default
import func
import hybrid
import var
import main
import radio
import television
import movies
import series
import kids
import streamswitch
import sport
import vod
import recorded
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
            main.source_plugin_list()
        elif var.LaunchArgument == "?page_television":
            television.source_plugin_list()
        elif var.LaunchArgument == "?page_radio":
            radio.source_plugin_list()
        elif var.LaunchArgument == "?page_movies":
            movies.source_plugin_list()
        elif var.LaunchArgument == "?page_series":
            series.source_plugin_list_program()
        elif var.LaunchArgument == "?page_kids":
            kids.source_plugin_list_program()
        elif var.LaunchArgument == "?page_sport":
            sport.source_plugin_list()
        elif var.LaunchArgument == "?page_vod":
            vod.source_plugin_list()
        elif var.LaunchArgument == "?page_recorded":
            recorded.source_plugin_list()
        elif var.LaunchArgument.startswith("?load_series_episodes_week="):
            actionSplit = var.LaunchArgument.replace('?load_series_episodes_week=', '').split(var.splitchar)
            series.source_plugin_list_episode_week(actionSplit[1])
        elif var.LaunchArgument.startswith("?load_series_episodes_vod="):
            actionSplit = var.LaunchArgument.replace('?load_series_episodes_vod=', '').split(var.splitchar)
            series.source_plugin_list_episode_vod(actionSplit[0])
        elif var.LaunchArgument.startswith("?load_kids_episodes_week="):
            actionSplit = var.LaunchArgument.replace('?load_kids_episodes_week=', '').split(var.splitchar)
            kids.source_plugin_list_episode_week(actionSplit[1])
        elif var.LaunchArgument.startswith("?load_kids_episodes_vod="):
            actionSplit = var.LaunchArgument.replace('?load_kids_episodes_vod=', '').split(var.splitchar)
            kids.source_plugin_list_episode_vod(actionSplit[0])

        #Play streams
        elif var.LaunchArgument.startswith("?play_stream_tv="):
            channelId = var.LaunchArgument.replace('?play_stream_tv=', '')
            streamswitch.switch_tv_id(channelId, ShowInformation=True)
        elif var.LaunchArgument.startswith("?play_stream_radio="):
            channelId = var.LaunchArgument.replace('?play_stream_radio=', '')
            streamswitch.switch_radio_id(channelId)
        elif var.LaunchArgument.startswith("?play_stream_program="):
            actionSplit = var.LaunchArgument.replace('?play_stream_program=', '').split(var.splitchar)
            streamswitch.switch_program_id(actionSplit[0])
        elif var.LaunchArgument.startswith("?play_stream_vod="):
            programId = var.LaunchArgument.replace('?play_stream_vod=', '')
            streamswitch.switch_vod_id(programId)
        elif var.LaunchArgument.startswith("?play_stream_recorded="):
            actionSplit = var.LaunchArgument.replace('?play_stream_recorded=', '').split(var.splitchar)
            streamswitch.switch_recorded_id(actionSplit[0], actionSplit[1])
        return True
    except:
        return True
