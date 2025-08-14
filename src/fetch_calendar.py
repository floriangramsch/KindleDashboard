from caldav import DAVClient
from datetime import datetime, time, timedelta
import os


def fetch_calendar():
    print(
        f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Fetching calender...")
    client = DAVClient(
        'https://cloud.floxsite.de/remote.php/dav/calendars/flo/')
    client.username = os.environ.get('NC_USERNAME')
    client.password = os.environ.get('NC_PASSWORD')

    principal = client.principal()
    calendars = principal.calendars()
    # for calendar in principal.calendars():
    #     print("📅", calendar.name, calendar.url)
    start = datetime.combine(datetime.today(), time.min)
    end = datetime.combine(datetime.today() + timedelta(days=7), time.max)

    events = {}
    calendar_names = list(map(lambda x: x.name, calendars))
    flonja_index = calendar_names.index("Flonja")

    for calendar in [calendars[flonja_index]]:
        todos = calendar.todos()
        calendar_event = calendar.search(start=start, end=end)

        if calendar.name not in events:
            events[calendar.name] = {
                'events': [],
                'todos': []
            }

        for todo_obj in todos:
            vtodo = todo_obj.vobject_instance.vtodo
            summary = getattr(vtodo, 'summary', None)
            due = getattr(vtodo, 'due', None)

            summary_text = summary.value if summary else "Kein Titel"
            due_str = due.value.strftime(
                '(%d.%m)') if due else ""

            events[calendar.name]['todos'].append(
                f"[ ] {summary_text} {due_str}")

        for event in calendar_event:
            vevent = event.vobject_instance
            if vevent is None:
                continue

            summary = vevent.vevent.summary.value
            start_dt = vevent.vevent.dtstart.value

            events[calendar.name]['events'].append(
                f"{start_dt.strftime('%A')} - {summary}")
            # f"{start_dt.strftime('%m-%d %H:%M')} - {summary}")

    # for cal_name, data in events.items():
    #     print(f"📅 {cal_name}")
    #     print("  Events:")
    #     for e in data['events']:
    #         print(f"    - {e}")
    #     print("  ToDos:")
    #     for t in data['todos']:
    #         print(f"    - {t}")
    #     print()

    return events


if __name__ == "__main__":
    print("TEST")
    from dotenv import load_dotenv

    load_dotenv()
    events = fetch_calendar()
    print(events)
