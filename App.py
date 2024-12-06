import schedule
import time
from win10toast_click import ToastNotifier
import salat
import datetime as dt
import pytz
import geocoder

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
    while True:
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
def CalculateTimes(): 
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
        print(y)
        times.append(y)

    return names, times


# Main function that combines everything
def main():

    namesX, timesX = CalculateTimes()

    ScheduleAlarms(namesX, timesX)

    runSchedule()
    


if __name__ == "__main__":
    print("Running...")
    main()
