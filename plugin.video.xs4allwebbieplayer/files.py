import os
import shutil
import var

def saveFile(fileName, content):
    try:
        filepath = os.path.join(var.addonstorage, fileName)
        filewrite = open(filepath, 'wb')
        filewrite.write(content)  
        filewrite.close()
    except:
        pass

def openFile(fileName):
    try:
        filepath = os.path.join(var.addonstorage, fileName)
        fileread = open(filepath, 'rb')
        content = fileread.read()  
        fileread.close()
        return content
    except:
        pass

def copyFile(fileName, destinationName):
    try:
        shutil.copy(fileName, destinationName)
    except:
        pass

def existFile(fileName):
    try:
        filepath = os.path.join(var.addonstorage, fileName)
        return os.path.isfile(filepath)
    except:
        return False

def sizeFile(fileName):
    try:
        filepath = os.path.join(var.addonstorage, fileName)
        return os.path.getsize(filepath)
    except:
        return False

def removeFileUser(fileName):
    try:
        filepath = os.path.join(var.addonstorage, fileName)
        os.remove(filepath)
        return True
    except:
        return False

def removeFile(fileName):
    try:
        os.remove(fileName)
        return True
    except:
        return False

def removeDirectoryUser(dirName):
    try:
        filepath = os.path.join(var.addonstorage, dirName)
        shutil.rmtree(filepath, ignore_errors=True)
        return True
    except:
        return False

def removeDirectory(dirName):
    try:
        shutil.rmtree(dirName, ignore_errors=True)
        return True
    except:
        return False

def createDirectoryUser(dirName):
    try:
        filepath = os.path.join(var.addonstorage, dirName)
        os.mkdir(filepath)
        return True
    except:
        return False

def createDirectory(dirName):
    try:
        os.mkdir(dirName)
        return True
    except:
        return False
