# IMS Weather Forecast Automation

Automated daily weather forecast generator for Israeli cities. Downloads forecast data from the Israel Meteorological Service (IMS), generates Instagram-ready story images, and delivers via email.

## Features

- **15 Israeli cities** positioned geographically on map of Israel
- **Hebrew + Gregorian + Jewish calendar** dates
- **Daily textual weather description**
- **Automated email delivery** via GitHub Actions
- **Multi-recipient support**

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/noamweisss/Automated-Daily-Forecast.git
cd Automated-Daily-Forecast
pip install -r requirements.txt
```

### Run

```bash
# Preview without sending email
python forecast_workflow.py --dry-run

# Full workflow (download → extract → generate → email)
python forecast_workflow.py
```

## Output

Generates a 1080x1920px Instagram story image with:
- Israel map background with gradient overlay
- Cities at geographic positions with weather icons and temperatures
- Date in Hebrew calendar, Gregorian calendar, and Jewish date
- Daily textual weather description

## Setup

For detailed setup instructions including email configuration and GitHub Actions automation, see [docs/SETUP.md](docs/SETUP.md).

## Architecture

The workflow consists of four phases:

1. **Download** - Fetch XML data from IMS (cities + country forecast)
2. **Extract** - Parse weather data for 15 cities + textual description
3. **Generate** - Create Instagram story image with map layout
4. **Email** - Send to configured recipients

For technical details, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Documentation

- [Setup Guide](docs/SETUP.md) - Installation and configuration
- [Architecture](docs/ARCHITECTURE.md) - Technical design and data flow
- [Development](docs/DEVELOPMENT.md) - Contributing and making changes
- [Deployment](docs/DEPLOYMENT.md) - GitHub Actions and production setup

## Project Structure

```
Automated-Daily-Forecast/
├── forecast_workflow.py          # Main orchestration
├── download_forecast.py          # XML download & encoding
├── extract_forecast.py           # Data extraction + Hebrew dates
├── generate_forecast_map.py      # Map-based image generation (V2)
├── send_email_smtp.py            # Email delivery (SMTP)
├── utils.py                      # Shared utilities + V2 asset paths
├── city_coordinates.py           # City positioning for V2 map
├── weather_icon_mapping.py       # Weather icon mapping for V2
├── assets/
│   ├── map/                      # Israel map PNG & SVG
│   ├── logos/                    # IMS & Ministry of Transport logos
│   └── weather_icons_v2/         # V2 emoji-style weather icons
├── fonts/                        # Noto Sans Hebrew + Open Sans
├── docs/                         # Documentation
├── output/                       # Generated images
└── archive/v1/               # Archived v1 code
```

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

| Version | Description | Status |
|---------|-------------|--------|
| **2.0** | Map-based geographic layout | Current |
| **1.0** | List-based vertical layout | [Archived](archive/v1/) |

## Data Sources

Weather data provided by the [Israel Meteorological Service (IMS)](https://ims.gov.il/):
- Cities forecast: `isr_cities.xml`
- Country description: `isr_country.xml`

## License

Internal IMS project for official use.

---

**Last Updated:** November 24, 2025
