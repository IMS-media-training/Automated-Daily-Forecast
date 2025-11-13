# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IMS Weather Forecast Automation - Automated daily weather forecast generator for Israeli cities. Downloads forecast data from Israel Meteorological Service (IMS), processes it, and generates Instagram-ready story images featuring 15 major Israeli cities.

**Current Status:** Phase 4b Complete (Workflow Integration) | Phase 4c Planned (GitHub Actions Automation)

## Essential Commands

### Development & Testing

```bash
# Run complete workflow (download + extract)
python forecast_workflow.py

# Dry-run mode (preview without changes)
python forecast_workflow.py --dry-run

# Extract forecast for specific date
python forecast_workflow.py --date 2025-10-15

# Download XML only
python download_forecast.py

# Extract forecast data only
python extract_forecast.py

# Generate forecast image (all 15 cities - Phase 3)
python generate_forecast_image.py

# Test email delivery (Phase 4a - dry-run)
python send_email_smtp.py --dry-run

# Send test email (Phase 4a - requires .env file)
python send_email_smtp.py

# Test image generation (Phase 2 POC - single city)
python exploration/generate_image.py

# View logs
cat logs/forecast_automation.log

# Verify utility functions
python utils.py
```

### Testing Individual Components

```bash
# Test minimal extraction (1 city)
python exploration/test_extraction_minimal.py

# Test full extraction (15 cities)
python exploration/extract_all_cities.py

# Inspect XML structure
python exploration/inspect_xml.py
```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Architecture

### Data Flow

**Complete Automation Workflow:**

1. **Download Phase** (`download_forecast.py`)
   - Downloads XML from IMS website with retry logic (3 attempts, 2s delay)
   - Converts encoding: ISO-8859-8 → UTF-8 (Hebrew support)
   - Saves two copies: current working file + dated archive
   - Auto-cleanup: Removes archives older than 14 days

2. **Extraction Phase** (`extract_forecast.py`)
   - Parses XML to extract weather data for 15 cities
   - Filters by target date (defaults to today)
   - Sorts cities north-to-south by latitude
   - Validates data completeness and city count
   - Falls back to archived XML if current file unavailable

3. **Image Generation Phase** (Phase 3 complete)
   - Generates single 1080x1920px Instagram story image
   - All 15 cities in vertical layout with centered positioning
   - Professional header with IMS logo and date aligned with list edges
   - Open Sans variable font with Hebrew support

4. **Email Delivery Phase** (Phase 4a complete - SMTP)
   - Sends forecast image via SMTP (built-in smtplib)
   - Professional HTML email template with Hebrew RTL support
   - Attachment: daily_forecast.jpg (Instagram-ready)
   - Environment variable configuration via .env file (secure)
   - Dry-run mode for safe testing before real sends

5. **Orchestration** (`forecast_workflow.py`)
   - Main entry point that coordinates all phases
   - Phase-aware execution (currently Phase 3, Phase 4 integration next)
   - Handles dry-run mode for safe testing
   - Comprehensive logging to console + file
   - Graceful error handling with fallback strategies

### Core Production Scripts

**forecast_workflow.py** - Main orchestration script
- Coordinates download → extract → generate → email workflow
- Phase-aware execution (currently Phase 4)
- Dry-run mode support
- Exit codes: 0 (success), 1 (failure)

**generate_forecast_image.py** - All 15 cities image generation (Phase 3)
- Single Instagram story image (1080x1920px) with all cities
- Vertically centered layout with balanced padding
- Header and list aligned at consistent ROW_PADDING boundaries
- Open Sans variable font with Hebrew RTL support
- Weather icons, temperatures, and city names for each location

**download_forecast.py** - XML download & encoding conversion
- URL: `https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_cities.xml`
- 30s timeout, 3 retries with exponential backoff
- Encoding conversion with XML declaration update
- Archive management with 14-day retention

**extract_forecast.py** - Weather data extraction
- ElementTree XML parsing
- Extracts: name (Eng/Heb), coordinates, temps, weather code, humidity, wind
- North-to-south sorting by latitude
- Archive fallback if main XML missing
- Validates expected city count (15)
- **Smart date detection:** Automatically falls back to next available date if target date has no data
  * Handles IMS publishing tomorrow's forecast after 16:00 daily
  * Tries each available date until valid data found
  * Logs clearly which date was used (target vs actual)

**utils.py** - Shared utilities
- Logging setup (console + file at `logs/forecast_automation.log`)
- Date handling (YYYY-MM-DD format matching XML)
- File management (ensure directories, archive cleanup)
- Data validation (city count, required fields)
- Formatting utilities

**send_email_smtp.py** - Email delivery via SMTP (Phase 4a)
- Built-in smtplib for simple, reliable email delivery
- HTML email template with Hebrew RTL support
- Image attachment with MIME encoding
- Environment variable configuration via .env file (EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT)
- Dry-run mode for testing without sending
- Environment validation with clear error messages
- Gmail App Password support (16-character passwords)
- Command-line interface for standalone testing

### Image Generation System (Phase 3)

**generate_forecast_image.py** - Production image generation (all 15 cities)
- Canvas: 1080x1920px (Instagram story format)
- Open Sans variable font: Weight 300-800, Width 75-100 axes
- Hebrew RTL text rendering (direct rendering, no bidi library needed)
- iOS-style weather icon PNGs (65px per city row, RGBA transparency)
- Professional header: White background, IMS logo, date (DD/MM/YYYY)
- Gradient background: Sky blue to white vertical blend
- Vertically centered city list with balanced top/bottom padding
- Header elements (logo, date) aligned with main list edges
- All design parameters configurable via constants at top of file
- Status: Phase 3 complete - all 15 cities working

**exploration/generate_image.py** - POC for single city testing
- Single city proof-of-concept (Tel Aviv)
- Used for Phase 2 development and testing
- Kept for reference and experimentation

**Font System:**
- Font: OpenSans-Variable.ttf (Variable font with Hebrew support)
- Configurable axes: `font.set_variation_by_axes([width, weight])` - note order!
- City name: Weight 600, Width 100, Size 40px
- Temperature: Weight 500, Width 100, Size 35px
- Date: Weight 400, Width 100, Size 50px

**Weather Icons:**
- Location: `assets/weather_icons/`
- Format: PNG with transparency (RGBA), 72x72px source
- Source: Twemoji by Twitter, Inc. (https://github.com/twitter/twemoji)
- License: CC-BY 4.0 (attribution in `assets/weather_icons/ATTRIBUTION.txt`)
- Mapping: `WEATHER_ICONS` dict in generate_forecast_image.py
- Total: 11 unique icons covering all 23 IMS Israel forecast codes
- Fallback: 1250_clear.png if unknown code encountered
- Complete mapping available in: `docs/PHASE_3.5_ICON_STRATEGY.md`

### Key Configuration Values

**Archive Management** (utils.py):
- `ARCHIVE_RETENTION_DAYS = 14` - How long to keep historical XML
- `EXPECTED_CITY_COUNT = 15` - Validation threshold

**Download Settings** (download_forecast.py):
- `DOWNLOAD_TIMEOUT = 30` seconds
- `MAX_RETRIES = 3`
- `RETRY_DELAY = 2` seconds

**File Paths** (utils.py):
- `XML_FILE = "isr_cities_utf8.xml"` - Current working XML
- `LOGS_DIR = "logs/"` - Application logs
- `ARCHIVE_DIR = "archive/"` - Historical XML files
- `OUTPUT_DIR = "output/"` - Generated images

**Image Design** (exploration/generate_image.py):
- All visual parameters in CONFIGURATION section at top of file
- Easy to modify: colors, sizes, positions, font settings

## Important Implementation Details

### Hebrew Text Handling

**Encoding:** All XML files MUST be UTF-8. Original IMS XML is ISO-8859-8.
 
**RTL Rendering (Automatic Detection):**
The script now automatically handles Hebrew RTL rendering across different environments.

1.  **Raqm Support Detection:** It uses `PIL.features.check('raqm')` to determine if Pillow has been installed with complex text layout support.
2.  **Modern Path (Raqm available):** If `True`, the script passes the original Hebrew string to `draw.text()` with the `direction='rtl'` argument, letting Pillow's advanced engine handle everything.
3.  **Fallback Path (Raqm unavailable):** If `False`, it pre-shapes the text using `bidi.algorithm.get_display()` before passing it to `draw.text()` (without the `direction` argument).

This ensures the text displays correctly whether running in a basic environment or a fully-featured one, without manual code changes.

**Font Requirements:** Use fonts with Hebrew Unicode support (e.g., Open Sans Variable)

### XML Structure

The IMS XML contains:
- Root: `<IsraelCitiesWeatherForecastMorning>`
- 15 `<Location>` elements (one per city)
- Each location has `<LocationMetaData>` (name, coordinates) and `<LocationData>`
- Each `<LocationData>` has 4 `<TimeUnitData>` blocks (4-day forecast)
- Each day has multiple `<Element>` tags with name/value pairs

**Critical:** Always filter by `<Date>` element to get correct day's forecast.

### City Sorting Logic

Cities are sorted **north to south** by latitude (descending):
```python
sorted_cities = sorted(cities_data, key=lambda city: city['latitude'], reverse=True)
```

**Order:** Qazrin (33.0°N) → Zefat → ... → Beer Sheva → Eilat (29.55°N)

### Error Handling Strategy

**Download failures:**
- Retry 3 times with 2s delay
- If all retries fail, extraction phase attempts archive fallback
- Workflow continues to extract if existing XML available

**Extraction failures:**
- Archive fallback if main XML unavailable
- **Smart date detection:** If target date has no data, automatically tries next available date
  * Handles case when IMS publishes tomorrow's forecast after 16:00
  * Iterates through all available dates until valid data found
  * Common after 4 PM Israel time when new forecast is published
- Validates city count and warns if ≠ 15
- Validates required fields per city
- Returns None if no cities extracted

**Logging:**
- All operations logged to console + `logs/forecast_automation.log`
- Log levels: INFO (normal), WARNING (recoverable), ERROR (critical)
- UTF-8 encoding for Hebrew text in logs

### Variable Font Usage

Open Sans uses two axes:
1. **Weight axis** (wght): 300 (Light) → 800 (ExtraBold)
2. **Width axis** (wdth): 75 (Condensed) → 100 (Normal)

**Correct API Usage:**
```python
font = ImageFont.truetype(str(FONT_VARIABLE), size)
font.set_variation_by_axes([width, weight])  # e.g., [100, 600] - ORDER MATTERS!
```

**IMPORTANT:** The axes order is `[width, weight]` for Open Sans, determined by the font's fvar table. **This order varies by font!**

**Common Mistakes - Do NOT Use These:**
```python
# ❌ WRONG: Dictionary syntax not supported
font.set_variation_by_name({'wght': weight, 'wdth': width})

# ❌ WRONG: Wrong number of arguments
font.set_variation_by_name('wght', weight)

# ❌ WRONG: String format not supported
font.set_variation_by_name(f"wght={weight},wdth={width}")

# ❌ WRONG: Incorrect axis order for Open Sans
font.set_variation_by_axes([weight, width])  # Width comes first!
```

**When in Doubt - Check PIL Documentation:**
```python
from PIL import ImageFont
help(ImageFont.FreeTypeFont.set_variation_by_axes)
# Output: set_variation_by_axes(self, axes: list[float]) -> None
```

**Best Practice:** Always check API documentation BEFORE trial-and-error attempts. Save 20-30 minutes of troubleshooting.

### Font Acquisition Best Practices

**IMPORTANT:** Always validate downloaded font files before using them in code.

**Correct URLs for Open Sans (Google Fonts GitHub):**
- Variable font: `https://github.com/google/fonts/raw/main/ofl/opensans/OpenSans%5Bwdth%2Cwght%5D.ttf`
- Static fonts: `https://github.com/google/fonts/raw/main/ofl/opensans/static/OpenSans-*.ttf`

**Critical Path Note:** The path is `/ofl/opensans/` NOT `/apache/opensans/` or `/apache/opensans/static/`

**File Validation Immediately After Download:**
```bash
# Should output "TrueType Font data", NOT "HTML document"
file path/to/font.ttf

# Check file size (font files typically 100KB-1MB)
ls -lh path/to/font.ttf
```

**Common Pitfall:** GitHub URLs without "raw" in the path will download HTML error pages instead of actual font files. Always verify the file is binary data, not HTML.

**Test Font Loading:**
```python
from PIL import ImageFont
try:
    font = ImageFont.truetype("path/to/font.ttf", 20)
    print("✓ Font loaded successfully")
except Exception as e:
    print(f"✗ Font load failed: {e}")
```

### Weather Icon System

Icons are PNG files with RGBA transparency overlay:
```python
# Load and resize icon
icon = Image.open(icon_path).convert('RGBA')
icon = icon.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)

# Paste with transparency
image.paste(icon, (x, y), icon)  # Third param is alpha mask
```

## Development Workflow

### Phase System

The project follows an incremental phase system:
- **Phase 1:** Download + Extraction (COMPLETE)
- **Phase 2:** Single city image generation POC (COMPLETE)
- **Phase 3:** Full design with all 15 cities (COMPLETE)
- **Phase 3.5:** Weather icon system with full IMS code coverage (COMPLETE)
- **Phase 4a:** Basic SMTP email delivery (COMPLETE)
- **Phase 4b:** Workflow integration (COMPLETE)
- **Phase 4c:** GitHub Actions automation (PLANNED)
- **Phase 5:** Production server deployment (FUTURE)

**CURRENT_PHASE** constant in forecast_workflow.py controls which steps execute (currently set to 4 - all phases active).

### Making Changes to Design

**Image Design:**

All image design parameters are in constants at the top of `generate_forecast_image.py`:
- Modify values in CONFIGURATION section
- No need to search through code for magic numbers
- Run `python generate_forecast_image.py` to test changes
- Output saved to `output/daily_forecast.jpg`
- For single-city testing, use `python exploration/generate_image.py`

**Email Design:**

Email appearance is controlled by `email_template.html`:
- Edit HTML/CSS directly in template file
- No Python code changes needed for design updates
- Test with `python send_email_smtp.py --dry-run`
- Template features: IMS gradient colors, Noto Sans Hebrew font, logo row
- Dynamic content: `{forecast_date}` placeholder auto-replaced at runtime

### Adding New Scripts

**Production scripts:** Place in project root alongside forecast_workflow.py
**Test/dev scripts:** Place in `exploration/` directory
**Documentation:** Place in `docs/` or `docs/dev-guides/`

### Logging Best Practices

Always use the shared logging system:
```python
from utils import setup_logging
logger = setup_logging()
logger.info("Normal operation")
logger.warning("Recoverable issue")
logger.error("Critical failure")
```

### File Validation Checklist

**Pre-Flight Checklist for All External Resources**

Before using any downloaded file (fonts, icons, data files), follow these validation steps:

**1. Verify File Type:**
```bash
file path/to/downloaded/file
# Expected: Specific file type (e.g., "TrueType Font data", "PNG image data")
# Warning: If you see "HTML document" or "ASCII text", the download failed
```

**2. Check File Size:**
```bash
ls -lh path/to/file
# Font files: typically 100KB-1MB
# Icon PNGs: typically 5KB-50KB
# XML data: varies by content
```

**3. Test Loading (for fonts):**
```python
from PIL import ImageFont
try:
    font = ImageFont.truetype("path/to/font.ttf", 20)
    print("✓ Font validation passed")
except Exception as e:
    print(f"✗ Font validation failed: {e}")
    # Do NOT proceed - fix the download issue first
```

**4. Never Assume Download Succeeded:**
- GitHub URLs can redirect to error pages (HTML instead of binary)
- Network issues can produce partial/corrupted files
- Validate immediately after download, not later during image generation

**Time Saved:** This checklist prevents 50+ lines of debugging corrupt/invalid files.

### Working Directory Management

**Best Practice:** Use absolute paths to avoid directory confusion.

**Good - Using pathlib with absolute paths:**
```python
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
FONT_PATH = BASE_DIR / "fonts" / "OpenSans-Variable.ttf"
OUTPUT_DIR = BASE_DIR / "output"
```

**Bad - Using relative paths:**
```python
FONT_PATH = "fonts/OpenSans-Variable.ttf"  # Breaks if cwd changes
OUTPUT_DIR = "output"  # Fragile and error-prone
```

**In Bash Commands:**
```bash
# Good: Explicit directory change with command chaining
cd /workspaces/Automated-Daily-Forecast && python generate_forecast_image.py

# Also Good: Absolute paths
python /workspaces/Automated-Daily-Forecast/generate_forecast_image.py

# Bad: Assuming current directory
python generate_forecast_image.py  # May fail if cwd is wrong
```

**Important Note:** Claude Code may reset the working directory between bash commands. Always use absolute paths or explicit `cd` commands.

## Data Specifications

### 15 Israeli Cities (North to South)

1. Qazrin, 2. Zefat (Safed), 3. Bet Shean, 4. Tiberias, 5. Haifa, 6. Nazareth, 7. Afula, 8. Tel Aviv-Yafo, 9. Lod, 10. Ashdod, 11. Jerusalem, 12. En Gedi, 13. Beer Sheva, 14. Mizpe Ramon, 15. Elat (Eilat)

### Weather Elements Extracted

**Always present (Day 1):**
- Maximum temperature (°C)
- Minimum temperature (°C)
- Weather code (numeric)
- Maximum/minimum relative humidity (%)
- Wind direction and speed

**Days 2-4:** Typically only temperature and weather code

### Weather Codes

**Complete mapping available:** All 23 Israel forecast codes documented in `ims_weather_codes.json` and `docs/PHASE_3.5_ICON_STRATEGY.md`

**Common codes:**
- 1250: Clear/Sunny
- 1220: Partly Cloudy
- 1140: Rainy
- 1020: Thunderstorms
- 1230: Cloudy
- 1310: Hot
- 1580: Extremely Hot

**Icon coverage:** All 23 codes have corresponding Twemoji icons (11 unique icons, with multiple codes sharing icons for visual consistency)

## Common Pitfalls

1. **Encoding issues:** Always ensure XML is UTF-8 before parsing. Don't try to parse ISO-8859-8 directly.

2. **Date format:** XML uses YYYY-MM-DD format. Always match this format when filtering forecasts.

3. **Hebrew text rendering:** Must use python-bidi `get_display()` for proper RTL rendering. Direct rendering will show reversed/disconnected characters.

4. **Variable font axes:**
   - Must call `set_variation_by_axes([width, weight])` AFTER creating font object, BEFORE using it
   - **CRITICAL:** Axis order is `[width, weight]` for Open Sans - varies by font!
   - **Check documentation first:** Use `help(ImageFont.FreeTypeFont.set_variation_by_axes)` before trial-and-error
   - Avoid guessing API syntax - saves 20-30 minutes

5. **Font file downloads:**
   - Always use GitHub "raw" URLs (e.g., `github.com/user/repo/raw/main/path/file.ttf`)
   - Validate file type immediately with `file` command after download
   - If you see "HTML document" instead of "TrueType Font data", the URL is wrong
   - Common issue: Missing "raw" in URL or incorrect repository path
   - **Prevents 50+ lines of troubleshooting**

6. **Dry-run mode:** When testing, always use `--dry-run` flag first to avoid modifying files accidentally.

7. **City name variations:** XML uses "Tel Aviv - Yafo" (with space-dash-space), not "Tel Aviv-Yafo". Check exact spelling when filtering cities.

8. **Archive fallback:** Don't assume main XML file always exists. Extraction has built-in fallback to latest archive.

9. **Working directory confusion:**
   - Use absolute paths in Python scripts (`Path(__file__).parent.absolute()`)
   - Claude Code may reset working directory between bash commands
   - In bash: Use `cd /full/path && command` or absolute paths

## Phase 4: Email Delivery (SMTP Implementation)

### Phase 4a: Basic SMTP Email (COMPLETE ✅)

**Status:** Working perfectly - email delivery validated locally

**What We Built:**
- Simple SMTP implementation using Python's built-in `smtplib`
- HTML email template with Hebrew RTL support
- Dry-run mode for safe testing
- Environment variable configuration via `.env` file
- Professional email formatting with forecast image attachment

**Key Files:**
- `send_email_smtp.py` - Complete SMTP email delivery script
- `email_template.html` - Professional HTML email template (external file)
- `.env.example` - Environment variable template
- `.env` - Local credentials (in .gitignore, never committed)

**Testing Results:**
- ✅ Dry-run mode validated configuration
- ✅ Real email sent successfully
- ✅ Email received with correct Hebrew RTL formatting
- ✅ Image attachment working (205KB forecast image)

**Critical Success Factors (vs Phase 4 v1 failures):**

1. **Actually load .env file:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # MUST be called before os.environ.get()
   ```
   Phase 4 v1 added python-dotenv to requirements but never imported/used it!

2. **Consistent variable naming everywhere:**
   - Same names in: `.env.example`, code, documentation
   - Used: `EMAIL_ADDRESS`, `EMAIL_PASSWORD`, `RECIPIENT_EMAIL`
   - NOT: `SENDER_EMAIL`, `FROM_EMAIL`, `TO_EMAIL` (v1 had mismatches)

3. **Simple approach first:**
   - Started with built-in `smtplib` (no external dependencies)
   - Avoided SendGrid complexity until proven necessary
   - Tested locally before any automation

4. **Environment validation with clear errors:**
   ```python
   def validate_environment_variables():
       # Check all required vars, fail fast with helpful message
   ```

5. **Security from day 1:**
   - `.env` in `.gitignore` before creating any credentials
   - Temporary Gmail account for testing (zero personal risk)
   - No credentials ever in code or git history

**Setup Instructions:**

1. **Create .env file from template:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

2. **Required environment variables:**
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_ADDRESS=your-gmail@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   RECIPIENT_EMAIL=recipient@example.com
   ```

3. **Generate Gmail App Password:**
   - Enable 2-Step Verification on Google account
   - Go to: https://myaccount.google.com/apppasswords
   - Generate 16-character App Password
   - Use App Password (NOT regular Gmail password)

4. **Test email delivery:**
   ```bash
   # Test configuration without sending
   python send_email_smtp.py --dry-run

   # Send real test email
   python send_email_smtp.py
   ```

**Email Template System:**

The email HTML is now separated into an external template file for easier customization:

- **Template file:** `email_template.html` (project root)
- **Template loading:** `send_email_smtp.py` reads and injects dynamic content
- **Dynamic content:** `{forecast_date}` placeholder replaced at runtime

**Template Features:**
- **Professional IMS branding:** Orange-to-blue gradient header matching IMS colors
- **Hebrew typography:** Noto Sans Hebrew font via Google Fonts CDN
- **RTL support:** Full Hebrew right-to-left layout with proper text alignment
- **Responsive design:** Mobile-friendly with max-width constraints
- **Logo row:** IMS logo and GitHub link displayed in tidy footer row
- **Transparency:** Link to IMS XML source for data transparency
- **Accessibility:** Semantic HTML with proper ARIA labels

**Customizing Email Design:**

To modify the email appearance, edit `email_template.html` directly:
```html
<!-- Header gradient (line 28) -->
background: linear-gradient(135deg, #ffa602 0%, #0090f7 100%);

<!-- Font family (line 12) -->
font-family: "Noto Sans Hebrew", Arial, sans-serif;

<!-- Logo row styling (lines 64-79) -->
.footer .logo-row {
    gap: 40px;  /* spacing between logos */
}
```

**Template Placeholder:**
- `{forecast_date}` - Replaced with DD/MM/YYYY format date at runtime

**Important:** The template uses `.replace()` for placeholder injection (not `.format()`) to avoid conflicts with CSS braces.

### Phase 4b: Workflow Integration (COMPLETE ✅)

**Status:** Working perfectly - email delivery integrated into main workflow

**What We Built:**
- Integrated `send_email_smtp.py` into `forecast_workflow.py` orchestration
- Updated import from `send_email` (old SendGrid) to `send_email_smtp` (working SMTP)
- Modified `step_send_email()` to call simplified `send_email()` function
- Email failures are CRITICAL (workflow fails if email fails - NOT silent)
- Dry-run mode passes through entire workflow

**Key Changes (forecast_workflow.py):**
```python
# Changed import
from send_email_smtp import send_email  # Was: from send_email import send_forecast_email

# Updated function call
success = send_email(
    image_path=image_path,
    dry_run=dry_run
)
# Old signature required: image_path, forecast_date, logger, dry_run
# New signature is simpler: image_path, dry_run (calculates date internally, uses own logger)
```

**Testing Results:**
- ✅ Dry-run mode validated all steps without sending
- ✅ Complete workflow executed successfully in 3.8 seconds
- ✅ All 4 phases working: Download → Extract → Generate → Email
- ✅ Email delivered successfully with forecast image attachment
- ✅ Security verified: .env not in git status

**Workflow Execution:**
```bash
# Test without sending email
python forecast_workflow.py --dry-run

# Run complete automation
python forecast_workflow.py
```

**Phase 4b Achievement:**
The IMS Weather Forecast Automation now runs end-to-end as a single command, with all phases coordinated through the main workflow script. Email delivery is no longer a separate manual step.

### Phase 4c: GitHub Actions Automation (PLANNED 📋)

**After Phase 4b completes:**
- Add GitHub Secrets for email credentials
- Create GitHub Actions workflow
- Daily scheduled run (6:00 AM Israel time)
- Manual trigger for testing
- Only after local workflow 100% reliable

### Key Lessons Learned (Phase 4a Session - Nov 6, 2025)

**What Made Phase 4a Succeed:**

1. **Incremental approach:**
   - Built SMTP first, validate locally, automation later
   - Each step fully working before moving to next
   - Time to working email: ~30 minutes (vs v1 never worked)

2. **Configuration discipline:**
   - Chose variable names upfront, used consistently everywhere
   - Documented in .env.example before writing any code
   - No "fix it later" approach to naming

3. **Proper dependency usage:**
   - Don't just add to requirements.txt - actually import and use
   - Test that environment variables are loaded correctly
   - Validate early with clear error messages

4. **Security mindset:**
   - .gitignore protection BEFORE creating credentials
   - Used temporary Gmail (no personal risk if leaked)
   - Verified `git status` before every commit

5. **Test locally first:**
   - GitHub Actions should be LAST step, not first
   - Local testing catches 90% of issues immediately
   - Much faster debug cycle than waiting for CI

**Anti-Patterns to Avoid (from Phase 4 v1):**

❌ Adding library to requirements.txt but not using it
❌ Inconsistent variable names across files
❌ Testing only in CI/automation environment
❌ Silent failures (marking errors as "non-critical")
❌ Premature complexity (SendGrid before basic SMTP works)

**Time Comparison:**

| Approach | Time to Working Email | Local Testing |
|----------|----------------------|---------------|
| Phase 4 v1 (SendGrid + GitHub Actions) | Never worked | ❌ Skipped |
| Phase 4a v2 (SMTP locally first) | 30 minutes | ✅ Validated |

## Future Phases

### Phase 5: Production Deployment

- Transition from GitHub Actions to IMS production servers
- Linux compatibility validation (Ubuntu/RHEL)
- IT team handoff and training documentation
- Production monitoring and alerting setup
- Backup and disaster recovery procedures
- before you commit, make sure all the docs are up to date. If they are not, update them and include them in the commit too