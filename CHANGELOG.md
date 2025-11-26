# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (V2 Milestone 1)
- Download and parse `isr_country.xml` for textual weather descriptions
- Hebrew calendar conversion using pyluach library (v2.2.0+)
- `format_hebrew_date()` utility function for Gregorian + Hebrew date formatting
- `extract_weather_description()` function to parse country XML
- Country XML archive management (matching cities XML pattern)
- Support for both cities and country XML in cleanup operations
- New return format from `extract_forecast()`: dictionary with cities, description, date, and hebrew_date

### Changed (V2 Milestone 1)
- `download_forecast.py`: Now downloads both cities and country XML files
- `extract_forecast.py`: Returns complete forecast data structure instead of just city list
- `utils.py`: Added country-specific helper functions and Hebrew date formatting
- `requirements.txt`: Added pyluach>=2.2.0 dependency
- Archive cleanup now handles both `isr_cities_*.xml` and `isr_country_*.xml` files

### V2 Roadmap (Planned)
- Map-based geographic layout with Israel silhouette (Milestone 2-3)
- Noto Sans Hebrew variable font (Milestone 2)
- New weather icon set (weather_icons 2.0) (Milestone 2)
- Dual logos: IMS + Ministry of Transport (Milestone 4)
- City-specific layouts (RTL/TTB/LTR) based on map position (Milestone 3)

### Removed
- Vertical list layout (preserved in archive/v1/)

---

## [1.0.0] - 2025-11-17

**Version 1 - List-Based Layout** (Archived)

Production release with automated daily forecasts via GitHub Actions.

### Features
- Download forecast data from IMS (isr_cities.xml)
- Extract weather for 15 Israeli cities, sorted north-to-south
- Generate 1080x1920px Instagram story image with vertical list layout
- Open Sans variable font with Hebrew RTL support
- Weather icons (Twemoji) covering all 23 IMS codes
- SMTP email delivery with professional HTML template
- Multi-recipient support via recipients.txt
- GitHub Actions automation (daily at 6 AM Israel time)
- Dry-run mode for safe testing

### Technical Details
- Python 3.8+ compatible
- ISO-8859-8 to UTF-8 encoding conversion
- Archive management with 14-day retention
- Smart date detection for IMS publishing schedule

---

## Version 1.x History (Summarized)

| Version | Date | Milestone |
|---------|------|-----------|
| 1.0.0 | 2025-11-17 | Phase 4c: Multi-recipient GitHub Actions |
| 4.2.0 | 2025-11-13 | External email template with IMS branding |
| 4.1.0 | 2025-11-10 | Daily random gradients |
| 4.0.0 | 2025-11-05 | GitHub Actions automation |
| 3.5.0 | 2025-11-03 | Complete Twemoji icon set (23 codes) |
| 3.0.0 | 2025-10-30 | All 15 cities image generation |
| 2.0.0 | 2025-10-16 | Single city POC with variable fonts |
| 1.0.0 | 2025-10-15 | XML download and data extraction |

For detailed v1 history, see `archive/v1/docs/` or checkout tag `v1.0-final`.

---

## Versioning Strategy

- **Major (x.0.0):** Breaking changes, major redesigns
- **Minor (x.y.0):** New features, backward compatible
- **Patch (x.y.z):** Bug fixes, minor improvements

---

**Maintained by:** Noam W, IMS Design Team
