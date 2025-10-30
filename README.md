# IMS Weather Forecast Automation

> Automated daily weather forecast generator for Israeli cities - from IMS data to Instagram-ready stories

## Overview

This project automates the creation of daily weather forecast images for the Israel Meteorological Service (IMS) social media accounts. It downloads forecast data from IMS, processes it, and generates beautifully designed Instagram story images featuring 15 major Israeli cities.

**Current Status:** Phase 3 Complete ✅ - All 15 Cities Image Generation

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

### Phase 4: Automation & Delivery 📅 PLANNED
- Automated daily execution (6:00 AM)
- Email delivery to social media team
- Windows Task Scheduler integration

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
   cd "C:\Users\noamw\Desktop\ims\Automated Daily Forecast"
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python utils.py
   ```

### Usage

#### Run the complete workflow (Phase 1)
```bash
# Download today's forecast and extract data
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

**Generate forecast image (Phase 3):**
```bash
python generate_forecast_image.py
```

**View logs:**
```bash
type logs\forecast_automation.log
```

## Project Structure

```
Automated Daily Forecast/
├── 📄 Production Scripts
│   ├── forecast_workflow.py      # Main orchestration script
│   ├── download_forecast.py      # XML download & encoding
│   ├── extract_forecast.py       # Data extraction
│   ├── generate_image.py         # Image generation (Phase 3)
│   └── utils.py                  # Shared utilities
│
├── 📁 Data & Output
│   ├── archive/                  # Historical XML (14 days)
│   ├── logs/                     # Automation logs
│   └── output/                   # Generated images
│
├── 📁 Assets
│   ├── assets/logos/             # IMS logo files
│   ├── assets/weather_icons/    # Weather emoji PNGs
│   └── fonts/                    # Open Sans variable font
│
├── 📁 Development
│   └── exploration/              # Test & development scripts
│
└── 📚 Documentation
    ├── README.md                 # This file
    ├── CHANGELOG.md              # Version history
    ├── docs/                     # Production documentation
    │   ├── PROJECT_DOCUMENTATION.md
    │   └── PROJECT_STRUCTURE.md
    └── docs/dev-guides/          # Development helper guides
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

### Image Generation (Phase 3)
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

### Code Organization

- **utils.py** - Shared utility functions (logging, validation, file management)
- **download_forecast.py** - Handles XML download and encoding conversion
- **extract_forecast.py** - Parses XML and extracts weather data
- **forecast_workflow.py** - Main orchestration script that ties everything together

## Version Control

This project uses Git for version control. See [GIT_GUIDE.md](GIT_GUIDE.md) for basic Git commands and workflows.

### Current Version
**v1.0.0** - Phase 1 Complete (October 2025)

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
- `requests>=2.31.0` - XML download
- `Pillow>=10.0.0` - Image generation
- `python-bidi>=0.4.2` - Hebrew RTL text support

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

**Last Updated:** October 30, 2025
**Phase Status:** Phase 3 Complete ✅ | Phase 4 Planned 📅
