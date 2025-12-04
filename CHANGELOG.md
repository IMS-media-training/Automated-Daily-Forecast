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

### Added (V2 Milestone 2)
- City coordinate mapping for V2 map-based layout (`city_coordinates.py`)
- Weather icon mapping for emoji-based icons V2 (`weather_icon_mapping.py`)
- Noto Sans Hebrew variable font (primary for V2)
- Israel map PNG & SVG assets (assets/map/)
- Ministry of Transport logo (PNG & SVG)
- V2 asset path constants in `utils.py` (MAP_DIR, LOGOS_DIR, WEATHER_ICONS_V2_DIR, etc.)
- Font constants: NOTO_SANS_HEBREW_FONT, OPEN_SANS_FONT

### Changed (V2 Milestone 2)
- Reorganized asset structure: created map/, logos/ subdirectories
- Renamed `weather_icons 2.0/` to `weather_icons_v2/` (no spaces)
- Renamed weather icon files from emoji codes to descriptive names (e.g., `clear.png`, `partly_cloudy.png`)
- Consolidated logo files in `assets/logos/` (removed duplicates)

### Removed (V2 Milestone 2)
- Fredoka-Variable.ttf font (unused)
- Duplicate logo files (IMS_logo.png, ims_logo_placeholder.png)
- Legacy weather icons moved to `archive/v1/weather_icons`

### Added (V2 Milestone 3 - In Progress)
- `generate_forecast_map.py`: V2 map-based image generator with CSS-like gradient system
- CSS-style linear gradient function supporting arbitrary angles (0-360°) and multiple color stops
- Designer-friendly gradient API matching CSS linear-gradient syntax
- Phase 1: Gradient background implementation (346° angle with negative/positive color stop positions)
- Phase 2: Israel map overlay with Figma-accurate positioning (533x1495px at 258,288)
- Phase 3: Header rendering with Hebrew date and separator line
- `render_header()` function with RTL text support using bidi library
- Static Noto Sans Hebrew Black font (complete, all glyphs including numbers)
- Font loading system with 4-tier fallback chain (Black Complete → Variable → Black Subset → OpenSans)
- Separator line with 100px horizontal padding (880px width centered on canvas)
- Test file naming convention: `{feature}_test_{NN}.png` format for consistent iteration tracking
- **Gemini Agent Integration**:
  - `GEMINI.md`: Context file for Gemini agents (matches `CLAUDE.md`)
  - `.gemini/commands/`: Custom slash commands for Gemini (`pre-commit`, `archive-session`)
  - `scripts/save_archive.py`: Utility for automated session archiving

### Changed (V2 Milestone 3 - In Progress)
- Gradient system now uses CSS-style angles instead of simple top-to-bottom
- Gradient supports color stops at negative and >100% positions for extended gradients
- Map assets automatically resized to match Figma design specifications
- Font constants in `utils.py`: Added `NOTO_SANS_HEBREW_BLACK_COMPLETE` for static font with correct weight
- Font loading prioritizes static fonts over variable fonts to ensure correct weight rendering

### Fixed
- `forecast_workflow.py`: Updated to use V2 map generator (`generate_forecast_map.py`) instead of archived V1 generator


### V2 Roadmap (Planned)
- Map-based geographic layout with Israel silhouette (Milestone 3)
- Dual logos: IMS + Ministry of Transport (Milestone 4)
- City-specific layouts (RTL/TTB/LTR) based on map position (Milestone 3)
- Gradient background (cyan → magenta) (Milestone 3)
- Textual weather description panel (Milestone 4)

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
