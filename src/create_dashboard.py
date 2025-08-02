from PIL import Image, ImageDraw, ImageFont
from fetch_calendar import fetch_calendar
from fetch_weather import mosmix
from datetime import datetime


class Dashboard():
    def __init__(self):
        # self.font_title = ImageFont.truetype(font_path, 72)
        self.font_title = self.create_font(72)
        # self.font_emoji = ImageFont.truetype(emoji_font_path, 72)
        self.font_emoji = self.create_font(72, True)
        # self.font_subtitle = ImageFont.truetype(font_path, 28)
        self.font_subtitle = self.create_font(28)
        # self.font_text = ImageFont.truetype(font_path, 48)
        self.font_text = self.create_font(48)

        calender = fetch_calendar()['Flonja']
        self.todos = calender['todos']
        self.events = calender['events']
        self.weather_df = mosmix()

        # Bildgröße Kindle Paperwhite 7. Gen: 1072 x 1448 px
        # 'L' = 8-bit Graustufen, weißer Hintergrund
        self.w, self.h = 1072, 1448
        self.img = Image.new('L', (self.w, self.h), color=255)
        self.draw = ImageDraw.Draw(self.img)

    def create_font(self, size: int, emoji: bool = False):
        font_path = "fonts/HackNerdFont-Regular.ttf"
        emoji_font_path = "fonts/NotoEmoji-VariableFont_wght.ttf"

        if emoji:
            return ImageFont.truetype(emoji_font_path, size)
        else:
            return ImageFont.truetype(font_path, size)

    def draw_todos(self, x, y):
        # todos
        self.draw.text((x + 20, y), "ToDos:", font=self.font_text, fill=0)
        y += 60
        if len(self.todos) == 0:
            self.draw.text((x + 40, y), "Einfach alles erledigt <3",
                           font=self.font_text, fill=0)
        else:
            for t in self.todos:
                self.draw.text((x + 40, y), t, font=self.font_text, fill=0)
                y += 50

    def draw_events(self, x, y):
        # events
        self.draw.text((x + 20, y), "Events:", font=self.font_text, fill=0)
        y += 60
        if len(self.events) == 0:
            self.draw.text((x + 40, y), "Momentan nichts zu tun <3",
                           font=self.font_text, fill=0)
        else:
            for e in self.events:
                self.draw.text((x + 40, y), e, font=self.font_text, fill=0)
                y += 50

    def draw_weather(self, x, y):
        default_y = y
        weather_by_time = {}
        for row in self.weather_df.iter_rows(named=True):
            dt = row["date"].strftime("%H:%M")
            if dt not in weather_by_time:
                weather_by_time[dt] = {}
            weather_by_time[dt][row["parameter"].upper()] = row["value"]

        line_break = False

        # Nur die nächsten 3 Stunden anzeigen
        for (time_str, params) in list(weather_by_time.items())[1:4]:
            self.draw.text((x, y),
                           f"{time_str}", font=self.font_subtitle, fill=0)
            y += 40

            if "WW" in params:
                try:
                    ww = int(params["WW"])
                    weather_labels = {
                        0: ["🌞", "Klarer Himmel"],
                        1: ["🌤️", "Ein paar Wolken"],
                        2: ["⛅", "Wolkig"],
                        3: ["☁️", "Bedeckt"],
                        45: ["🌫️", "Leichter Nebel"],
                        48: ["🌫️", "Dichter Nebel"],
                        51: ["🌦️", "Leichter Sprühregen"],
                        53: ["🌦️", "Sprühregen"],
                        55: ["🌧️", "Starker Sprühregen"],
                        56: ["🧊", "Leichter gefrierender Sprühregen"],
                        57: ["🧊", "Starker gefrierender Sprühregen"],
                        61: ["🌦️", "Leichter Regen"],
                        63: ["🌧️", "Regen"],
                        65: ["🌧️", "Starker Regen"],
                        66: ["🧊", "Leichter gefrierender Regen"],
                        67: ["🧊", "Starker gefrierender Regen"],
                        71: ["🌨️", "Leichter Schneefall"],
                        73: ["🌨️", "Schneefall"],
                        75: ["❄️", "Starker Schneefall"],
                        77: ["❄️", "Schneegriesel"],
                        80: ["🌦️", "Leichter Schauer"],
                        81: ["🌦️", "Schauer"],
                        82: ["🌧️", "Starker Schauer"],
                        85: ["🌨️", "Leichter Schneeschauer"],
                        86: ["🌨️", "Schneeschauer"],
                        95: ["⛈️", "Gewitter"],
                        96: ["⛈️", "Starkes Gewitter"],
                        99: ["⛈️", "Heftiges Gewitter"],
                    }
                    label = weather_labels.get(ww, f"Code {ww}")
                    self.draw.text((x+100, y-60),
                                   f"{label[0]}", font=self.create_font(48, True), fill=0)

                    if len(label[1]) > 16:
                        self.draw.text((x, y),
                                       f"{label[1][:16]}-", font=self.create_font(30), fill=0)
                        self.draw.text((x, y+50),
                                       f"{label[1][16:]}", font=self.create_font(30), fill=0)

                        line_break = True
                    else:
                        self.draw.text((x, y),
                                       f"{label[1]}", font=self.create_font(30), fill=0)

                    y += 100 if line_break else 50

                except:
                    pass

            if "TTT" in params:
                self.draw.text((x, y),
                               f"{params['TTT']} °C", font=self.font_text, fill=0)
                y += 50

            if "RR1C" in params:
                self.draw.text((x, y),
                               f"{params['RR1C']} mm", font=self.font_text, fill=0)
                y += 50

            if "WWP" in params:
                perc = float(params["WWP"]) * 100
                self.draw.text((x, y),
                               f"{perc:.1f} %", font=self.font_text, fill=0)
                y += 50

            x += 1/3 * self.w
            y = default_y

    def draw_footer(self, x, y):
        current_time = datetime.now().strftime("%d.%m %H:%M")
        self.draw.text(
            (x, y), f"Zuletzt geupdatet: {current_time}", font=self.font_subtitle, fill=0)

    def draw_header(self, x, y):
        self.draw.text((x, y), "📅 ",
                       font=self.font_emoji, fill=0)
        self.draw.text((x+100, y), "Kalender & ToDos",
                       font=self.font_title, fill=0)

        y += 72+10
        self.draw.text((x, y), "Ich liebe Se Bebi <3",
                       font=self.create_font(62), fill=0)

    def create_dashboard(self):
        y = 30
        x = 20

        self.draw_header(x, y)
        y += 200

        # self.draw.text((x, y), "Test", font=self.font_text)

        # for cal_name, data in self.events.items():
        self.draw_weather(x, y)
        self.draw_todos(x, self.h // 3 + 50)
        self.draw_events(x,  (3*self.h) // 4)
        self.draw_footer(x, 1400)

        # Datei speichern
        self.img.save("public/kindle_dashboard.png")


dashboard = Dashboard()
dashboard.create_dashboard()
