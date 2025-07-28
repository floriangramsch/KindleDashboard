from PIL import Image, ImageDraw, ImageFont
from fetch_calendar import fetch_calendar
from datetime import datetime


def create_dashboard():
    print("Creating Dashboard...")
    # Bildgröße Kindle Paperwhite 7. Gen: 1072 x 1448 px
    # 'L' = 8-bit Graustufen, weißer Hintergrund
    img = Image.new('L', (1072, 1448), color=255)
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
    y += 100
    events = fetch_calendar()

    for cal_name, data in events.items():
        # draw.text((padding, y), f"{cal_name}:", font=font_subtitle, fill=0)
        # y += 40

        draw.text((padding + 20, y), "Events:", font=font_text, fill=0)
        y += 60
        for e in data['events']:
            draw.text((padding + 40, y), e, font=font_text, fill=0)
            y += 50

        y += 60
        draw.text((padding + 20, y), "ToDos:", font=font_text, fill=0)
        y += 60
        for t in data['todos']:
            draw.text((padding + 40, y), t, font=font_text, fill=0)
            y += 50

        # y += 40  # Abstand zu nächstem Kalender

    current_time = datetime.now().strftime("%H:%M %d.%m")
    draw.text((padding, 1400),
              f"Zuletzt geupdatet: {current_time}", font=font_subtitle, fill=0)
    # Datei speichern
    img.save("public/kindle_dashboard.png")
