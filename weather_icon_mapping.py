"""
Weather icon mapping for V2.
Maps IMS weather codes to V2 icon filenames.

Based on actual XML data analysis:
- Primary codes: 1250 (Clear), 1220 (Partly Cloudy)
- Additional codes mapped for completeness
"""

from pathlib import Path


# Base path to weather icons
WEATHER_ICONS_V2_DIR = Path(__file__).parent / "assets" / "weather_icons_v2"

# Map IMS weather codes to V2 icon filenames (after renaming)
WEATHER_CODE_TO_ICON_V2 = {
    # Core codes (seen in actual data)
    1250: "clear.png",                    # Clear/Sunny
    1220: "partly_cloudy.png",            # Partly Cloudy

    # Extended codes (for future/seasonal variations)
    1230: "cloudy.png",                   # Cloudy
    1260: "mostly_clear.png",             # Mostly Clear
    1270: "mostly_cloudy.png",            # Mostly Cloudy

    # Rain
    1530: "partly_cloudy_rain.png",       # Partly Cloudy + Rain
    1140: "rainy.png",                    # Rainy
    1540: "heavy_rain.png",               # Heavy Rain

    # Thunderstorms
    1020: "thunderstorm.png",             # Thunderstorms
    1010: "thunderstorm_dry.png",         # Dry Thunderstorm

    # Snow/Frost
    1060: "snow.png",                     # Snow
    1300: "frost.png",                    # Frost

    # Fog
    1160: "cloudy.png",                   # Fog (use cloudy icon)

    # Extreme Heat
    1580: "very_hot.png",                 # Very Hot
    1590: "hot.png",                      # Hot/Muggy

    # Wind
    1570: "windy.png",                    # Windy/Storm
}


def get_weather_icon_path(weather_code: int) -> Path:
    """
    Get the full path to a weather icon for a given IMS code.

    Args:
        weather_code: IMS weather code (int)

    Returns:
        Path to the icon file (defaults to clear.png if code not found)
    """
    icon_filename = WEATHER_CODE_TO_ICON_V2.get(
        weather_code,
        "clear.png"  # Default to clear/sunny
    )
    return WEATHER_ICONS_V2_DIR / icon_filename
