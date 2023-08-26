from datetime import datetime, timedelta
import func
import xbmcgui
import path
import var

def list_load(listContainer):
    #Sort alarms by upcoming time
    var.AlarmDataJson.sort(key=lambda x: x['starttime'], reverse=False)

    for alarm in var.AlarmDataJson:
        try:
            ExternalId = alarm['externalid']
            #ChannelName = alarm['channelname']
            ProgramName = alarm['programname']
            ProgramTimeStart = alarm['starttime']

            ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
            ProgramDescription = 'Om ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            listitem = xbmcgui.ListItem()
            listitem.setProperty('ProgramTimeStart', ProgramTimeStart)
            listitem.setProperty('ProgramName', ProgramName)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.addItem(listitem)
        except:
            continue
