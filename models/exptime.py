from datetime import timedelta, datetime

from werkzeug.local import F

now = datetime.now()
tM = timedelta(minutes=5)
td = timedelta(minutes=1)
tNotf = timedelta(days=3)

def getExpTime():
    return  now + tM

def checkExpTime(tm):
    if str(now) <= str(tm):
        return True
    else:
        return False

def getMvExpTime():
    return  now + td

def getUserNotExpTime():
    return  now + tNotf

def checkUserNotExpTime(notificationTime):
    if str(now) <= str(notificationTime):
        return True
    else:
        return False

print(getExpTime())
''' 
print(getUserNotExpTime())
print(checkUserNotExpTime('2022-01-02 21:22:44.330410')) '''