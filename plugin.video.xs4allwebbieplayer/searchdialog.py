import classes
import func
import hybrid
import json
import xbmc
import dialog
import files
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

def search_history_add(searchTerm, searchJsonFile):
    #Check search term
    if func.string_isnullorempty(searchTerm) == True:
        return

    #Remove search term from Json
    search_history_remove(searchTerm, searchJsonFile, False)

    #Set Json target list variable
    if searchJsonFile == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFile == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFile == 'SearchHistorySearch.js':
        searchHistoryTargetJson = var.SearchHistorySearchJson

    #Add search history to Json
    searchHistoryTargetJson.insert(0, searchTerm)

    #Trim search history length
    if len(searchHistoryTargetJson) > 40:
        searchHistoryTargetJson = searchHistoryTargetJson[:40]

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(searchHistoryTargetJson).encode('ascii')
    files.saveFileUser(searchJsonFile, JsonDumpBytes)

def search_history_remove(searchTerm, searchJsonFile, saveJson=True):
    #Set Json target list variable
    if searchJsonFile == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFile == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFile == 'SearchHistorySearch.js':
        searchHistoryTargetJson = var.SearchHistorySearchJson

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
        files.saveFileUser(searchJsonFile, JsonDumpBytes)

def search_dialog(searchJsonFile, headerText='Zoeken'):
    #Set Json target list variable
    if searchJsonFile == 'SearchHistoryChannel.js':
        search_history_channel_json_load()
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFile == 'SearchHistoryRadio.js':
        search_history_radio_json_load()
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFile == 'SearchHistorySearch.js':
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
        keyboard = xbmc.Keyboard('default', 'heading')
        keyboard.setHeading(headerText)
        keyboard.setDefault('')
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            #Get keyboard text
            keyboardText = keyboard.getText()

            #Add search history to Json
            search_history_add(keyboardText, searchJsonFile)

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
        search_history_add(searchString, searchJsonFile)

        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = searchString
        return searchResult
