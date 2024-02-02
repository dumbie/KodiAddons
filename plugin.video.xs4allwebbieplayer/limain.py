import apilogin
import download
import lifunc
import xbmcgui
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

        if ApiLoggedIn == True:
            listAction = 'page_television'
            listItem = xbmcgui.ListItem('Televisie')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/television.png'),'icon': path.resources('resources/skins/default/media/common/television.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        listAction = 'page_radio'
        listItem = xbmcgui.ListItem('Radio')
        listItem.setProperty('Action', listAction)
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/radio.png'), 'icon': path.resources('resources/skins/default/media/common/radio.png')})
        dirIsFolder = True
        dirUrl = var.LaunchUrl + '?' + listAction
        listContainer.append((dirUrl, listItem, dirIsFolder))

        if ApiLoggedIn == True:
            listAction = 'page_movies'
            listItem = xbmcgui.ListItem('Films')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/movies.png'), 'icon': path.resources('resources/skins/default/media/common/movies.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if ApiLoggedIn == True:
            listAction = 'page_series'
            listItem = xbmcgui.ListItem('Series')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/series.png'), 'icon': path.resources('resources/skins/default/media/common/series.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False and ApiLoggedIn == True:
            listAction = 'page_epg'
            listItem = xbmcgui.ListItem('TV Gids')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/epg.png'), 'icon': path.resources('resources/skins/default/media/common/epg.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False and ApiLoggedIn == True:
            listAction = 'page_search'
            listItem = xbmcgui.ListItem('Terugzoeken')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if ApiLoggedIn == True:
            listAction = 'page_sport'
            listItem = xbmcgui.ListItem('Sport Gemist')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/sport.png'), 'icon': path.resources('resources/skins/default/media/common/sport.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if ApiLoggedIn == True:
            listAction = 'page_vod'
            listItem = xbmcgui.ListItem('Programma Gemist')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/vod.png'), 'icon': path.resources('resources/skins/default/media/common/vod.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if ApiLoggedIn == True:
            listAction = 'page_kids'
            if remoteMode == False and var.addon.getSetting('KidsPageLock') == 'true':
                listItem = xbmcgui.ListItem('Kids met slot')
            else:
                listItem = xbmcgui.ListItem('Kids')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/kids.png'), 'icon': path.resources('resources/skins/default/media/common/kids.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if ApiLoggedIn == True and RecordingAccess == True:
            listAction = 'page_recorded'
            listItem = xbmcgui.ListItem('Bekijk Opnames')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/recorddone.png'), 'icon': path.resources('resources/skins/default/media/common/recorddone.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False and ApiLoggedIn == True and RecordingAccess == True:
            listAction = 'page_recording_event'
            listItem = xbmcgui.ListItem('Geplande Opnames')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/record.png'), 'icon': path.resources('resources/skins/default/media/common/record.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False and ApiLoggedIn == True and RecordingAccess == True:
            listAction = 'page_recording_series'
            listItem = xbmcgui.ListItem('Geplande Series')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/recordseries.png'), 'icon': path.resources('resources/skins/default/media/common/recordseries.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False and ApiLoggedIn == True:
            listAction = 'page_alarm'
            listItem = xbmcgui.ListItem('Alarmen')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/alarm.png'), 'icon': path.resources('resources/skins/default/media/common/alarm.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False:
            listAction = 'page_sleep'
            listItem = xbmcgui.ListItem('Slaap Timer')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/sleep.png'), 'icon': path.resources('resources/skins/default/media/common/sleep.png')})
            dirIsFolder = True
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False:
            listAction = 'addon_settings'
            listItem = xbmcgui.ListItem('Instellingen')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/settings.png'), 'icon': path.resources('resources/skins/default/media/common/settings.png')})
            dirIsFolder = False
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False:
            listAction = 'page_help'
            listItem = xbmcgui.ListItem('Help')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/help.png'), 'icon': path.resources('resources/skins/default/media/common/help.png')})
            dirIsFolder = False
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))

        if remoteMode == False:
            listAction = 'addon_shutdown'
            listItem = xbmcgui.ListItem('Sluiten')
            listItem.setProperty('Action', listAction)
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/shutdown.png'), 'icon': path.resources('resources/skins/default/media/common/shutdown.png')})
            dirIsFolder = False
            dirUrl = var.LaunchUrl + '?' + listAction
            listContainer.append((dirUrl, listItem, dirIsFolder))
    except:
        pass
