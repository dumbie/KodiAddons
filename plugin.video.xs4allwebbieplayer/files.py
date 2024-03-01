import os
import shutil
import var

def listFilesUser():
    return listFiles(var.addonstorage)

def listFiles(dirPath):
    try:
        return [x for x in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, x))]
    except:
        return []

def listDirectoriesUser():
    return listDirectories(var.addonstorage)

def listDirectories(dirPath):
    try:
        return [x for x in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, x))]
    except:
        return []

def saveFileUser(fileName, fileContent):
    return saveFile(os.path.join(var.addonstorage, fileName), fileContent)

def saveFile(filePath, fileContent):
    try:
        fileWrite = open(filePath, 'wb')
        fileWrite.write(fileContent)
        fileWrite.close()
        return True
    except:
        return False

def openFileUser(fileName):
    return openFile(os.path.join(var.addonstorage, fileName))

def openFile(filePath):
    try:
        fileRead = open(filePath, 'rb')
        fileContent = fileRead.read()
        fileRead.close()
        return fileContent
    except:
        return None

def copyFileUser(fileName, destinationName):
    return copyFile(os.path.join(var.addonstorage, fileName), os.path.join(var.addonstorage, destinationName))

def copyFile(filePath, destinationPath):
    try:
        shutil.copy(filePath, destinationPath)
        return True
    except:
        return False

def existFileUser(fileName):
    return existFile(os.path.join(var.addonstorage, fileName))

def existFile(filePath):
    try:
        return os.path.isfile(filePath)
    except:
        return False

def existDirectoryUser(dirName):
    return existDirectory(os.path.join(var.addonstorage, dirName))

def existDirectory(dirPath):
    try:
        return os.path.isdir(dirPath)
    except:
        return False

def sizeFileUser(fileName):
    return sizeFile(os.path.join(var.addonstorage, fileName))

def sizeFile(filePath):
    try:
        return os.path.getsize(filePath)
    except:
        return False

def removeFileUser(fileName):
    return removeFile(os.path.join(var.addonstorage, fileName))

def removeFile(filePath):
    try:
        os.remove(filePath)
        return True
    except:
        return False

def removeDirectoryUser(dirName):
    return removeDirectory(os.path.join(var.addonstorage, dirName))

def removeDirectory(dirPath):
    try:
        shutil.rmtree(dirPath, ignore_errors=True)
        return True
    except:
        return False

def createDirectoryUser(dirName):
    return createDirectory(os.path.join(var.addonstorage, dirName))

def createDirectory(dirPath):
    try:
        os.mkdir(dirPath)
        return True
    except:
        return False
