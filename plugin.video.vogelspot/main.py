import json
import xbmc
import xbmcgui
import download
import func
import path
import var

def switch_to_page():
    if var.guiMain == None:
        var.guiMain = Gui('main.xml', var.addonpath, 'default', '720p')
        var.guiMain.doModal()
        var.guiMain = None

def close_the_page():
    if var.guiMain != None:
        #Stop the playing media
        xbmc.Player().stop()

        #Close the shown window
        var.guiMain.close()

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Add streams list to the page
        listcontainer = self.getControl(1001)
        if listcontainer.size() == 0:
            self.list_add_streams()

    def list_add_streams(self):
        #Check if addon is busy
        if var.busy_main == True: return
        var.busy_main = True

        #Clear streams from the list
        listcontainer = self.getControl(1001)
        listcontainer.reset()

        #Update the load status
        func.updateLabelText(self, 1, 'Loading streams')

        #Open streams json file
        string_streams = download.download_streams()
        json_streams = json.loads(string_streams)

        #Update the load status
        func.updateLabelText(self, 1, 'Adding streams')

        #Sort streams by name
        json_streams.sort(key=lambda x: (x['source'], x['name'], x["location"]))

        #Add streams to the list
        for channel in json_streams:
            try:
                #Load stream information
                StreamName = channel['name']
                StreamLocation = channel['location']
                StreamSource = channel['source']
                StreamUrl = channel['stream']
                StreamTokenUrl = channel['token']
                StreamName += ' [COLOR ff71c6fe]' + StreamLocation + '[/COLOR]'
                StreamName += ' [COLOR ff26671e]' + StreamSource + '[/COLOR]'
                StreamImage = path.ImageUrl + channel['id'] + '.png'

                #Add stream to the list
                listitem = xbmcgui.ListItem(StreamName)
                listitem.setProperty('StreamUrl', StreamUrl)
                listitem.setProperty('StreamTokenUrl', StreamTokenUrl)
                listitem.setArt({'thumb': StreamImage, 'icon': StreamImage})
                listitem.setInfo('video', {'Genre': 'Vogel', 'Plot': StreamName})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the total stream count
        func.updateLabelText(self, 1, str(listcontainer.size()) + ' streams')

        #Focus on the stream list
        self.setFocus(listcontainer)
        xbmc.sleep(200)
        listcontainer.selectItem(0)
        xbmc.sleep(200)

        var.busy_main = False

    def onAction(self, action):
        actionId = action.getId()
        if actionId == var.ACTION_PREVIOUS_MENU: close_the_page()
        elif actionId == var.ACTION_BACKSPACE: close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            self.open_stream(listItemSelected)
        elif clickId == 3000:
            close_the_page()
        elif clickId == 9000:
            xbmc.executebuiltin('Action(FullScreen)')

    def open_stream(self, listItem):
        StreamUrl = listItem.getProperty('StreamUrl')
        StreamTokenUrl = listItem.getProperty('StreamTokenUrl')

        if func.string_isnullorempty(StreamTokenUrl) == False:
            DownloadToken = download.download_token(StreamTokenUrl)
            DownloadToken = DownloadToken.replace('|', '%7C')
            StreamUrl += '&' + DownloadToken

        xbmc.Player().play(item=StreamUrl, listitem=listItem, windowed=True)
