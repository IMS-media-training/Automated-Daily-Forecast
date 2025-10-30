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
from datetime import datetime
from typing import Optional, List, Dict

from utils import setup_logging, get_today_date, print_separator
from download_forecast import download_and_convert
from extract_forecast import extract_forecast
from generate_forecast_image import generate_all_cities_image


# ============================================================================
# WORKFLOW CONFIGURATION
# ============================================================================

# Phase 1: Download + Extract only
# Phase 2: Add image generation (single city POC)
# Phase 3: All 15 cities image generation
# Phase 4: Add email delivery

CURRENT_PHASE = 3


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


def step_generate_image(cities_data: List[Dict], forecast_date: str, logger, dry_run: bool = False) -> bool:
    """
    Step 3: Generate Instagram story image (Phase 3 - All 15 Cities).

    Args:
        cities_data: List of city data dictionaries
        forecast_date: Forecast date in YYYY-MM-DD format
        logger: Logger instance
        dry_run: If True, simulate without creating image

    Returns:
        True if successful, False otherwise
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: GENERATE IMAGE (Phase 3 - All 15 Cities)")
    logger.info("=" * 60)

    if dry_run:
        logger.info("DRY RUN: Skipping image generation")
        logger.info(f"Would generate 1080x1920px image with {len(cities_data)} cities")
        return True

    try:
        # Setup output path
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "daily_forecast.jpg"

        logger.info(f"Generating forecast image for {len(cities_data)} cities")
        logger.info(f"Output path: {output_path}")

        # Generate image
        success = generate_all_cities_image(cities_data, forecast_date, output_path)

        if success:
            logger.info("Image generation completed successfully!")
        else:
            logger.error("Image generation failed")

        return success

    except Exception as e:
        logger.error(f"Image generation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_send_email(image_path: str, logger, dry_run: bool = False) -> bool:
    """
    Step 4: Send email to social media manager (Phase 4 - Not Implemented Yet).

    Args:
        image_path: Path to generated image
        logger: Logger instance
        dry_run: If True, simulate without sending

    Returns:
        True if successful, False otherwise
    """
    logger.info("\n" + "=" * 60)
    logger.info("STEP 4: SEND EMAIL (Phase 4 - Not Implemented)")
    logger.info("=" * 60)

    logger.info("Email delivery will be implemented in Phase 4")
    logger.info(f"Would send image: {image_path}")

    # Placeholder for future implementation
    return True


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def run_workflow(dry_run: bool = False, target_date: Optional[str] = None) -> bool:
    """
    Execute the complete daily forecast workflow.

    Args:
        dry_run: If True, simulate without making changes
        target_date: Target date for extraction (default: today)

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

    if target_date is None:
        target_date = get_today_date()

    logger.info(f"Target date: {target_date}")

    if dry_run:
        logger.info("DRY RUN MODE: No files will be modified")

    # Track overall success
    workflow_success = True

    # ========================================================================
    # STEP 1: DOWNLOAD XML
    # ========================================================================

    if not step_download(logger, dry_run=dry_run):
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

        if CURRENT_PHASE >= 2:
            if not step_generate_image(cities_data, target_date, logger, dry_run=dry_run):
                logger.error("Image generation failed")
                workflow_success = False
        else:
            logger.info("\nSkipping image generation (Phase 2/3 - not yet implemented)")

        # ====================================================================
        # STEP 4: SEND EMAIL (Phase 4 - Future)
        # ====================================================================

        if CURRENT_PHASE >= 4:
            if not step_send_email("output/weather_story_DATE.jpg", logger, dry_run=dry_run):
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
        logger.info("\n[DRY RUN] No files were modified")

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
        target_date=args.date
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
