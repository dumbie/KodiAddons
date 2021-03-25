import os
import var

def addon(fileName):
    return os.path.join(var.addonpath, fileName)

def addonstorage(fileName):
    return os.path.join(var.addonstorage, fileName)
