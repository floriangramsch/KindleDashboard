from wetterdienst import Settings
from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest
# import polars as pl
from datetime import datetime, timedelta, timezone


# def pretty_print_forecast(df: pl.DataFrame) -> None:
#     """Schön formatierte Wettervorhersage."""
#     # Label- und Einheiten-Mapping (ShortCodes, in Upper-Case)
#     labels = {
#         "TTT": ("Temperatur", "°C"),
#         "RR1C": ("Regen (1 h, korr.)", "mm"),
#         "RR3C": ("Regen (3 h), korr.", "mm"),
#         "wwP": ("Regenwahrscheinlichkeit", "%"),
#         "ww": ("Wetter", ""),
#     }

#     labels.update({
#         "temperature_air_mean_2m": ("Temperatur", "°C"),
#         "total_precipitation_last_1h": ("Regen (1 h)", "mm"),
#         "total_precipitation_last_3h": ("Regen (3 h)", "mm"),
#         "probability_precipitation_last_1h": ("Regenwahrscheinlichkeit", "%"),
#         "weather_significant": ("Wetter", ""),
#     })

#     # Wettercode → Emoji + Beschreibung
#     weather_symbols = {
#         0: "☀️ Wolkenlos",
#         1: "🌤️ Leicht bewölkt",
#         2: "🌥️ Wolkig",
#         3: "☁️ Stark bewölkt bis bedeckt",
#         45: "🌫️ Nebel",
#         48: "🌫️ Nebel mit Reifbildung",
#         51: "🌧️ Leichter Sprühregen",
#         53: "🌧️ Mäßiger Sprühregen",
#         55: "🌧️ Starker Sprühregen",
#         56: "🧊 Leichter gefrierender Sprühregen",
#         57: "🧊 Mäßiger/starker gefrierender Sprühregen",
#         61: "🌧️ Leichter Regen",
#         63: "🌧️ Mäßiger Regen",
#         65: "🌧️ Starker Regen",
#         66: "🧊 Leichter gefrierender Regen",
#         67: "🧊 Mäßiger/starker gefrierender Regen",
#         71: "🌨️ Leichter Schneefall",
#         73: "🌨️ Mäßiger Schneefall",
#         75: "🌨️ Starker Schneefall",
#         77: "❄️ Schneegriesel",
#         80: "🌦️ Leichter Regenschauer",
#         81: "🌦️ Mäßiger/starker Regenschauer",
#         82: "🌧️ Sehr starker Regenschauer",
#         85: "🌨️ Leichter Schneeschauer",
#         86: "🌨️ Mäßiger/starker Schneeschauer",
#         95: "⛈️ Gewitter (leicht/mäßig, ohne Graupel/Hagel)",
#         96: "⛈️ Starkes Gewitter (ohne/mit leichtem Graupel/Hagel)",
#         99: "⛈️ Starkes Gewitter mit Graupel oder Hagel",
#     }

#     # Sortieren & Runden
#     df = df.sort("date").with_columns(pl.col("value").round(1))
#     grouped = df.group_by("date", maintain_order=True).agg(
#         [pl.col("parameter"), pl.col("value")]
#     )

#     print("\n🌦️ Wettervorhersage:\n")
#     for row in grouped.iter_rows(named=True):
#         print(f"🕒 {row['date'].strftime('%Y-%m-%d %H:%M')}")
#         for param, val in zip(row["parameter"], row["value"]):
#             key = param.upper()               # Normiere
#             label, unit = labels.get(key, (key, ""))
#             if key == "WW":
#                 symbol = weather_symbols.get(int(val), f"Code {int(val)}")
#                 print(f"   • {label}: {symbol}")
#             elif key == "WWP":
#                 perc = val * 100
#                 print(f"   • {label}: {perc:.1f}{unit}")
#                 # print(f"   • {label}: {int(val)}{unit}")
#             else:
#                 print(f"   • {label}: {val} {unit}")
#         print("-" * 32)


def mosmix():
    """MOSMIX-Vorhersage abrufen und schön ausgeben."""
    settings = Settings(
        ts_shape="long",
        ts_humanize=False,      # Humanize aus, um bei ShortCodes zu bleiben
        ts_convert_units=True,
    )

    now = datetime.now(timezone.utc)
    later = now + timedelta(hours=6)

    request = DwdMosmixRequest(
        parameters=[
            ("hourly", "large", "TTT"),   # Temperatur
            ("hourly", "large", "RR1C"),   # Regenmenge 1 h (Forecast t−1…t)
            ("hourly", "large", "RR3C"),   # Regenmenge 3 h
            ("hourly", "large", "wwP"),   # Regen-Wahrscheinlichkeit (%)
            ("hourly", "large", "ww"),    # Wetterzustandscode
        ],
        start_date=now,
        end_date=later,
        settings=settings,
    )

    stations = request.filter_by_rank(
        latlon=(49.995757, 8.228819),  # Mainz
        rank=1
    )

    responses = list(stations.values.query())
    if not responses:
        print("Keine Daten gefunden.")
        return

    return responses[0].df


if __name__ == "__main__":
    data = mosmix()
    # pretty_print_forecast(data)
