import lifunc
import xbmcgui
import path
import var

def list_load(listContainer):
    try:
        if var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Televisie')
            listItem.setProperty('Action', 'page_television')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/television.png'),'icon': path.resources('resources/skins/default/media/common/television.png')})
            lifunc.auto_add_item(listItem, listContainer, dirUrl='page_television', dirFolder=True)

        listItem = xbmcgui.ListItem('Radio')
        listItem.setProperty('Action', 'page_radio')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/radio.png'), 'icon': path.resources('resources/skins/default/media/common/radio.png')})
        lifunc.auto_add_item(listItem, listContainer, dirUrl='page_radio', dirFolder=True)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Films')
            listItem.setProperty('Action', 'page_movies')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/movies.png'), 'icon': path.resources('resources/skins/default/media/common/movies.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Series')
            listItem.setProperty('Action', 'page_series')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/series.png'), 'icon': path.resources('resources/skins/default/media/common/series.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('TV Gids')
            listItem.setProperty('Action', 'page_epg')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/epg.png'), 'icon': path.resources('resources/skins/default/media/common/epg.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Terugzoeken')
            listItem.setProperty('Action', 'page_search')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Sport Gemist')
            listItem.setProperty('Action', 'page_sport')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/sport.png'), 'icon': path.resources('resources/skins/default/media/common/sport.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Programma Gemist')
            listItem.setProperty('Action', 'page_vod')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/vod.png'), 'icon': path.resources('resources/skins/default/media/common/vod.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            if var.addon.getSetting('KidsPageLock') == 'true':
                listItem = xbmcgui.ListItem('Kids met slot')
            else:
                listItem = xbmcgui.ListItem('Kids')
            listItem.setProperty('Action', 'page_kids')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/kids.png'), 'icon': path.resources('resources/skins/default/media/common/kids.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True and var.RecordingAccess == True:
            listItem = xbmcgui.ListItem('Bekijk Opnames (?)')
            listItem.setProperty('Action', 'page_recorded')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/recorddone.png'), 'icon': path.resources('resources/skins/default/media/common/recorddone.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True and var.RecordingAccess == True:
            listItem = xbmcgui.ListItem('Geplande Opnames (?)')
            listItem.setProperty('Action', 'page_recording_event')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/record.png'), 'icon': path.resources('resources/skins/default/media/common/record.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True and var.RecordingAccess == True:
            listItem = xbmcgui.ListItem('Geplande Series (?)')
            listItem.setProperty('Action', 'page_recording_series')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/recordseries.png'), 'icon': path.resources('resources/skins/default/media/common/recordseries.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None and var.ApiLoggedIn == True:
            listItem = xbmcgui.ListItem('Alarmen (?)')
            listItem.setProperty('Action', 'page_alarm')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/alarm.png'), 'icon': path.resources('resources/skins/default/media/common/alarm.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None:
            listItem = xbmcgui.ListItem('Slaap Timer')
            listItem.setProperty('Action', 'page_sleep')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/sleep.png'), 'icon': path.resources('resources/skins/default/media/common/sleep.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None:
            listItem = xbmcgui.ListItem('Instellingen')
            listItem.setProperty('Action', 'addon_settings')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/settings.png'), 'icon': path.resources('resources/skins/default/media/common/settings.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None:
            listItem = xbmcgui.ListItem('Help')
            listItem.setProperty('Action', 'page_help')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/help.png'), 'icon': path.resources('resources/skins/default/media/common/help.png')})
            lifunc.auto_add_item(listItem, listContainer)

        if listContainer != None:
            listItem = xbmcgui.ListItem('Sluiten')
            listItem.setProperty('Action', 'addon_shutdown')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/shutdown.png'), 'icon': path.resources('resources/skins/default/media/common/shutdown.png')})
            lifunc.auto_add_item(listItem, listContainer)

        lifunc.auto_end_items()
    except:
        pass
