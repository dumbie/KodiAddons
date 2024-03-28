import alarmfunc
import func
import lifunc
import path
import var

def list_load_combined(listContainer=None, forceLoad=False):
    try:
        #Load set program alarms
        alarmfunc.alarm_json_load(forceLoad)

        #Add items to sort list
        listContainerSort = []
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStart'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
    for alarm in var.AlarmDataJson:
        try:
            ExternalId = alarm['externalid']
            ProgramName = alarm['programname']
            ProgramTimeStart = alarm['starttime']

            ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
            ProgramDescription = '[COLOR FF888888]Om[/COLOR] ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' [COLOR FF888888]op[/COLOR] ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            #Set item icons
            iconDefault = path.icon_television(ExternalId)
            iconFanart = path.icon_fanart()

            #Set item details
            jsonItem = {
                'ProgramTimeStart': ProgramTimeStart,
                'ProgramName': ProgramName,
                'ProgramDescription': ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDescription, 'Tagline': ProgramDescription, 'Title': ProgramName},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault, 'fanart': iconFanart},
                'ItemAction': 'alarm_remove'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
