import var

def openFile(filePath):
    try:
        fileread = open(filePath, 'rb')
        content = fileread.read()  
        fileread.close()
        return content
    except:
        return None
