# IMS Weather Automation - Project Structure

**Last Updated:** October 16, 2025
**Status:** Phase 2 Complete - Image Generation POC

---

## 📁 Current File Structure

```folders
C:\Users\noamw\Desktop\ims\Automated Daily Forecast\
│
├── 📄 Core XML Data
│   ├── isr_cities_utf8.xml                    # Current/latest XML (always UTF-8)
│   └── IMS_Logo.svg                           # Source logo file
│
├── 📁 archive/                                 # Historical XML files (14 days)
│   ├── README.md                               # Archive folder documentation
│   ├── isr_cities_2025-10-16.xml             # Example: Today's archived XML
│   ├── isr_cities_2025-10-15.xml             # Example: Yesterday's XML
│   └── ...                                     # Auto-managed (keep 14 days)
│
├── 📁 logs/                                    # Operation logs
│   ├── README.md                               # Logs folder documentation
│   └── forecast_automation.log                # Main log file
│
├── 📁 output/                                  # Generated images
│   ├── README.md                               # Output folder documentation
│   └── test_city_forecast.jpg                 # Example: Test image (Tel Aviv POC)
│
├── 📁 assets/                                  # Image generation assets (Phase 2)
│   ├── logos/                                  # IMS logo files
│   │   └── ims_logo_placeholder.png           # Placeholder logo (awaiting conversion)
│   └── weather_icons/                          # Weather emoji PNGs
│       ├── sunny.png                           # Code 1250
│       ├── partly_cloudy.png                   # Code 1220
│       ├── mostly_clear.png                    # Code 1310
│       └── very_hot.png                        # Code 1580
│
├── 📁 fonts/                                   # Typography (Phase 2)
│   └── Fredoka-Variable.ttf                   # Variable font (Hebrew support)
│
├── 🐍 Production Scripts (Phase 1 - Complete)
│   ├── download_forecast.py                   # ✅ Download & convert XML from IMS
│   ├── extract_forecast.py                    # ✅ Extract weather data with error handling
│   ├── forecast_workflow.py                   # ✅ Main orchestration script
│   └── utils.py                               # ✅ Shared utility functions
│
├── 📁 exploration/                             # Development & test scripts
│   ├── README.md                               # Exploration scripts documentation
│   ├── generate_image.py                      # ✅ Phase 2 POC: Single city image generation
│   ├── test_extraction_minimal.py             # ✅ Minimal extraction test (1 city)
│   ├── extract_all_cities.py                  # ✅ Full extraction test (15 cities)
│   ├── inspect_xml.py                         # ✅ XML structure inspector
│   ├── test_date.py                           # ✅ Date formatting tests
│   ├── find_todays_forecast.py                # ✅ Available dates lister
│   └── parse_weather.py                       # ⚠️ Unicode error - for reference
│
└── 📚 Documentation
    ├── README.md                              # Main project documentation
    ├── CHANGELOG.md                           # Version history
    ├── requirements.txt                       # Python dependencies
    └── docs/                                  # Organized documentation
        ├── README.md                          # Documentation index
        ├── PROJECT_DOCUMENTATION.md           # Comprehensive technical docs
        ├── PROJECT_STRUCTURE.md               # This file
        └── dev-guides/                        # Development helper guides
            ├── README.md                      # Dev guides index
            ├── GIT_GUIDE.md                   # Git workflow guide
            ├── GITHUB_SETUP.md                # GitHub setup guide
            ├── QUICK_START_GITHUB.md          # Quick GitHub reference
            └── YOUR_NEXT_STEPS.md             # Publishing checklist
```

---

## 🔄 Data Flow

### **Daily Automated Workflow (When Complete)**

```blocks
┌─────────────────────────────────────────────────────────────┐
│  1. DOWNLOAD PHASE                                          │
│     forecast_workflow.py calls download_forecast.py         │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  IMS Website              │
              │  isr_cities.xml           │
              │  (ISO-8859-8 encoding)    │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  Download & Convert       │
              │  ISO-8859-8 → UTF-8       │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  Save Two Copies:         │
              │  1. isr_cities_utf8.xml   │
              │  2. archive/YYYY-MM-DD    │
              └───────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  2. EXTRACTION PHASE                                        │
│     forecast_workflow.py calls extract_forecast.py          │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  Parse XML                │
              │  Extract 15 cities        │
              │  Filter for today's date  │
              │  Sort North → South       │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  Validate Data:           │
              │  ✓ 15 cities?             │
              │  ✓ All data present?      │
              │  ⚠ Log warnings           │
              └───────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  3. IMAGE GENERATION PHASE (Phase 2 - Future)               │
│     Generate 1080x1920px Instagram story                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  output/                  │
              │  weather_story_DATE.jpg   │
              └───────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  4. EMAIL DELIVERY PHASE (Phase 4 - Future)                 │
│     Email image to social media manager                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Script Purposes

### **Production Scripts (To Be Created)**

| Script | Purpose | Input | Output | Dependencies |
|--------|---------|-------|--------|--------------|
| `download_forecast.py` | Download XML from IMS, convert encoding, archive | IMS URL | `isr_cities_utf8.xml` + archive copy | `requests` |
| `extract_forecast.py` | Extract weather data for specified date | XML file, target date | List of city dictionaries | Built-in only |
| `forecast_workflow.py` | Orchestrate entire daily workflow | None (uses today's date) | Image file (future) | All other scripts |
| `utils.py` | Shared utility functions | Various | Various | Built-in only |

### **Working Scripts (Current)**

| Script | Status | Purpose |
|--------|--------|---------|
| `test_extraction_minimal.py` | ✅ WORKING | Proves extraction works for one city (Tel Aviv) |
| `extract_all_cities.py` | ✅ WORKING | Prototype that extracts all 15 cities successfully |

### **Exploration Scripts (Reference)**

| Script | Status | Purpose |
|--------|--------|---------|
| `parse_weather.py` | ⚠️ Unicode error | Explores LocationData structure |
| `inspect_xml.py` | ✅ WORKING | Shows internal Element structure |
| `test_date.py` | ✅ WORKING | Tests Python date formatting |
| `find_todays_forecast.py` | ✅ WORKING | Lists available dates in XML |

---

## 📦 Dependencies

### **Python Standard Library (Built-in)**

- `xml.etree.ElementTree` - XML parsing
- `datetime` - Date handling
- `logging` - Log file management
- `os` - File system operations
- `pathlib` - Path handling
- `glob` - File pattern matching
- `sys` - System operations

### **External Libraries (Installed)**

- `requests>=2.31.0` - HTTP downloading
- `Pillow>=10.0.0` - Image generation (Phase 2)
- `python-bidi>=0.4.2` - Hebrew RTL text support (Phase 2)

Install all:
```bash
pip install -r requirements.txt
```

### **Future Dependencies (Phase 4+)**

- `smtplib` - Email sending (built-in, no installation needed)

---

## 🗂️ File Retention Policies

| Folder | File Type | Retention | Management |
|--------|-----------|-----------|------------|
| `archive/` | XML files | 14 days | Auto-cleanup by `download_forecast.py` |
| `logs/` | Log files | Manual | Review and clean manually as needed |
| `output/` | Image files | Manual | Keep as archive or manual cleanup |

---

## 🔧 Configuration Values

### **Archive Management**

- **Days to keep:** 14 days
- **Cleanup frequency:** Every time `download_forecast.py` runs
- **Naming format:** `isr_cities_YYYY-MM-DD.xml`

### **Expected Data**

- **City count:** Exactly 15 cities expected
- **Warning threshold:** Any count ≠ 15 triggers warning
- **Forecast days:** 4-day forecast (today + 3 days)

### **Download Settings**

- **URL:** `https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_cities.xml`
- **Source encoding:** ISO-8859-8 (Hebrew)
- **Target encoding:** UTF-8
- **Timeout:** 30 seconds
- **Retries:** 3 attempts

### **Logging Settings**

- **Log file:** `logs/forecast_automation.log`
- **Log levels:** INFO, SUCCESS, WARNING, ERROR
- **Output:** Both console AND log file

---

## 📊 Data Specifications

### **XML Structure**

```xml
<IsraelCitiesWeatherForecastMorning>
  <Identification>
    <IssueDateTime>YYYY-MM-DD HH:MM</IssueDateTime>
  </Identification>
  <Location> (×15)
    <LocationMetaData>
      <LocationNameEng>City Name</LocationNameEng>
      <LocationNameHeb>שם העיר</LocationNameHeb>
      <DisplayLat>32.1</DisplayLat>
      <DisplayLon>34.76</DisplayLon>
    </LocationMetaData>
    <LocationData>
      <TimeUnitData> (×4 days)
        <Date>YYYY-MM-DD</Date>
        <Element>
          <ElementName>Maximum temperature</ElementName>
          <ElementValue>30</ElementValue>
        </Element>
        <!-- More elements -->
      </TimeUnitData>
    </LocationData>
  </Location>
</IsraelCitiesWeatherForecastMorning>
```

### **Weather Elements**

- Maximum temperature (°C)
- Minimum temperature (°C)
- Weather code (numeric)
- Maximum relative humidity (%)
- Minimum relative humidity (%)
- Wind direction and speed

**Note:** Day 1 has all elements; Days 2-4 typically have only temperature and weather code.

### **Weather Codes** (Common)

- `1250` - Clear/Sunny
- `1220` - Partly Cloudy
- `1310` - Mostly Clear
- `1580` - Very Hot/Sunny

---

## 🚀 Execution

### **Manual Testing (Current)**

```bash
# Test minimal extraction (one city)
python exploration/test_extraction_minimal.py

# Test full extraction (all 15 cities)
python exploration/extract_all_cities.py
```

### **Production Usage (Future)**

```bash
# Normal run (download, extract, generate image)
python forecast_workflow.py

# Dry run (preview without changing files)
python forecast_workflow.py --dry-run

# Check logs
type logs\forecast_automation.log
```

### **Automated Scheduling (Phase 4)**

- **Method:** Windows Task Scheduler
- **Frequency:** Daily at 6:00 AM
- **Command:** `python forecast_workflow.py`
- **Working Directory:** `C:\Users\noamw\Desktop\ims\Automated Daily Forecast\`

---

## 📝 Development Status

### **Phase 1: Complete ✅**

- [x] Python environment setup (3.13.2)
- [x] XML structure understanding
- [x] UTF-8 encoding working
- [x] Hebrew text handling
- [x] Full extraction working (all 15 cities)
- [x] North-to-South sorting
- [x] Download script with retry logic
- [x] Archive management (14-day retention)
- [x] Enhanced extraction with error handling
- [x] Main workflow orchestration
- [x] Comprehensive logging system
- [x] Dry-run mode

### **Phase 2: Complete ✅**

- [x] Fredoka variable font integration
- [x] Hebrew RTL text rendering with python-bidi
- [x] iOS-style weather emoji icons (PNG overlays)
- [x] Professional header with logo and date
- [x] White header + gradient background
- [x] 1080x1920px image generation
- [x] Single city proof-of-concept (Tel Aviv)
- [x] Easy-to-configure design constants

### **Phase 3: Planned 📅**

- [ ] Single image with all 15 cities
- [ ] Vertical layout design (north to south)
- [ ] Weather icon, temperature, city name for each
- [ ] Final production-ready design

### **Phase 4: Planned 📅**

- [ ] Email delivery to social media team
- [ ] Automated daily scheduling (6:00 AM)
- [ ] Error notification system

### **Phase 5: Future 📅**

- [ ] Server deployment
- [ ] Linux compatibility testing
- [ ] Handoff to IT team

---

## 🎓 For Beginners

### **Understanding This Structure**

**Think of it like organizing a kitchen:**

- **Raw ingredients** = XML files (in `archive/`)
- **Recipe book** = Python scripts
- **Prep area** = Current working XML file
- **Final dishes** = Generated images (in `output/`)
- **Kitchen log** = What you cooked and when (in `logs/`)

**The workflow:**

1. **Shop for ingredients** (download XML)
2. **Prep ingredients** (convert encoding, extract data)
3. **Cook** (generate image) - Phase 2
4. **Serve** (email image) - Phase 4
5. **Clean up** (delete old archives)
6. **Write in log book** (record what happened)

### **Key Concepts**

**Script** = A Python file that does one specific job
**Workflow** = Multiple scripts working together
**Archive** = Old copies kept as backup
**Log** = A diary of what the script did
**Dry Run** = Practice run without making real changes
**Encoding** = How Hebrew letters are stored in the file

---

**Last Updated:** October 16, 2025
**Next Step:** Phase 3 - Complete design with all 15 cities in single image
