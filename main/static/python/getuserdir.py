import os 
from django.conf import settings
def getlines(id, username):
    timelinelength = 0
    try:
        USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
        finaldir = os.path.join(USER_DIR, username)
        testname = "test" + str(id)
        finaldir2 = os.path.join(finaldir, testname)
        histdir = os.path.join(finaldir2, 'history')
        onlyfiles = [f for f in os.listdir(histdir) if os.path.isfile(os.path.join(histdir, f))]
        timelinelength = len(onlyfiles) - 1
        with open(os.path.join(finaldir2, 'main.py'), "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = "The coding file could not be found, backend error"
    
    return timelinelength, lines

def gethistory(username, id, value):
    timelinelength = 0
    try:
        USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
        finaldir = os.path.join(USER_DIR, username)
        finaldir2 = os.path.join(finaldir, 'test' + str(id))
        historydir = os.path.join(finaldir2, 'history')
        onlyfiles = [f for f in os.listdir(historydir) if os.path.isfile(os.path.join(historydir, f))]
        timelinelength = len(onlyfiles)
        historylist = []
        for i in range(timelinelength):
            with open(os.path.join(historydir, onlyfiles[i]), "r") as f:
                lines = f.readlines()
            historylist.append(lines)
        

        codeline = ''.join(historylist[int(value)])

    except FileNotFoundError:
        codeline = "The coding file could not be found, backend error"
    
    return codeline

        