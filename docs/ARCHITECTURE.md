# Architecture

## Overview

The IMS Weather Forecast Automation system downloads forecast data from the Israel Meteorological Service, processes it, generates Instagram-ready images, and delivers them via email.

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Download   │ ──▶ │   Extract   │ ──▶ │  Generate   │ ──▶ │    Email    │
│    XML      │     │    Data     │     │   Image     │     │   Deliver   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Data Sources

### Cities Forecast
- **URL:** `https://ims.gov.il/.../isr_cities.xml`
- **Content:** Weather data for 15 Israeli cities
- **Encoding:** ISO-8859-8 (converted to UTF-8)

### Country Forecast (V2)
- **URL:** `https://ims.gov.il/.../isr_country.xml`
- **Content:** Textual weather description for entire country
- **Usage:** Daily weather summary text

## Core Components

### forecast_workflow.py
Main orchestration script that coordinates all phases.

### download_forecast.py
Downloads both cities and country XML from IMS with retry logic, ISO-8859-8 to UTF-8 conversion, and archive management.

**Key Functions:**
- `download_xml_from_ims(url, logger)` - Downloads with retry logic
- `convert_encoding(raw_content, logger)` - ISO-8859-8 → UTF-8
- `download_and_convert(logger, dry_run)` - Main workflow

### extract_forecast.py
Parses XML files to extract weather data for 15 cities, textual description, and dates.

**Key Functions:**
- `extract_forecast()` - Returns dict with cities, description, date, hebrew_date
- `extract_weather_description()` - Parses country XML for Hebrew description
- `parse_xml_file()` - Handles XML parsing with error handling

**Return Structure:**
```python
{
    'cities': List[Dict],        # 15 cities with forecast data
    'description': str,          # Hebrew weather description from country XML
    'date': str,                 # Target date (YYYY-MM-DD)
    'hebrew_date': str           # Formatted Gregorian + Hebrew date
}
```

### generate_forecast_map.py (V2)
Generates map-based Instagram story image with geographic city positioning.

### send_email_smtp.py
Sends forecast image via SMTP with HTML template.

### utils.py
Shared utilities: logging, date handling, file management, validation, Hebrew calendar.

**Key Functions:**
- `setup_logging()` - Configures console and file logging
- `format_hebrew_date(date_str)` - Converts Gregorian to Hebrew calendar using pyluach
- `get_archive_path()` / `get_country_archive_path()` - Archive file management
- `validate_city_count()` / `validate_city_data()` - Data validation

**Hebrew Calendar:**
- Uses pyluach library for conversion
- Output: "DD/MM/YYYY ו׳ בכסלו תשפ״ו" (Gregorian + Hebrew)

## File Structure

```
├── forecast_workflow.py      # Orchestration
├── download_forecast.py      # Data download
├── extract_forecast.py       # Data extraction
├── generate_forecast_map.py  # Image generation (V2)
├── send_email_smtp.py        # Email delivery
├── utils.py                  # Utilities
├── assets/
│   ├── weather_icons 2.0/    # Weather icons
│   ├── map/                  # Israel map image
│   └── fonts/                # Noto Sans Hebrew
├── output/                   # Generated images
├── logs/                     # Application logs
└── archive/                  # Historical data
```

## Image Generation (V2)

### Layout
- Canvas: 1080x1920px (Instagram story)
- Background: Cyan-to-magenta gradient with Israel map overlay
- Cities: Positioned geographically on map

### City Positioning
Cities use manual x,y coordinates from Figma design matching their geographic locations on the Israel map.

### Component Layouts
- **RTL:** Icon left, text right (coastal cities)
- **TTB:** Icon top, text below (inland cities)
- **LTR:** Text left, icon right (eastern cities)

---

*This documentation will be expanded as V2 development progresses.*
