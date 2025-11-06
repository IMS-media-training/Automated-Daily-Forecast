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
        'RECIPIENT_EMAIL': 'Recipient email address',
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


def create_email_html(forecast_date, recipient_name="Weather Forecast Team"):
    """
    Create HTML email body with Hebrew RTL support.

    Args:
        forecast_date (str): Date in DD/MM/YYYY format (Hebrew convention)
        recipient_name (str): Name to use in greeting

    Returns:
        str: HTML email body
    """
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="he">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                direction: rtl;
                text-align: right;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .content {{
                padding: 30px 20px;
                color: #333333;
                line-height: 1.6;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .image-container {{
                text-align: center;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .footer {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666666;
            }}
            .footer a {{
                color: #667eea;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>תחזית מזג האוויר היומית</h1>
                <p style="margin: 5px 0 0 0; font-size: 16px;">Daily Weather Forecast</p>
            </div>

            <div class="content">
                <p>שלום {recipient_name},</p>

                <p>מצורפת תחזית מזג האוויר ליום <strong>{forecast_date}</strong> עבור 15 הערים המרכזיות בישראל.</p>

                <p>התחזית כוללת:</p>
                <ul>
                    <li>טמפרטורות מקסימום ומינימום</li>
                    <li>תיאור מזג האוויר (אייקונים)</li>
                    <li>ערים ממוינות מצפון לדרום</li>
                </ul>

                <p>התמונה מוכנה לפרסום ב-Instagram Stories (1080x1920 פיקסלים).</p>
            </div>

            <div class="image-container">
                <p style="margin-bottom: 10px; color: #666;"><strong>תחזית יומית - Daily Forecast</strong></p>
                <p style="font-size: 12px; color: #999; margin-top: 5px;">
                    התמונה מצורפת לאימייל / Image attached to email
                </p>
            </div>

            <div class="footer">
                <p>מערכת אוטומטית לתחזית מזג אוויר - השירות המטאורולוגי הישראלי</p>
                <p>IMS Weather Forecast Automation System</p>
                <p style="margin-top: 10px;">
                    <a href="https://ims.gov.il">ims.gov.il</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
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
        recipient_email = env_vars['RECIPIENT_EMAIL']
        smtp_server = env_vars['SMTP_SERVER']
        smtp_port = env_vars['SMTP_PORT']

        logger.info(f"SMTP Configuration:")
        logger.info(f"  Server: {smtp_server}:{smtp_port}")
        logger.info(f"  From: {sender_email}")
        logger.info(f"  To: {recipient_email}")

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
        msg['To'] = recipient_email
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
        logger.info(f"To: {recipient_email}")
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
  RECIPIENT_EMAIL    - Recipient email address
  SMTP_SERVER        - SMTP server (smtp.gmail.com for Gmail)
  SMTP_PORT          - SMTP port (587 for TLS)

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
