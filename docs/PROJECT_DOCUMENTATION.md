# IMS Weather Story Automation Project

## Comprehensive Project Documentation

**Last Updated:** October 16, 2025
**Project Status:** Phase 3 Complete ✅ | Ready for Phase 4

---

## 🎯 Project Overview

### Goal

Build an automated Python script that:

1. Downloads daily weather forecast XML from Israel Meteorological Service (IMS)
2. Parses the forecast data for 15 Israeli cities
3. Generates a designed Instagram story image (1080x1920px)
4. Emails the image to the social media manager
5. Runs automatically every morning at 6:00 AM

### Background

- **Team:** IMS Social Media & Design Team
- **User Role:** Designer with basic technical skills, learning Python
- **End Goal:** Deploy on IMS servers after approval from CEO
- **Approach:** Build incrementally, one phase at a time

---

## 📋 Project Phases

### Phase 1: XML Parsing & Data Extraction ✅ COMPLETE

**Goal:** Successfully extract forecast data from XML file with robust automation

**Status:** All tasks completed successfully on October 16, 2025

**Core Tasks:**

- [x] Install Python 3.13.2
- [x] Set up VS Code
- [x] Convert XML file to UTF-8 encoding
- [x] Verify Hebrew text displays correctly
- [x] Parse XML structure correctly
- [x] Extract city data (name, coordinates, temperatures, weather code)
- [x] Filter for specific date
- [x] Sort cities by latitude (north to south)

**Production Automation Tasks:**

- [x] Create test extraction scripts (minimal & full)
- [x] Prove basic extraction works
- [x] Build automatic XML download from IMS website
- [x] Implement encoding conversion (ISO-8859-8 → UTF-8)
- [x] Add archive management (keep 14 days of historical XML)
- [x] Enhance extraction with error handling
- [x] Create main workflow orchestration script
- [x] Add comprehensive logging system
- [x] Implement dry-run mode for testing
- [x] Dynamic date handling (use today's date)
- [x] Fallback to archived data if download fails
- [x] Validate city count (expect exactly 15, warn if different)

**Achievement:** ✅ Full production-ready automation with download, extraction, error handling, logging, and archive management!

**Phase 2 Image Generation Tasks:**

- [x] Fredoka variable font integration (weight 300-700, width 75-125)
- [x] Hebrew RTL text rendering with python-bidi
- [x] iOS-style weather emoji icons (PNG overlays)
- [x] Professional header design with logo placeholder and date
- [x] White header + sky-to-white gradient background
- [x] 1080x1920px image generation (Instagram story format)
- [x] Single city proof-of-concept (Tel Aviv)
- [x] Easy-to-configure design constants for all visual parameters

**Achievement:** ✅ Professional image generation with variable fonts, weather icons, and Hebrew text support!

**Deliverables:**
- `forecast_workflow.py` - Main orchestration script
- `download_forecast.py` - XML download with retry logic
- `extract_forecast.py` - Data extraction with validation
- `utils.py` - Shared utilities and logging
- Comprehensive error handling and validation
- Console and file logging
- Dry-run mode for safe testing
- 14-day archive retention system

### Phase 2: Single City Image Generation (POC) ✅ COMPLETE

**Goal:** Create proof-of-concept image with one city

**Status:** All tasks completed successfully on October 16, 2025

**Achievement:** Successfully created proof-of-concept image generator with professional design elements, variable font system, and proper emoji rendering.

**Core Tasks:**

- [x] Set up Pillow library (10.0.0) and python-bidi (0.4.2)
- [x] Integrated Fredoka variable font with Hebrew support
- [x] Created 1080x1920px image canvas
- [x] Rendered Tel Aviv with weather icon, temperature, Hebrew name
- [x] Implemented Hebrew RTL (right-to-left) text with python-bidi
- [x] iOS-style weather emoji icons (PNG overlays from Twemoji)
- [x] Professional header with logo placeholder and date
- [x] White header + sky-to-white gradient background
- [x] Easy-to-configure design constants
- [x] Exported as JPG

**Deliverables:**
- `exploration/generate_image.py` - Complete POC script
- `fonts/Fredoka-Variable.ttf` - Variable font with Hebrew support
- `assets/weather_icons/` - 4 weather emoji PNG files
- `assets/logos/` - Logo placeholder
- Updated dependencies in requirements.txt
- Robust Hebrew text rendering that auto-adapts to the environment

### Phase 3: Complete Design - All 15 Cities ✅ COMPLETE

**Goal:** Generate single image displaying all 15 cities

**Status:** All tasks completed successfully on October 30, 2025

**Core Tasks:**

- [x] Single image displaying all 15 cities (1080x1920px)
- [x] Vertical layout with city rows (north to south)
- [x] Weather icon, temperature, and Hebrew city name for each
- [x] Open Sans variable font integration
- [x] Vertically centered list with balanced padding
- [x] Header elements aligned with main list edges
- [x] Production-ready design in `generate_forecast_image.py`

### Phase 4: Scheduling & Email Delivery ⏳ NOT STARTED

- Daily scheduling (Windows Task Scheduler)
- 6:00 AM execution
- Email functionality
- Error handling and logging

### Phase 5: Server Compatibility ⏳ FUTURE

- Test on IMS servers
- Linux compatibility if needed
- Deployment documentation

---

## 📁 File Structure

```XML
C:\Users\noamw\Desktop\ims\Automated Daily Forecast\
├── isr_cities_utf8.xml              # Main XML data file (UTF-8 encoded)
├── ims_project_docs.md              # This file - comprehensive project documentation
├── PROJECT_STRUCTURE.md             # Detailed file structure and script purposes
├── Claude session.md                # Previous conversation log
│
├── archive/                         # Historical XML files (14-day retention)
│   └── README.md                    # Archive folder documentation
│
├── logs/                            # Application logs
│   └── README.md                    # Logs folder documentation
│
├── output/                          # Generated weather story images
│   └── README.md                    # Output folder documentation
│
├── exploration/                     # Development & test scripts
│   ├── README.md                    # Exploration scripts documentation
│   ├── test_extraction_minimal.py   # ✅ Minimal extraction test (1 city)
│   ├── extract_all_cities.py        # ✅ Full extraction test (15 cities)
│   ├── inspect_xml.py               # ✅ XML structure inspector
│   ├── test_date.py                 # ✅ Date formatting tests
│   ├── find_todays_forecast.py      # ✅ Available dates lister
│   └── parse_weather.py             # ⚠️ Unicode error - for reference
│
└── [future production scripts]      # To be created in root directory
    ├── download_forecast.py         # Download & encode XML from IMS
    ├── extract_forecast.py          # Production extraction with error handling
    ├── forecast_workflow.py         # Main orchestration script
    └── utils.py                     # Shared utility functions
```

---

## 🗺️ Data Structure Reference

### XML Structure

```xml
<IsraelCitiesWeatherForecastMorning>
    <Identification>
        <IssueDateTime>2025-09-28 04:46</IssueDateTime>
    </Identification>
    <Location>
        <LocationMetaData>
            <LocationId>520</LocationId>
            <LocationNameEng>Elat</LocationNameEng>
            <LocationNameHeb>אילת</LocationNameHeb>
            <DisplayLat>29.55</DisplayLat>
            <DisplayLon>34.9</DisplayLon>
        </LocationMetaData>
        <LocationData>
            <TimeUnitData>
                <Date>2025-09-28</Date>
                <Element>
                    <ElementName>Maximum temperature</ElementName>
                    <ElementValue>39</ElementValue>
                </Element>
                <Element>
                    <ElementName>Minimum temperature</ElementName>
                    <ElementValue>26</ElementValue>
                </Element>
                <Element>
                    <ElementName>Weather code</ElementName>
                    <ElementValue>1580</ElementValue>
                </Element>
                <!-- More elements... -->
            </TimeUnitData>
            <!-- 3 more TimeUnitData blocks for following days -->
        </LocationData>
    </Location>
    <!-- 14 more Location blocks -->
</IsraelCitiesWeatherForecastMorning>
```

**Key Points:**

- Each `<Location>` represents one city
- Each city has 4 `<TimeUnitData>` blocks (4-day forecast)
- Each `<TimeUnitData>` has a `<Date>` element
- Weather data is stored in `<Element>` tags with `<ElementName>` and `<ElementValue>`

### Cities Data

**15 Cities (Alphabetical in XML):**
Elat, Ashdod, Beer Sheva, Bet Shean, Haifa, Tiberias, Jerusalem, Lod, Mizpe Ramon, Nazareth, En Gedi, Afula, Zefat, Qazrin, Tel Aviv-Yafo

**Required Sort Order (North to South by Latitude):**

1. Qazrin (33.0°N)
2. Zefat (33.05°N)
3. Bet Shean (32.45°N)
4. Tiberias (32.8°N)
5. Haifa (32.82°N)
6. Nazareth (32.75°N)
7. Afula (32.52°N)
8. Tel Aviv-Yafo (32.1°N)
9. Lod (31.85°N)
10. Ashdod (31.84°N)
11. Jerusalem (31.78°N)
12. En Gedi (31.42°N)
13. Beer Sheva (31.25°N)
14. Mizpe Ramon (30.61°N)
15. Elat (29.55°N)

### Weather Codes

Weather codes are numeric values that need to be mapped to emoji icons. Examples:

- 1250: Clear/Sunny
- 1220: Partly Cloudy
- 1310: Mostly Clear
- 1580: Very Hot/Sunny

**Note:** Full weather code mapping needs to be researched from IMS documentation.

---

## 🔧 Technical Decisions Made

### Language & Libraries

- **Python 3.13.2:** Main programming language
- **xml.etree.ElementTree:** XML parsing (Python standard library)
- **Pillow (PIL):** Image generation
- **python-bidi:** Fallback for Hebrew RTL text rendering

### Encoding

- **Issue:** Original XML had encoding problems with Hebrew text
- **Solution:** Converted to UTF-8 encoding
- **File:** `isr_cities_utf8.xml` is the working version

### Design Approach

- Build incrementally, test each component
- Start with console output before moving to image generation
- Focus on getting Phase 1 working completely before moving forward

---

## 🐛 Known Issues & Considerations

### ✅ Resolved Issues

#### Issue #1: Zero Cities Extracted - RESOLVED ✅

- **Original Problem:** Script reported finding 15 cities but extracted 0 cities' worth of data
- **Solution:** Created minimal test scripts that successfully extract data from all 15 cities
- **Final Status:** Production extraction script works perfectly with all 15 cities, proper sorting, and validation

#### Issue #2: Production Automation - RESOLVED ✅

- **Original Problem:** Needed production-ready scripts with error handling, logging, and automation
- **Solution:** Built complete workflow system with download, extraction, logging, and error handling
- **Final Status:** Full production system operational with dry-run mode for testing

### ⚠️ Outstanding Items

### Item #1: Weather Code Mapping

- **Status:** Partial understanding
- **Known Codes:**
  - `1250` - Clear/Sunny
  - `1220` - Partly Cloudy
  - `1580` - Very Hot/Sunny
- **Next Steps:** Research complete IMS weather code documentation or reverse-engineer from historical data


#### Item #2: Production Script Error Handling

- **Status:** Not yet implemented
- **Needed:** Robust error handling for download failures, network issues, malformed XML, missing data
- **Priority:** High - needed before automation

---

## 💡 Learning Points & Progress

### Skills Developed

- Basic XML parsing with ElementTree
- File path handling in Windows
- Text encoding (UTF-8)
- Hebrew text handling
- Python project structure

### Successful Milestones

✅ Python environment set up correctly
✅ UTF-8 encoding issue resolved
✅ Hebrew text displays correctly
✅ XML file structure understood
✅ City sorting logic implemented
✅ Production download automation complete
✅ Archive management system operational
✅ Comprehensive logging system working
✅ Error handling and validation implemented
✅ **Phase 1 Complete - Full automation working!**
✅ **Phase 2 Complete - Image generation POC working!**
✅ **Phase 3 Complete - All 15 cities image working!**

### Challenges Encountered & Resolved

- ✅ XML parsing complexity - Resolved with ElementTree and proper structure understanding
- ✅ Extraction logic debugging - Successfully debugged with minimal test scripts
- ✅ Hebrew text encoding - Resolved with ISO-8859-8 to UTF-8 conversion
- ✅ Error handling - Implemented comprehensive try-catch blocks with logging
- ✅ Archive management - Built automated 14-day retention system
- ✅ Hebrew RTL Rendering - Implemented robust, environment-adaptive solution

---

## 📝 Notes for Future Development

### For Email Functionality (Phase 4)

- Use `smtplib` for sending emails
- Store credentials securely (environment variables)
- Add error notifications if script fails

### For Server Deployment (Phase 5)

- Test on Linux environment
- Document all dependencies in requirements.txt
- Create deployment guide for IT team

---

## 🎓 Resources & References

- **Python XML Parsing:** [ElementTree Documentation](https://docs.python.org/3/library/xml.etree.elementtree.html)
- **Pillow Library:** [Pillow Docs](https://pillow.readthedocs.io/)
- **Hebrew Fonts:** Google Fonts with Hebrew support
- **Instagram Story Size:** 1080x1920px (9:16 aspect ratio)

---

## 🤝 Project Team & Workflow

**Developer:** Noam (IMS Design Team)  
**Manager:** Social Media Team Manager  
**Approval Required From:** IMS CEO (for server deployment)

**Development Approach:**

- Incremental development with testing at each stage
- No hard deadlines - focus on learning and quality
- Regular testing and validation
- Clear documentation for future handoff

---

## 📧 Contact & Support

For questions or issues with this project, consult:

1. Claude AI assistant for coding help
2. Python documentation for technical references
3. IMS IT team for server deployment questions

---

## End of Documentation
