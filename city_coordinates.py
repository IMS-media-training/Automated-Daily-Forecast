"""
City positioning for V2 map-based layout.
Coordinates are manually defined from Figma design.
"""

from typing import TypedDict


class CityPosition(TypedDict):
    """Type definition for city position data."""
    x: int
    y: int
    layout: str  # 'RTL', 'TTB', or 'LTR'


# City positions on 1080x1920 canvas
# Coordinates from Figma Story-Layout-V2.0 design
CITY_POSITIONS: dict[str, CityPosition] = {
    'Zefat': {'x': 335, 'y': 19, 'layout': 'RTL'},
    'Nazareth': {'x': 424, 'y': 180, 'layout': 'RTL'},
    'Katzrin': {'x': 681, 'y': 170, 'layout': 'TTB'},
    'Tiberias': {'x': 588, 'y': 331, 'layout': 'RTL'},
    'Haifa': {'x': 159, 'y': 224, 'layout': 'RTL'},
    'Afula': {'x': 424, 'y': 289, 'layout': 'TTB'},
    'Tel Aviv': {'x': 99, 'y': 421, 'layout': 'RTL'},
    'Lod': {'x': 337, 'y': 457, 'layout': 'TTB'},
    'Beit Shean': {'x': 574, 'y': 490, 'layout': 'TTB'},
    'Ashdod': {'x': 75, 'y': 567, 'layout': 'RTL'},
    'Jerusalem': {'x': 328, 'y': 623, 'layout': 'RTL'},
    'Ein Gedi': {'x': 571, 'y': 702, 'layout': 'LTR'},
    'Beer Sheva': {'x': 300, 'y': 738, 'layout': 'TTB'},
    'Mitzpe Ramon': {'x': 265, 'y': 981, 'layout': 'TTB'},
    'Eilat': {'x': 315, 'y': 1260, 'layout': 'TTB'},
}

# Layout type meanings:
# RTL (Right-to-Left): Icon left, text right - for coastal cities
# TTB (Top-to-Bottom): Icon top, text below - for inland cities
# LTR (Left-to-Right): Text left, icon right - for eastern cities
