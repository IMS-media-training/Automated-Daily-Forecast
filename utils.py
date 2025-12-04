"""
IMS Weather Forecast Automation - Utility Functions

Shared utilities for logging, date handling, validation, and file management.
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import glob

try:
    from pyluach import dates, hebrewcal
except ImportError:
    # pyluach may not be installed yet
    dates = None
    hebrewcal = None


# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"
ARCHIVE_DIR = PROJECT_ROOT / "archive"
OUTPUT_DIR = PROJECT_ROOT / "output"
XML_FILE = PROJECT_ROOT / "isr_cities_utf8.xml"
COUNTRY_XML_FILE = PROJECT_ROOT / "isr_country_utf8.xml"

# V2 Asset Paths
ASSETS_DIR = PROJECT_ROOT / "assets"
MAP_DIR = ASSETS_DIR / "map"
LOGOS_DIR = ASSETS_DIR / "logos"
WEATHER_ICONS_V2_DIR = ASSETS_DIR / "weather_icons_v2"

# Specific asset files
ISRAEL_MAP_PNG = MAP_DIR / "israel_map.png"
ISRAEL_MAP_SVG = MAP_DIR / "israel_map.svg"
IMS_LOGO_PNG = LOGOS_DIR / "ims_logo.png"
MOT_LOGO_PNG = LOGOS_DIR / "mot_logo.png"

# Font paths
FONTS_DIR = PROJECT_ROOT / "fonts"
NOTO_SANS_HEBREW_BLACK_COMPLETE = FONTS_DIR / "NotoSansHebrew-Black-Complete.ttf"  # Static Black weight (complete, all glyphs)
NOTO_SANS_HEBREW_VARIABLE = FONTS_DIR / "NotoSansHebrew-Variable-Complete.ttf"  # Complete variable font (all glyphs)
NOTO_SANS_HEBREW_BLACK = FONTS_DIR / "NotoSansHebrew-Black.ttf"     # Static Black subset (Hebrew only, no numbers)
NOTO_SANS_HEBREW_SEMIBOLD = FONTS_DIR / "NotoSansHebrew-SemiBold.ttf"  # Static SemiBold subset (Hebrew only, no numbers)
OPEN_SANS_FONT = FONTS_DIR / "OpenSans-Variable.ttf"              # Backup

ARCHIVE_RETENTION_DAYS = 14
EXPECTED_CITY_COUNT = 15


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging to output to both console and file.

    Args:
        log_level: Logging level (default: logging.INFO)

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)

    # Configure logger
    logger = logging.getLogger('ims_forecast')
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler (with color-friendly format)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        '%(levelname)-8s | %(message)s'
    )
    console_handler.setFormatter(console_format)

    # File handler (with detailed timestamp)
    log_file = LOGS_DIR / 'forecast_automation.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# ============================================================================
# DATE UTILITIES
# ============================================================================

def get_today_date() -> str:
    """
    Get today's date in YYYY-MM-DD format (matching XML date format).

    Returns:
        Today's date as string
    """
    return datetime.now().strftime('%Y-%m-%d')


def format_hebrew_date(date_str: Optional[str] = None) -> str:
    """
    Convert Gregorian date to Hebrew calendar date with full formatting.

    Args:
        date_str: Date in YYYY-MM-DD format (default: today)

    Returns:
        Formatted date string: "DD/MM/YYYY Hebrew_Date"
        Example: "26/11/2025 ו׳ בכסלו תשפ״ו"
    """
    if dates is None:
        # Fallback if pyluach not installed
        if date_str is None:
            date_str = get_today_date()
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')

    try:
        # Parse the date
        if date_str is None:
            date_str = get_today_date()

        # Convert string to datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        # Format Gregorian part (DD/MM/YYYY)
        gregorian_part = date_obj.strftime('%d/%m/%Y')

        # Convert Gregorian to Hebrew calendar
        gregorian_date = dates.GregorianDate(date_obj.year, date_obj.month, date_obj.day)
        hebrew_date = gregorian_date.to_heb()

        # Get Hebrew date string and split into components
        # Format from pyluach: "ו׳ כסלו תשפ״ו"
        hebrew_date_parts = hebrew_date.hebrew_date_string().split()

        if len(hebrew_date_parts) == 3:
            # Add ב before the month name: "ו׳ בכסלו תשפ״ו"
            hebrew_day = hebrew_date_parts[0]
            hebrew_month = hebrew_date_parts[1]
            hebrew_year = hebrew_date_parts[2]
            hebrew_part = f'{hebrew_day} ב{hebrew_month} {hebrew_year}'
        else:
            # Fallback if format is unexpected
            hebrew_part = hebrew_date.hebrew_date_string()

        return f'{gregorian_part} {hebrew_part}'

    except Exception as e:
        # Fallback to Gregorian only if conversion fails
        if date_str is None:
            date_str = get_today_date()
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')


def get_archive_filename(date_str: Optional[str] = None) -> str:
    """
    Generate archive filename for a given date.

    Args:
        date_str: Date in YYYY-MM-DD format (default: today)

    Returns:
        Filename like 'isr_cities_2025-10-15.xml'
    """
    if date_str is None:
        date_str = get_today_date()
    return f'isr_cities_{date_str}.xml'


def get_archive_path(date_str: Optional[str] = None) -> Path:
    """
    Get full path to archive file for a given date.

    Args:
        date_str: Date in YYYY-MM-DD format (default: today)

    Returns:
        Full path to archive file
    """
    return ARCHIVE_DIR / get_archive_filename(date_str)


def get_country_archive_filename(date_str: Optional[str] = None) -> str:
    """
    Generate archive filename for country XML for a given date.

    Args:
        date_str: Date in YYYY-MM-DD format (default: today)

    Returns:
        Filename like 'isr_country_2025-10-15.xml'
    """
    if date_str is None:
        date_str = get_today_date()
    return f'isr_country_{date_str}.xml'


def get_country_archive_path(date_str: Optional[str] = None) -> Path:
    """
    Get full path to country archive file for a given date.

    Args:
        date_str: Date in YYYY-MM-DD format (default: today)

    Returns:
        Full path to country archive file
    """
    return ARCHIVE_DIR / get_country_archive_filename(date_str)


# ============================================================================
# FILE MANAGEMENT
# ============================================================================

def ensure_directories() -> None:
    """
    Create all required project directories if they don't exist.
    """
    LOGS_DIR.mkdir(exist_ok=True)
    ARCHIVE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)


def cleanup_old_archives(logger: logging.Logger, dry_run: bool = False) -> int:
    """
    Delete XML files in archive older than ARCHIVE_RETENTION_DAYS.
    Handles both cities and country XML files.

    Args:
        logger: Logger instance for output
        dry_run: If True, only show what would be deleted

    Returns:
        Number of files deleted (or would be deleted in dry-run)
    """
    cutoff_date = datetime.now() - timedelta(days=ARCHIVE_RETENTION_DAYS)

    # Find all XML files in archive (both cities and country)
    archive_files = glob.glob(str(ARCHIVE_DIR / 'isr_cities_*.xml'))
    archive_files.extend(glob.glob(str(ARCHIVE_DIR / 'isr_country_*.xml')))
    deleted_count = 0

    for file_path in archive_files:
        # Extract date from filename
        filename = os.path.basename(file_path)
        try:
            # Format: isr_cities_YYYY-MM-DD.xml or isr_country_YYYY-MM-DD.xml
            date_str = filename.replace('isr_cities_', '').replace('isr_country_', '').replace('.xml', '')
            file_date = datetime.strptime(date_str, '%Y-%m-%d')

            # Check if older than cutoff
            if file_date < cutoff_date:
                if dry_run:
                    logger.info(f"[DRY RUN] Would delete old archive: {filename}")
                else:
                    os.remove(file_path)
                    logger.info(f"Deleted old archive: {filename}")
                deleted_count += 1

        except (ValueError, IndexError):
            logger.warning(f"Skipping file with invalid date format: {filename}")

    if deleted_count == 0:
        logger.info(f"No archive files older than {ARCHIVE_RETENTION_DAYS} days found")
    elif dry_run:
        logger.info(f"[DRY RUN] Would delete {deleted_count} old archive file(s)")
    else:
        logger.info(f"Deleted {deleted_count} old archive file(s)")

    return deleted_count


# ============================================================================
# DATA VALIDATION
# ============================================================================

def validate_city_count(cities_data: List[Dict], logger: logging.Logger) -> bool:
    """
    Validate that we extracted the expected number of cities.

    Args:
        cities_data: List of city dictionaries
        logger: Logger instance for output

    Returns:
        True if count is as expected, False otherwise
    """
    actual_count = len(cities_data)

    if actual_count == EXPECTED_CITY_COUNT:
        logger.info(f"City count validation: OK ({actual_count} cities)")
        return True
    else:
        logger.warning(
            f"City count mismatch! Expected {EXPECTED_CITY_COUNT}, "
            f"got {actual_count}"
        )
        return False


def validate_city_data(city: Dict, logger: logging.Logger) -> bool:
    """
    Validate that a city dictionary has all required data.

    Args:
        city: City data dictionary
        logger: Logger instance for output

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['name_eng', 'name_heb', 'latitude', 'longitude',
                      'max_temp', 'min_temp', 'weather_code']

    missing_fields = []
    for field in required_fields:
        if field not in city or city[field] is None:
            missing_fields.append(field)

    if missing_fields:
        logger.error(
            f"City '{city.get('name_eng', 'Unknown')}' missing data: "
            f"{', '.join(missing_fields)}"
        )
        return False

    return True


# ============================================================================
# FORMATTING UTILITIES
# ============================================================================

def format_temperature_range(min_temp: str, max_temp: str) -> str:
    """
    Format temperature range for display.

    Args:
        min_temp: Minimum temperature as string
        max_temp: Maximum temperature as string

    Returns:
        Formatted string like "18-27°C"
    """
    return f"{min_temp}-{max_temp}°C"


def print_separator(logger: logging.Logger, char: str = "=", length: int = 60) -> None:
    """
    Print a separator line to the log.

    Args:
        logger: Logger instance
        char: Character to use for separator
        length: Length of separator line
    """
    logger.info(char * length)


# ============================================================================
# MODULE INFORMATION
# ============================================================================

if __name__ == "__main__":
    # Test logging setup
    logger = setup_logging()

    print_separator(logger)
    logger.info("IMS Weather Forecast - Utility Functions Test")
    print_separator(logger)

    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Logs directory: {LOGS_DIR}")
    logger.info(f"Archive directory: {ARCHIVE_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info(f"Main XML file: {XML_FILE}")

    logger.info(f"\nToday's date: {get_today_date()}")
    logger.info(f"Archive filename: {get_archive_filename()}")
    logger.info(f"Archive path: {get_archive_path()}")

    logger.info("\nEnsuring directories exist...")
    ensure_directories()
    logger.info("Directories created successfully")

    logger.info(f"\nExpected city count: {EXPECTED_CITY_COUNT}")
    logger.info(f"Archive retention: {ARCHIVE_RETENTION_DAYS} days")

    print_separator(logger)
    logger.info("Utility functions test complete!")
    print_separator(logger)
