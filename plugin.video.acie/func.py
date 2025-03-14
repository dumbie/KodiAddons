import var
import files
import hybrid
import os

#Check user folders
def check_user_folders():
    files.createDirectory(var.addonstorageuser)

#Get addon path
def path_addon(fileName):
    return os.path.join(var.addonpath, fileName)

#Generate addon url
def generate_addon_url(**kwargs):
    return var.LaunchUrl + "?" + hybrid.urlencode(kwargs)