# Changelog

All notable changes to the IMS Weather Forecast Automation project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.2.0] - 2025-11-13

### Added
- **External Email Template:** Created `email_template.html` as a separate file for easier email design customization
- **IMS Professional Branding:** Updated email template with orange-to-blue gradient header matching IMS brand colors
- **Noto Sans Hebrew Font:** Enhanced email typography with professional Hebrew font via Google Fonts CDN
- **Logo Row:** Added footer with IMS and GitHub logos displayed in clean, tidy row
- **Data Transparency:** Included direct link to IMS XML source in email body

### Changed
- **Email Template Architecture:** Refactored `send_email_smtp.py` to load HTML from external file instead of inline string
- **Simplified Function:** Reduced `create_email_html()` from ~110 lines to ~18 lines
- **Template Injection:** Uses `.replace()` method instead of `.format()` to avoid CSS brace conflicts
- **Content Updates:** Changed greeting to "בוקר טוב מצוות ניו מדיה" (New Media team)

### Improved
- **Maintainability:** Email design changes no longer require Python code modifications
- **Version Control:** HTML template can be reviewed and versioned independently
- **Documentation:** Updated CLAUDE.md and README.md with email template system details

## [4.1.0] - 2025-11-10

### Added
- **Daily Random Gradients:** The forecast image background now features a new, randomly selected gradient every day, adding visual variety.
- **Gradient Test Mode:** A new script `test_gradients.py` was added to generate a set of test images with different gradient backgrounds, allowing for easy visual testing of new color schemes.

### Changed
- **Separator Lines:** The separator lines between cities in the forecast image are now solid black for improved accessibility and visual consistency, replacing the previous adaptive color logic.
- **`send_email.py`:** This file, which used the SendGrid API, is no longer the primary email module. The project now uses `send_email_smtp.py`.
- **`.gitignore`:** Updated to ignore development guides, IDE-specific documentation, and dry-run output images.

### Fixed
- **Email Module Import:** The import of the email module is now conditional, allowing the project to run in environments where email dependencies are not installed (e.g., for testing image generation only).
- **Dry-Run Mode:** The dry-run mode has been enhanced to generate test images without requiring email configuration, making it easier to test the image generation pipeline.

## [4.0.0] - 2025-11-05

### Phase 4 Complete: Automation & Email Delivery via GitHub Actions ✅

**Major Release:** Successfully implemented automated daily workflow with email delivery using GitHub Actions and SMTP. The system now runs completely hands-free in the cloud.

### Added

#### Email Delivery System
- **New Script: `send_email_smtp.py`**
  - SMTP integration for email delivery
  - HTML email template with Hebrew RTL support
  - Professional design with gradient header and structured layout
  - Image attachment
  - Environment variable configuration for security
  - Comprehensive error handling with detailed diagnostics
  - Command-line interface for standalone testing
  - Dry-run mode for testing without sending

#### Email Template Features
- **Professional HTML Design**
  - Hebrew RTL layout with proper text direction
  - Gradient header (purple-blue) with forecast date
  - Bilingual date display (Hebrew DD/MM/YYYY + English)
  - Structured content sections with icons
  - IMS branding and footer with organization details
  - Responsive design for email clients
  - Plain text fallback for compatibility

- **Email Configuration**
  - Subject: "תחזית יומית IMS - {date}" (Hebrew)
  - Attachment: `ims_daily_forecast.jpg`
  - Support for multiple recipients (comma-separated)

#### GitHub Actions Automation
- **New Workflow: `.github/workflows/daily-forecast.yml`**
  - Scheduled execution: Daily at 6:00 AM Israel time (3:00 AM UTC)
  - Manual trigger support via GitHub UI
  - Dry-run mode option for testing
  - Python 3.13 with pip dependency caching
  - Complete workflow: Download → Extract → Generate → Email

- **Workflow Features**
  - Timeout: 15 minutes (typical run: 2-3 minutes)
  - Artifact storage: Images (90 days), Logs (30 days)
  - Failure notifications via GitHub email
  - Detailed workflow summary in GitHub UI
  - Environment variable injection from GitHub Secrets

- **GitHub Secrets Configuration**
  - `EMAIL_ADDRESS`: Sender email address
  - `EMAIL_PASSWORD`: Sender email password or app password
  - `RECIPIENT_EMAIL`: Recipient email address
  - `SMTP_SERVER`: SMTP server address
  - `SMTP_PORT`: SMTP port

#### Documentation & Setup Instructions
- **CLAUDE.md**: Added comprehensive GitHub Actions section
  - Setup instructions for SMTP and GitHub Secrets
  - Workflow features and monitoring guide
  - Local testing commands with environment variables
  - Future deployment planning for Phase 5

- **README.md**: Phase 4 feature section
  - GitHub Actions automation overview
  - Scheduled and manual execution instructions
  - Secrets configuration guide
  - Monitoring and artifact access
  - Updated project structure with automation files

### Changed

- **forecast_workflow.py**:
  - Updated `CURRENT_PHASE` from 3 to 4
  - Integrated `send_email_smtp.py` import
  - Updated `step_send_email()` from placeholder to functional implementation
  - Added forecast_date parameter to email step
  - Enhanced workflow orchestration with email delivery
  - Updated documentation strings to reflect Phase 4 completion

- **requirements.txt**:
  - Added `python-dotenv>=1.0.0` for environment variable management.

- **README.md**:
  - Updated current status: "Phase 4 Complete ✅"
  - Added GitHub Actions automation section with setup guide
  - Expanded project structure to include `.github/workflows/`
  - Updated dependencies list
  - Changed last updated date to November 5, 2025
  - Updated phase status: "Phase 4 Complete ✅ | Phase 5 Planned 📅"

- **CLAUDE.md**:
  - Updated current status to Phase 4 Complete
  - Added email testing commands to Essential Commands
  - Updated Data Flow section with Email Delivery Phase
  - Added `send_email_smtp.py` to Core Production Scripts
  - Updated Phase System section with Phase 4 complete
  - Added comprehensive GitHub Actions Automation section
  - Updated Future Phases to Phase 5: Production Deployment

### Technical Details

#### SMTP Integration
- **Authentication**: Email and password/app password via environment variables
- **Email Sending**: Python's built-in `smtplib`
- **Attachment Handling**: `MIMEImage` for JPEG images
- **Error Handling**: Specific diagnostics for SMTP errors

#### GitHub Actions Environment
- **Runner**: ubuntu-latest
- **Python**: 3.13 with pip caching
- **Artifacts**: GitHub Actions artifact storage
- **Secrets**: Encrypted environment variable injection
- **Scheduling**: Cron-based (POSIX cron syntax)
- **Triggers**: Both scheduled and manual (workflow_dispatch)

#### Email Delivery Flow
1. Generate forecast image (output/daily_forecast.jpg)
2. Load environment variables from GitHub Secrets
3. Format email with Hebrew/English date displays
4. Attach image
5. Send via SMTP
6. Log delivery status

### Improved

- **Automation**: Completely hands-free daily workflow execution
- **Reliability**: Cloud-based execution (no local machine dependency)
- **Monitoring**: Built-in artifact storage and failure notifications
- **Security**: Secrets managed by GitHub (never in code)
- **Testing**: Dry-run mode for safe testing before production
- **Scalability**: Easy to add more recipients or modify schedule
- **Maintainability**: Clear separation of email logic in dedicated module

### What's Next

**Phase 5: Production Deployment** (Future)
- Transition from GitHub Actions to IMS production servers
- Linux compatibility validation (Ubuntu/RHEL)
- IT team handoff and training documentation
- Production monitoring and alerting setup
- Backup and disaster recovery procedures

---

## [3.5.0] - 2025-11-03

### Phase 3.5 Complete: Complete Weather Icon Set ✅

**Feature Release:** Implemented comprehensive weather icon system covering all 23 IMS Israel forecast codes using Twemoji icon set.

### Added
- **Complete Weather Icon Set**: 11 unique Twemoji icons covering all 23 IMS codes
  - Source: Twemoji by Twitter, Inc. (https://github.com/twitter/twemoji)
  - License: CC-BY 4.0 with attribution
  - Format: PNG (72x72px) with RGBA transparency
  - CDN: jsdelivr.net for reliable downloads
- **Icon Files**: Downloaded and organized 11 weather icons:
  - 1250_clear.png (☀ Sun) - Clear, Hot, Extremely Hot
  - 1220_partly_cloudy.png (⛅ Sun Behind Cloud) - Partly Cloudy
  - 1230_cloudy.png (☁ Cloud) - Cloudy conditions
  - 1530_partly_cloudy_rain.png (🌦 Sun Behind Rain Cloud) - Partly cloudy with rain
  - 1140_rainy.png (🌧 Cloud With Rain) - Rain conditions
  - 1020_thunderstorms.png (⛈ Lightning And Rain) - Storms
  - 1060_snow.png (🌨 Cloud With Snow) - All snow conditions
  - 1160_fog.png (🌫 Fog) - Fog, Dust, Sandstorms
  - 1260_windy.png (🌬 Wind Face) - Windy
  - 1300_frost.png (❄ Snowflake) - Cold conditions
  - 1270_muggy.png (💧 Droplet) - Muggy/Humid
- **Attribution File**: `assets/weather_icons/ATTRIBUTION.txt`
  - Complete Twemoji license documentation
  - Icon usage mapping
  - Download source documentation
- **IMS Weather Codes Documentation**: `ims_weather_codes.json`
  - Complete mapping of 23 Israel forecast codes
  - 31 worldwide forecast codes
  - Wind direction codes
  - Extracted from official IMS documentation (CodesForIMSWebSite_1.pdf)
- **Phase 3.5 Strategy Document**: `docs/PHASE_3.5_ICON_STRATEGY.md`
  - Complete icon implementation documentation
  - Icon sourcing research and evaluation
  - Final icon mapping table
  - Implementation timeline

### Changed
- **generate_forecast_image.py**:
  - Expanded `WEATHER_ICONS` dictionary from 4 to 23 codes (lines 80-127)
  - Updated fallback icon from `mostly_clear.png` to `1250_clear.png`
  - Multiple codes now share icons for visual consistency
  - Complete coverage: Clear (3 codes), Cloudy (2), Rain (2), Thunderstorms (2), Snow (4), Fog/Dust (3), Cold/Frost (3), Wind (1), Muggy (1)
- **CLAUDE.md**:
  - Updated Weather Icons section with Twemoji details
  - Added complete icon source, license, and coverage information
  - Updated Known Weather Codes section with reference to full documentation
  - Removed note about incomplete weather code mapping
- **README.md**: Updated project status to Phase 3.5 Complete

### Improved
- **Visual Consistency**: Single icon set (Twemoji) ensures uniform aesthetic
- **License Compliance**: Proper CC-BY 4.0 attribution documentation
- **Icon Coverage**: 100% coverage of all IMS Israel forecast codes (23/23)
- **Maintainability**: Clear mapping in code with descriptive comments
- **Scalability**: Easy to add new codes by mapping to existing icons

### Implementation Details
- **Strategy**: Use single consistent icon set with multiple codes mapping to same icon
- **Rationale**: Visual consistency more important than unique icons per code
- **Example**: All snow types (Light snow, Heavy snow, Sleet) use same snow icon
- **Fallback**: Generic clear/sunny icon for any unknown future codes
- **Testing**: Verified with real IMS forecast data (codes 1220, 1250)

---

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
- Email delivery to social media team (smtplib)
- Error notification system

#### Phase 5: Server Deployment (Future)
- Deploy to IMS production servers
- Linux compatibility testing
- Handoff to IT team
- Production monitoring setup

---

## Version History

### [Unreleased]
- Phase 5: Production server deployment and IT handoff

### [4.0.0] - 2025-11-05
- Phase 4 complete: Automation & email delivery via GitHub Actions
- SendGrid API integration
- Automated daily workflow

### [3.5.0] - 2025-11-03
- Phase 3.5 complete: Complete weather icon set with full IMS code coverage
- Twemoji icon system

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
**Last Updated:** November 10, 2025