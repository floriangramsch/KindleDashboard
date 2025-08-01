from PIL import Image, ImageDraw, ImageFont
from fetch_calendar import fetch_calendar
from datetime import datetime


def create_dashboard():
    w, h = 1072, 1448
    # Bildgröße Kindle Paperwhite 7. Gen: 1072 x 1448 px
    # 'L' = 8-bit Graustufen, weißer Hintergrund
    img = Image.new('L', (w, h), color=255)
    draw = ImageDraw.Draw(img)

    # Schrift laden
    # Pfad anpassen oder Systemschrift verwenden
    # font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"  # mac
    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # linux
    font_path = "fonts/HackNerdFont-Regular.ttf"
    emoji_font_path = "fonts/NotoEmoji-VariableFont_wght.ttf"
    font_title = ImageFont.truetype(font_path, 72)
    font_emoji = ImageFont.truetype(emoji_font_path, 72)
    font_subtitle = ImageFont.truetype(font_path, 28)
    font_text = ImageFont.truetype(font_path, 48)

    y = 30
    padding = 20

    draw.text((padding, y), "📅 ", font=font_emoji, fill=0)
    draw.text((padding+100, y), "Kalender & ToDos", font=font_title, fill=0)

    y += 72+10
    draw.text((padding, y), "Ich liebe Se Bebi <3",
              font=ImageFont.truetype(font_path, 62), fill=0)
    y += 100
    events = fetch_calendar()

    for cal_name, data in events.items():
        # draw.text((padding, y), f"{cal_name}:", font=font_subtitle, fill=0)
        # y += 40

        # todos
        draw.text((padding + 20, y), "ToDos:", font=font_text, fill=0)
        y += 60
        if len(data['todos']) == 0:
            draw.text((padding + 40, y), "Einfach alles erledigt <3",
                      font=font_text, fill=0)
        else:
            for t in data['todos']:
                draw.text((padding + 40, y), t, font=font_text, fill=0)
                y += 50

        # events
        y = h // 2
        draw.text((padding + 20, y), "Events:", font=font_text, fill=0)
        y += 60
        if len(data['events']) == 0:
            draw.text((padding + 40, y), "Momentan nichts zu tun <3",
                      font=font_text, fill=0)
        else:
            for e in data['events']:
                draw.text((padding + 40, y), e, font=font_text, fill=0)
                y += 50

        y += 40  # Abstand zu nächstem Kalender

    current_time = datetime.now().strftime("%d.%m %H:%M")
    draw.text((padding, 1400),
              f"Zuletzt geupdatet: {current_time}", font=font_subtitle, fill=0)
    # Datei speichern
    img.save("public/kindle_dashboard.png")


create_dashboard()
