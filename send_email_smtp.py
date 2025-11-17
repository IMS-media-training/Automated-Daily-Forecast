#!/usr/bin/env python3
"""
IMS Weather Forecast - Email Delivery (SMTP)
Phase 4 v2: Simple SMTP implementation with Gmail

Sends daily weather forecast images via email using Python's built-in SMTP library.
"""

import os
import sys
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from datetime import datetime

# CRITICAL: Load environment variables from .env file
# This was MISSING in Phase 4 v1 - causing all local runs to fail!
from dotenv import load_dotenv
load_dotenv()

from utils import setup_logging

# Initialize logging
logger = setup_logging()

# Paths
BASE_DIR = Path(__file__).parent.absolute()
DEFAULT_IMAGE_PATH = BASE_DIR / "output" / "daily_forecast.jpg"
EMAIL_TEMPLATE_PATH = BASE_DIR / "email_template.html"
RECIPIENTS_FILE_PATH = BASE_DIR / "recipients.txt"


def validate_environment_variables():
    """
    Validate that all required environment variables are present.

    This is CRITICAL - Phase 4 v1 failed because variables were missing/misnamed.
    Fail fast with clear error messages.

    Returns:
        dict: Dictionary of validated environment variables

    Raises:
        ValueError: If any required variable is missing
    """
    required_vars = {
        'EMAIL_ADDRESS': 'Sender email address (Gmail account)',
        'EMAIL_PASSWORD': 'Gmail App Password (16 characters)',
        'SMTP_SERVER': 'SMTP server address (e.g., smtp.gmail.com)',
        'SMTP_PORT': 'SMTP port (e.g., 587 for TLS)',
    }

    env_vars = {}
    missing_vars = []

    for var_name, description in required_vars.items():
        value = os.environ.get(var_name)
        if not value:
            missing_vars.append(f"  - {var_name}: {description}")
        else:
            env_vars[var_name] = value

    if missing_vars:
        error_msg = (
            "\n" + "="*70 + "\n"
            "ERROR: Missing required environment variables\n"
            "="*70 + "\n\n"
            "The following variables are not set:\n\n"
            + "\n".join(missing_vars) + "\n\n"
            "To fix this:\n"
            "1. Copy .env.example to .env\n"
            "2. Fill in your actual credentials in .env\n"
            "3. Verify .env is loaded (check file exists in project root)\n\n"
            "Security Note: .env file is in .gitignore - it will never be committed\n"
            "="*70
        )
        raise ValueError(error_msg)

    # Convert port to integer
    try:
        env_vars['SMTP_PORT'] = int(env_vars['SMTP_PORT'])
    except ValueError:
        raise ValueError(f"SMTP_PORT must be a number, got: {env_vars['SMTP_PORT']}")

    return env_vars


def read_recipients():
    """
    Read email recipients from recipients.txt file.

    Format:
        - One email address per line
        - Lines starting with # are comments (ignored)
        - Empty lines are ignored

    Returns:
        list: List of recipient email addresses

    Raises:
        FileNotFoundError: If recipients.txt doesn't exist
        ValueError: If no valid recipients found
    """
    if not RECIPIENTS_FILE_PATH.exists():
        error_msg = (
            "\n" + "="*70 + "\n"
            "ERROR: Recipients file not found\n"
            "="*70 + "\n\n"
            f"Expected file: {RECIPIENTS_FILE_PATH}\n\n"
            "To fix this:\n"
            "1. Copy recipients.txt.example to recipients.txt\n"
            "2. Edit recipients.txt and add email addresses (one per line)\n"
            "3. Lines starting with # are comments\n"
            "4. Empty lines are ignored\n\n"
            "Example:\n"
            "  user1@example.com\n"
            "  user2@gmail.com\n"
            "  # This is a comment\n"
            "="*70
        )
        raise FileNotFoundError(error_msg)

    recipients = []
    with open(RECIPIENTS_FILE_PATH, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Basic email validation (contains @ symbol)
            if '@' not in line:
                logger.warning(f"Line {line_num}: Invalid email format (missing @): {line}")
                continue

            recipients.append(line)

    if not recipients:
        error_msg = (
            "\n" + "="*70 + "\n"
            "ERROR: No valid recipients found\n"
            "="*70 + "\n\n"
            f"File: {RECIPIENTS_FILE_PATH}\n\n"
            "The recipients.txt file exists but contains no valid email addresses.\n"
            "Add at least one email address (one per line).\n"
            "="*70
        )
        raise ValueError(error_msg)

    return recipients


def create_email_html(forecast_date):
    """
    Create HTML email body with Hebrew RTL support by reading from a template file.

    Args:
        forecast_date (str): Date in DD/MM/YYYY format (Hebrew convention)

    Returns:
        str: HTML email body
    """
    if not EMAIL_TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Email template file not found: {EMAIL_TEMPLATE_PATH}")

    with open(EMAIL_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Use .replace() to insert dynamic content (avoids conflicts with CSS braces)
    html = html_template.replace("{forecast_date}", forecast_date)
    return html


def send_email(image_path=None, dry_run=False):
    """
    Send forecast email via SMTP with image attachment.

    Args:
        image_path (Path, optional): Path to forecast image. Defaults to output/daily_forecast.jpg
        dry_run (bool): If True, validate settings but don't send email

    Returns:
        bool: True if email sent successfully (or dry-run passed), False otherwise
    """
    try:
        # Validate environment variables first
        logger.info("Validating environment variables...")
        env_vars = validate_environment_variables()

        sender_email = env_vars['EMAIL_ADDRESS']
        sender_password = env_vars['EMAIL_PASSWORD']
        smtp_server = env_vars['SMTP_SERVER']
        smtp_port = env_vars['SMTP_PORT']

        # Read recipients from recipients.txt
        logger.info("Reading recipients from recipients.txt...")
        recipients = read_recipients()

        logger.info(f"SMTP Configuration:")
        logger.info(f"  Server: {smtp_server}:{smtp_port}")
        logger.info(f"  From: {sender_email}")
        logger.info(f"  To: {len(recipients)} recipient(s)")
        for recipient in recipients:
            logger.info(f"      - {recipient}")

        # Use default image path if not specified
        if image_path is None:
            image_path = DEFAULT_IMAGE_PATH
        else:
            image_path = Path(image_path)

        # Validate image exists
        if not image_path.exists():
            logger.error(f"Forecast image not found: {image_path}")
            logger.error("Generate the image first using: python generate_forecast_image.py")
            return False

        logger.info(f"Image: {image_path}")

        # Get forecast date from today
        forecast_date = datetime.now().strftime("%d/%m/%Y")

        # Create email message
        logger.info("Creating email message...")
        msg = MIMEMultipart('related')
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)  # Multiple recipients separated by commas
        msg['Subject'] = f"תחזית מזג אוויר יומית - {forecast_date} | Daily Weather Forecast"

        # Create HTML body
        html_body = create_email_html(forecast_date)
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        # Attach forecast image
        logger.info("Attaching forecast image...")
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data, name=image_path.name)
            image.add_header('Content-Disposition', 'attachment', filename=image_path.name)
            msg.attach(image)

        if dry_run:
            logger.info("\n" + "="*70)
            logger.info("DRY RUN MODE - Email not sent")
            logger.info("="*70)
            logger.info("Email configuration validated successfully!")
            logger.info(f"Subject: {msg['Subject']}")
            logger.info(f"From: {msg['From']}")
            logger.info(f"To: {msg['To']}")
            logger.info(f"Attachment: {image_path.name} ({len(img_data):,} bytes)")
            logger.info("="*70)
            logger.info("\nTo send the email for real, run without --dry-run flag")
            return True

        # Send email via SMTP
        logger.info(f"Connecting to SMTP server {smtp_server}:{smtp_port}...")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(0)  # Set to 1 for verbose SMTP debugging

            logger.info("Starting TLS encryption...")
            server.starttls()

            logger.info("Logging in to SMTP server...")
            server.login(sender_email, sender_password)

            logger.info("Sending email...")
            server.send_message(msg)

        logger.info("\n" + "="*70)
        logger.info("✓ Email sent successfully!")
        logger.info("="*70)
        logger.info(f"From: {sender_email}")
        logger.info(f"To: {len(recipients)} recipient(s)")
        for recipient in recipients:
            logger.info(f"    - {recipient}")
        logger.info(f"Subject: {msg['Subject']}")
        logger.info(f"Attachment: {image_path.name}")
        logger.info("="*70)

        return True

    except ValueError as e:
        # Configuration error (missing env vars)
        logger.error(str(e))
        return False

    except smtplib.SMTPAuthenticationError:
        logger.error("\n" + "="*70)
        logger.error("SMTP Authentication Failed")
        logger.error("="*70)
        logger.error("\nPossible causes:")
        logger.error("1. Incorrect email address or password")
        logger.error("2. Not using an App Password (required for Gmail)")
        logger.error("3. 2-Step Verification not enabled on Google account")
        logger.error("\nTo fix:")
        logger.error("1. Go to: https://myaccount.google.com/apppasswords")
        logger.error("2. Generate a new 16-character App Password")
        logger.error("3. Update EMAIL_PASSWORD in your .env file")
        logger.error("="*70)
        return False

    except smtplib.SMTPException as e:
        logger.error(f"\nSMTP Error: {e}")
        logger.error("\nCheck your SMTP settings:")
        logger.error(f"  SMTP_SERVER: {env_vars.get('SMTP_SERVER', 'NOT SET')}")
        logger.error(f"  SMTP_PORT: {env_vars.get('SMTP_PORT', 'NOT SET')}")
        logger.error("\nFor Gmail, use:")
        logger.error("  SMTP_SERVER=smtp.gmail.com")
        logger.error("  SMTP_PORT=587")
        return False

    except Exception as e:
        logger.error(f"\nUnexpected error: {e}")
        logger.exception("Full traceback:")
        return False


def main():
    """Main entry point for email sending script."""
    parser = argparse.ArgumentParser(
        description='Send daily weather forecast via email (SMTP)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test configuration without sending (recommended first step)
  python send_email_smtp.py --dry-run

  # Send email with default image (output/daily_forecast.jpg)
  python send_email_smtp.py

  # Send email with specific image
  python send_email_smtp.py --image-path output/custom_forecast.jpg

Environment Variables Required (create .env file):
  EMAIL_ADDRESS      - Sender Gmail address
  EMAIL_PASSWORD     - Gmail App Password (16 chars)
  SMTP_SERVER        - SMTP server (smtp.gmail.com for Gmail)
  SMTP_PORT          - SMTP port (587 for TLS)

Recipients Configuration (create recipients.txt file):
  One email address per line
  Lines starting with # are comments
  Empty lines are ignored

Security Notes:
  - .env file is in .gitignore and never committed
  - Use a temporary Gmail account for testing
  - Generate App Password at: https://myaccount.google.com/apppasswords
        """
    )

    parser.add_argument(
        '--image-path',
        type=str,
        help='Path to forecast image (default: output/daily_forecast.jpg)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate configuration without sending email'
    )

    args = parser.parse_args()

    logger.info("="*70)
    logger.info("IMS Weather Forecast - Email Delivery (Phase 4 v2)")
    logger.info("="*70)

    # Send email
    success = send_email(
        image_path=args.image_path,
        dry_run=args.dry_run
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
