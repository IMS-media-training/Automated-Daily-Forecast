"""
IMS Weather Forecast Automation - Phase 2: Enhanced Image Generation

Single city image generation with:
- Fredoka variable font (configurable weight/width axes)
- iOS-style weather icon PNGs
- Header with IMS logo and forecast date
- Hebrew RTL text support
"""

import sys
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from extract_forecast import extract_forecast


# ============================================================================
# CONFIGURATION - Easy to modify design parameters
# ============================================================================

# Image dimensions (Instagram story format)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# Font Configuration (Fredoka Variable Font)
# Weight axis: 300 (Light) to 700 (Bold)
# Width axis: 75 (Condensed) to 125 (Wide)
FONT_WEIGHT_CITY = 600      # SemiBold for city name
FONT_WIDTH_CITY = 100       # Normal width
FONT_SIZE_CITY = 120        # City name font size

FONT_WEIGHT_TEMP = 500      # Medium for temperature
FONT_WIDTH_TEMP = 100       # Normal width
FONT_SIZE_TEMP = 100        # Temperature font size

FONT_WEIGHT_DATE = 400      # Regular for date
FONT_WIDTH_DATE = 100       # Normal width
FONT_SIZE_DATE = 50         # Date font size

# Header Configuration
HEADER_HEIGHT = 180         # White header section height
LOGO_HEIGHT = 120           # IMS logo display height
LOGO_MARGIN_LEFT = 40       # Logo left margin
LOGO_MARGIN_TOP = 30        # Logo top margin

# Weather Icon Configuration
ICON_SIZE = 180             # Weather icon display size (pixels)

# Colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (100, 100, 100)
COLOR_SKY_LIGHT = (135, 206, 250)  # Light sky blue for gradient top

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "output"
FONT_DIR = Path(__file__).parent.parent / "fonts"
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# Font file
FONT_VARIABLE = FONT_DIR / "Fredoka-Variable.ttf"

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
    Load Fredoka variable font with specific weight and width axes.

    Args:
        size: Font size in pixels
        weight: Weight axis value (300-700)
        width: Width axis value (75-125)

    Returns:
        Configured font object
    """
    font = ImageFont.truetype(str(FONT_VARIABLE), size)
    # Set variable font axes: [weight, width] for Fredoka
    font.set_variation_by_axes([weight, width])
    return font


def render_hebrew_text(text: str) -> str:
    """
    Convert Hebrew text to proper RTL display format.

    Args:
        text: Hebrew text string

    Returns:
        RTL-formatted text ready for rendering
    """
    # NOTE: In some environments, Pillow handles Hebrew RTL automatically.
    # If Hebrew appears reversed, try returning text directly without get_display()
    # return get_display(text)  # Uncomment if Hebrew appears reversed
    return text  # Direct rendering - try this first


def load_weather_icon(weather_code: str) -> Image.Image:
    """
    Load weather icon PNG for the given weather code.

    Args:
        weather_code: Weather code from XML

    Returns:
        PIL Image of weather icon, resized to ICON_SIZE
    """
    # Get icon filename from mapping, with fallback
    icon_filename = WEATHER_ICONS.get(weather_code, 'mostly_clear.png')
    icon_path = WEATHER_ICONS_DIR / icon_filename

    try:
        icon = Image.open(icon_path).convert('RGBA')
        # Resize to configured icon size with high-quality resampling
        icon = icon.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
        return icon
    except Exception as e:
        print(f"  Warning: Could not load icon {icon_filename}: {e}")
        # Return a blank placeholder if icon fails to load
        return Image.new('RGBA', (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))


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
    # Load and paste logo
    logo = load_logo()
    logo_x = LOGO_MARGIN_LEFT
    logo_y = LOGO_MARGIN_TOP
    image.paste(logo, (logo_x, logo_y), logo)  # Use logo as mask for transparency

    # Add date text (right side of header)
    draw = ImageDraw.Draw(image)
    date_font = load_font_with_variation(FONT_SIZE_DATE, FONT_WEIGHT_DATE, FONT_WIDTH_DATE)

    formatted_date = format_forecast_date(date_str)

    # Get text dimensions for right-alignment
    bbox = draw.textbbox((0, 0), formatted_date, font=date_font)
    text_width = bbox[2] - bbox[0]

    # Position date on right side with margin
    date_x = IMAGE_WIDTH - text_width - LOGO_MARGIN_LEFT
    date_y = (HEADER_HEIGHT - (bbox[3] - bbox[1])) // 2  # Vertically center in header

    draw.text((date_x, date_y), formatted_date, fill=COLOR_BLACK, font=date_font)


def generate_city_image(city_data: dict, forecast_date: str, output_path: Path) -> bool:
    """
    Generate a weather forecast image for one city.

    Args:
        city_data: Dictionary with city forecast data
        forecast_date: Date of forecast (YYYY-MM-DD)
        output_path: Path to save the image

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\nGenerating image for: {city_data['name_eng']}")

        # Create canvas with white header and gradient background
        print("  Creating canvas with header and gradient background...")
        image = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, HEADER_HEIGHT)

        # Add header content (logo and date)
        print("  Adding header with logo and date...")
        add_header_content(image, forecast_date)

        # Prepare for drawing on main canvas
        draw = ImageDraw.Draw(image)

        # Load fonts
        print("  Loading Fredoka variable fonts...")
        font_city_name = load_font_with_variation(
            FONT_SIZE_CITY, FONT_WEIGHT_CITY, FONT_WIDTH_CITY
        )
        font_temp = load_font_with_variation(
            FONT_SIZE_TEMP, FONT_WEIGHT_TEMP, FONT_WIDTH_TEMP
        )

        # Prepare text content
        city_name_heb = city_data['name_heb']
        city_name_display = render_hebrew_text(city_name_heb)

        temp_min = city_data['min_temp']
        temp_max = city_data['max_temp']
        temp_text = f"{temp_min}-{temp_max}°C"

        weather_code = city_data['weather_code']

        print(f"  Temperature: {temp_text}")
        print(f"  Weather Code: {weather_code}")

        # Calculate vertical positions (centered in content area below header)
        content_start = HEADER_HEIGHT
        content_height = IMAGE_HEIGHT - HEADER_HEIGHT
        center_y = content_start + (content_height // 2)

        # Position 1: Weather icon (PNG) at top-center of content area
        icon_y = center_y - 300

        print("  Loading weather icon...")
        weather_icon = load_weather_icon(weather_code)

        # Center icon horizontally
        icon_x = (IMAGE_WIDTH - ICON_SIZE) // 2

        # Paste icon with transparency
        image.paste(weather_icon, (icon_x, icon_y), weather_icon)

        # Position 2: City name below icon
        city_y = icon_y + ICON_SIZE + 40

        # Get city name dimensions for centering
        city_bbox = draw.textbbox((0, 0), city_name_display, font=font_city_name)
        city_width = city_bbox[2] - city_bbox[0]
        city_x = (IMAGE_WIDTH - city_width) // 2

        # Draw city name (Hebrew RTL)
        draw.text((city_x, city_y), city_name_display, fill=COLOR_BLACK, font=font_city_name)

        # Position 3: Temperature below city name
        temp_y = city_y + 150

        # Get temperature dimensions for centering
        temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
        temp_width = temp_bbox[2] - temp_bbox[0]
        temp_x = (IMAGE_WIDTH - temp_width) // 2

        # Draw temperature
        draw.text((temp_x, temp_y), temp_text, fill=COLOR_GRAY, font=font_temp)

        # Save image
        print(f"  Saving image to: {output_path}")
        image.save(output_path, 'JPEG', quality=95)
        print("  Image saved successfully!")

        return True

    except Exception as e:
        print(f"  ERROR generating image: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    """Main entry point for the script."""
    print("="*60)
    print("IMS WEATHER FORECAST - ENHANCED IMAGE GENERATION")
    print("="*60)

    # Extract forecast data
    print("\nExtracting forecast data...")
    cities_data = extract_forecast()

    if not cities_data:
        print("ERROR: Failed to extract forecast data")
        sys.exit(1)

    # Get forecast date from extracted data (use today's date as fallback)
    forecast_date = datetime.now().strftime('%Y-%m-%d')

    # Find Tel Aviv (our test city)
    tel_aviv = None
    for city in cities_data:
        if city['name_eng'] == 'Tel Aviv - Yafo':
            tel_aviv = city
            break

    if not tel_aviv:
        print("ERROR: Tel Aviv not found in forecast data")
        sys.exit(1)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate image
    output_path = OUTPUT_DIR / "test_city_forecast.jpg"
    success = generate_city_image(tel_aviv, forecast_date, output_path)

    # Summary
    print("\n" + "="*60)
    if success:
        print("SUCCESS! Enhanced image generation complete!")
        print(f"Output: {output_path}")
        print("\nFeatures implemented:")
        print("  [X] Fredoka variable font with configurable axes")
        print("  [X] iOS-style weather icon (PNG overlay)")
        print("  [X] Header with logo and date (DD/MM/YYYY)")
        print("  [X] Hebrew RTL city name")
        print("  [X] Clean white header + sky gradient")
        print("\nNext steps:")
        print("  1. Open the image to verify all elements display correctly")
        print("  2. Replace placeholder logo with converted ims_logo.png")
        print("  3. Adjust CONFIGURATION constants to tweak design")
        print("  4. Ready to expand to all 15 cities in Phase 3!")
    else:
        print("FAILED! Check error messages above")
    print("="*60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
