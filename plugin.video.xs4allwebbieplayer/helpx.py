import xbmcgui
import guifunc
import var

def switch_to_page():
    if var.guiHelp == None:
        var.guiHelp = Gui('help.xml', var.addonpath, 'default', '720p')
        var.guiHelp.setProperty('WebbiePlayerPage', 'Open')
        var.guiHelp.show()

def close_the_page():
    if var.guiHelp != None:
        #Close the shown window
        var.guiHelp.close()
        var.guiHelp = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        self.set_help_text()

    def onClick(self, clickId):
        if clickId == 4000:
            close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()

    def set_help_text(self):
        helpText = 'Sommige tv zenders willen niet laden'
        helpText += '\n[COLOR gray]Als alleen NPO 1, 2 en 3 laden betekent dit dat uw apparaat niet de stream beveiliging (Widevine DRM) van de andere zenders kan openen, u kunt proberen Widevine opnieuw te installeren door naar de Webbie Player instellingen te gaan en op "Stream > Update de benodigde Widevine beveiliging bestanden" te drukken.[/COLOR]'

        helpText += '\n\nGoede draadloos verbinding vereist'
        helpText += '\n[COLOR gray]Als u via draadloos internet kijkt zorg er dan voor dat u een goed signaal heeft anders kunt u storingen zoals haperingen krijgen tijdens het tv kijken, u kunt de maximale beeld kwaliteit verlagen in de Webbie Player "Stream" instellingen.[/COLOR]'

        helpText += '\n\nMinder zenders beschikbaar buitenshuis'
        helpText += '\n[COLOR gray]Als u buitenshuis via een telefoon of VPN verbinding kijkt kunnen er minder zenders beschikbaar zijn en kunt u een foutmelding krijgen dat u geen rechten heeft om te kijken als u een zender aanklikt.[/COLOR]'

        helpText += '\n\nKodi loopt vast bij starten stream'
        helpText += '\n[COLOR gray]Als Kodi vast loopt kunt u proberen de volgende Kodi instelling in te schakelen: "Kodi instellingen > Speler > Video > Synchroniseer video met beeldschermfrequentie > Aan", als dit niet werkt kunt u proberen de "Lokale proxy server" te gebruiken die in te schakelen is via de Webbie Player "Stream" instellingen.[/COLOR]'

        helpText += '\n\nStotterend beeld tijdens het kijken'
        helpText += '\n[COLOR gray]Als u last heeft van kleine stotteringen kunt u proberen de volgende Kodi instelling in te schakelen: "Kodi instellingen > Speler > Video > Aanpassen beeldscherm verversfrequentie > Starten/Stoppen"[/COLOR]'

        helpText += '\n\nSneller menu navigatie inschakelen'
        helpText += '\n[COLOR gray]Tijdens het afspelen kunt u de menu navigatie sneller maken door de volgende Kodi instelling in te schakelen: "Kodi instellingen > Speler > Video > Limiteer GUI tijdens afspelen > Onbeperkt"[/COLOR]'

        helpText += '\n\nEigen achtergrond afbeelding instellen'
        helpText += '\n[COLOR gray]U kunt uw eigen achtergrond weergeven door een "background.png" afbeelding te plaatsen in de "userdata/addon_data/plugin.video.xs4allwebbieplayer" map.[/COLOR]'

        helpText += '\n\nWelke knoppen kan ik gebruiken?'
        helpText += '\nNummers: [COLOR gray]Door het invoeren van een nummer kunt u rechtstreeks naar een zender schakelen.[/COLOR]\nMedia knoppen: [COLOR gray]Hiermee kunt u naar de volgende en vorige zender tijdens het tv kijken of in de tv gids.[/COLOR]\nSpoel knoppen: [COLOR gray]Hiermee kunt u naar de volgende en vorige dag in de tv gids.[/COLOR]\nMenu knop: [COLOR gray]Hiermee kunt u naar de vorig bekeken zender terug zappen tijdens het tv kijken.[/COLOR]\nPijl omhoog/omlaag: [COLOR gray]Kunt u de volume mee aanpassen tijdens het tv kijken.[/COLOR]\nPijl links: [COLOR gray]Kunt u mee terug naar de stream op de televisie pagina.[/COLOR]'

        helpText += '\n\nGebruik Webbie Player op eigen risico'
        helpText += '\n[COLOR gray]Als er een DDoS aanval wordt uitgevoerd op de interactieve tv server kan Webbie Player door een onbekende reden als aanvaller beschouwt worden en is er een kleine kans dat uw internet verbinding tijdelijk kan worden uitgeschakeld door uw provider.[/COLOR]'

        helpText += '\n\nRadio zender werkt niet meer'
        helpText += '\n[COLOR gray]Als een bepaalde radio zender niet meer werkt kunt u dit aan de ontwikkelaar van Webbie Player melden via https://contact.arnoldvink.com zodat de radio zender aangepast kan worden in de lijst.[/COLOR]'

        helpText += '\n\nOndersteuning en fouten melden'
        helpText += '\n[COLOR gray]Als u tegen een probleem aanloopt of een fout tegen komt kunt u die melden via https://help.arnoldvink.com zodat ik u kan proberen te helpen om alles weer aan de gang te krijgen.[/COLOR]'

        helpText += '\n\nOntwikkelaar donatie'
        helpText += '\n[COLOR gray]Als u mijn project waardeert en mij wilt ondersteunen met mijn projecten kunt u een donatie maken via https://donation.arnoldvink.com[/COLOR]'

        helpText += '\n\nAdd-on is gemaakt door Arnold Vink'
        helpText += '\n[COLOR gray]Versie: v' + var.addonversion + '[/COLOR]'

        guifunc.updateTextBoxText(self, 3000, helpText)

        #Focus on the close button
        closeButton = self.getControl(4000)
        guifunc.controlFocus(self, closeButton)
