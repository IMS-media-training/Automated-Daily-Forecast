# Changelog

All notable changes to the IMS Weather Forecast Automation project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2025-10-30

### Documentation & Hebrew Rendering Enhancements

Minor release focused on documentation improvements and enhanced Hebrew text rendering robustness.

### Added
- **GEMINI.md** - Documentation for potential Google Gemini AI assistant integration
- **Claude session history tracking** (`claude_sessions/` folder)
- **Automatic Raqm support detection** in generate_forecast_image.py
  - Uses `PIL.features.check('raqm')` to detect Pillow's complex text layout support
  - Dual-path rendering system for maximum compatibility

### Changed
- **CLAUDE.md**: Enhanced with comprehensive Hebrew rendering documentation
  - Added Raqm support detection explanation
  - Documented modern vs. fallback rendering paths
- **README.md**: Updated to reflect Phase 3 completion status
- **PROJECT_DOCUMENTATION.md**: Added detailed Hebrew rendering implementation notes
- **generate_forecast_image.py**:
  - Added automatic Raqm support detection
  - Dual-path Hebrew RTL rendering:
    - **Modern path (Raqm available):** Uses Pillow's advanced engine with `direction='rtl'`
    - **Fallback path (Raqm unavailable):** Pre-shapes text using python-bidi
  - Added `TEST_MODE_FORCE_RAQM` configuration option for testing

### Improved
- **Hebrew RTL text rendering robustness** across different Pillow installations
- **Cross-environment compatibility** for systems with/without Raqm
- **Documentation clarity** for Hebrew text handling and font requirements

---

## [3.0.0] - 2025-10-30

### Phase 3 Complete: All 15 Cities Image Generation ✅

**Major Release:** Successfully implemented production-ready image generation system displaying all 15 Israeli cities in a single Instagram story image.

### Added

#### Production Image Generation System
- **New Script: `generate_forecast_image.py`** (449 lines)
  - Single Instagram story image (1080x1920px) with all 15 cities
  - Vertically centered layout with balanced padding
  - Professional design with proper spacing and alignment
  - Weather icons, temperatures, and Hebrew names for each city
  - Modular helper functions for maintainability

#### Layout Design
- **Vertically Centered City List**
  - Dynamic positioning: Cities centered with 160px bottom padding
  - Row height: 105px per city (accommodates 15 cities with spacing)
  - Total list height: 1575px for 15 cities
  - Top padding calculated dynamically: ROW_PADDING (160px)

- **Professional Header** (180px height)
  - IMS logo positioned at left edge of main list
  - Date display (DD/MM/YYYY format) at right edge of main list
  - Header elements aligned to list edges for visual continuity
  - Clean white background

- **City Row Layout** (per city)
  - Weather icon: 65px × 65px (left-aligned with padding)
  - Temperature display: Centered between icon and city name
  - City name in Hebrew: Right-aligned (RTL support)
  - Element spacing: 40px gaps between icon, temp, and name
  - Horizontal padding: 160px breathing room on sides

#### Font System Upgrade
- **Switched from Fredoka to Open Sans Variable Font**
  - Font file: `OpenSans-Variable.ttf` (532KB)
  - Weight axis: 300-800 (Light to ExtraBold)
  - Width axis: 75-100 (Condensed to Normal)
  - Full Hebrew Unicode support

- **Typography Hierarchy**
  - City names: Weight 600, Width 100, Size 40px
  - Temperatures: Weight 500, Width 100, Size 35px
  - Date: Weight 400, Width 100, Size 50px
  - Configurable via constants at top of file

#### Enhanced Visual Design
- **Gradient Background**
  - Sky blue (#87CEEB) to white vertical blend
  - Smooth transition creating depth

- **Semi-Transparent Separators**
  - Light gray lines (rgba(200, 200, 200, 0.3)) between cities
  - 2px width, centered horizontally
  - Subtle visual separation without overwhelming design

#### Hebrew Text Rendering System
- **Automatic Raqm Support Detection**
  - Detects Pillow's complex text layout capabilities
  - Dual-path rendering for maximum compatibility

- **Modern Path (Raqm available)**
  - Native Pillow RTL rendering with `direction='rtl'`
  - Leverages advanced text shaping engine

- **Fallback Path (No Raqm)**
  - Pre-shapes text using python-bidi library
  - Ensures correct display on basic Pillow installations

#### Project Documentation
- **CLAUDE.md** (356 lines) - Comprehensive AI assistant instructions
  - Complete project overview and current status
  - Essential commands for development and testing
  - Detailed architecture and data flow documentation
  - Important implementation details and best practices
  - Development workflow and phase system
  - Common pitfalls and solutions

#### Configuration System
- All visual parameters in CONFIGURATION section at top of generate_forecast_image.py
- Easy customization without searching through code:
  - Canvas dimensions
  - Font paths and settings
  - Colors (header, background gradient, separator)
  - Layout measurements (padding, row height, icon size, spacing)
  - Header dimensions
  - File paths (logo, output)

### Changed
- **forecast_workflow.py**: Updated to Phase 3
  - Integrated image generation step
  - Updated CURRENT_PHASE constant to 3
  - Enhanced workflow logging

- **Font System**: Complete migration from Fredoka to Open Sans
  - Better variable font axis support
  - Improved Hebrew rendering
  - Professional typography for production use

- **exploration/generate_image.py**: Updated for compatibility testing
  - Kept as single-city POC for experimentation
  - Uses same font system as production script

### Removed
- **Fredoka-Variable.ttf** font file (replaced by Open Sans)

### Technical Details

#### Image Export
- Format: JPEG (production-ready for Instagram)
- Quality: 95 (high quality with manageable file size)
- Output path: `output/daily_forecast.jpg`

#### Error Handling
- Graceful fallbacks for missing weather icons
- Font loading validation
- Hebrew rendering compatibility checks
- Comprehensive logging throughout generation process

#### Dependencies
- Pillow (PIL) with optional Raqm support
- python-bidi (fallback for Hebrew RTL)
- Existing forecast data extraction system

### Output
Successfully generates Instagram story images featuring:
- **All 15 Israeli cities** (Qazrin to Eilat, north to south)
- Weather icon + temperature range + Hebrew name per city
- Professional header with IMS logo and formatted date
- Beautiful gradient background with subtle separators
- Proper Hebrew RTL text rendering across all environments

### What's Next

**Phase 3.5: Finalizing Icon Gallery** (Current Focus)
- Transform IMS weather code documentation (Hebrew PDF) to accessible format
- Source complete weather icon set matching all IMS codes
- Illustrate missing weather icons manually (SVG format) if needed
- Ensure script compatibility with full icon library

**Phase 4: Automation & Email Delivery** (Planned)
- Windows Task Scheduler integration (daily 6:00 AM execution)
- Email delivery system to social media team (smtplib)
- Error notification system
- Automated workflow monitoring

**Phase 5: Server Deployment** (Future)
- Deploy to IMS production servers
- Linux compatibility testing and validation
- IT team handoff documentation
- Production monitoring setup

---

## [2.0.0] - 2025-10-16

### Phase 2 Complete: Enhanced Image Generation (Single City POC) ✅

Successfully implemented proof-of-concept image generation with professional design elements, variable font system, and proper emoji rendering.

### Added

#### Image Generation System
- **Fredoka Variable Font Integration**
  - Weight axis: 300-700 (Light to Bold)
  - Width axis: 75-125 (Condensed to Wide)
  - Full Hebrew language support
  - Easy-to-configure font constants

- **iOS-Style Weather Icons**
  - High-quality Twemoji PNG overlays (512x512px)
  - 4 weather codes: sunny, partly cloudy, mostly clear, very hot
  - Transparent PNG overlay system

- **Professional Header Design**
  - IMS logo placeholder (awaiting SVG→PNG conversion)
  - Forecast date in DD/MM/YYYY format
  - Clean white background (180px header)

- **Hebrew RTL Text Rendering**
  - python-bidi library integration
  - Proper right-to-left text display
  - Hebrew city names render correctly

- **Visual Design**
  - 1080x1920px Instagram story format
  - White header section with logo and date
  - Sky-to-white gradient background
  - Centered layout with weather icon, city name, temperature

#### Assets & Resources
- Created assets/ folder structure:
  - `assets/logos/` - IMS logo files
  - `assets/weather_icons/` - Weather emoji PNGs
- Added `fonts/Fredoka-Variable.ttf`
- Downloaded 4 Twemoji weather icons

#### Project Organization
- Reorganized documentation into `docs/` structure
  - Created `docs/` for production documentation
  - Created `docs/dev-guides/` for development helpers
  - Moved PROJECT_STRUCTURE.md to docs/
  - Renamed ims_project_docs.md → PROJECT_DOCUMENTATION.md
  - Moved Git/GitHub guides to dev-guides/
- Created navigation README files for docs folders

### Changed
- **exploration/generate_image.py**: Complete rewrite with modular design
  - Added configuration constants section
  - Implemented variable font loading with axes control
  - PNG icon overlay system with transparency
  - Header generation with logo and date
  - Modular helper functions for reusability
- Font system: Switched from Heebo to Fredoka variable font

### Removed
- Heebo font files (3 files) - replaced with Fredoka variable font

### Technical Details

#### New Dependencies
- `python-bidi>=0.4.2` - Hebrew RTL support
- `cairosvg` - SVG conversion (optional, for logo)
- `svglib`, `reportlab` - SVG rendering (optional)

#### Configuration System
All design elements configurable via constants in generate_image.py:
- Font weights and widths (variable axes)
- Font sizes for city, temperature, date
- Header dimensions and margins
- Icon size and positioning
- Color palette (white, black, gray, sky blue)

### Output
Successfully generates Instagram story POC image featuring:
- White header with IMS logo placeholder and date (16/10/2025)
- Colorful weather icon (iOS-style emoji)
- Hebrew city name in Fredoka font (RTL: תל אביב - יפו)
- Temperature range display (18-27°C)
- Beautiful sky-to-white gradient background

### What's Next
**Phase 3: Complete Design - All 15 Cities** ✅ COMPLETED in v3.0.0
- Vertical layout for 15 city rows
- City positioning system (north to south)
- Weather icon, temperature, and city name display
- Production-ready image generation

See v3.0.0 above for full implementation details.

---

## [1.0.0] - 2025-10-15

### Phase 1 Complete: XML Download & Data Extraction ✅

This marks the completion of Phase 1, establishing a solid foundation for automated weather data collection and processing.

### Added

#### Core Functionality
- **Automatic XML Download:** Downloads daily forecast XML from IMS website
- **Encoding Conversion:** Handles Hebrew text encoding (ISO-8859-8 → UTF-8)
- **Data Extraction:** Parses XML and extracts weather data for 15 cities
- **Geographic Sorting:** Automatically sorts cities north to south by latitude
- **Archive Management:** Maintains 14-day rolling archive of historical XML files
- **Fallback System:** Automatically uses archived data if download fails

#### Production Scripts
- `forecast_workflow.py` - Main orchestration script
- `download_forecast.py` - XML download and encoding handler
- `extract_forecast.py` - Weather data extraction engine
- `utils.py` - Shared utilities (logging, validation, file management)

#### Features
- **Comprehensive Logging:** Dual output to console and file (`logs/forecast_automation.log`)
- **Error Handling:** Robust error handling with graceful fallbacks
- **Dry-Run Mode:** Test without modifying files (`--dry-run` flag)
- **Date Flexibility:** Extract data for any date in forecast range
- **Data Validation:** Validates city count and data completeness
- **Command-Line Interface:** Full CLI with helpful arguments

#### Development Tools
- Test scripts in `exploration/` folder:
  - `test_extraction_minimal.py` - Single city extraction test
  - `extract_all_cities.py` - Full 15-city extraction test
  - `inspect_xml.py` - XML structure inspector
  - `test_date.py` - Date formatting tests
  - `find_todays_forecast.py` - Available dates lister

#### Documentation
- `README.md` - Main project documentation
- `ims_project_docs.md` - Comprehensive technical documentation
- `PROJECT_STRUCTURE.md` - Detailed file structure reference
- `CHANGELOG.md` - This file
- `GIT_GUIDE.md` - Git workflow guide for beginners

#### Version Control
- Git repository initialized
- `.gitignore` configured for Python projects
- `requirements.txt` for dependency management

#### Project Organization
- Folder structure with `archive/`, `logs/`, `output/` directories
- README files in each folder explaining purpose
- Clean separation of production vs. exploration code

### Technical Details

#### Data Coverage
- **Cities:** 15 Israeli cities from Qazrin to Elat
- **Forecast Range:** 4 days (today + 3 days)
- **Data Points:** Temperature (max/min), weather code, humidity, wind
- **Update Source:** IMS official XML feed

#### Key Configurations
- Archive retention: 14 days
- Expected city count: 15
- Log file: `logs/forecast_automation.log`
- Main XML: `isr_cities_utf8.xml`

#### Dependencies
- Python 3.13+
- `requests` library for HTTP downloads
- Standard library: `xml.etree.ElementTree`, `datetime`, `logging`, `pathlib`

### Development Journey

#### Challenges Overcome
1. **Hebrew Encoding:** Successfully resolved UTF-8 encoding issues for Hebrew text
2. **XML Parsing:** Mastered ElementTree for complex nested XML structure
3. **Date Handling:** Implemented flexible date filtering and formatting
4. **Error Resilience:** Built comprehensive error handling and fallback systems

#### Testing Approach
- Created minimal test scripts to verify each component
- Iterative testing and refinement
- Validated with real IMS data

### What's Next

#### Phase 3: Complete Design - All 15 Cities (Planned)
- Single image with all 15 cities in vertical layout
- Implement row-based positioning (north to south)
- Weather icon, temperature, and city name for each
- Final design refinement and spacing
- Export production-ready JPG images

#### Phase 4: Automation & Delivery (Planned)
- Windows Task Scheduler integration
- Daily execution at 6:00 AM
- Email delivery to social media manager
- Error notification system

#### Phase 5: Server Deployment (Future)
- Deploy to IMS production servers
- Linux compatibility testing
- Handoff to IT team
- Production monitoring setup

---

## Version History

### [Unreleased]
- Phase 3.5: Finalizing icon gallery (weather code documentation & complete icon set)
- Phase 4: Automation & email delivery system

### [3.0.1] - 2025-10-30
- Documentation enhancements and Hebrew rendering improvements
- Automatic Raqm support detection
- GEMINI.md addition

### [3.0.0] - 2025-10-30
- Phase 3 complete: All 15 cities image generation
- Open Sans variable font system
- Production-ready Instagram story image generator

### [2.0.0] - 2025-10-16
- Phase 2 complete: Enhanced image generation (single city POC)
- Fredoka variable font, iOS-style icons, Hebrew RTL text
- Documentation reorganization

### [1.0.0] - 2025-10-15
- Phase 1 complete: XML download and data extraction
- Initial Git repository setup
- Comprehensive documentation

---

## Notes

### Versioning Strategy
- **Major version (x.0.0):** Phase completion milestones
- **Minor version (1.x.0):** New features within a phase
- **Patch version (1.0.x):** Bug fixes and minor improvements

### Change Categories
- **Added:** New features
- **Changed:** Changes to existing functionality
- **Deprecated:** Soon-to-be-removed features
- **Removed:** Removed features
- **Fixed:** Bug fixes
- **Security:** Security vulnerability fixes

---

**Maintained by:** Noam W, IMS Design Team
**Last Updated:** October 30, 2025
