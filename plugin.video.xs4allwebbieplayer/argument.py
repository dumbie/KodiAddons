import sys
import xbmcaddon
import default
import func
import hybrid
import lichannelradio
import lichanneltelevision
import lifunc
import likidsepisode
import likidsprogram
import limain
import limovies
import lirecorded
import liseriesepisode
import liseriesprogram
import lisport
import livod
import streamplay
import var
import widevine

def set_launch_argument_source():
    try:
        var.LaunchUrl = str(sys.argv[0])
        var.LaunchHandle = int(sys.argv[1])
        var.LaunchArgument = hybrid.urllib_unquote(str(sys.argv[2]))[1:]
        return True
    except:
        return False

def handle_launch_argument_source():
    try:
        #Handle settings
        if var.LaunchArgument == "InputAdaptiveSettings":
            xbmcaddon.Addon('inputstream.adaptive').openSettings()
        elif var.LaunchArgument == "UpdateWidevineFiles":
            widevine.enable_widevine_support(True)
        elif var.LaunchArgument == "ResetUserdata":
            default.reset_userdata()
        elif var.LaunchArgument == "ResetThumbnails":
            default.reset_thumbnails()

        #List main menu
        elif func.string_isnullorempty(var.LaunchArgument):
            limain.list_load_combined()

        #Decode pickle directory url
        jsonItem = func.picklestring_to_object(var.LaunchArgument)
        listItem = lifunc.jsonitem_to_listitem(jsonItem)
        actionItem = jsonItem['ItemAction']

        #List pages
        if actionItem == "page_television":
            lichanneltelevision.list_load_combined()
        elif actionItem == "page_radio":
            lichannelradio.list_load_combined()
        elif actionItem == "page_movies":
            limovies.list_load_combined()
        elif actionItem == "page_series":
            liseriesprogram.list_load_combined()
        elif actionItem == "page_kids":
            likidsprogram.list_load_combined()
        elif actionItem == "page_sport":
            lisport.list_load_combined()
        elif actionItem == "page_vod":
            livod.list_load_combined()
        elif actionItem == "page_recorded":
            lirecorded.list_load_combined()

        #List programs
        elif actionItem == "load_series_episodes_program":
            liseriesepisode.list_load_program_combined(jsonItem['ProgramName'], jsonItem['PictureUrl'])
        elif actionItem == "load_series_episodes_vod":
            liseriesepisode.list_load_vod_combined(jsonItem['ProgramId'], jsonItem['PictureUrl'])
        elif actionItem == "load_kids_episodes_program":
            likidsepisode.list_load_program_combined(jsonItem['ProgramName'], jsonItem['PictureUrl'])
        elif actionItem == "load_kids_episodes_vod":
            likidsepisode.list_load_vod_combined(jsonItem['ProgramId'], jsonItem['PictureUrl'])

        #Play streams
        elif actionItem == "play_stream_tv":
            streamplay.play_tv(listItem)
        elif actionItem == "play_stream_radio":
            streamplay.play_radio(listItem)
        elif actionItem == "play_stream_program":
            streamplay.play_program(listItem)
        elif actionItem == "play_stream_vod":
            streamplay.play_vod(listItem)
        elif actionItem == "play_stream_recorded":
            streamplay.play_recorded(listItem)
        return True
    except:
        return False
