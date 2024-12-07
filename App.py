import schedule
import time
from win10toast_click import ToastNotifier
import salat
import datetime as dt
import pytz
import geocoder
import pystray
import PIL.Image
import threading
import sys

running = True

#Exit
def exitApplication(icon=None, item=None):
    global running
    running = False  # Stop the schedule loop
    print("Exiting application...")
    if icon:  # Stop the tray icon if running
        icon.stop()
    sys.exit(0)  # Exit the program


# Show the notification
def showToast(titleX, messageX):
    ToastNotifier().show_toast(title=titleX, msg=messageX, threaded=True)


# Schedule alarms
def ScheduleAlarms(names, times):
    schedule.every().day.at(times[0]).do(lambda : showToast(names[0], f"go pray {names[0]}"))
    schedule.every().day.at(times[1]).do(lambda : showToast(names[1], f"go pray {names[1]}"))
    schedule.every().day.at(times[2]).do(lambda : showToast(names[2], f"go pray {names[2]}"))
    schedule.every().day.at(times[3]).do(lambda : showToast(names[3], f"go pray {names[3]}"))
    schedule.every().day.at(times[4]).do(lambda : showToast(names[4], f"go pray {names[4]}"))
    schedule.every().day.at(times[5]).do(lambda : showToast(names[5], f"go pray {names[5]}"))


# Run the scheduled tasks
def runSchedule():
    global running
    while running:
        schedule.run_pending()  # Run any scheduled tasks
        time.sleep(1)


# TODO: make latitude and longitude save on device for offline usage
# Get Latitude and Longitude from IP
def getLocation():
    currentLocation = geocoder.ip("me")
    if currentLocation.latlng:
        latitude, longitude = currentLocation.latlng
        return latitude, longitude
    else:
        print("Failed to retrieve current location")


# Calculate prayer times
def calculateTimes(): 
    prayerTimes = salat.PrayerTimes(salat.CalculationMethod.KARACHI, salat.AsrMethod.STANDARD)
    latitude, longitude = getLocation()
    date = dt.date.today()
    timezone = pytz.timezone("Asia/Amman")

    prayerTimes = prayerTimes.calc_times(date, timezone, longitude, latitude)

    names = list(prayerTimes.keys())

    times = []
    notFormattedTimes = list(prayerTimes.values())

    for time in notFormattedTimes:
        y = time.strftime("%H:%M")
        times.append(y)

    return names, times


# Tray Icon Buttons functions
def onClick(icon, item):
    if str(item) == "Not so secret":
        print("I use arch btw")
    else :
        print("To Be implemented")

#
def runTrayIcon():
    image = PIL.Image.open("assets/PrayerTimes.png")
    icon = pystray.Icon(
        "PrayerTimes",
        image,
        menu=pystray.Menu(
            pystray.MenuItem("Not so secret", onClick),
            pystray.MenuItem("Quit", exitApplication),
        ),
    )

    # Run the tray icon
    icon.run()


# Main function that combines everything
def main():

    namesX, timesX = calculateTimes()

    ScheduleAlarms(namesX, timesX)

    tray_thread = threading.Thread(target=runTrayIcon, daemon=True)
    tray_thread.start()

    runSchedule()

    try:
        runSchedule()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected.")
        exitApplication()


if __name__ == "__main__":
    print("Running...")
    main()
