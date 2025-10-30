"""
IMS Weather Forecast Automation - Phase 3: All 15 Cities Image Generation

Generates single Instagram story image featuring all 15 Israeli cities with:
- Fredoka variable font (configurable weight/width axes)
- iOS-style weather icon PNGs
- Header with IMS logo and forecast date
- Hebrew RTL text support
- Vertical city rows with line separators
"""

from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display # For RTL text handling
from PIL import features # To check for Raqm support


# ============================================================================
# CONFIGURATION - Easy to modify design parameters
# ============================================================================

# --- FOR TESTING HEBREW RENDERING ---
# Set to True to simulate an environment WITH libraqm support.
# Set to False to simulate an environment WITHOUT libraqm support.
# Set to None for automatic detection (production mode).
TEST_MODE_FORCE_RAQM = None

# Image dimensions (Instagram story format)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# Font Configuration (Open Sans Variable Font)
# Weight axis: 300 (Light) to 800 (ExtraBold)
# Width axis: 75 (Condensed) to 100 (Normal)
FONT_WEIGHT_CITY = 600      # SemiBold for city name
FONT_WIDTH_CITY = 100       # Normal width
FONT_SIZE_CITY = 40         # City name font size (reduced for spacious layout)

FONT_WEIGHT_TEMP = 500      # Medium for temperature
FONT_WIDTH_TEMP = 100       # Normal width
FONT_SIZE_TEMP = 35         # Temperature font size (reduced for spacious layout)

FONT_WEIGHT_DATE = 400      # Regular for date
FONT_WIDTH_DATE = 100       # Normal width
FONT_SIZE_DATE = 50         # Date font size

# Header Configuration
HEADER_HEIGHT = 180         # White header section height
LOGO_HEIGHT = 120           # IMS logo display height
LOGO_MARGIN_TOP = 30        # Logo top margin

# City Row Configuration
BOTTOM_PADDING = 160        # Bottom padding for breathing room
ROW_HEIGHT = 105            # Height per city row (1580px ÷ 15 cities, accounting for bottom padding)
ICON_SIZE = 65              # Weather icon size
ROW_PADDING = 160           # Horizontal padding for breathing room (left/right margins)
ELEMENT_SPACING = 40        # Spacing between icon, temp, and city name
SEPARATOR_COLOR = (255, 255, 255, 50)  # Semi-transparent white line

# Colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (100, 100, 100)
COLOR_SKY_LIGHT = (135, 206, 250)  # Light sky blue for gradient top

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
FONT_DIR = BASE_DIR / "fonts"
ASSETS_DIR = BASE_DIR / "assets"

# Font file (variable font)
FONT_VARIABLE = FONT_DIR / "OpenSans-Variable.ttf"

# Asset paths
LOGO_PATH = ASSETS_DIR / "logos" / "IMS_logo.png"
WEATHER_ICONS_DIR = ASSETS_DIR / "weather_icons"

# Weather Code to Icon Mapping
WEATHER_ICONS = {
    '1250': 'sunny.png',          # Clear/Sunny
    '1220': 'partly_cloudy.png',  # Partly Cloudy
    '1310': 'mostly_clear.png',   # Mostly Clear
    '1580': 'very_hot.png',       # Very Hot/Sunny
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_font_with_variation(size: int, weight: int, width: int) -> ImageFont.FreeTypeFont:
    """
    Load Open Sans variable font with specific weight and width axes.

    Args:
        size: Font size in pixels
        weight: Weight axis value (300-800)
        width: Width axis value (75-100)

    Returns:
        Configured font object
    """
    font = ImageFont.truetype(str(FONT_VARIABLE), size)
    # Set variable font axes: Open Sans has 'wdth' (width) and 'wght' (weight)
    # The axes list order is determined by the font file's fvar table
    font.set_variation_by_axes([width, weight])
    return font


def render_hebrew_text(text: str) -> str:
    """
    Convert Hebrew text to proper RTL display format if Pillow lacks Raqm support.

    Args:
        text: Hebrew text string

    Returns:
        RTL-formatted text ready for rendering
    """
    has_raqm = features.check('raqm')
    if TEST_MODE_FORCE_RAQM is not None:
        has_raqm = TEST_MODE_FORCE_RAQM

    # If Pillow is built with Raqm support, it can handle RTL rendering itself.
    # We just need to pass `direction='rtl'` to the draw.text() call.
    if has_raqm:
        print("  (Hebrew Rendering: Using Pillow's Raqm support)")
        return text
    # Otherwise, we manually shape the text for older/basic Pillow installations.
    print("  (Hebrew Rendering: Using python-bidi fallback)")
    return get_display(text)


def load_weather_icon(weather_code: str, size: int) -> Image.Image:
    """
    Load weather icon PNG for the given weather code.

    Args:
        weather_code: Weather code from XML
        size: Target size for the icon

    Returns:
        PIL Image of weather icon, resized to specified size
    """
    # Get icon filename from mapping, with fallback
    icon_filename = WEATHER_ICONS.get(weather_code, 'mostly_clear.png')
    icon_path = WEATHER_ICONS_DIR / icon_filename

    try:
        icon = Image.open(icon_path).convert('RGBA')
        # Resize to specified size with high-quality resampling
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        return icon
    except Exception as e:
        print(f"  Warning: Could not load icon {icon_filename}: {e}")
        # Return a blank placeholder if icon fails to load
        return Image.new('RGBA', (size, size), (0, 0, 0, 0))


def load_logo() -> Image.Image:
    """
    Load IMS logo PNG.

    Returns:
        PIL Image of logo, resized to fit header
    """
    try:
        logo = Image.open(LOGO_PATH).convert('RGBA')

        # Calculate proportional width based on LOGO_HEIGHT
        aspect_ratio = logo.width / logo.height
        new_width = int(LOGO_HEIGHT * aspect_ratio)

        # Resize logo maintaining aspect ratio
        logo = logo.resize((new_width, LOGO_HEIGHT), Image.Resampling.LANCZOS)
        return logo
    except Exception as e:
        print(f"  Warning: Could not load logo: {e}")
        # Return a small placeholder
        return Image.new('RGBA', (LOGO_HEIGHT, LOGO_HEIGHT), (200, 200, 200, 255))


def format_forecast_date(date_str: str) -> str:
    """
    Format forecast date as DD/MM/YYYY.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Formatted date string DD/MM/YYYY
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except:
        # Fallback to original string if parsing fails
        return date_str


# ============================================================================
# IMAGE GENERATION FUNCTIONS
# ============================================================================

def create_gradient_background(width: int, height: int, header_height: int) -> Image.Image:
    """
    Create image with white header and gradient background.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        header_height: Height of white header section

    Returns:
        PIL Image with header and gradient background
    """
    # Create blank image
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Draw white header
    draw.rectangle([(0, 0), (width, header_height)], fill=COLOR_WHITE)

    # Draw vertical gradient below header (sky blue to white)
    for y in range(header_height, height):
        # Calculate color interpolation (0.0 at header_height, 1.0 at bottom)
        ratio = (y - header_height) / (height - header_height)
        r = int(COLOR_SKY_LIGHT[0] + (COLOR_WHITE[0] - COLOR_SKY_LIGHT[0]) * ratio)
        g = int(COLOR_SKY_LIGHT[1] + (COLOR_WHITE[1] - COLOR_SKY_LIGHT[1]) * ratio)
        b = int(COLOR_SKY_LIGHT[2] + (COLOR_WHITE[2] - COLOR_SKY_LIGHT[2]) * ratio)

        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return image


def add_header_content(image: Image.Image, date_str: str) -> None:
    """
    Add logo and date to header section of image.

    Args:
        image: PIL Image object to modify
        date_str: Forecast date string (YYYY-MM-DD)
    """
    # Load and paste logo (aligned with main list left edge)
    logo = load_logo()
    logo_x = ROW_PADDING  # Align with main list padding
    logo_y = LOGO_MARGIN_TOP
    image.paste(logo, (logo_x, logo_y), logo)  # Use logo as mask for transparency

    # Add date text (right side of header, aligned with main list right edge)
    draw = ImageDraw.Draw(image)
    date_font = load_font_with_variation(FONT_SIZE_DATE, FONT_WEIGHT_DATE, FONT_WIDTH_DATE)

    formatted_date = format_forecast_date(date_str)

    # Get text dimensions for right-alignment
    bbox = draw.textbbox((0, 0), formatted_date, font=date_font)
    text_width = bbox[2] - bbox[0]

    # Position date on right side aligned with main list padding
    date_x = IMAGE_WIDTH - text_width - ROW_PADDING  # Align with main list padding
    date_y = (HEADER_HEIGHT - (bbox[3] - bbox[1])) // 2  # Vertically center in header

    draw.text((date_x, date_y), formatted_date, fill=COLOR_BLACK, font=date_font)


def draw_city_row(image: Image.Image, draw: ImageDraw.Draw, city_data: dict,
                  y_position: int, font_city: ImageFont.FreeTypeFont,
                  font_temp: ImageFont.FreeTypeFont, is_last_row: bool = False) -> None:
    """
    Draw a single city row with Hebrew name, weather icon, and temperature.

    Layout (left to right): [Weather Icon] | [Temperature Range] | [Hebrew City Name]

    Args:
        image: PIL Image object to modify
        draw: ImageDraw object for drawing
        city_data: Dictionary with city forecast data
        y_position: Top Y coordinate of this row
        font_city: Font for city name
        font_temp: Font for temperature
        is_last_row: If True, don't draw separator line below
    """
    # Prepare text content
    city_name_heb = city_data['name_heb']
    city_name_display = render_hebrew_text(city_name_heb)

    temp_min = city_data['min_temp']
    temp_max = city_data['max_temp']
    temp_text = f"{temp_min}-{temp_max}°C"

    weather_code = city_data['weather_code']

    # Calculate vertical center of row
    row_center_y = y_position + (ROW_HEIGHT // 2)

    # Position 1: Weather Icon (left side)
    icon = load_weather_icon(weather_code, ICON_SIZE)
    icon_x = ROW_PADDING  # Left alignment at padding boundary
    icon_y = row_center_y - (ICON_SIZE // 2)  # Vertically centered in row

    # Paste icon with transparency
    image.paste(icon, (icon_x, icon_y), icon)

    # Position 2: Temperature (after icon)
    temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
    temp_text_width = temp_bbox[2] - temp_bbox[0]
    temp_text_height = temp_bbox[3] - temp_bbox[1]

    temp_x = icon_x + ICON_SIZE + ELEMENT_SPACING  # After icon with spacing
    temp_y = row_center_y - (temp_text_height // 2)

    draw.text((temp_x, temp_y), temp_text, fill=COLOR_GRAY, font=font_temp)

    # Position 3: Hebrew City Name (right side)
    # Get text dimensions for proper positioning
    city_bbox = draw.textbbox((0, 0), city_name_display, font=font_city)
    city_text_width = city_bbox[2] - city_bbox[0]
    city_text_height = city_bbox[3] - city_bbox[1]

    city_x = IMAGE_WIDTH - ROW_PADDING - city_text_width  # Right alignment with padding
    city_y = row_center_y - (city_text_height // 2)

    # Conditionally add `direction='rtl'` only if Raqm support is available
    has_raqm = features.check('raqm')
    if TEST_MODE_FORCE_RAQM is not None:
        has_raqm = TEST_MODE_FORCE_RAQM

    if has_raqm:
        draw.text((city_x, city_y), city_name_display, fill=COLOR_BLACK, font=font_city, direction='rtl')
    else:
        # Otherwise, draw the pre-shaped text without the direction argument
        draw.text((city_x, city_y), city_name_display, fill=COLOR_BLACK, font=font_city)

    # Draw separator line below row (except for last row)
    if not is_last_row:
        separator_y = y_position + ROW_HEIGHT
        # Draw semi-transparent white line
        draw.line([(ROW_PADDING, separator_y), (IMAGE_WIDTH - ROW_PADDING, separator_y)],
                 fill=SEPARATOR_COLOR, width=1)


def generate_all_cities_image(cities_data: list, forecast_date: str, output_path: Path) -> bool:
    """
    Generate a weather forecast image for all 15 cities.

    Args:
        cities_data: List of dictionaries with city forecast data (should be 15 cities)
        forecast_date: Date of forecast (YYYY-MM-DD)
        output_path: Path to save the image

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\nGenerating forecast image for {len(cities_data)} cities")

        # Create canvas with white header and gradient background
        print("  Creating canvas with header and gradient background...")
        image = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, HEADER_HEIGHT)

        # Add header content (logo and date)
        print("  Adding header with logo and date...")
        add_header_content(image, forecast_date)

        # Prepare for drawing on main canvas
        draw = ImageDraw.Draw(image)

        # Load fonts
        print("  Loading Open Sans variable fonts...")
        font_city_name = load_font_with_variation(
            FONT_SIZE_CITY, FONT_WEIGHT_CITY, FONT_WIDTH_CITY
        )
        font_temp = load_font_with_variation(
            FONT_SIZE_TEMP, FONT_WEIGHT_TEMP, FONT_WIDTH_TEMP
        )

        # Calculate total list height and center it vertically in available space
        num_cities = len(cities_data)
        total_list_height = num_cities * ROW_HEIGHT
        available_height = IMAGE_HEIGHT - HEADER_HEIGHT
        vertical_offset = (available_height - total_list_height) // 2

        # Calculate starting Y position for first city row (centered)
        content_start = HEADER_HEIGHT + vertical_offset

        # Draw each city row
        print(f"  Drawing {len(cities_data)} city rows (vertically centered)...")
        for idx, city_data in enumerate(cities_data):
            y_pos = content_start + (idx * ROW_HEIGHT)
            is_last = (idx == len(cities_data) - 1)

            print(f"    [{idx+1:2d}/15] {city_data['name_eng']:20s} - {city_data['min_temp']}-{city_data['max_temp']}°C")

            draw_city_row(image, draw, city_data, y_pos, font_city_name, font_temp, is_last)

        # Save image
        print(f"\n  Saving image to: {output_path}")
        image.save(output_path, 'JPEG', quality=95)
        print("  Image saved successfully!")

        return True

    except Exception as e:
        print(f"  ERROR generating image: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN SCRIPT (for standalone testing)
# ============================================================================

def main():
    """Main entry point for standalone testing."""
    import sys

    # Add project root to path for imports
    sys.path.insert(0, str(BASE_DIR))
    from extract_forecast import extract_forecast
    from utils import setup_logging

    print("="*60)
    print("IMS WEATHER FORECAST - PHASE 3: ALL 15 CITIES")
    print("="*60)

    # Setup logging for standalone run
    logger = setup_logging()

    # Extract forecast data
    print("\nExtracting forecast data...")
    # Pass the logger to the extraction function
    cities_data = extract_forecast(logger=logger)

    if not cities_data:
        print("ERROR: Failed to extract forecast data")
        sys.exit(1)

    print(f"Extracted {len(cities_data)} cities")

    # Get forecast date (use today's date as fallback)
    forecast_date = datetime.now().strftime('%Y-%m-%d')

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate image
    output_path = OUTPUT_DIR / "daily_forecast.jpg"
    success = generate_all_cities_image(cities_data, forecast_date, output_path)

    # Summary
    print("\n" + "="*60)
    if success:
        print("SUCCESS! Phase 3 image generation complete!")
        print(f"Output: {output_path}")
        print("\nFeatures implemented:")
        print("  [X] All 15 Israeli cities in single image")
        print("  [X] Vertical layout with balanced rows")
        print("  [X] Hebrew city names (RTL)")
        print("  [X] Weather icons for each city")
        print("  [X] Temperature ranges")
        print("  [X] Line separators between rows")
        print("  [X] Sky blue gradient background")
        print("  [X] Professional header with IMS logo and date")
        print("\nReady for Phase 4: Automation & Email Delivery!")
    else:
        print("FAILED! Check error messages above")
    print("="*60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
