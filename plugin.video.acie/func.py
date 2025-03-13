import var
import files
import hybrid

#Check user folders
def check_user_folders():
    files.createDirectory(var.addonstorageuser)

#Generate addon url
def generate_addon_url(**kwargs):
    return var.LaunchUrl + "?" + hybrid.urlencode(kwargs)