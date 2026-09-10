from Tools.Calandar_tools import find_calendar_event,reschedule_calendar_event,cancel_calendar_event


def main():

    result = find_calendar_event.invoke({
    "title": "Project consultation",
    "date": "2026-09-10",
    "time": "18:30",
    "timezone": "Africa/Casablanca",
    })

    print(result)
    event_id = result["events"][0]["event_id"]
    result = cancel_calendar_event.invoke({
    "event_id": event_id
    })

    print(result)


if __name__ == "__main__":
    main()