# IMS Weather Automation - Project Structure

**Last Updated:** November 17, 2025
**Status:** Phase 4 Complete (Multi-Recipient Support)

---

## 📁 File Structure

```
Automated-Daily-Forecast/
├── forecast_workflow.py      # Main orchestration script
├── download_forecast.py      # XML download & encoding
├── extract_forecast.py       # Data extraction
├── generate_forecast_image.py # Image generation
├── send_email_smtp.py        # Email delivery (SMTP)
├── utils.py                  # Shared utilities
├── email_template.html       # External email template
├── recipients.txt            # Email recipients (gitignored)
├── recipients.txt.example    # Recipients template
├── .env                      # Environment variables (gitignored)
├── .env.example              # Environment template
├── archive/                  # Historical XML (14 days)
├── assets/                   # Logos, weather icons, and fonts
├── docs/                     # Project documentation
├── exploration/              # Test & development scripts
├── logs/                     # Automation logs
├── output/                   # Generated images
├── .github/                  # GitHub Actions workflows
├── requirements.txt          # Python dependencies
└── README.md                 # Project README
```

---

## 🔄 Data Flow

The daily automated workflow follows these steps:

1.  **Download:** The `forecast_workflow.py` script calls `download_forecast.py` to download the latest forecast XML from the IMS website. The XML is converted from ISO-8859-8 to UTF-8 and saved to the root directory as `isr_cities_utf8.xml`. A copy is also saved to the `archive/` directory.
2.  **Extraction:** The `forecast_workflow.py` script calls `extract_forecast.py` to parse the XML file, extract the weather data for the 15 target cities, and sort them from north to south.
3.  **Image Generation:** The `forecast_workflow.py` script calls `generate_forecast_image.py` to create the 1080x1920px Instagram story image. The image is generated with a random daily gradient background.
4.  **Email Delivery:** The `forecast_workflow.py` script calls `send_email_smtp.py` to send the generated image to multiple recipients (from `recipients.txt`) via SMTP using the external `email_template.html` template.

---

## 🎯 Script Purposes

### Production Scripts

| Script | Purpose |
|---|---|
| `forecast_workflow.py` | Orchestrates the entire daily workflow. |
| `download_forecast.py` | Downloads the XML from IMS, converts the encoding, and archives it. |
| `extract_forecast.py` | Extracts the weather data for the specified date from the XML file. |
| `generate_forecast_image.py` | Generates the forecast image. |
| `send_email_smtp.py` | Sends the forecast image via email using SMTP. |
| `utils.py` | Contains shared utility functions used by the other scripts. |

### Exploration Scripts

The `exploration/` directory contains scripts used for testing and development.

---

## 📦 Dependencies

### External Libraries

-   `requests>=2.31.0`: For downloading the XML from IMS.
-   `Pillow>=10.0.0`: For image generation.
-   `python-bidi>=0.4.2`: For Hebrew RTL text support.
-   `python-dotenv>=1.0.0`: For managing environment variables.

All dependencies can be installed by running:
```bash
pip install -r requirements.txt
```

---

## 🗂️ File Retention Policies

| Folder | File Type | Retention | Management |
|---|---|---|---|
| `archive/` | XML files | 14 days | Automatically managed by `download_forecast.py`. |
| `logs/` | Log files | Manual | Logs are appended to `forecast_automation.log`. |
| `output/` | Image files | Manual | Generated images are saved in this directory. |

---