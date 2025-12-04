# CLAUDE.md

## Project Overview

IMS Weather Forecast V2 - Map-based Instagram story generator with geographic city placement. Downloads forecast data from Israel Meteorological Service, generates 1080x1920px images with cities positioned on Israel map.

**Status**: V2 Development (Milestone 1 Complete)

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
├── forecast_workflow.py          # Main orchestration
├── download_forecast.py          # Download cities & country XML
├── extract_forecast.py           # Data extraction with Hebrew dates
├── generate_forecast_map.py      # V2 map-based generator (TODO)
├── send_email_smtp.py            # Email delivery
├── utils.py                      # Shared utilities + Hebrew calendar
├── city_coordinates.py           # City positions for map layout (V2)
├── weather_icon_mapping.py       # Icon mapping for V2
├── assets/
│   ├── map/                      # Israel map PNG & SVG
│   ├── logos/                    # IMS & MoT logos (PNG/SVG)
│   └── weather_icons_v2/         # V2 emoji-style icon set (renamed)
├── fonts/
│   ├── NotoSansHebrew-Black-Complete.ttf  # Primary: Static Black (weight 900, all glyphs)
│   ├── NotoSansHebrew-Variable-Complete.ttf  # Variable font (all glyphs)
│   ├── NotoSansHebrew-SemiBold.ttf        # Static SemiBold subset (Hebrew only)
│   └── OpenSans-Variable.ttf              # Backup font
└── archive/v1/                   # Archived V1 code & assets
```

## Code Style

- Use `pathlib` for all file paths
- Use `setup_logging()` from utils.py for logging
- UTF-8 encoding everywhere
- Absolute paths preferred over relative

## Test File Naming Convention

When generating test images during development, use consistent incremental naming:
- Format: `{feature}_test_{NN}.png` where NN is zero-padded number (00, 01, 02, ...)
- Examples:
  - `output/header_test_00.png` - First header test
  - `output/header_test_01.png` - Second header test (with fixes)
  - `output/cities_test_00.png` - First cities rendering test
  - `output/full_test_00.png` - Complete image test
- Purpose: Allows easy comparison between iterations and tracking progress
- Cleanup: Remove test files before final commit, keep only production outputs

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

### CSS-Like Gradient System (V2)
IMPORTANT: V2 uses designer-friendly CSS-style gradients with angle and color stops.
```python
# Gradient configuration (generate_forecast_map.py)
GRADIENT_ANGLE = 346  # degrees (0=top, 90=right, 180=bottom, 270=left)
GRADIENT_STOPS = [
    ((220, 255, 87), -62.6),    # #DCFF57 at -62.6%
    ((34, 178, 255), 112.14)    # #22B2FF at 112.14%
]
```
- Supports arbitrary angles matching CSS linear-gradient syntax
- Color stops can be negative or >100% for extended gradients
- Easy iteration on design without code changes

### City Coordinates
Cities use manual x,y positions from Figma design (not calculated from lat/long).

### Hebrew Calendar
- Uses pyluach library for Gregorian to Hebrew date conversion
- Output format: "DD/MM/YYYY Hebrew_Day ב-Month Hebrew_Year"
- Example: "26/11/2025 ו׳ בכסלו תשפ״ו"

### Data Structure (extract_forecast.py)
`extract_forecast()` returns a dictionary:
```python
{
    'cities': List[Dict],        # 15 cities with forecast data
    'description': str,          # Hebrew weather description
    'date': str,                 # YYYY-MM-DD
    'hebrew_date': str           # Full formatted date string
}
```

### City Coordinates (city_coordinates.py)
V2 uses manual positioning from Figma design:
- 15 cities with x, y coordinates on 1080x1920 canvas
- Layout types: RTL (coastal), TTB (inland), LTR (eastern)
- Import: `from city_coordinates import CITY_POSITIONS`

### Weather Icon Mapping (weather_icon_mapping.py)
Maps IMS weather codes to V2 icon filenames:
- Primary codes: 1250 (Clear), 1220 (Partly Cloudy)
- Extended codes for seasonal variations
- Import: `from weather_icon_mapping import get_weather_icon_path`

### V2 Asset Paths (utils.py)
New constants for V2 assets:
- `ISRAEL_MAP_PNG`, `ISRAEL_MAP_SVG` - Map files
- `IMS_LOGO_PNG`, `MOT_LOGO_PNG` - Logo files
- `WEATHER_ICONS_V2_DIR` - Icon directory
- `NOTO_SANS_HEBREW_BLACK_COMPLETE` - Static Black font (complete, all glyphs) **[Priority 1]**
- `NOTO_SANS_HEBREW_VARIABLE` - Variable font (complete, all glyphs)
- `NOTO_SANS_HEBREW_BLACK` - Static Black subset (Hebrew only, no numbers)
- `NOTO_SANS_HEBREW_SEMIBOLD` - Static SemiBold subset (Hebrew only, no numbers)
- `OPEN_SANS_FONT` - Backup font

**Font Loading Strategy:**
- **Priority 1:** Static Black Complete (correct weight built-in, all glyphs)
- **Priority 2:** Variable font (needs weight configuration)
- **Priority 3:** Black subset (Hebrew only, missing numbers)
- **Priority 4:** OpenSans fallback

## Data Sources

- Cities forecast: `https://ims.gov.il/.../isr_cities.xml`
- Country forecast: `https://ims.gov.il/.../isr_country.xml` (textual description)

## Current Milestone

**Milestone 1: Data Pipeline Update** ✓ COMPLETE
- [x] Download and parse isr_country.xml
- [x] Add Hebrew calendar conversion (pyluach)
- [x] Update extraction to include weather description
- [x] Test complete data pipeline

**Milestone 2: Asset Preparation** ✓ COMPLETE
- [x] Export Israel map from Figma (PNG & SVG)
- [x] Download Noto Sans Hebrew variable font
- [x] Organize new assets structure (map/, logos/, weather_icons_v2/)
- [x] Create city coordinate mapping (15 cities)
- [x] Create weather icon mapping
- [x] Archive legacy V1 assets

**Milestone 3 - Map-Based Image Generator** (In Progress)
- [x] Implement generate_forecast_map.py with CSS-like gradient system
- [x] Create CSS gradient background with angle and color stops (346deg, #DCFF57 → #22B2FF)
- [x] Load and position Israel map overlay (533x1495px at 258,288)
- [x] Render header with Hebrew date and separator line
- [ ] Implement city rendering with RTL/TTB/LTR layouts
- [ ] Render all 15 cities with weather icons and temperatures
- [ ] Render weather description with text wrapping
- [ ] Render IMS and MoT logos

**Key Features Implemented:**
- **CSS-like gradient system**: Designer-friendly API with angle (degrees) and color stops (position %)
- **Figma-accurate positioning**: Map and gradient match Figma design specifications
- **Phase 1, 2 & 3 complete**: Background gradient, map overlay, and header rendering functional
- **Header rendering**: RTL Hebrew text with bidi, Noto Sans Hebrew Black font, centered white separator line (100px padding)

## Git Workflow

### Multiple Remotes
This project has TWO remote repositories that must stay in sync:
- `origin` - Personal GitHub (portfolio): github.com/noamweisss/Automated-Daily-Forecast
- `ims-production` - IMS GitHub (production): github.com/IMS-media-training/Automated-Daily-Forecast

IMPORTANT: Always push to BOTH remotes after commits:
```bash
git push origin main && git push ims-production main
```

### Pre-Commit Documentation Checklist
IMPORTANT: Before EVERY commit, check and update these docs if affected:
- [ ] CLAUDE.md - Update if commands, structure, or critical notes changed
- [ ] README.md - Update if features, setup, or architecture changed
- [ ] CHANGELOG.md - Add entry to [Unreleased] section
- [ ] docs/SETUP.md - Update if installation or configuration changed
- [ ] docs/ARCHITECTURE.md - Update if data flow or components changed
- [ ] docs/DEVELOPMENT.md - Update if dev practices changed
- [ ] docs/DEPLOYMENT.md - Update if GitHub Actions or deployment changed

Use `/pre-commit` command to get this checklist before committing.

## Version

- V2 Development started: 2025-11-24
- V1 archived: See `archive/v1/` or `git checkout v1.0-final`
- Always check figma context before implementing or updating any visual element.
the link to the main V2 layout is @https://www.figma.com/design/YVPUc24KCJIFrHpoXKrHz7/Story-Layout-V2.0?node-id=1-2&m=dev