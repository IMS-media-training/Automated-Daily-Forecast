# IMS Weather Forecast Automation

> Automated daily weather forecast generator for Israeli cities - from IMS data to Instagram-ready stories

## Overview

This project automates the creation of daily weather forecast images for the Israel Meteorological Service (IMS) social media accounts. It downloads forecast data from IMS, processes it, and generates beautifully designed Instagram story images featuring 15 major Israeli cities.

**Current Status:** Phase 4 Complete ✅ - Automation & Email Delivery via GitHub Actions

## Features

### Phase 1: Data Collection & Processing ✅ COMPLETE
- ✅ Downloads daily forecast XML from IMS website
- ✅ Handles Hebrew encoding conversion (ISO-8859-8 → UTF-8)
- ✅ Extracts weather data for 15 Israeli cities
- ✅ Sorts cities geographically (north to south)
- ✅ Archives historical data (14-day retention)
- ✅ Comprehensive error handling and logging
- ✅ Dry-run mode for safe testing

### Phase 2: Image Generation (Single City POC) ✅ COMPLETE
- ✅ Variable font with Hebrew support (configurable weight/width axes)
- ✅ iOS-style weather emoji icons (PNG overlays)
- ✅ Professional header with IMS logo and forecast date (DD/MM/YYYY)
- ✅ Robust Hebrew RTL text rendering (auto-adapts to environment)
- ✅ White header + sky-to-white gradient background
- ✅ Easy-to-configure design constants
- ✅ Generates 1080x1920px Instagram story images
- ✅ Proof-of-concept with Tel Aviv data (exploration/generate_image.py)

### Phase 3: Complete Design - All 15 Cities ✅ COMPLETE
- ✅ Single image displaying all 15 cities (1080x1920px Instagram story)
- ✅ Vertical layout with city rows (north to south)
- ✅ Weather icon, temperature, and Hebrew city name for each
- ✅ Open Sans variable font (weight 300-800, width 75-100)
- ✅ Vertically centered list with balanced padding
- ✅ Header elements aligned with main list edges
- ✅ Production-ready design (generate_forecast_image.py)

### phase 3.5: Finalizing The Icon Gallery ✅ COMPLETE
- ✅ Transformed official IMS documentation from Hebrew PDF to JSON format
- ✅ Found complete Twemoji icon set covering all 23 IMS weather codes
- ✅ Mapped all weather codes to appropriate icons (11 unique icons)
- ✅ Full icon coverage with proper attribution (CC-BY 4.0)

### Phase 4: Automation & Email Delivery ✅ COMPLETE
- ✅ SMTP integration for professional email delivery
- ✅ Automated daily execution via GitHub Actions (6:00 AM Israel time)
- ✅ External HTML email template with IMS branding
- ✅ Professional design: Orange-to-blue gradient, Noto Sans Hebrew font
- ✅ Easy template customization without code changes
- ✅ Manual trigger support for testing
- ✅ Artifact storage (images & logs) for 90 days
- ✅ Environment variable configuration for secure credentials
- ✅ Dry-run mode for safe testing

### Recent Enhancements
- ✅ **Daily Random Gradients:** The forecast image background now features a new, randomly selected gradient every day.
- ✅ **Gradient Test Mode:** A new mode to generate test images with different gradient colors.

### Phase 5: Server Deployment 📅 FUTURE
- Deployment to IMS production servers
- Linux compatibility testing
- Production monitoring and maintenance

## Quick Start

### Prerequisites

- Python 3.13+ installed
- Internet connection (to download XML from IMS)
- Windows/Linux operating system

### Installation

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/noamweisss/Automated-Daily-Forecast.git
   cd Automated-Daily-Forecast
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root and add your SMTP credentials. You can copy the example file:
    ```bash
    cp .env.example .env
    ```
    Then, edit the `.env` file with your credentials.


### Usage

#### Run the complete workflow
```bash
# Download today's forecast, generate the image, and send the email
python forecast_workflow.py

# Preview without making changes (dry-run mode)
python forecast_workflow.py --dry-run

# Extract data for a specific date
python forecast_workflow.py --date 2025-10-15
```

#### Run individual components

**Download XML from IMS:**
```bash
python download_forecast.py
```

**Extract forecast data:**
```bash
python extract_forecast.py
python extract_forecast.py --date 2025-10-15
```

**Generate forecast image:**
```bash
python generate_forecast_image.py
```

**Send the forecast email:**
```bash
python send_email_smtp.py
```

**Test gradient generation:**
```bash
python test_gradients.py
```

**View logs:**
```bash
tail -f logs/forecast_automation.log
```

### GitHub Actions Automation

The project is configured to run automatically via GitHub Actions:

**Scheduled Execution:**
- Runs daily at 6:00 AM Israel time (3:00 AM UTC)
- Downloads latest forecast from IMS
- Generates Instagram story image
- Sends email to configured recipients via SMTP

**Manual Execution:**
- Go to: Actions → IMS Daily Weather Forecast → Run workflow
- Choose dry-run mode to test without sending email
- View generated images in workflow artifacts

**Required GitHub Secrets:**
Configure these in: Settings → Secrets and variables → Actions → New repository secret
1. `EMAIL_ADDRESS` - Your sender email address
2. `EMAIL_PASSWORD` - Your email account password or app password
3. `RECIPIENT_EMAIL` - The recipient's email address
4. `SMTP_SERVER` - Your SMTP server address
5. `SMTP_PORT` - Your SMTP port

**Monitoring:**
- View workflow runs: Actions tab
- Download artifacts: Generated images and logs available for 90 days
- Email notifications: GitHub sends email on workflow failures

## Project Structure

```
Automated-Daily-Forecast/
├── forecast_workflow.py      # Main orchestration script
├── download_forecast.py      # XML download & encoding
├── extract_forecast.py       # Data extraction
├── generate_forecast_image.py # Image generation
├── send_email_smtp.py        # Email delivery (SMTP)
├── email_template.html       # Professional email template
├── utils.py                  # Shared utilities
├── archive/                  # Historical XML (14 days)
├── assets/                   # Logos, weather icons, and fonts
├── docs/                     # Project documentation
├── exploration/              # Test & development scripts
├── logs/                     # Automation logs
├── output/                   # Generated images
├── .github/                  # GitHub Actions workflows
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Weather Data

The automation processes forecasts for **15 Israeli cities**, sorted north to south:

1. Qazrin
2. Zefat (Safed)
3. Bet Shean
4. Tiberias
5. Haifa
6. Nazareth
7. Afula
8. Tel Aviv-Yafo
9. Lod
10. Ashdod
11. Jerusalem
12. En Gedi
13. Beer Sheva
14. Mizpe Ramon
15. Elat (Eilat)

**Data includes:**
- Maximum & minimum temperatures
- Weather condition codes
- Humidity levels (Day 1)
- Wind information (Day 1)

## Configuration

### Data Processing
Key settings are defined in [utils.py](utils.py):

| Setting | Value | Description |
|---------|-------|-------------|
| `ARCHIVE_RETENTION_DAYS` | 14 days | How long to keep historical XML files |
| `EXPECTED_CITY_COUNT` | 15 cities | Number of cities we expect in the data |
| `XML_FILE` | `isr_cities_utf8.xml` | Main working XML file |

### Image Generation
Design settings in [generate_forecast_image.py](generate_forecast_image.py):
- **Open Sans Font**: Variable axes (weight 300-800, width 75-100)
- **Image Size**: 1080x1920px (Instagram story format)
- **Header**: 180px white section with logo and date aligned to list edges
- **Layout**: Vertically centered city list with balanced padding
- **Weather Icons**: 65px iOS-style emoji PNGs per city row
- **Cities**: All 15 cities in single image
- All visual parameters configurable via constants at top of file

## Logging

All operations are logged to:
- **Console:** Real-time feedback during execution
- **Log file:** `logs/forecast_automation.log` (persistent record)

Log levels: INFO, WARNING, ERROR

## Development

### Running Tests

```bash
# Test minimal extraction (1 city)
python exploration/test_extraction_minimal.py

# Test full extraction (all 15 cities)
python exploration/extract_all_cities.py

# Inspect XML structure
python exploration/inspect_xml.py
```

## Version Control

This project uses Git for version control. See [GIT_GUIDE.md](docs/dev-guides/GIT_GUIDE.md) for basic Git commands and workflows.

### Version History
See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Troubleshooting

### Common Issues

**Problem:** `ModuleNotFoundError: No module named 'requests'`
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Problem:** Hebrew text displays as gibberish
**Solution:** Ensure the XML file is UTF-8 encoded. The download script handles this automatically.

**Problem:** No cities extracted
**Solution:** Check that the target date exists in the XML file. IMS provides 4-day forecasts.

**Problem:** Workflow fails to download XML
**Solution:** Check internet connection. The script will automatically fall back to archived XML if available.

## Contributing

This project is developed by the IMS Design & Social Media Team.

**Development approach:**
- Incremental development by phase
- Comprehensive testing before advancing
- Clear documentation for maintainability
- No hard deadlines - focus on quality

## Technical Requirements

- **Python:** 3.13+ (tested on 3.13.2)
- **Platform:** Windows (primary), Linux-compatible design
- **Network:** Internet access to download XML from IMS servers

### Dependencies
See [requirements.txt](requirements.txt) for full list:
- `requests>=2.31.0` - XML download from IMS
- `Pillow>=10.0.0` - Image generation with Hebrew RTL support
- `python-bidi>=0.4.2` - Hebrew RTL text rendering
- `python-dotenv>=1.0.0` - Environment variable management

## Data Source

Weather data is provided by the Israel Meteorological Service (IMS):
- **URL:** https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_cities.xml
- **Update frequency:** Multiple times daily
- **Format:** XML with ISO-8859-8 encoding (Hebrew)
- **Forecast range:** 4 days (today + 3 days)

## License

Internal IMS project. For official use by IMS Social Media Team.

## Contact

**Project Lead:** Noam W (IMS Design Team)
**Email:** noamweisss@icloud.com
**Organization:** Israel Meteorological Service

For deployment questions, consult IMS IT Department.

---

**Last Updated:** November 13, 2025