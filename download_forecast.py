"""
IMS Weather Forecast Automation - Download & Convert XML

Downloads the daily weather forecast XML from IMS website,
converts encoding from ISO-8859-8 to UTF-8, and saves both
current and archived copies.
"""

import sys
import time
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not installed")
    print("Please install it with: pip install requests")
    sys.exit(1)

from utils import (
    setup_logging,
    get_today_date,
    get_archive_path,
    get_country_archive_path,
    ensure_directories,
    cleanup_old_archives,
    print_separator,
    XML_FILE,
    COUNTRY_XML_FILE
)


# ============================================================================
# CONFIGURATION
# ============================================================================

IMS_CITIES_XML_URL = "https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_cities.xml"
IMS_COUNTRY_XML_URL = "https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_country.xml"
DOWNLOAD_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


# ============================================================================
# DOWNLOAD FUNCTIONS
# ============================================================================

def download_xml_from_ims(url: str, logger, timeout: int = DOWNLOAD_TIMEOUT) -> Optional[bytes]:
    """
    Download XML file from IMS website with retry logic.

    Args:
        url: URL to download from
        logger: Logger instance
        timeout: Request timeout in seconds

    Returns:
        Raw XML content as bytes, or None if failed
    """
    logger.info(f"Downloading XML from: {url}")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise exception for bad status codes

            logger.info(f"Download successful (attempt {attempt}/{MAX_RETRIES})")
            logger.info(f"Response size: {len(response.content)} bytes")
            return response.content

        except requests.exceptions.Timeout:
            logger.error(f"Attempt {attempt}/{MAX_RETRIES}: Request timed out after {timeout} seconds")

        except requests.exceptions.ConnectionError:
            logger.error(f"Attempt {attempt}/{MAX_RETRIES}: Connection error - check internet connection")

        except requests.exceptions.HTTPError as e:
            logger.error(f"Attempt {attempt}/{MAX_RETRIES}: HTTP error - {e}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt}/{MAX_RETRIES}: Request failed - {e}")

        # Wait before retrying (unless it was the last attempt)
        if attempt < MAX_RETRIES:
            logger.info(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    logger.error(f"Failed to download XML after {MAX_RETRIES} attempts")
    return None


def convert_encoding(raw_content: bytes, logger) -> Optional[str]:
    """
    Convert XML from ISO-8859-8 (Hebrew) to UTF-8 encoding.

    Args:
        raw_content: Raw XML bytes in ISO-8859-8 encoding
        logger: Logger instance

    Returns:
        XML content as UTF-8 string, or None if failed
    """
    try:
        # Decode from ISO-8859-8
        xml_text = raw_content.decode('iso-8859-8')
        logger.info("Successfully decoded from ISO-8859-8 encoding")

        # Update XML declaration to UTF-8
        if '<?xml' in xml_text:
            # Replace encoding declaration
            xml_text = xml_text.replace('encoding="ISO-8859-8"', 'encoding="UTF-8"')
            xml_text = xml_text.replace('encoding="iso-8859-8"', 'encoding="UTF-8"')
            logger.info("Updated XML encoding declaration to UTF-8")

        return xml_text

    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode XML from ISO-8859-8: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during encoding conversion: {e}")
        return None


def save_xml_file(content: str, file_path: Path, logger, dry_run: bool = False) -> bool:
    """
    Save XML content to file in UTF-8 encoding.

    Args:
        content: XML content as string
        file_path: Path where to save the file
        logger: Logger instance
        dry_run: If True, don't actually save the file

    Returns:
        True if successful, False otherwise
    """
    if dry_run:
        logger.info(f"[DRY RUN] Would save XML to: {file_path}")
        return True

    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(exist_ok=True)

        # Write file in UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        file_size = file_path.stat().st_size
        logger.info(f"Saved XML to: {file_path} ({file_size} bytes)")
        return True

    except IOError as e:
        logger.error(f"Failed to save XML to {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error saving XML: {e}")
        return False


# ============================================================================
# MAIN DOWNLOAD WORKFLOW
# ============================================================================

def download_and_convert(logger, dry_run: bool = False) -> bool:
    """
    Complete workflow: download, convert, and save XML files.
    Downloads both cities and country XML files.

    Args:
        logger: Logger instance
        dry_run: If True, don't actually save files

    Returns:
        True if successful, False otherwise
    """
    print_separator(logger)
    logger.info("IMS WEATHER FORECAST DOWNLOAD")
    print_separator(logger)

    # Ensure directories exist
    ensure_directories()
    logger.info("Project directories verified")

    today = get_today_date()
    success_count = 0

    # ========================================================================
    # CITIES XML
    # ========================================================================
    logger.info("\n[CITIES 1/4] Downloading cities XML from IMS website...")
    raw_cities_xml = download_xml_from_ims(IMS_CITIES_XML_URL, logger)

    if raw_cities_xml is None:
        logger.error("Cities XML download failed")
    else:
        logger.info("\n[CITIES 2/4] Converting encoding (ISO-8859-8 → UTF-8)...")
        utf8_cities_xml = convert_encoding(raw_cities_xml, logger)

        if utf8_cities_xml is None:
            logger.error("Cities XML encoding conversion failed")
        else:
            logger.info("\n[CITIES 3/4] Saving current cities XML file...")
            if not save_xml_file(utf8_cities_xml, XML_FILE, logger, dry_run):
                logger.error("Failed to save current cities XML file")
            else:
                logger.info("\n[CITIES 4/4] Saving cities XML to archive...")
                archive_path = get_archive_path(today)
                if save_xml_file(utf8_cities_xml, archive_path, logger, dry_run):
                    success_count += 1
                else:
                    logger.warning("Failed to save cities archive copy")

    # ========================================================================
    # COUNTRY XML
    # ========================================================================
    logger.info("\n[COUNTRY 1/4] Downloading country XML from IMS website...")
    raw_country_xml = download_xml_from_ims(IMS_COUNTRY_XML_URL, logger)

    if raw_country_xml is None:
        logger.error("Country XML download failed")
    else:
        logger.info("\n[COUNTRY 2/4] Converting encoding (ISO-8859-8 → UTF-8)...")
        utf8_country_xml = convert_encoding(raw_country_xml, logger)

        if utf8_country_xml is None:
            logger.error("Country XML encoding conversion failed")
        else:
            logger.info("\n[COUNTRY 3/4] Saving current country XML file...")
            if not save_xml_file(utf8_country_xml, COUNTRY_XML_FILE, logger, dry_run):
                logger.error("Failed to save current country XML file")
            else:
                logger.info("\n[COUNTRY 4/4] Saving country XML to archive...")
                country_archive_path = get_country_archive_path(today)
                if save_xml_file(utf8_country_xml, country_archive_path, logger, dry_run):
                    success_count += 1
                else:
                    logger.warning("Failed to save country archive copy")

    # ========================================================================
    # CLEANUP
    # ========================================================================
    logger.info("\n[CLEANUP] Cleaning up old archive files...")
    deleted_count = cleanup_old_archives(logger, dry_run)

    # Success summary
    print_separator(logger)
    if success_count == 2:
        if dry_run:
            logger.info("[DRY RUN] Download and conversion simulation complete!")
        else:
            logger.info("Download and conversion complete!")
        logger.info(f"Current cities XML: {XML_FILE}")
        logger.info(f"Current country XML: {COUNTRY_XML_FILE}")
        logger.info(f"Cities archive: {get_archive_path(today)}")
        logger.info(f"Country archive: {get_country_archive_path(today)}")
    elif success_count == 1:
        logger.warning("Partial success: Only 1 of 2 XML files downloaded")
    else:
        logger.error("Failed to download any XML files")
        print_separator(logger)
        return False

    if deleted_count > 0:
        logger.info(f"Cleaned up {deleted_count} old archive file(s)")

    print_separator(logger)

    return success_count > 0


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Download and convert IMS weather forecast XML'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate download without saving files'
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

    # Run download workflow
    success = download_and_convert(logger, dry_run=args.dry_run)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
