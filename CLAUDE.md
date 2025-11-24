# CLAUDE.md

## Project Overview

IMS Weather Forecast V2 - Map-based Instagram story generator with geographic city placement. Downloads forecast data from Israel Meteorological Service, generates 1080x1920px images with cities positioned on Israel map.

**Status**: V2 Development (Milestone 1)

## Essential Commands

```bash
# Run complete workflow
python forecast_workflow.py

# Dry-run (preview without email)
python forecast_workflow.py --dry-run

# Download XML only
python download_forecast.py

# Extract forecast data
python extract_forecast.py

# Test email delivery
python send_email_smtp.py --dry-run

# View logs
cat logs/forecast_automation.log
```

## Project Structure

```
├── forecast_workflow.py      # Main orchestration
├── download_forecast.py      # Cities XML download
├── extract_forecast.py       # Data extraction
├── generate_forecast_map.py  # V2 map-based generator (TODO)
├── send_email_smtp.py        # Email delivery
├── utils.py                  # Shared utilities
├── assets/
│   ├── weather_icons 2.0/    # New icon set
│   └── map/                  # Israel map PNG (TODO)
└── archive/v1/               # Archived v1 code
```

## Code Style

- Use `pathlib` for all file paths
- Use `setup_logging()` from utils.py for logging
- UTF-8 encoding everywhere
- Absolute paths preferred over relative

## Critical Implementation Notes

### XML Encoding
IMPORTANT: IMS XML files are ISO-8859-8 encoded. Always convert to UTF-8 before parsing.

### Hebrew Text (RTL)
- Use `bidi.algorithm.get_display()` for RTL text rendering
- Or use Pillow's `direction='rtl'` with Raqm support

### Variable Fonts
IMPORTANT: Axis order is `[width, weight]` for set_variation_by_axes()
```python
font.set_variation_by_axes([100, 600])  # width=100, weight=600
```

### City Coordinates
Cities use manual x,y positions from Figma design (not calculated from lat/long).

## Data Sources

- Cities forecast: `https://ims.gov.il/.../isr_cities.xml`
- Country forecast: `https://ims.gov.il/.../isr_country.xml` (textual description)

## Current Milestone

**Milestone 1: Data Pipeline Update**
- [ ] Download and parse isr_country.xml
- [ ] Add Hebrew calendar conversion (pyluach)
- [ ] Update extraction to include weather description
- [ ] Test complete data pipeline

## Version

- V2 Development started: 2025-11-24
- V1 archived: See `archive/v1/` or `git checkout v1.0-final`
