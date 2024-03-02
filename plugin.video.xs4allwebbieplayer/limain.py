import apilogin
import download
import func
import getset
import lifunc
import path
import var

def list_load_combined(listContainer=None):
    try:
        #Check if logged in on launch
        if var.ApiLoggedIn() == False:
             apilogin.ApiLogin()

        #Check if user is logged in
        if var.ApiLoggedIn() == True:
             download.download_recording_profile()

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
    try:
        ApiLoggedIn = var.ApiLoggedIn()
        RecordingAccess = var.RecordingAccess()

        if ApiLoggedIn == True and getset.setting_get('MainShowTelevision') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/television.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Televisie',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_television'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if getset.setting_get('MainShowRadio') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/radio.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Radio',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_radio'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if ApiLoggedIn == True and getset.setting_get('MainShowMovies') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/movies.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Films',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_movies'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if ApiLoggedIn == True and getset.setting_get('MainShowSeries') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/series.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Series',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_series'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and ApiLoggedIn == True and getset.setting_get('MainShowEpg') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/epg.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'TV Gids',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_epg'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and ApiLoggedIn == True and getset.setting_get('MainShowSearch') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/search.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Terugzoeken',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_search'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if ApiLoggedIn == True and getset.setting_get('MainShowSport') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/sport.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Sport Gemist',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_sport'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if ApiLoggedIn == True and getset.setting_get('MainShowVod') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/vod.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Programma Gemist',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_vod'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if ApiLoggedIn == True and getset.setting_get('MainShowKids') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/kids.png')

            #Set item details
            if remoteMode == False and getset.setting_get('KidsPageLock') == 'true':
                itemLabel = 'Kids met slot'
            else:
                itemLabel = 'Kids'

            jsonItem = {
                'ItemLabel': itemLabel,
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_kids'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if ApiLoggedIn == True and RecordingAccess == True and getset.setting_get('MainShowRecordDone') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/recorddone.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Bekijk Opnames',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_recorded'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and ApiLoggedIn == True and RecordingAccess == True and getset.setting_get('MainShowRecordEvent') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/recordevent.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Geplande Opnames',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_recording_event'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and ApiLoggedIn == True and RecordingAccess == True and getset.setting_get('MainShowRecordSeries') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/recordseries.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Geplande Series',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_recording_series'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and ApiLoggedIn == True and getset.setting_get('MainShowAlarm') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/alarm.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Alarmen',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_alarm'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and getset.setting_get('MainShowSleep') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/sleep.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Slaap Timer',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_sleep'
            }
            dirIsfolder = True
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and getset.setting_get('MainShowHelp') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/help.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Help',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'page_help'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and getset.setting_get('MainShowSettings') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/settings.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Instellingen',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'addon_settings'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == False and getset.setting_get('MainShowShutdown') == 'true':
            #Set item icons
            iconDefault = path.resources('resources/skins/default/media/common/shutdown.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Sluiten',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'addon_shutdown'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))

        if remoteMode == True:
            #Set item icons
            iconDefault = path.resources('resources/icon.png')

            #Set item details
            jsonItem = {
                'ItemLabel': 'Toon Webbie Player',
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'addon_launch'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
    except:
        pass
