"""
IMS Weather Forecast Automation - Extract Forecast Data

Production-ready extraction script that parses XML, extracts weather data
for all 15 cities, filters by date, sorts north to south, and validates.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
import glob

from utils import (
    setup_logging,
    get_today_date,
    get_archive_path,
    get_country_archive_path,
    validate_city_count,
    validate_city_data,
    format_temperature_range,
    format_hebrew_date,
    print_separator,
    XML_FILE,
    COUNTRY_XML_FILE,
    ARCHIVE_DIR
)


# ============================================================================
# EXTRACTION FUNCTIONS
# ============================================================================

def parse_xml_file(xml_path: Path, logger) -> Optional[ET.Element]:
    """
    Parse XML file and return root element.

    Args:
        xml_path: Path to XML file
        logger: Logger instance

    Returns:
        XML root element, or None if failed
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        logger.info(f"Successfully parsed XML file: {xml_path.name}")
        return root

    except ET.ParseError as e:
        logger.error(f"XML parsing error: {e}")
        return None
    except FileNotFoundError:
        logger.error(f"XML file not found: {xml_path}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error parsing XML: {e}")
        return None


def get_issue_datetime(root: ET.Element, logger) -> Optional[str]:
    """
    Extract forecast issue date/time from XML.

    Args:
        root: XML root element
        logger: Logger instance

    Returns:
        Issue datetime string, or None if not found
    """
    try:
        issue_elem = root.find('.//IssueDateTime')
        if issue_elem is not None and issue_elem.text:
            return issue_elem.text
        else:
            logger.warning("Issue date/time not found in XML")
            return None
    except Exception as e:
        logger.error(f"Error extracting issue date/time: {e}")
        return None


def extract_city_forecast(location: ET.Element, target_date: str, logger) -> Optional[Dict]:
    """
    Extract forecast data for one city/location.

    Args:
        location: XML Location element
        target_date: Target date in YYYY-MM-DD format
        logger: Logger instance

    Returns:
        City data dictionary, or None if extraction failed
    """
    try:
        # Extract metadata
        metadata = location.find('LocationMetaData')
        if metadata is None:
            logger.error("LocationMetaData not found")
            return None

        city_name_eng = metadata.find('LocationNameEng').text
        city_name_heb = metadata.find('LocationNameHeb').text
        latitude = float(metadata.find('DisplayLat').text)
        longitude = float(metadata.find('DisplayLon').text)

        # Find the forecast for target date
        location_data = location.find('LocationData')
        if location_data is None:
            logger.error(f"LocationData not found for {city_name_eng}")
            return None

        target_forecast = None
        for time_unit in location_data.findall('TimeUnitData'):
            date_elem = time_unit.find('Date')
            if date_elem is not None and date_elem.text == target_date:
                target_forecast = time_unit
                break

        # If no forecast found for this date, return None
        if target_forecast is None:
            logger.warning(f"No forecast found for {city_name_eng} on {target_date}")
            return None

        # Extract weather elements
        max_temp = None
        min_temp = None
        weather_code = None
        max_humidity = None
        min_humidity = None
        wind = None

        for element in target_forecast.findall('Element'):
            elem_name_node = element.find('ElementName')
            elem_value_node = element.find('ElementValue')

            if elem_name_node is None or elem_value_node is None:
                continue

            elem_name = elem_name_node.text
            elem_value = elem_value_node.text

            if elem_name == "Maximum temperature":
                max_temp = elem_value
            elif elem_name == "Minimum temperature":
                min_temp = elem_value
            elif elem_name == "Weather code":
                weather_code = elem_value
            elif elem_name == "Maximum relative humidity":
                max_humidity = elem_value
            elif elem_name == "Minimum relative humidity":
                min_humidity = elem_value
            elif elem_name == "Wind direction and speed":
                wind = elem_value

        # Build city data dictionary
        city_info = {
            'name_eng': city_name_eng,
            'name_heb': city_name_heb,
            'latitude': latitude,
            'longitude': longitude,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'weather_code': weather_code,
            'max_humidity': max_humidity,
            'min_humidity': min_humidity,
            'wind': wind
        }

        return city_info

    except AttributeError as e:
        logger.error(f"Missing required XML element: {e}")
        return None
    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error extracting city data: {e}")
        return None


def get_available_dates(root: ET.Element, logger) -> List[str]:
    """
    Get all available forecast dates from the XML.

    Args:
        root: XML root element
        logger: Logger instance

    Returns:
        List of dates in YYYY-MM-DD format, sorted chronologically
    """
    dates = set()

    try:
        # Find all Date elements across all locations
        for date_elem in root.findall('.//TimeUnitData/Date'):
            if date_elem.text:
                dates.add(date_elem.text)

        # Sort dates chronologically
        sorted_dates = sorted(list(dates))

        if sorted_dates:
            logger.info(f"Available forecast dates in XML: {', '.join(sorted_dates)}")
        else:
            logger.warning("No forecast dates found in XML")

        return sorted_dates

    except Exception as e:
        logger.error(f"Error getting available dates: {e}")
        return []


def extract_all_cities(root: ET.Element, target_date: str, logger) -> List[Dict]:
    """
    Extract forecast data for all cities in the XML.

    If no data found for target_date, automatically falls back to the first
    available date in the XML (handles case where XML has tomorrow's forecast).

    Args:
        root: XML root element
        target_date: Target date in YYYY-MM-DD format
        logger: Logger instance

    Returns:
        List of city data dictionaries
    """
    cities_data = []

    # Find all Location elements
    locations = root.findall('.//Location')
    logger.info(f"Found {len(locations)} city locations in XML")

    # Extract data from each location
    for location in locations:
        city_data = extract_city_forecast(location, target_date, logger)
        if city_data is not None:
            # Validate city data
            if validate_city_data(city_data, logger):
                cities_data.append(city_data)
            else:
                logger.warning(f"Skipping city with invalid data: {city_data.get('name_eng', 'Unknown')}")

    logger.info(f"Successfully extracted {len(cities_data)} cities")

    # Smart date detection: If no cities found, try subsequent available dates
    if len(cities_data) == 0:
        logger.warning(f"No data found for target date: {target_date}")
        logger.info("Attempting smart date detection...")

        available_dates = get_available_dates(root, logger)

        if available_dates:
            # Try each available date until we find one with data
            for fallback_date in available_dates:
                # Skip the target date if we already tried it
                if fallback_date == target_date:
                    continue

                logger.info(f"Trying fallback date: {fallback_date}")

                # Re-extract with fallback date
                for location in locations:
                    city_data = extract_city_forecast(location, fallback_date, logger)
                    if city_data is not None:
                        if validate_city_data(city_data, logger):
                            cities_data.append(city_data)

                # If we got cities, we're done
                if len(cities_data) > 0:
                    logger.info(f"✓ Successfully extracted {len(cities_data)} cities using date: {fallback_date}")
                    logger.info(f"Note: IMS published new forecast - using {fallback_date} instead of {target_date}")
                    break
                else:
                    logger.warning(f"No valid data found for {fallback_date}, trying next date...")

            if len(cities_data) == 0:
                logger.error("No valid data found in any available date")
        else:
            logger.error("No available dates found in XML")

    return cities_data


def sort_cities_north_to_south(cities_data: List[Dict], logger) -> List[Dict]:
    """
    Sort cities by latitude (north to south = highest to lowest).

    Args:
        cities_data: List of city data dictionaries
        logger: Logger instance

    Returns:
        Sorted list of city data dictionaries
    """
    try:
        sorted_cities = sorted(cities_data, key=lambda city: city['latitude'], reverse=True)
        logger.info("Cities sorted north to south by latitude")
        return sorted_cities
    except Exception as e:
        logger.error(f"Error sorting cities: {e}")
        return cities_data


def extract_weather_description(country_xml_path: Path, target_date: str, logger) -> Optional[str]:
    """
    Extract textual weather description from country XML.

    Args:
        country_xml_path: Path to country XML file
        target_date: Target date in YYYY-MM-DD format
        logger: Logger instance

    Returns:
        Weather description string in Hebrew, or None if not found
    """
    try:
        # Parse the country XML
        root = parse_xml_file(country_xml_path, logger)
        if root is None:
            return None

        # Find the forecast for target date
        # Country XML structure: Location/LocationData/TimeUnitData with Date and PredictedConditions
        location_data = root.find('.//LocationData')
        if location_data is None:
            logger.warning("LocationData not found in country XML")
            return None

        # Search for the target date
        for time_unit in location_data.findall('TimeUnitData'):
            date_elem = time_unit.find('Date')
            if date_elem is not None and date_elem.text == target_date:
                # Found the right date, extract the description in Hebrew
                # Look for Element with ElementName = "Weather in Hebrew"
                for element in time_unit.findall('Element'):
                    elem_name = element.find('ElementName')
                    elem_value = element.find('ElementValue')

                    if (elem_name is not None and elem_name.text == 'Weather in Hebrew' and
                        elem_value is not None and elem_value.text):
                        description = elem_value.text.strip()
                        logger.info(f"Found weather description for {target_date}")
                        return description

        logger.warning(f"No weather description found for {target_date} in country XML")
        return None

    except Exception as e:
        logger.error(f"Error extracting weather description: {e}")
        return None


def find_latest_archive(logger) -> Optional[Path]:
    """
    Find the most recent XML file in the archive directory.

    Args:
        logger: Logger instance

    Returns:
        Path to latest archive file, or None if not found
    """
    try:
        archive_files = glob.glob(str(ARCHIVE_DIR / 'isr_cities_*.xml'))

        if not archive_files:
            logger.warning("No archive files found")
            return None

        # Sort by filename (date is in filename)
        latest_file = max(archive_files)
        logger.info(f"Found latest archive: {Path(latest_file).name}")
        return Path(latest_file)

    except Exception as e:
        logger.error(f"Error finding latest archive: {e}")
        return None


def find_latest_country_archive(logger) -> Optional[Path]:
    """
    Find the most recent country XML file in the archive directory.

    Args:
        logger: Logger instance

    Returns:
        Path to latest country archive file, or None if not found
    """
    try:
        archive_files = glob.glob(str(ARCHIVE_DIR / 'isr_country_*.xml'))

        if not archive_files:
            logger.warning("No country archive files found")
            return None

        # Sort by filename (date is in filename)
        latest_file = max(archive_files)
        logger.info(f"Found latest country archive: {Path(latest_file).name}")
        return Path(latest_file)

    except Exception as e:
        logger.error(f"Error finding latest country archive: {e}")
        return None


# ============================================================================
# MAIN EXTRACTION WORKFLOW
# ============================================================================

def extract_forecast(target_date: Optional[str] = None,
                    use_archive_fallback: bool = True,
                    logger=None) -> Optional[Dict]:
    """
    Complete extraction workflow: parse XML, extract data, sort, validate.

    Args:
        target_date: Date to extract (default: today)
        use_archive_fallback: If True, try archive if main file fails
        logger: Logger instance

    Returns:
        Dictionary containing:
            - 'cities': List of city data dictionaries
            - 'description': Weather description string (Hebrew)
            - 'date': Target date used (YYYY-MM-DD)
            - 'hebrew_date': Formatted date with Hebrew calendar
        Returns None if failed
    """
    if logger is None:
        logger = setup_logging()

    print_separator(logger)
    logger.info("IMS WEATHER FORECAST EXTRACTION")
    print_separator(logger)

    # Use today's date if not specified
    if target_date is None:
        target_date = get_today_date()
        logger.info(f"Using today's date: {target_date}")
    else:
        logger.info(f"Using specified date: {target_date}")

    # Try to parse the main XML file
    logger.info(f"\nAttempting to parse: {XML_FILE.name}")
    root = parse_xml_file(XML_FILE, logger)

    # Fallback to latest archive if main file fails
    if root is None and use_archive_fallback:
        logger.warning("Main XML file failed, trying archive fallback...")
        archive_path = find_latest_archive(logger)

        if archive_path is not None:
            logger.info(f"Attempting to parse archive: {archive_path.name}")
            root = parse_xml_file(archive_path, logger)

    # If we still don't have valid XML, abort
    if root is None:
        logger.error("Failed to parse XML file (no fallback available)")
        return None

    # Get issue date/time
    issue_datetime = get_issue_datetime(root, logger)
    if issue_datetime:
        logger.info(f"Forecast issued: {issue_datetime}")

    # Extract all cities
    logger.info(f"\nExtracting forecast data for {target_date}...")
    cities_data = extract_all_cities(root, target_date, logger)

    if not cities_data:
        logger.error("No cities extracted - check target date and XML content")
        return None

    # Validate city count
    validate_city_count(cities_data, logger)

    # Sort cities
    logger.info("\nSorting cities north to south...")
    cities_data = sort_cities_north_to_south(cities_data, logger)

    # Extract weather description from country XML
    logger.info("\nExtracting weather description from country XML...")
    country_xml_path = COUNTRY_XML_FILE
    weather_description = None

    if country_xml_path.exists():
        weather_description = extract_weather_description(country_xml_path, target_date, logger)
    elif use_archive_fallback:
        logger.warning("Country XML file not found, trying archive fallback...")
        archive_country_path = find_latest_country_archive(logger)
        if archive_country_path:
            weather_description = extract_weather_description(archive_country_path, target_date, logger)

    if weather_description:
        logger.info(f"Weather description: {weather_description[:50]}..." if len(weather_description) > 50 else f"Weather description: {weather_description}")
    else:
        logger.warning("No weather description found (will continue without it)")

    # Format Hebrew date
    hebrew_date = format_hebrew_date(target_date)
    logger.info(f"Hebrew date: {hebrew_date}")

    # Display summary
    print_separator(logger)
    logger.info("EXTRACTION COMPLETE")
    print_separator(logger)
    logger.info(f"Target date: {target_date}")
    logger.info(f"Hebrew date: {hebrew_date}")
    logger.info(f"Cities extracted: {len(cities_data)}")
    logger.info(f"Weather description: {'Found' if weather_description else 'Not found'}")
    logger.info(f"Sorted: North to South")
    logger.info("Note: If smart date detection was used, actual date may differ from target")

    # Display brief city list
    logger.info("\nExtracted cities:")
    for i, city in enumerate(cities_data, 1):
        temp_range = format_temperature_range(city['min_temp'], city['max_temp'])
        logger.info(
            f"  {i:2d}. {city['name_eng']:20s} | {temp_range:10s} | "
            f"Code: {city['weather_code']}"
        )

    print_separator(logger)

    # Return complete forecast data
    return {
        'cities': cities_data,
        'description': weather_description,
        'date': target_date,
        'hebrew_date': hebrew_date
    }


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract weather forecast data from IMS XML'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Target date in YYYY-MM-DD format (default: today)'
    )
    parser.add_argument(
        '--no-fallback',
        action='store_true',
        help="Don't use archive fallback if main XML fails"
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Setup logging
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging(log_level)

    # Run extraction
    forecast_data = extract_forecast(
        target_date=args.date,
        use_archive_fallback=not args.no_fallback,
        logger=logger
    )

    # Exit with appropriate code
    sys.exit(0 if forecast_data is not None else 1)


if __name__ == "__main__":
    main()
