"""
IMS Weather Forecast Automation - Main Workflow

Main orchestration script that coordinates the complete daily workflow:
1. Download XML from IMS website
2. Extract forecast data
3. Generate Instagram story image (Phase 2 - future)
4. Send email to social media manager (Phase 4 - future)

This script is designed to run automatically every morning at 6:00 AM.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import random
import xml.etree.ElementTree as ET
import glob

from utils import setup_logging, get_today_date, print_separator, XML_FILE, ARCHIVE_DIR
from download_forecast import download_and_convert
from extract_forecast import extract_forecast, get_available_dates, parse_xml_file
from generate_forecast_image import generate_all_cities_image
# Note: send_email_smtp is imported conditionally in step_send_email() to avoid
# requiring email dependencies in dry-run mode


# ============================================================================
# WORKFLOW CONFIGURATION
# ============================================================================

# Phase 1: Download + Extract only
# Phase 2: Add image generation (single city POC)
# Phase 3: All 15 cities image generation
# Phase 4: Add email delivery

CURRENT_PHASE = 4


# ============================================================================
# GRADIENT TEST HELPERS
# ============================================================================

def get_next_dry_run_filename(output_dir: Path) -> Path:
    """
    Get the next sequential filename for dry-run images (test_000.jpg, test_001.jpg, etc.).

    Args:
        output_dir: Directory to save dry-run images

    Returns:
        Path object for next available filename
    """
    # Ensure dry-run directory exists
    dry_run_dir = output_dir / "dry-run"
    dry_run_dir.mkdir(parents=True, exist_ok=True)

    # Find highest existing test number
    existing_files = list(dry_run_dir.glob("test_*.jpg"))
    if not existing_files:
        next_number = 0
    else:
        # Extract numbers from filenames
        numbers = []
        for file in existing_files:
            try:
                # Extract number from "test_XXX.jpg"
                num_str = file.stem.split('_')[1]
                numbers.append(int(num_str))
            except (IndexError, ValueError):
                continue

        next_number = max(numbers) + 1 if numbers else 0

    # Format with 3 digits (000, 001, 002, etc.)
    filename = dry_run_dir / f"test_{next_number:03d}.jpg"
    return filename


def get_random_date_from_xml(logger) -> Optional[str]:
    """
    Get a random date from available XML data (main file or archive).

    Args:
        logger: Logger instance

    Returns:
        Random date string in YYYY-MM-DD format, or None if no dates available
    """
    # Try main XML file first
    xml_path = Path(__file__).parent / XML_FILE

    if xml_path.exists():
        logger.info(f"Reading dates from main XML: {xml_path.name}")
        root = parse_xml_file(xml_path, logger)
        if root is not None:
            available_dates = get_available_dates(root, logger)
            if available_dates:
                selected_date = random.choice(available_dates)
                logger.info(f"Randomly selected date: {selected_date}")
                return selected_date

    # Fallback to archive if main file not available
    logger.info("Main XML not found, checking archive...")
    archive_dir = Path(__file__).parent / ARCHIVE_DIR

    if not archive_dir.exists():
        logger.warning("Archive directory does not exist")
        return None

    # Get all archive files
    archive_files = sorted(glob.glob(str(archive_dir / "isr_cities_*.xml")), reverse=True)

    if not archive_files:
        logger.warning("No archive XML files found")
        return None

    # Try each archive file until we find dates
    for archive_path in archive_files:
        logger.info(f"Reading dates from archive: {Path(archive_path).name}")
        root = parse_xml_file(Path(archive_path), logger)
        if root is not None:
            available_dates = get_available_dates(root, logger)
            if available_dates:
                selected_date = random.choice(available_dates)
                logger.info(f"Randomly selected date: {selected_date}")
                return selected_date

    logger.warning("No dates found in any XML files")
    return None


def resolve_gradient_test_date(gradient_test: str, logger) -> Optional[str]:
    """
    Resolve gradient test mode to a specific date.

    Args:
        gradient_test: One of 'today', 'tomorrow', or 'random'
        logger: Logger instance

    Returns:
        Resolved date string in YYYY-MM-DD format
    """
    if gradient_test == 'today':
        date = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"Gradient test mode 'today': {date}")
        return date

    elif gradient_test == 'tomorrow':
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        logger.info(f"Gradient test mode 'tomorrow': {date}")
        return date

    elif gradient_test == 'random':
        logger.info("Gradient test mode 'random': selecting random date from available data...")
        return get_random_date_from_xml(logger)

    else:
        logger.error(f"Invalid gradient test mode: {gradient_test}")
        return None


# ============================================================================
# WORKFLOW STEPS
# ============================================================================

def step_download(logger, dry_run: bool = False) -> bool:
    """
    Step 1: Download and convert XML from IMS.

    Args:
        logger: Logger instance
        dry_run: If True, simulate without saving

    Returns:
        True if successful, False otherwise
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 1: DOWNLOAD XML")
    logger.info("=" * 60)

    success = download_and_convert(logger, dry_run=dry_run)

    if success:
        logger.info("Download step completed successfully")
    else:
        logger.error("Download step failed")

    return success


def step_extract(logger, target_date: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Step 2: Extract forecast data from XML.

    Args:
        logger: Logger instance
        target_date: Target date (default: today)

    Returns:
        List of city data dictionaries, or None if failed
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 2: EXTRACT FORECAST DATA")
    logger.info("=" * 60)

    cities_data = extract_forecast(
        target_date=target_date,
        use_archive_fallback=True,
        logger=logger
    )

    if cities_data:
        logger.info("Extraction step completed successfully")
    else:
        logger.error("Extraction step failed")

    return cities_data


def step_generate_image(cities_data: List[Dict], forecast_date: str, logger, dry_run: bool = False) -> tuple[bool, Optional[Path]]:
    """
    Step 3: Generate Instagram story image (Phase 3 - All 15 Cities).

    Args:
        cities_data: List of city data dictionaries
        forecast_date: Forecast date in YYYY-MM-DD format
        logger: Logger instance
        dry_run: If True, save to dry-run subfolder with sequential naming

    Returns:
        Tuple of (success: bool, output_path: Path or None)
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: GENERATE IMAGE (Phase 3 - All 15 Cities)")
    logger.info("=" * 60)

    try:
        # Setup output path
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)

        if dry_run:
            # Dry-run mode: save to dry-run subfolder with sequential naming
            output_path = get_next_dry_run_filename(output_dir)
            logger.info("DRY RUN: Generating test image with sequential naming")
            logger.info(f"Output path: {output_path}")
        else:
            # Production mode: save to standard location
            output_path = output_dir / "daily_forecast.jpg"
            logger.info(f"Generating forecast image for {len(cities_data)} cities")
            logger.info(f"Output path: {output_path}")

        # Generate image
        success = generate_all_cities_image(cities_data, forecast_date, output_path)

        if success:
            logger.info("Image generation completed successfully!")
            if dry_run:
                logger.info(f"✓ Test image saved: {output_path.name}")
            return True, output_path
        else:
            logger.error("Image generation failed")
            return False, None

    except Exception as e:
        logger.error(f"Image generation error: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def step_send_email(image_path: str, forecast_date: str, logger, dry_run: bool = False) -> bool:
    """
    Step 4: Send email to social media manager (Phase 4).

    Uses send_email_smtp.py for SMTP-based email delivery.
    Email failures are CRITICAL - workflow will fail if email fails.

    Args:
        image_path: Path to generated image
        forecast_date: Forecast date in YYYY-MM-DD format (for logging only - email calculates internally)
        logger: Logger instance (for workflow logging - email has its own logger)
        dry_run: If True, skip email sending entirely (no import needed)

    Returns:
        True if successful, False otherwise
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 4: SEND EMAIL (Phase 4 - SMTP)")
    logger.info("=" * 60)

    # Skip email entirely in dry-run mode (don't even import the module)
    if dry_run:
        logger.info("DRY RUN: Skipping email delivery")
        logger.info(f"Would send email with image: {image_path}")
        return True

    try:
        # Import send_email only when actually needed (not in dry-run)
        # This avoids requiring email dependencies when just testing gradients
        from send_email_smtp import send_email

        # Note: send_email() uses its own logger and calculates forecast_date internally
        # We only pass image_path and dry_run flag
        success = send_email(
            image_path=image_path,
            dry_run=False  # Already handled above
        )

        if success:
            logger.info("✓ Email delivery completed successfully!")
        else:
            logger.error("✗ Email delivery failed")
            logger.error("Email failure is CRITICAL - check environment variables and configuration")

        return success

    except Exception as e:
        logger.error(f"✗ Email delivery error: {e}")
        logger.error("Email failure is CRITICAL - workflow cannot continue")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def run_workflow(dry_run: bool = False, target_date: Optional[str] = None, gradient_test: Optional[str] = None) -> bool:
    """
    Execute the complete daily forecast workflow.

    Args:
        dry_run: If True, simulate without making changes
        target_date: Target date for extraction (default: today)
        gradient_test: Gradient test mode ('today', 'tomorrow', or 'random') - overrides target_date

    Returns:
        True if successful, False if any step failed
    """
    # Setup logging
    logger = setup_logging()

    # Print workflow header
    print_separator(logger, "=", 60)
    logger.info("IMS WEATHER FORECAST AUTOMATION")
    logger.info(f"Phase {CURRENT_PHASE} - {'DRY RUN' if dry_run else 'PRODUCTION RUN'}")
    print_separator(logger, "=", 60)

    start_time = datetime.now()
    logger.info(f"Workflow started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Handle gradient test mode (overrides target_date)
    if gradient_test:
        logger.info(f"GRADIENT TEST MODE: {gradient_test}")
        resolved_date = resolve_gradient_test_date(gradient_test, logger)
        if resolved_date is None:
            logger.error("Failed to resolve gradient test date")
            return False
        target_date = resolved_date

    if target_date is None:
        target_date = get_today_date()

    logger.info(f"Target date: {target_date}")

    if dry_run:
        logger.info("DRY RUN MODE: Images will be generated, email will be skipped")

    # Track overall success
    workflow_success = True

    # ========================================================================
    # STEP 1: DOWNLOAD XML
    # ========================================================================

    # Note: Always download XML even in dry-run mode (extraction needs the file)
    # Dry-run only affects image generation and email sending
    if not step_download(logger, dry_run=False):
        logger.error("Workflow aborted: Download failed")
        logger.info("Note: Extraction will attempt to use existing/archived XML")
        # Don't abort yet - extraction might work with existing data

    # ========================================================================
    # STEP 2: EXTRACT FORECAST DATA
    # ========================================================================

    cities_data = step_extract(logger, target_date=target_date)

    if cities_data is None:
        logger.error("Workflow failed: Extraction failed")
        workflow_success = False
    else:
        logger.info(f"Successfully extracted data for {len(cities_data)} cities")

        # ====================================================================
        # STEP 3: GENERATE IMAGE (Phase 3 - All 15 Cities)
        # ====================================================================

        generated_image_path = None
        if CURRENT_PHASE >= 2:
            image_success, generated_image_path = step_generate_image(cities_data, target_date, logger, dry_run=dry_run)
            if not image_success:
                logger.error("Image generation failed")
                workflow_success = False
        else:
            logger.info("\nSkipping image generation (Phase 2/3 - not yet implemented)")

        # ====================================================================
        # STEP 4: SEND EMAIL (Phase 4)
        # ====================================================================

        if CURRENT_PHASE >= 4:
            # Use generated image path if available, otherwise fall back to default
            if generated_image_path:
                email_image_path = generated_image_path
            else:
                email_image_path = Path(__file__).parent / "output" / "daily_forecast.jpg"

            if not step_send_email(str(email_image_path), target_date, logger, dry_run=dry_run):
                logger.error("Email delivery failed")
                workflow_success = False
        else:
            logger.info("\nSkipping email delivery (Phase 4 - not yet implemented)")

    # ========================================================================
    # WORKFLOW SUMMARY
    # ========================================================================

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print_separator(logger, "=", 60)
    logger.info("WORKFLOW SUMMARY")
    print_separator(logger, "=", 60)

    logger.info(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"End time:   {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Duration:   {duration:.1f} seconds")
    logger.info(f"Target date: {target_date}")

    if workflow_success:
        logger.info("Status:     SUCCESS")
        logger.info("\nAll workflow steps completed successfully!")
    else:
        logger.error("Status:     FAILED")
        logger.error("\nOne or more workflow steps failed - check logs above")

    if dry_run:
        logger.info("\n[DRY RUN] Images generated to output/dry-run/ folder, email skipped")

    print_separator(logger, "=", 60)

    return workflow_success


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description='IMS Weather Forecast Automation - Main Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Normal run (download today's forecast and extract)
  python forecast_workflow.py

  # Dry run (preview without changing files)
  python forecast_workflow.py --dry-run

  # Extract specific date
  python forecast_workflow.py --date 2025-09-28

  # Test gradients with today's date
  python forecast_workflow.py --gradient-test today

  # Test gradients with tomorrow's date
  python forecast_workflow.py --gradient-test tomorrow

  # Test gradients with random date from available data
  python forecast_workflow.py --gradient-test random

  # Verbose output
  python forecast_workflow.py --verbose

This script is designed to run automatically via Windows Task Scheduler
every morning at 6:00 AM.
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate workflow without making changes'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Target date in YYYY-MM-DD format (default: today)'
    )
    parser.add_argument(
        '--gradient-test',
        type=str,
        choices=['today', 'tomorrow', 'random'],
        help='Gradient test mode: "today", "tomorrow", or "random" (picks random date from available data). Overrides --date.'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Note: Verbose flag is handled by individual modules
    if args.verbose:
        print("Note: Verbose logging should be configured in utils.py setup_logging()")

    # Run workflow
    success = run_workflow(
        dry_run=args.dry_run,
        target_date=args.date,
        gradient_test=args.gradient_test
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
