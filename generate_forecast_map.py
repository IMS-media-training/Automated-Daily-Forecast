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
from PIL import Image, ImageFont

from utils import (
    setup_logging,
    OUTPUT_DIR,
    ISRAEL_MAP_PNG,
    IMS_LOGO_PNG,
    MOT_LOGO_PNG,
    NOTO_SANS_HEBREW_FONT,
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

# Logos positioning
LOGOS_X = 633
LOGOS_Y = 1709


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


def render_header(canvas: Image.Image, hebrew_date: str, logger) -> None:
    """Phase 3: Render header with Hebrew date and separator line."""
    pass


def render_cities(canvas: Image.Image, cities: List[Dict], logger) -> None:
    """Phase 4: Render all cities with icons and temperature data."""
    pass


def render_description(canvas: Image.Image, description: str, logger) -> None:
    """Phase 5: Render weather description text."""
    pass


def render_logos(canvas: Image.Image, logger) -> None:
    """Phase 6: Render IMS and MoT logos."""
    pass


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

        # Phase 3: Header (TODO)
        # render_header(canvas, forecast_data['hebrew_date'], logger)

        # Phase 4: Cities (TODO)
        # render_cities(canvas, forecast_data['cities'], logger)

        # Phase 5: Description (TODO)
        # render_description(canvas, forecast_data['description'], logger)

        # Phase 6: Logos (TODO)
        # render_logos(canvas, logger)

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

    # TODO: Load actual forecast data from extract_forecast.py
    # For now, create minimal test data
    from datetime import datetime
    date_str = args.date if args.date else datetime.now().strftime('%Y-%m-%d')

    test_data = {
        'date': date_str,
        'hebrew_date': '03/12/2025 ג׳ בכסלו תשפ״ו',
        'description': 'מעונן חלקית',
        'cities': []
    }

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = OUTPUT_DIR / f'forecast_map_{date_str}.png'

    # Generate the image
    success = generate_forecast_map(test_data, output_path, logger)

    if success:
        logger.info(f"\n✓ Image generated: {output_path}")
    else:
        logger.error("\n✗ Image generation failed")
        exit(1)


if __name__ == '__main__':
    main()
