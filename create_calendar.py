from icalendar import Calendar, Event
import datetime
import os
from pathlib import Path
import json

def create_calendar(calendars, names, details):
    cal = Calendar()

    for c, calendy in enumerate(calendars):
        calendy = calendy.replace("\'", "\"")
        calendy = json.loads(calendy)
        frequency = calendy['Frequency']
        times = calendy['Times']
        today = datetime.date.today()
        day = int(today.strftime("%d"))
        month = int(today.strftime("%m"))
        year = int(today.strftime("%y"))

        name = names[c]
        detail = details[c]

        for i in range(day, 28, frequency):
            for time in times:
                event = Event()
                event.add('summary', name)
                event.add('description', detail)
                event.add('dtstart', datetime.datetime(year, month, i, time, 0))
                event.add('dtend', datetime.datetime(year, month, i, time, 30))

                # Adding events to calendar
                cal.add_component(event)

    try:
        directory = str(Path(__file__).parent.parent) + "/prescription-manager-and-reminder/static/uploads/"
        f = open(os.path.join(directory, 'example.ics'), 'wb')
    except:
        f = open(os.path.join('static/uploads/example.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()