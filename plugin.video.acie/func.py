import var
import files
import hybrid
import os
import sys

#Check user folders
def check_user_folders():
    files.createDirectory(var.addonstorageuser)

#Get addon path
def path_addon(fileName):
    return os.path.join(var.addonpath, fileName)

#Generate addon url
def generate_addon_url(**kwargs):
    LaunchUrl = str(sys.argv[0])
    return LaunchUrl + "?" + hybrid.urlencode(kwargs)

#Check if string is empty
def string_isnullorempty(string):
    if string and string.strip():
        return False
    else:
        return True