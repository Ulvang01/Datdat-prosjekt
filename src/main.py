from datetime import datetime as time

def printTime():
    now = time.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

printTime()