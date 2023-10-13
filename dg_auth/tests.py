from django.test import TestCase
import time
import re

# Create your tests here.
def setFormatDate():
    today = time.gmtime(time.time())
    next = time.gmtime(time.time() + 31556926)
    todayFormat = time.strftime("%Y-%m-%d %H:%M:%S", today)
    nextFormat = time.strftime("%Y-%m-%d %H:%M:%S", next)

    print(todayFormat, nextFormat)

def getData():
    appData = f'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"'
    appDataSplit = appData.split(";")
    app = appDataSplit[0].replace('"', "")
    app_version = re.findall(r'\d+', appDataSplit[1])
    print(app_version, appDataSplit[1])
    
getData()