import var
import xbmcgui
import xbmcaddon
import widevine
import default
import func
import var
import main
import radio
import television
import movies
import switch
import sport
import vod
import recorded
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

def handle_launch_argument_source():
    try:
        #Fix share variables every source request
        #Fix add listitem to dirurl string conversion
        #Fix resolve missing details in switch code

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
        elif var.LaunchArgument == "?page_sport":
            sport.source_plugin_list()
        elif var.LaunchArgument == "?page_vod":
            vod.source_plugin_list()
        elif var.LaunchArgument == "?page_recorded":
            recorded.source_plugin_list()

        #Play streams
        elif var.LaunchArgument.startswith("?play_stream_tv="):
            channelId = var.LaunchArgument.replace('?play_stream_tv=', '')
            switch.stream_tv_channelid(channelId)
        elif var.LaunchArgument.startswith("?play_stream_radio="):
            channelId = var.LaunchArgument.replace('?play_stream_radio=', '')
            switch.stream_radio_channelid(channelId)
        elif var.LaunchArgument.startswith("?play_stream_program="):
            programId = var.LaunchArgument.replace('?play_stream_program=', '')
            switch.stream_program_id(programId)
        elif var.LaunchArgument.startswith("?play_stream_vod="):
            programId = var.LaunchArgument.replace('?play_stream_vod=', '')
            switch.stream_vod_id(programId)
        elif var.LaunchArgument.startswith("?play_stream_recorded="):
            actionSplit = var.LaunchArgument.replace('?play_stream_recorded=', '').split(',')
            switch.stream_recorded_id(actionSplit[0], actionSplit[1])
        return True
    except:
        return True
