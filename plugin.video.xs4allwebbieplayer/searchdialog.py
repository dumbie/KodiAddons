import xbmc
import classes
import dialog
import hybrid
import searchhistory

def search_keyboard(headerText='Zoeken'):
    keyboard = xbmc.Keyboard('default', 'heading')
    keyboard.setHeading(headerText)
    keyboard.setDefault('')
    keyboard.setHiddenInput(False)
    keyboard.doModal()
    if keyboard.isConfirmed() == True:
        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = keyboard.getText()
        return searchResult
    else:
        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = True
        searchResult.string = ''
        return searchResult

def search_dialog(searchJsonFileName, headerText='Zoeken'):
    #Set Json target list variable
    if searchJsonFileName == 'SearchHistoryChannel.js':
        searchHistoryJson = searchhistory.search_history_channel_json_load()
    elif searchJsonFileName == 'SearchHistoryRadio.js':
        searchHistoryJson = searchhistory.search_history_radio_json_load()
    elif searchJsonFileName == 'SearchHistorySearch.js':
        searchHistoryJson = searchhistory.search_history_search_json_load()
    else:
        searchHistoryJson = []

    #Set search history
    dialogAnswers = hybrid.deep_copy_list(searchHistoryJson)
    dialogAnswers.insert(0, '- Leeg zoekterm gebruiken')
    dialogAnswers.insert(0, '+ Nieuw zoekterm gebruiken')

    dialogHeader = headerText
    dialogSummary = 'Selecteer een eerder gebruikte zoekterm of klik op nieuw zoekterm.'
    dialogFooter = ''

    #Select search string
    searchString = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)

    #Check search string
    if searchString == '+ Nieuw zoekterm gebruiken':
        #Set search result
        searchResult = search_keyboard()

        #Add search history to Json
        searchhistory.search_history_add(searchResult.string, searchJsonFileName)

        #Return search result
        return searchResult
    elif searchString == '- Leeg zoekterm gebruiken':
        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = ''
        return searchResult
    elif searchString == 'DialogCancel':
        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = True
        searchResult.string = ''
        return searchResult
    else:
        #Set search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = searchString

        #Add search history to Json
        searchhistory.search_history_add(searchResult.string, searchJsonFileName)

        #Return search result
        return searchResult
