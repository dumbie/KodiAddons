import xbmc
import xbmcgui
import lichannelradio
import download
import dialog
import favorite
import func
import lifunc
import path
import searchdialog
import stream
import var
import zap

def switch_to_page():
    if var.guiRadio == None:
        var.guiRadio = Gui('radio.xml', var.addonpath, 'default', '720p')
        var.guiRadio.show()

def close_the_page():
    if var.guiRadio != None:
        #Close the shown window
        var.guiRadio.close()
        var.guiRadio = None

def show_visualisation():
    try:
        if xbmc.Player().isPlayingAudio():
            func.open_window_id(var.WINDOW_VISUALISATION)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Radio speelt niet.', notificationIcon, 2500, False)
    except:
        pass

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        self.buttons_add_navigation()
        self.load_channels(False, False)

    def onClick(self, clickId):
        if var.thread_zap_wait_timer == None:
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'play_stream':
                    stream.play_stream_radio(listItemSelected)
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'go_back':
                    close_the_page()
                elif listItemAction == 'refresh_programs':
                    self.load_channels(True, True)
                elif listItemAction == "switch_all_favorites":
                    self.switch_all_favorites()
                elif listItemAction == "search_channelprogram":
                    self.search_channelprogram()
                elif listItemAction == "show_visualisation":
                    show_visualisation()
            elif clickId == 3001:
                close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        focusChannel = xbmc.getCondVisibility('Control.HasFocus(1000)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.switch_all_favorites()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_channelprogram()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusChannel:
            self.open_context_menu()
        else:
            zap.check_remote_number(self, 1000, actionId, True, False)

    def open_context_menu(self):
        dialogAnswers = []
        dialogHeader = 'Radio Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde zender?'
        dialogFooter = ''

        #Get the selected channel
        listcontainer = self.getControl(1000)
        listItemSelected = listcontainer.getSelectedItem()

        #Check if channel is favorite
        if listItemSelected.getProperty('ChannelFavorite') == 'true':
            dialogAnswers.append('Zender onmarkeren als favoriet')
        else:
            dialogAnswers.append('Zender markeren als favoriet')

        #Add switch favorite/all button
        if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            dialogAnswers.append('Toon alle zenders')
        else:
            dialogAnswers.append('Toon favorieten zenders')

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Zender markeren als favoriet' or dialogResult == 'Zender onmarkeren als favoriet':
            self.switch_favorite_channel(listcontainer, listItemSelected)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_all_favorites()

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Alle of favorieten')
        listitem.setProperty('Action', 'switch_all_favorites')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoek naar zender')
        listitem.setProperty('Action', 'search_channelprogram')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Toon visualisatie')
        listitem.setProperty('Action', 'show_visualisation')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/visualisation.png'), 'icon': path.resources('resources/skins/default/media/common/visualisation.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Vernieuwen')
        listitem.setProperty('Action', 'refresh_programs')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def switch_favorite_channel(self, listContainer, listItemSelected):
        favoriteResult = favorite.favorite_toggle(listItemSelected, 'FavoriteRadio.js')
        if favoriteResult == 'Removed' and var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            #Remove item from the list
            removeListItemId = listContainer.getSelectedPosition()
            listContainer.removeItem(removeListItemId)
            xbmc.sleep(100)
            listContainer.selectItem(removeListItemId)
            xbmc.sleep(100)

            #Update the status
            self.count_channels(False)

    def switch_all_favorites(self):
        try:
            #Switch favorites mode on or off
            if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
                var.addon.setSetting('LoadChannelFavoritesOnly', 'false')
            else:
                #Check if there are favorites set
                if var.FavoriteRadioDataJson == []:
                    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
                    xbmcgui.Dialog().notification(var.addonname, 'Geen favorieten zenders.', notificationIcon, 2500, False)
                    return
                var.addon.setSetting('LoadChannelFavoritesOnly', 'true')

            self.load_channels(True, False)
        except:
            pass

    def search_channelprogram(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistoryRadio.js', 'Zoek naar zender')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchChannelTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_channels(True, False)
        var.SearchChannelTerm = ''

    def load_channels(self, forceLoad=False, forceUpdate=False):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zenders worden vernieuwd.', notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the channels
        func.updateLabelText(self, 1, 'Zenders downloaden')
        downloadResult = download.download_channels_radio(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, 'Zenders laden')

        #Add items to sort list
        listcontainersort = []
        lichannelradio.list_load(listcontainersort)

        #Sort and add items to container
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_channels(True)

    #Update the status
    def count_channels(self, resetSelect=False):
        #Set channel type string
        channelTypeString = 'zenders'
        if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            channelTypeString = 'favorieten zenders'

        #Update status label text
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' zenders gevonden')
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' ' + channelTypeString)

            if resetSelect == True:
                lifunc.focus_on_channelid_in_list(self, 1000, 0, True, var.addon.getSetting('CurrentRadioId'))
        else:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen ' + channelTypeString)
                listcontainer.selectItem(0)
            xbmc.sleep(100)
