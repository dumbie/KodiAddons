import xbmc
import xbmcgui
import download
import func
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
                elif listItemAction == "search_channelprogram":
                    self.search_channelprogram()
                elif listItemAction == "show_visualisation":
                    show_visualisation()
            elif clickId == 3001:
                close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_channelprogram()
        else:
            zap.check_remote_number(self, 1000, actionId, True, False)

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoek naar zender')
        listitem.setProperty('Action', 'search_channelprogram')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Toon visualisatie')
        listitem.setProperty('Action', 'show_visualisation')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/visualisation.png'), 'icon': path.resources('resources/skins/default/media/common/visualisation.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_programs')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_channelprogram(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek naar zender')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_channels(True, False)
        var.SearchFilterTerm = ''

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

        #Add channels to the list
        func.updateLabelText(self, 1, 'Zenders laden')
        ChannelNumberInt = 0
        for channel in var.ChannelsDataJsonRadio['radios']:
            try:
                #Load channel basics
                ChannelName = channel['name']

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch = func.search_filter_string(ChannelName)
                    searchResultFound = var.SearchFilterTerm in searchMatch
                    if searchResultFound == False: continue

                #Load channel details
                ChannelId = channel['id']
                ChannelStream = channel['stream']

                #Update channel number
                ChannelNumberInt += 1
                ChannelNumberString = str(ChannelNumberInt)
                ChannelNumberAccent = func.get_provider_color_string() + ChannelNumberString + '[/COLOR]'

                #Add radio channel
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'play_stream')
                listitem.setProperty('ChannelId', ChannelId)
                listitem.setProperty('ChannelName', ChannelName)
                listitem.setProperty('ChannelNumber', ChannelNumberString)
                listitem.setProperty('ChannelNumberAccent', ChannelNumberAccent)
                listitem.setProperty('StreamUrl', ChannelStream)
                listitem.setInfo('music', {'Genre': 'Radio'})
                listitem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the status
        self.count_radio(True)

    #Update the status
    def count_radio(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' gevonden zenders')
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' zenders')

            if resetSelect == True:
                func.focus_on_channel_list(self, 1000, 0, True, var.addon.getSetting('CurrentRadioId'))
        else:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen zenders')
                listcontainer.selectItem(0)
            xbmc.sleep(100)
