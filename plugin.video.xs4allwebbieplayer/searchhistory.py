import json
import files
import func

def search_history_search_json_load():
    try:
        return json.loads(files.openFileUser('SearchHistorySearch.js'))
    except:
        return []

def search_history_channel_json_load():
    try:
        return json.loads(files.openFileUser('SearchHistoryChannel.js'))
    except:
        return []

def search_history_radio_json_load():
    try:
        return json.loads(files.openFileUser('SearchHistoryRadio.js'))
    except:
        return []

def search_history_add(searchTerm, searchJsonFileName):
    #Check search term
    if func.string_isnullorempty(searchTerm) == True:
        return

    #Remove search term from Json
    search_history_remove(searchTerm, searchJsonFileName)

    #Set Json target list variable
    if searchJsonFileName == 'SearchHistoryChannel.js':
        searchHistoryJson = search_history_channel_json_load()
    elif searchJsonFileName == 'SearchHistoryRadio.js':
        searchHistoryJson = search_history_radio_json_load()
    elif searchJsonFileName == 'SearchHistorySearch.js':
        searchHistoryJson = search_history_search_json_load()
    else:
        return

    #Add search history to Json
    searchHistoryJson.insert(0, searchTerm)

    #Trim search history length
    if len(searchHistoryJson) > 40:
        searchHistoryJson = searchHistoryJson[:40]

    #Save json data to storage
    JsonDumpBytes = json.dumps(searchHistoryJson).encode('ascii')
    files.saveFileUser(searchJsonFileName, JsonDumpBytes)

def search_history_remove(searchTerm, searchJsonFileName):
    #Set Json target list variable
    if searchJsonFileName == 'SearchHistoryChannel.js':
        searchHistoryJson = search_history_channel_json_load()
    elif searchJsonFileName == 'SearchHistoryRadio.js':
        searchHistoryJson = search_history_radio_json_load()
    elif searchJsonFileName == 'SearchHistorySearch.js':
        searchHistoryJson = search_history_search_json_load()
    else:
        return

    #Remove search term from Json
    for search in searchHistoryJson:
        try:
            if search == searchTerm:
                searchHistoryJson.remove(search)
        except:
            continue

    #Save json data to storage
    JsonDumpBytes = json.dumps(searchHistoryJson).encode('ascii')
    files.saveFileUser(searchJsonFileName, JsonDumpBytes)
