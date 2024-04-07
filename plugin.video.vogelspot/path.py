import os
import var

StreamsUrl = 'https://raw.githubusercontent.com/dumbie/kodirepo/master/plugin.video.vogelspot/streams/streams.js'
ImageUrl = 'https://raw.githubusercontent.com/dumbie/kodirepo/master/plugin.video.vogelspot/streams/'

def addon(fileName):
    return os.path.join(var.addonpath, fileName)

def addonstorage(fileName):
    return os.path.join(var.addonstorage, fileName)
