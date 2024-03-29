import sys
import xbmcaddon
import xbmcgui
import alarmfunc
import cache
import favorite
import func
import hybrid
import lialarm
import lichannelradio
import lichanneltelevision
import liepgload
import lifunc
import likidsepisode
import likidsprogram
import limain
import limovies
import lirecorded
import lirecordingevent
import lirecordingseries
import lisearch
import liseriesepisode
import liseriesprogram
import lisport
import livod
import settings
import streamplay
import var
import welcome
import widevine

def set_launch_argument_source():
    try:
        var.LaunchUrl = str(sys.argv[0])
        var.LaunchHandle = int(sys.argv[1])
        var.LaunchArgument = hybrid.urllib_unquote(str(sys.argv[2])).lstrip("?json=")
        return True
    except:
        return False

def handle_launch_argument_source():
    try:
        #Handle settings
        if var.LaunchArgument == "InputAdaptiveSettings":
            xbmcaddon.Addon('inputstream.adaptive').openSettings()
            return True
        elif var.LaunchArgument == "UpdateWidevineFiles":
            widevine.enable_widevine_support(True)
            return True
        elif var.LaunchArgument == "UpdateKodiAddons":
            func.check_addon_updates()
            return True
        elif var.LaunchArgument == "ResetUserdata":
            settings.reset_userdata()
            return True
        elif var.LaunchArgument == "ResetThumbnails":
            settings.reset_thumbnails()
            return True
        elif var.LaunchArgument == "OpenWelcomeScreen":
            welcome.show_welcome()
            return True

        #List main menu
        elif func.string_isnullorempty(var.LaunchArgument):
            limain.list_load_combined()
            func.run_addon(False)
            return True

        #Decode pickle directory url
        jsonItem = func.jsonstring_to_dictionary(var.LaunchArgument)
        listItem = lifunc.jsonitem_to_listitem(jsonItem)
        actionItem = jsonItem['ItemAction']

        #List actions
        if actionItem == "addon_launch":
            func.run_addon()
        elif actionItem == "switch_all_favorites":
            favorite.favorite_switch_mode('', True)
        elif actionItem == "cache_remove_all":
            cache.cache_remove_all(False)
        elif actionItem == "action_none":
            xbmcgui.Dialog().notification(var.addonname, "Geen functie via afstandsbediening.", var.addonicon, 2500, False)

        #Search actions
        elif actionItem == "page_search":
            lisearch.list_load_history()
        elif actionItem == "load_search_keyboard":
            lisearch.list_load_keyboard()
        elif actionItem == "load_search_term":
            lisearch.list_load_term(jsonItem['SearchTerm'])

        #Epg actions
        elif actionItem == "page_epg":
            lichanneltelevision.list_load_combined(epgMode=True)
        elif actionItem == "load_epg_days":
            liepgload.list_load_days(channelId=jsonItem['ChannelId'])
        elif actionItem == "load_epg_programs":
            liepgload.list_load_combined(channelId=jsonItem['ChannelId'], dateTime=jsonItem['DateTime'])

        #Vod actions
        elif actionItem == "page_vod":
            livod.list_load_days()
        elif actionItem == "load_vod_programs":
            livod.list_load_combined(dateTime=jsonItem['DateTime'])

        #Alarm actions
        elif actionItem == "page_alarm":
            lialarm.list_load_combined()
        elif actionItem == "alarm_remove":
            alarmfunc.alarm_remove(jsonItem['ProgramTimeStart'], True)

        #List pages
        elif actionItem == "page_television":
            lichanneltelevision.list_load_combined(downloadEpg=True)
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
        elif actionItem == "page_recorded":
            lirecorded.list_load_combined()
        elif actionItem == "page_recording_event":
            lirecordingevent.list_load_combined()
        elif actionItem == "page_recording_series":
            lirecordingseries.list_load_combined()

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
            streamplay.play_tv(listItem, ShowInformation=True)
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
