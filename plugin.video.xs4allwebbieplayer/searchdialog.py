import json
import xbmc
import classes
import dialog
import files
import func
import hybrid
import var

def search_history_search_json_load(forceLoad=False):
    try:
        if var.SearchHistorySearchJson == [] or forceLoad == True:
            if files.existFileUser('SearchHistorySearch.js') == True:
                SearchHistoryJsonString = files.openFileUser('SearchHistorySearch.js')
                var.SearchHistorySearchJson = json.loads(SearchHistoryJsonString)
    except:
        var.SearchHistorySearchJson = []

def search_history_channel_json_load(forceLoad=False):
    try:
        if var.SearchHistoryChannelJson == [] or forceLoad == True:
            if files.existFileUser('SearchHistoryChannel.js') == True:
                SearchHistoryJsonString = files.openFileUser('SearchHistoryChannel.js')
                var.SearchHistoryChannelJson = json.loads(SearchHistoryJsonString)
    except:
        var.SearchHistoryChannelJson = []

def search_history_radio_json_load(forceLoad=False):
    try:
        if var.SearchHistoryRadioJson == [] or forceLoad == True:
            if files.existFileUser('SearchHistoryRadio.js') == True:
                SearchHistoryJsonString = files.openFileUser('SearchHistoryRadio.js')
                var.SearchHistoryRadioJson = json.loads(SearchHistoryJsonString)
    except:
        var.SearchHistoryRadioJson = []

def search_history_add(searchTerm, searchJsonFileName):
    #Check search term
    if func.string_isnullorempty(searchTerm) == True:
        return

    #Set Json target list variable
    if searchJsonFileName == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFileName == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFileName == 'SearchHistorySearch.js':
        searchHistoryTargetJson = var.SearchHistorySearchJson
    else:
        return

    #Remove search term from Json
    search_history_remove(searchTerm, searchJsonFileName, False)

    #Add search history to Json
    searchHistoryTargetJson.insert(0, searchTerm)

    #Trim search history length
    if len(searchHistoryTargetJson) > 40:
        searchHistoryTargetJson = searchHistoryTargetJson[:40]

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(searchHistoryTargetJson).encode('ascii')
    files.saveFileUser(searchJsonFileName, JsonDumpBytes)

def search_history_remove(searchTerm, searchJsonFileName, saveJson=True):
    #Set Json target list variable
    if searchJsonFileName == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFileName == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFileName == 'SearchHistorySearch.js':
        searchHistoryTargetJson = var.SearchHistorySearchJson
    else:
        return

    #Remove search term from Json
    for search in searchHistoryTargetJson:
        try:
            if search == searchTerm:
                searchHistoryTargetJson.remove(search)
                break
        except:
            continue

    #Save the raw json data to storage
    if saveJson == True:
        JsonDumpBytes = json.dumps(searchHistoryTargetJson).encode('ascii')
        files.saveFileUser(searchJsonFileName, JsonDumpBytes)

def search_keyboard(searchJsonFileName, headerText='Zoeken'):
    keyboard = xbmc.Keyboard('default', 'heading')
    keyboard.setHeading(headerText)
    keyboard.setDefault('')
    keyboard.setHiddenInput(False)
    keyboard.doModal()
    if keyboard.isConfirmed() == True:
        #Get keyboard text
        keyboardText = keyboard.getText()

        #Add search history to Json
        search_history_add(keyboardText, searchJsonFileName)

        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = keyboardText
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
        search_history_channel_json_load()
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFileName == 'SearchHistoryRadio.js':
        search_history_radio_json_load()
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFileName == 'SearchHistorySearch.js':
        search_history_search_json_load()
        searchHistoryTargetJson = var.SearchHistorySearchJson

    #Set search history
    dialogAnswers = hybrid.deep_copy_list(searchHistoryTargetJson)
    dialogAnswers.insert(0, '- Leeg zoek term gebruiken')
    dialogAnswers.insert(0, '+ Nieuw zoek term gebruiken')

    dialogHeader = headerText
    dialogSummary = 'Selecteer een eerder gebruikte zoek term of klik op nieuw zoek term.'
    dialogFooter = ''

    #Select search string
    searchString = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)

    #Check search string
    if searchString == '+ Nieuw zoek term gebruiken':
        return search_keyboard(searchJsonFileName)
    elif searchString == '- Leeg zoek term gebruiken':
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
        #Add search history to Json
        search_history_add(searchString, searchJsonFileName)

        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = searchString
        return searchResult
