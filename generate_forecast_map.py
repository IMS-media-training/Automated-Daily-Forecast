"""
IMS Weather Forecast V2 - Map-Based Image Generator

Generates 1080x1920px Instagram story images with:
- Cyan-to-green gradient background
- Israel map overlay with geographic city positioning
- Weather icons and temperature data
- Hebrew text with RTL rendering
- IMS and MoT logos

Author: Automated Daily Forecast Team
Version: 2.0
"""

import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont

from utils import (
    setup_logging,
    OUTPUT_DIR,
    ISRAEL_MAP_PNG,
    IMS_LOGO_PNG,
    MOT_LOGO_PNG,
    NOTO_SANS_HEBREW_BLACK_COMPLETE,
    NOTO_SANS_HEBREW_VARIABLE,
    NOTO_SANS_HEBREW_BLACK,
    NOTO_SANS_HEBREW_SEMIBOLD,
    OPEN_SANS_FONT,
    WEATHER_ICONS_V2_DIR,
    ensure_directories
)
from city_coordinates import CITY_POSITIONS
from weather_icon_mapping import get_weather_icon_path

# Try to import bidi for RTL text rendering
try:
    from bidi.algorithm import get_display
    BIDI_AVAILABLE = True
except ImportError:
    BIDI_AVAILABLE = False


# ============================================================================
# CONSTANTS
# ============================================================================

# Canvas dimensions
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920

# Gradient definition (from Figma - Green-Blue 02)
# linear-gradient(346deg, #DCFF57 -62.6%, #22B2FF 112.14%)
GRADIENT_ANGLE = 346  # degrees (CSS convention: 0 = top, 90 = right)
GRADIENT_STOPS = [
    ((220, 255, 87), -62.6),    # #DCFF57 (Lime Yellow) at -62.6%
    ((34, 178, 255), 112.14)    # #22B2FF (Bright Blue) at 112.14%
]

# Text colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Header positioning
HEADER_Y_START = 57
HEADER_WIDTH = 1080
HEADER_SEPARATOR_Y = 135  # 57 + 36 (text height) + 40 (gap) + 2 (adjustment)
SEPARATOR_HEIGHT = 7

# Map positioning and dimensions (from Figma)
MAP_X = 258
MAP_Y = 288  # Figma shows 288.3, rounded to 288
MAP_WIDTH = 533  # Target width from Figma
MAP_HEIGHT = 1495  # Target height from Figma

# Weather Description positioning
DESCRIPTION_X = 100  # Left padding
DESCRIPTION_Y = 1550  # Below cities, above logos
DESCRIPTION_WIDTH = 880  # 1080 - (2 * 100 padding)
DESCRIPTION_FONT_SIZE = 22
DESCRIPTION_LINE_HEIGHT = 32  # Line spacing

# Logos positioning
LOGOS_X = 633
LOGOS_Y = 1709

# Phase 3 & 4: Text Styles from Figma
FONT_SIZE_HEADER = 36
FONT_WEIGHT_HEADER = 900  # Black
FONT_WIDTH_HEADER = 100   # Normal width

FONT_SIZE_CITY_NAME = 24
FONT_WEIGHT_CITY_NAME = 900  # Black
FONT_WIDTH_CITY_NAME = 100

FONT_SIZE_TEMP = 20
FONT_WEIGHT_TEMP = 600  # SemiBold
FONT_WIDTH_TEMP = 100

# Icon and Spacing from Figma
ICON_DISPLAY_SIZE = 50
CITY_ICON_TEXT_SPACING = 16
CITY_NAME_TEMP_SPACING = 4  # Natural text box padding

# City name mapping: XML names -> CITY_POSITIONS keys
CITY_NAME_MAPPING = {
    'Tel Aviv - Yafo': 'Tel Aviv',
    'Qazrin': 'Katzrin',
    'En Gedi': 'Ein Gedi',
    'Bet Shean': 'Beit Shean',
    'Elat': 'Eilat',
    'Mizpe Ramon': 'Mitzpe Ramon',
}


# ============================================================================
# PHASE 1: CANVAS & GRADIENT BACKGROUND
# ============================================================================

def create_css_linear_gradient(width: int, height: int,
                                angle: float,
                                color_stops: List[Tuple[Tuple[int, int, int], float]]) -> Image.Image:
    """
    Create a CSS-style linear gradient with arbitrary angle and color stops.

    Supports CSS-like syntax:
    - angle: degrees (0 = top, 90 = right, 180 = bottom, 270 = left)
    - color_stops: [(color_rgb, position_percent), ...] where position can be negative or >100%

    Example:
        create_css_linear_gradient(1080, 1920, 346, [
            ((220, 255, 87), -62.6),   # #DCFF57 at -62.6%
            ((34, 178, 255), 112.14)    # #22B2FF at 112.14%
        ])

    Args:
        width: Canvas width in pixels
        height: Canvas height in pixels
        angle: Gradient angle in degrees (CSS convention: 0deg = to top)
        color_stops: List of (RGB_tuple, position_percent) tuples

    Returns:
        PIL Image with gradient background
    """
    import math

    # Sort color stops by position
    sorted_stops = sorted(color_stops, key=lambda x: x[1])

    # Convert CSS angle to radians
    # CSS: 0deg = to top (↑), 90deg = to right (→)
    # We need to convert to standard math angles and adjust
    angle_rad = math.radians(90 - angle)  # Convert CSS to standard math angle

    # Calculate gradient direction vector
    dx = math.cos(angle_rad)
    dy = -math.sin(angle_rad)  # Negative because y increases downward

    # Canvas center
    cx, cy = width / 2, height / 2

    # Calculate the maximum distance from center to any corner
    # This determines the gradient line length
    corners = [
        (0, 0), (width, 0), (0, height), (width, height)
    ]
    max_dist = max(
        abs((x - cx) * dx + (y - cy) * dy)
        for x, y in corners
    )

    # Gradient line goes from -max_dist to +max_dist through center
    # Position 0% corresponds to -max_dist, 100% corresponds to +max_dist
    gradient_length = 2 * max_dist

    # Create image and calculate color for each pixel
    gradient = Image.new('RGB', (width, height))
    pixels = gradient.load()

    for y in range(height):
        for x in range(width):
            # Project pixel onto gradient line
            # Distance from center along gradient direction
            projection = (x - cx) * dx + (y - cy) * dy

            # Convert to percentage (-max_dist = 0%, +max_dist = 100%)
            if gradient_length > 0:
                position_percent = ((projection + max_dist) / gradient_length) * 100
            else:
                position_percent = 50  # Fallback

            # Find surrounding color stops and interpolate
            color = interpolate_color_stops(sorted_stops, position_percent)
            pixels[x, y] = color

    return gradient


def interpolate_color_stops(sorted_stops: List[Tuple[Tuple[int, int, int], float]],
                             position: float) -> Tuple[int, int, int]:
    """
    Interpolate color at a given position from sorted color stops.

    Args:
        sorted_stops: List of (RGB_tuple, position_percent) sorted by position
        position: Position percentage to get color for

    Returns:
        RGB tuple for the interpolated color
    """
    # Before first stop - use first color
    if position <= sorted_stops[0][1]:
        return sorted_stops[0][0]

    # After last stop - use last color
    if position >= sorted_stops[-1][1]:
        return sorted_stops[-1][0]

    # Find surrounding stops
    for i in range(len(sorted_stops) - 1):
        stop1_color, stop1_pos = sorted_stops[i]
        stop2_color, stop2_pos = sorted_stops[i + 1]

        if stop1_pos <= position <= stop2_pos:
            # Linear interpolation
            if stop2_pos == stop1_pos:
                factor = 0
            else:
                factor = (position - stop1_pos) / (stop2_pos - stop1_pos)

            r = int(stop1_color[0] * (1 - factor) + stop2_color[0] * factor)
            g = int(stop1_color[1] * (1 - factor) + stop2_color[1] * factor)
            b = int(stop1_color[2] * (1 - factor) + stop2_color[2] * factor)

            return (r, g, b)

    # Fallback (shouldn't reach here)
    return sorted_stops[-1][0]


def initialize_canvas(logger) -> Image.Image:
    """
    Initialize the canvas with CSS-style gradient background.

    Args:
        logger: Logger instance

    Returns:
        PIL Image with gradient background (RGBA mode)
    """
    logger.info(f"Initializing canvas ({CANVAS_WIDTH}x{CANVAS_HEIGHT}px)")

    # Create CSS-style gradient background
    logger.info(f"Creating gradient: {GRADIENT_ANGLE}deg with {len(GRADIENT_STOPS)} color stops")
    canvas = create_css_linear_gradient(
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        GRADIENT_ANGLE,
        GRADIENT_STOPS
    )

    # Convert to RGBA to support transparency overlays
    canvas = canvas.convert('RGBA')

    logger.info("Canvas initialized successfully")
    return canvas


# ============================================================================
# PHASE 2: MAP OVERLAY
# ============================================================================

def render_map_overlay(canvas: Image.Image, logger) -> None:
    """
    Load and composite Israel map onto canvas.
    Resizes the map to match Figma dimensions (533x1495px).

    Args:
        canvas: PIL Image to draw on
        logger: Logger instance
    """
    try:
        logger.info("Loading Israel map...")

        # Load the map image
        if not ISRAEL_MAP_PNG.exists():
            logger.error(f"Map file not found: {ISRAEL_MAP_PNG}")
            return

        map_img = Image.open(ISRAEL_MAP_PNG)
        original_size = map_img.size
        logger.info(f"Map loaded: {original_size[0]}x{original_size[1]}px, mode={map_img.mode}")

        # Convert to RGBA if not already (to support transparency)
        if map_img.mode != 'RGBA':
            map_img = map_img.convert('RGBA')

        # Resize map to match Figma dimensions
        map_img = map_img.resize((MAP_WIDTH, MAP_HEIGHT), Image.Resampling.LANCZOS)
        logger.info(f"Map resized to: {MAP_WIDTH}x{MAP_HEIGHT}px")

        # Composite the map onto the canvas at the specified position
        # Using the map's alpha channel for proper transparency blending
        canvas.paste(map_img, (MAP_X, MAP_Y), map_img)

        logger.info(f"Map positioned at ({MAP_X}, {MAP_Y})")

    except Exception as e:
        logger.error(f"Error rendering map overlay: {e}", exc_info=True)


def render_city_rtl(canvas: Image.Image, draw: ImageDraw.ImageDraw,
                    x: int, y: int, icon: Image.Image,
                    city_name: str, temp_text: str,
                    font_city: ImageFont.FreeTypeFont,
                    font_temp: ImageFont.FreeTypeFont, logger) -> None:
    """
    Render city with RTL layout: Icon left, text right.
    Used for coastal cities (Haifa, Tel Aviv, etc.)

    Layout: [ICON] --16px-- [CITY_NAME]
                             [TEMP]

    Args:
        canvas: PIL Image to composite icon onto
        draw: ImageDraw instance for text
        x, y: Center position (icon center for RTL)
        icon: Weather icon (50x50px RGBA)
        city_name: City name (already converted to RTL display)
        temp_text: Temperature string (e.g., "18°-28°")
        font_city: Font for city name
        font_temp: Font for temperature
        logger: Logger instance
    """
    # Position icon (x, y is icon center)
    icon_x = x - (ICON_DISPLAY_SIZE // 2)
    icon_y = y - (ICON_DISPLAY_SIZE // 2)
    canvas.paste(icon, (icon_x, icon_y), icon)

    # Text starts 16px to the right of icon center
    text_x = x + (ICON_DISPLAY_SIZE // 2) + CITY_ICON_TEXT_SPACING

    # Measure text heights for vertical centering
    city_bbox = draw.textbbox((0, 0), city_name, font=font_city)
    city_height = city_bbox[3] - city_bbox[1]

    temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
    temp_height = temp_bbox[3] - temp_bbox[1]

    # Total text block height (city + spacing + temp)
    total_text_height = city_height + CITY_NAME_TEMP_SPACING + temp_height

    # Center text block vertically with icon
    text_block_y = y - (total_text_height // 2)

    # Draw city name
    city_y = text_block_y
    draw.text((text_x, city_y), city_name, fill=COLOR_WHITE, font=font_city)

    # Draw temperature below city name
    temp_y = city_y + city_height + CITY_NAME_TEMP_SPACING
    draw.text((text_x, temp_y), temp_text, fill=COLOR_WHITE, font=font_temp)


def render_city_ttb(canvas: Image.Image, draw: ImageDraw.ImageDraw,
                    x: int, y: int, icon: Image.Image,
                    city_name: str, temp_text: str,
                    font_city: ImageFont.FreeTypeFont,
                    font_temp: ImageFont.FreeTypeFont, logger) -> None:
    """
    Render city with TTB layout: Icon top, text below.
    Used for inland cities (Afula, Lod, Beer Sheva, etc.)

    Layout:    [ICON]
            --16px--
           [CITY_NAME]
             [TEMP]

    Args:
        canvas: PIL Image to composite icon onto
        draw: ImageDraw instance for text
        x, y: Center position (icon center for TTB)
        icon: Weather icon (50x50px RGBA)
        city_name: City name (already converted to RTL display)
        temp_text: Temperature string (e.g., "18°-28°")
        font_city: Font for city name
        font_temp: Font for temperature
        logger: Logger instance
    """
    # Position icon (x, y is icon center)
    icon_x = x - (ICON_DISPLAY_SIZE // 2)
    icon_y = y - (ICON_DISPLAY_SIZE // 2)
    canvas.paste(icon, (icon_x, icon_y), icon)

    # Text starts 16px below icon center
    text_start_y = y + (ICON_DISPLAY_SIZE // 2) + CITY_ICON_TEXT_SPACING

    # Measure text dimensions for centering
    city_bbox = draw.textbbox((0, 0), city_name, font=font_city)
    city_width = city_bbox[2] - city_bbox[0]
    city_height = city_bbox[3] - city_bbox[1]

    temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
    temp_width = temp_bbox[2] - temp_bbox[0]
    temp_height = temp_bbox[3] - temp_bbox[1]

    # Center city name horizontally with icon
    city_x = x - (city_width // 2)
    city_y = text_start_y
    draw.text((city_x, city_y), city_name, fill=COLOR_WHITE, font=font_city)

    # Center temperature horizontally with icon
    temp_x = x - (temp_width // 2)
    temp_y = city_y + city_height + CITY_NAME_TEMP_SPACING
    draw.text((temp_x, temp_y), temp_text, fill=COLOR_WHITE, font=font_temp)


def render_city_ltr(canvas: Image.Image, draw: ImageDraw.ImageDraw,
                    x: int, y: int, icon: Image.Image,
                    city_name: str, temp_text: str,
                    font_city: ImageFont.FreeTypeFont,
                    font_temp: ImageFont.FreeTypeFont, logger) -> None:
    """
    Render city with LTR layout: Text left, icon right.
    Used for eastern cities (Ein Gedi)

    Layout: [CITY_NAME] --16px-- [ICON]
            [TEMP]

    Args:
        canvas: PIL Image to composite icon onto
        draw: ImageDraw instance for text
        x, y: Center position (icon center for LTR)
        icon: Weather icon (50x50px RGBA)
        city_name: City name (already converted to RTL display)
        temp_text: Temperature string (e.g., "18°-28°")
        font_city: Font for city name
        font_temp: Font for temperature
        logger: Logger instance
    """
    # Position icon (x, y is icon center)
    icon_x = x - (ICON_DISPLAY_SIZE // 2)
    icon_y = y - (ICON_DISPLAY_SIZE // 2)
    canvas.paste(icon, (icon_x, icon_y), icon)

    # Measure text dimensions
    city_bbox = draw.textbbox((0, 0), city_name, font=font_city)
    city_width = city_bbox[2] - city_bbox[0]
    city_height = city_bbox[3] - city_bbox[1]

    temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
    temp_width = temp_bbox[2] - temp_bbox[0]
    temp_height = temp_bbox[3] - temp_bbox[1]

    # Total text block height (city + spacing + temp)
    total_text_height = city_height + CITY_NAME_TEMP_SPACING + temp_height

    # Center text block vertically with icon
    text_block_y = y - (total_text_height // 2)

    # Text ends 16px to the left of icon center
    # Calculate text_x based on the widest text element
    max_text_width = max(city_width, temp_width)
    text_x = x - (ICON_DISPLAY_SIZE // 2) - CITY_ICON_TEXT_SPACING - max_text_width

    # Draw city name
    city_y = text_block_y
    # Right-align city name
    city_x = text_x + max_text_width - city_width
    draw.text((city_x, city_y), city_name, fill=COLOR_WHITE, font=font_city)

    # Draw temperature below city name
    temp_y = city_y + city_height + CITY_NAME_TEMP_SPACING
    # Right-align temperature
    temp_x = text_x + max_text_width - temp_width
    draw.text((temp_x, temp_y), temp_text, fill=COLOR_WHITE, font=font_temp)


def render_header(canvas: Image.Image, hebrew_date: str, logger) -> None:
    """
    Phase 3: Render header with Hebrew date and separator line.

    Args:
        canvas: PIL Image (RGBA mode) to draw on
        hebrew_date: Formatted date string (e.g., "04/12/2025 ג׳ בכסלו תשפ״ו")
        logger: Logger instance
    """
    try:
        logger.info("Rendering header...")

        # Load font - try static Black font first (has correct weight built-in + all glyphs)
        font = None
        font_errors = []

        # Priority 1: Try loading Noto Sans Hebrew Black (complete static font with all glyphs)
        if NOTO_SANS_HEBREW_BLACK_COMPLETE.exists():
            try:
                font = ImageFont.truetype(str(NOTO_SANS_HEBREW_BLACK_COMPLETE), FONT_SIZE_HEADER)
                logger.info("Font loaded: Noto Sans Hebrew Black (complete static, all glyphs)")
            except OSError as e:
                font_errors.append(f"Noto Sans Hebrew Black Complete: {e}")
                font = None

        # Priority 2: Try loading Noto Sans Hebrew Variable font
        if font is None and NOTO_SANS_HEBREW_VARIABLE.exists():
            try:
                font = ImageFont.truetype(str(NOTO_SANS_HEBREW_VARIABLE), FONT_SIZE_HEADER)
                logger.warning("Font loaded: Noto Sans Hebrew Variable (may have incorrect weight)")
            except OSError as e:
                font_errors.append(f"Noto Sans Hebrew Variable: {e}")
                font = None

        # Priority 3: Try loading Noto Sans Hebrew Black subset (Hebrew only, no numbers)
        if font is None and NOTO_SANS_HEBREW_BLACK.exists():
            try:
                font = ImageFont.truetype(str(NOTO_SANS_HEBREW_BLACK), FONT_SIZE_HEADER)
                logger.warning("Font loaded: Noto Sans Hebrew Black (static subset - no numbers)")
            except OSError as e:
                font_errors.append(f"Noto Sans Hebrew Black: {e}")
                font = None

        # Priority 4: Fallback to OpenSans
        if font is None and OPEN_SANS_FONT.exists():
            try:
                font = ImageFont.truetype(str(OPEN_SANS_FONT), FONT_SIZE_HEADER)
                logger.warning("Using OpenSans font as fallback")
            except OSError as e:
                font_errors.append(f"OpenSans: {e}")

        # If all fonts failed, skip header rendering
        if font is None:
            logger.error(f"Failed to load any font: {', '.join(font_errors)}")
            logger.warning("Header rendering skipped due to font loading errors")
            return

        # Process Hebrew text for RTL
        if BIDI_AVAILABLE:
            date_display = get_display(hebrew_date)
        else:
            logger.warning("bidi library not available, Hebrew may not render correctly")
            date_display = hebrew_date

        # Create draw instance
        draw = ImageDraw.Draw(canvas)

        # Calculate text dimensions
        bbox = draw.textbbox((0, 0), date_display, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position text (centered horizontally)
        text_x = (CANVAS_WIDTH - text_width) // 2
        text_y = HEADER_Y_START

        # Draw text with white color
        draw.text((text_x, text_y), date_display, fill=COLOR_WHITE, font=font)
        logger.info(f"Header date rendered at ({text_x}, {text_y}), size: {text_width}x{text_height}px")

        # Draw separator line with horizontal padding
        SEPARATOR_HORIZONTAL_PADDING = 100
        separator_x1 = SEPARATOR_HORIZONTAL_PADDING
        separator_x2 = CANVAS_WIDTH - SEPARATOR_HORIZONTAL_PADDING
        separator_y_top = HEADER_SEPARATOR_Y
        separator_y_bottom = HEADER_SEPARATOR_Y + SEPARATOR_HEIGHT

        draw.rectangle(
            [(separator_x1, separator_y_top), (separator_x2, separator_y_bottom)],
            fill=COLOR_WHITE
        )
        logger.info(f"Separator line rendered at y={separator_y_top}, x={separator_x1}-{separator_x2}, height={SEPARATOR_HEIGHT}px")

        logger.info("Header rendered successfully")

    except Exception as e:
        logger.error(f"Error rendering header: {e}", exc_info=True)
        logger.warning("Continuing with image generation despite header error")


def render_cities(canvas: Image.Image, cities: List[Dict], logger) -> None:
    """
    Phase 4: Render all cities with icons and temperature data.

    Supports three layout types:
    - RTL: Icon left, text right (coastal cities)
    - TTB: Icon top, text below (inland cities)
    - LTR: Text left, icon right (eastern cities)

    Args:
        canvas: PIL Image (RGBA mode) to draw on
        cities: List of city dictionaries with name, min_temp, max_temp, weather_code
        logger: Logger instance
    """
    try:
        logger.info(f"Rendering {len(cities)} cities...")

        # Load fonts for city names and temperatures
        font_city = None
        font_temp = None
        font_errors = []

        # Load city name font (24px, Black weight 900)
        if NOTO_SANS_HEBREW_BLACK_COMPLETE.exists():
            try:
                font_city = ImageFont.truetype(str(NOTO_SANS_HEBREW_BLACK_COMPLETE), FONT_SIZE_CITY_NAME)
                logger.info("City font loaded: Noto Sans Hebrew Black (complete)")
            except OSError as e:
                font_errors.append(f"City font (Black Complete): {e}")

        if font_city is None and NOTO_SANS_HEBREW_VARIABLE.exists():
            try:
                font_city = ImageFont.truetype(str(NOTO_SANS_HEBREW_VARIABLE), FONT_SIZE_CITY_NAME)
                logger.warning("City font loaded: Variable font (may need weight adjustment)")
            except OSError as e:
                font_errors.append(f"City font (Variable): {e}")

        # Load temperature font (20px, SemiBold weight 600)
        # IMPORTANT: Use Black Complete first because temperature needs NUMBERS (0-9°-)
        # SemiBold is Hebrew-only subset and doesn't have Latin digits
        if NOTO_SANS_HEBREW_BLACK_COMPLETE.exists():
            try:
                font_temp = ImageFont.truetype(str(NOTO_SANS_HEBREW_BLACK_COMPLETE), FONT_SIZE_TEMP)
                logger.info("Temperature font loaded: Noto Sans Hebrew Black (complete - has all glyphs including numbers)")
            except OSError as e:
                font_errors.append(f"Temp font (Black Complete): {e}")

        if font_temp is None and NOTO_SANS_HEBREW_VARIABLE.exists():
            try:
                font_temp = ImageFont.truetype(str(NOTO_SANS_HEBREW_VARIABLE), FONT_SIZE_TEMP)
                logger.info("Temperature font loaded: Variable font (fallback)")
            except OSError as e:
                font_errors.append(f"Temp font (Variable): {e}")

        # Fallback to OpenSans if needed
        if font_city is None and OPEN_SANS_FONT.exists():
            try:
                font_city = ImageFont.truetype(str(OPEN_SANS_FONT), FONT_SIZE_CITY_NAME)
                logger.warning("City font: Using OpenSans fallback")
            except OSError as e:
                font_errors.append(f"City font (OpenSans): {e}")

        if font_temp is None and OPEN_SANS_FONT.exists():
            try:
                font_temp = ImageFont.truetype(str(OPEN_SANS_FONT), FONT_SIZE_TEMP)
                logger.warning("Temp font: Using OpenSans fallback")
            except OSError as e:
                font_errors.append(f"Temp font (OpenSans): {e}")

        # Check if fonts loaded successfully
        if font_city is None or font_temp is None:
            logger.error(f"Failed to load fonts: {', '.join(font_errors)}")
            logger.warning("City rendering skipped due to font loading errors")
            return

        # Create draw instance
        draw = ImageDraw.Draw(canvas)

        # Render each city
        rendered_count = 0
        for city_data in cities:
            # Get city names (XML uses name_eng and name_heb)
            city_name_eng = city_data.get('name_eng', '')
            city_name_heb = city_data.get('name_heb', city_name_eng)

            # Apply name mapping for position lookup
            position_key = CITY_NAME_MAPPING.get(city_name_eng, city_name_eng)
            
            # Debug: Log mapping
            if position_key != city_name_eng:
                logger.debug(f"Mapped city '{city_name_eng}' -> '{position_key}'")

            # Check if city exists in position mapping
            if position_key not in CITY_POSITIONS:
                logger.warning(f"City '{city_name_eng}' (mapped to '{position_key}') not found in CITY_POSITIONS, skipping")
                continue

            position_data = CITY_POSITIONS[position_key]
            # Apply Map Offset (Coordinates are relative to the map, not the canvas)
            x = position_data['x'] + MAP_X
            y = position_data['y'] + MAP_Y
            layout = position_data['layout']

            # Get weather icon
            weather_code = city_data.get('weather_code', 1250)
            icon_path = get_weather_icon_path(weather_code)

            # Load and resize weather icon
            if not icon_path.exists():
                logger.warning(f"Icon not found for city '{city_name_eng}' (code {weather_code}): {icon_path}")
                continue

            try:
                icon = Image.open(icon_path)
                if icon.mode != 'RGBA':
                    icon = icon.convert('RGBA')
                icon = icon.resize((ICON_DISPLAY_SIZE, ICON_DISPLAY_SIZE), Image.Resampling.LANCZOS)
            except Exception as e:
                logger.error(f"Error loading icon for '{city_name_eng}': {e}")
                continue

            # Prepare text strings
            # Temperature format: "18°-28°" (min-max)
            temp_text = f"{city_data['min_temp']}°-{city_data['max_temp']}°"

            # Convert Hebrew city name to RTL display
            if BIDI_AVAILABLE:
                city_display = get_display(city_name_heb)
            else:
                city_display = city_name_heb

            # Measure text dimensions
            city_bbox = draw.textbbox((0, 0), city_display, font=font_city)
            city_text_width = city_bbox[2] - city_bbox[0]
            city_text_height = city_bbox[3] - city_bbox[1]

            temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
            temp_text_width = temp_bbox[2] - temp_bbox[0]
            temp_text_height = temp_bbox[3] - temp_bbox[1]

            # Debug: Log city rendering details
            logger.info(f"Rendering '{city_name_eng}' at ({x}, {y}) with layout={layout}")

            # Render based on layout type
            if layout == 'RTL':
                render_city_rtl(canvas, draw, x, y, icon,
                              city_display, temp_text,
                              font_city, font_temp, logger)
            elif layout == 'TTB':
                render_city_ttb(canvas, draw, x, y, icon,
                              city_display, temp_text,
                              font_city, font_temp, logger)
            elif layout == 'LTR':
                render_city_ltr(canvas, draw, x, y, icon,
                              city_display, temp_text,
                              font_city, font_temp, logger)
            else:
                logger.warning(f"Unknown layout type '{layout}' for city '{city_name_eng}'")
                continue

            rendered_count += 1

        logger.info(f"Cities rendered successfully: {rendered_count}/{len(cities)}")

    except Exception as e:
        logger.error(f"Error rendering cities: {e}", exc_info=True)
        logger.warning("Continuing with image generation despite cities error")


def render_description(canvas: Image.Image, description: str, logger) -> None:
    """
    Phase 5: Render weather description text with RTL support and text wrapping.

    Args:
        canvas: PIL Image (RGBA mode) to draw on
        description: Hebrew weather description text
        logger: Logger instance
    """
    try:
        # Skip if no description
        if not description or description.strip() == "":
            logger.info("No weather description to render, skipping")
            return

        logger.info("Rendering weather description...")

        # Load font for description (Regular or Medium weight)
        font = None
        font_errors = []

        # Try Noto Sans Hebrew Variable first (can set to lower weight)
        if NOTO_SANS_HEBREW_VARIABLE.exists():
            try:
                font = ImageFont.truetype(str(NOTO_SANS_HEBREW_VARIABLE), DESCRIPTION_FONT_SIZE)
                logger.info("Description font loaded: Noto Sans Hebrew Variable")
            except OSError as e:
                font_errors.append(f"Variable font: {e}")

        # Fallback to Black Complete
        if font is None and NOTO_SANS_HEBREW_BLACK_COMPLETE.exists():
            try:
                font = ImageFont.truetype(str(NOTO_SANS_HEBREW_BLACK_COMPLETE), DESCRIPTION_FONT_SIZE)
                logger.info("Description font loaded: Noto Sans Hebrew Black (fallback)")
            except OSError as e:
                font_errors.append(f"Black Complete: {e}")

        # Fallback to OpenSans
        if font is None and OPEN_SANS_FONT.exists():
            try:
                font = ImageFont.truetype(str(OPEN_SANS_FONT), DESCRIPTION_FONT_SIZE)
                logger.warning("Description font: Using OpenSans fallback")
            except OSError as e:
                font_errors.append(f"OpenSans: {e}")

        if font is None:
            logger.error(f"Failed to load description font: {', '.join(font_errors)}")
            return

        # Create draw instance
        draw = ImageDraw.Draw(canvas)

        # Wrap text to fit within DESCRIPTION_WIDTH
        lines = wrap_hebrew_text(description, font, DESCRIPTION_WIDTH, draw)
        logger.info(f"Description wrapped into {len(lines)} lines")

        # Calculate starting Y position (centered in available space)
        total_text_height = len(lines) * DESCRIPTION_LINE_HEIGHT
        current_y = DESCRIPTION_Y

        # Draw each line with RTL rendering
        for line in lines:
            # Convert to RTL display
            if BIDI_AVAILABLE:
                line_display = get_display(line)
            else:
                line_display = line

            # Measure line width for right alignment
            bbox = draw.textbbox((0, 0), line_display, font=font)
            line_width = bbox[2] - bbox[0]

            # Right-align text (typical for Hebrew)
            text_x = DESCRIPTION_X + DESCRIPTION_WIDTH - line_width

            # Draw the line
            draw.text((text_x, current_y), line_display, fill=COLOR_WHITE, font=font)
            current_y += DESCRIPTION_LINE_HEIGHT

        logger.info(f"Weather description rendered at ({DESCRIPTION_X}, {DESCRIPTION_Y})")

    except Exception as e:
        logger.error(f"Error rendering description: {e}", exc_info=True)
        logger.warning("Continuing with image generation despite description error")


def wrap_hebrew_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """
    Wrap Hebrew text to fit within a maximum width.

    Args:
        text: Hebrew text to wrap
        font: Font to use for measuring
        max_width: Maximum width in pixels
        draw: ImageDraw instance for text measurement

    Returns:
        List of text lines that fit within max_width
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        # Try adding word to current line
        test_line = ' '.join(current_line + [word])

        # Measure width (with RTL conversion if available)
        if BIDI_AVAILABLE:
            test_display = get_display(test_line)
        else:
            test_display = test_line

        bbox = draw.textbbox((0, 0), test_display, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            # Word fits, add it to current line
            current_line.append(word)
        else:
            # Word doesn't fit, start new line
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Single word is too long, add it anyway
                lines.append(word)

    # Add remaining words
    if current_line:
        lines.append(' '.join(current_line))

    return lines


def render_logos(canvas: Image.Image, logger) -> None:
    """
    Phase 6: Render IMS and Ministry of Transport logos.

    Args:
        canvas: PIL Image (RGBA mode) to draw on
        logger: Logger instance
    """
    try:
        logger.info("Rendering logos...")

        # Define logo dimensions and spacing
        LOGO_HEIGHT = 80  # Target height for logos
        LOGO_SPACING = 40  # Horizontal spacing between logos

        logos_to_render = []

        # Load IMS logo (or placeholder)
        if IMS_LOGO_PNG.exists():
            try:
                ims_logo = Image.open(IMS_LOGO_PNG)
                if ims_logo.mode != 'RGBA':
                    ims_logo = ims_logo.convert('RGBA')

                # Scale to target height
                aspect_ratio = ims_logo.width / ims_logo.height
                new_width = int(LOGO_HEIGHT * aspect_ratio)
                ims_logo = ims_logo.resize((new_width, LOGO_HEIGHT), Image.Resampling.LANCZOS)
                logos_to_render.append(('IMS', ims_logo))
                logger.info(f"IMS logo loaded: {new_width}x{LOGO_HEIGHT}px")
            except Exception as e:
                logger.error(f"Error loading IMS logo: {e}")
                # Placeholder for failed load
                ims_ph = Image.new('RGBA', (100, LOGO_HEIGHT), (200, 200, 200, 255))
                draw_ph = ImageDraw.Draw(ims_ph)
                draw_ph.rectangle([0, 0, 99, LOGO_HEIGHT-1], outline=COLOR_BLACK)
                draw_ph.text((10, 30), "IMS", fill=COLOR_BLACK)
                logos_to_render.append(('IMS_PH', ims_ph))
        else:
            logger.warning(f"IMS logo not found: {IMS_LOGO_PNG}")
            # Placeholder for missing file
            ims_ph = Image.new('RGBA', (100, LOGO_HEIGHT), (200, 200, 200, 255))
            draw_ph = ImageDraw.Draw(ims_ph)
            draw_ph.rectangle([0, 0, 99, LOGO_HEIGHT-1], outline=COLOR_BLACK)
            draw_ph.text((10, 30), "IMS", fill=COLOR_BLACK)
            logos_to_render.append(('IMS_PH', ims_ph))

        # Load Ministry of Transport logo (or placeholder)
        if MOT_LOGO_PNG.exists():
            try:
                mot_logo = Image.open(MOT_LOGO_PNG)
                if mot_logo.mode != 'RGBA':
                    mot_logo = mot_logo.convert('RGBA')

                # Scale to target height
                aspect_ratio = mot_logo.width / mot_logo.height
                new_width = int(LOGO_HEIGHT * aspect_ratio)
                mot_logo = mot_logo.resize((new_width, LOGO_HEIGHT), Image.Resampling.LANCZOS)
                logos_to_render.append(('MoT', mot_logo))
                logger.info(f"MoT logo loaded: {new_width}x{LOGO_HEIGHT}px")
            except Exception as e:
                logger.error(f"Error loading MoT logo: {e}")
                # Placeholder
                mot_ph = Image.new('RGBA', (100, LOGO_HEIGHT), (200, 200, 200, 255))
                draw_ph = ImageDraw.Draw(mot_ph)
                draw_ph.rectangle([0, 0, 99, LOGO_HEIGHT-1], outline=COLOR_BLACK)
                draw_ph.text((10, 30), "MoT", fill=COLOR_BLACK)
                logos_to_render.append(('MoT_PH', mot_ph))
        else:
            logger.warning(f"MoT logo not found: {MOT_LOGO_PNG}")
            # Placeholder
            mot_ph = Image.new('RGBA', (100, LOGO_HEIGHT), (200, 200, 200, 255))
            draw_ph = ImageDraw.Draw(mot_ph)
            draw_ph.rectangle([0, 0, 99, LOGO_HEIGHT-1], outline=COLOR_BLACK)
            draw_ph.text((10, 30), "MoT", fill=COLOR_BLACK)
            logos_to_render.append(('MoT_PH', mot_ph))

        # Calculate total width of logo row
        if not logos_to_render:
            logger.warning("No logos to render")
            return

        total_width = sum(logo[1].width for logo in logos_to_render)
        total_width += LOGO_SPACING * (len(logos_to_render) - 1)

        # Center logos horizontally on canvas
        current_x = (CANVAS_WIDTH - total_width) // 2
        logo_y = LOGOS_Y

        # Render each logo
        for name, logo in logos_to_render:
            canvas.paste(logo, (current_x, logo_y), logo)
            logger.info(f"{name} logo positioned at ({current_x}, {logo_y})")
            current_x += logo.width + LOGO_SPACING

        logger.info("Logos rendered successfully")

    except Exception as e:
        logger.error(f"Error rendering logos: {e}", exc_info=True)
        logger.warning("Continuing with image generation despite logos error")


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_forecast_map(forecast_data: Dict, output_path: Path, logger) -> bool:
    """
    Generate complete forecast map image from forecast data.

    Args:
        forecast_data: Dictionary with 'cities', 'description', 'date', 'hebrew_date'
        output_path: Path where to save the output image
        logger: Logger instance

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting V2 Map-Based Image Generation")
        logger.info("=" * 60)

        # Phase 1: Initialize canvas with gradient
        canvas = initialize_canvas(logger)

        # Phase 2: Map overlay
        render_map_overlay(canvas, logger)

        # Phase 3: Header
        render_header(canvas, forecast_data['hebrew_date'], logger)

        # Phase 4: Cities
        render_cities(canvas, forecast_data['cities'], logger)

        # Phase 5: Description
        render_description(canvas, forecast_data.get('description', ''), logger)

        # Phase 6: Logos
        render_logos(canvas, logger)

        # Save the image
        logger.info(f"Saving image to: {output_path}")
        canvas.save(output_path, 'PNG', quality=95)
        logger.info("Image saved successfully")

        logger.info("=" * 60)
        logger.info("V2 Image Generation Complete!")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error(f"Error generating forecast map: {e}", exc_info=True)
        return False


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Generate V2 map-based forecast image'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Date in YYYY-MM-DD format (default: today)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: output/forecast_map_{date}.png)'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    # Ensure directories exist
    ensure_directories()

    # Load actual forecast data from extract_forecast.py
    from extract_forecast import extract_forecast
    from datetime import datetime

    date_str = args.date if args.date else None

    logger.info("Extracting forecast data...")
    forecast_data = extract_forecast(target_date=date_str, logger=logger)

    if forecast_data is None:
        logger.error("Failed to extract forecast data")
        exit(1)

    date_str = forecast_data['date']

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = OUTPUT_DIR / f'forecast_map_{date_str}.png'

    # Generate the image
    success = generate_forecast_map(forecast_data, output_path, logger)

    if success:
        logger.info(f"\n✓ Image generated: {output_path}")
    else:
        logger.error("\n✗ Image generation failed")
        exit(1)


if __name__ == '__main__':
    main()
