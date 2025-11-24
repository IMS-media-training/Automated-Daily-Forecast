# IMS Weather Story Automation Project

## Technical Documentation

**Last Updated:** November 10, 2025
**Project Status:** Phase 4 Complete ✅

---

## 🎯 Project Overview

### Goal

This project automates the creation of daily weather forecast images for the Israel Meteorological Service (IMS). It is a Python application designed to be run as a daily scheduled task, generating visually appealing and informative Instagram stories.

The core functionality of the application is to:

1.  **Fetch Data:** Download the latest weather forecast data from the IMS website, which is provided in XML format with ISO-8859-8 encoding.
2.  **Process Data:** Convert the XML data to UTF-8, parse it, and extract the relevant forecast information for 15 major Israeli cities.
3.  **Generate Image:** Create a 1080x1920 image (Instagram story format) that displays the weather forecast for all 15 cities, sorted geographically from north to south. The image includes the IMS logo, the date, and weather icons for each city. The image has a daily random gradient background.
4.  **Deliver Image:** The application can deliver the generated image via email using SMTP.

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

-   Each `<Location>` represents one city.
-   Each city has 4 `<TimeUnitData>` blocks (a 4-day forecast).
-   Each `<TimeUnitData>` has a `<Date>` element.
-   Weather data is stored in `<Element>` tags with an `<ElementName>` and `<ElementValue>`.

### Cities Data

The project processes data for 15 Israeli cities, which are then sorted from north to south by latitude.

### Weather Codes

The project uses a comprehensive mapping of IMS weather codes to Twemoji icons, as defined in `ims_weather_codes.json`. This file covers all 23 IMS weather codes for Israel.

---

## 🔧 Technical Implementation

### Core Modules

-   **`forecast_workflow.py`:** The main entry point of the application. It orchestrates the entire workflow by calling the other modules in the correct order. It also handles command-line arguments and logging.
-   **`download_forecast.py`:** This module is responsible for downloading the XML forecast data from the IMS website. It includes features like retry logic, timeout handling, and encoding conversion (from ISO-8859-8 to UTF-8). It also manages an archive of historical forecast data.
-   **`extract_forecast.py`:** This module parses the XML data and extracts the weather forecast for each of the 15 target cities. It then sorts the cities by latitude (from north to south) and validates the extracted data.
-   **`generate_forecast_image.py`:** This module uses the `Pillow` library to generate the final forecast image. It includes extensive configuration options for fonts, colors, and layout. It also handles the rendering of right-to-left (RTL) Hebrew text and generates a random gradient background for each image.
-   **`send_email_smtp.py`:** This module handles email delivery of the forecast image using a standard SMTP server.
-   **`utils.py`:** This module contains a collection of utility functions that are shared across the other modules. This includes functions for logging, date handling, file management, and data validation.

### Key Libraries

-   **`requests`:** For downloading the XML forecast data.
-   **`Pillow`:** For all image generation tasks.
-   **`python-bidi`:** For right-to-left text rendering.
-   **`python-dotenv`:** For managing environment variables for SMTP credentials.

### Automation

The project is automated using a GitHub Actions workflow defined in `.github/workflows/daily-forecast.yml`. The workflow is configured to run daily at 6:00 AM Israel time and can also be triggered manually. It uses GitHub Secrets to securely store and use the SMTP credentials.

### Configuration

The application is configured through a combination of constants defined at the top of the Python scripts and environment variables for sensitive information like SMTP credentials.

---

## 📝 Future Development

### Phase 5: Server Deployment

-   Test the application in a Linux environment.
-   Create a comprehensive deployment guide for the IT team.
-   Transition the application from GitHub Actions to a production server.

---

## End of Documentation
