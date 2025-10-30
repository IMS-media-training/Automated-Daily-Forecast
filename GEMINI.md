# GEMINI.md

## Project Purpose and Functionality

This project automates the creation of daily weather forecast images for the Israel Meteorological Service (IMS). It is a Python application designed to be run as a daily scheduled task, generating visually appealing and informative Instagram stories.

The core functionality of the application is to:

1.  **Fetch Data:** Download the latest weather forecast data from the IMS website, which is provided in XML format with ISO-8859-8 encoding.
2.  **Process Data:** Convert the XML data to UTF-8, parse it, and extract the relevant forecast information for 15 major Israeli cities.
3.  **Generate Image:** Create a 1080x1920 image (Instagram story format) that displays the weather forecast for all 15 cities, sorted geographically from north to south. The image includes the IMS logo, the date, and weather icons for each city.

## Project Structure

The project is organized into the following directory structure:

```
Automated Daily Forecast/
├── 📄 Production Scripts
│   ├── forecast_workflow.py      # Main orchestration script
│   ├── download_forecast.py      # XML download & encoding
│   ├── extract_forecast.py       # Data extraction
│   ├── generate_forecast_image.py # Image generation
│   └── utils.py                  # Shared utilities
│
├── 📁 Data & Output
│   ├── archive/                  # Historical XML (14 days)
│   ├── logs/                     # Automation logs
│   └── output/                   # Generated images
│
├── 📁 Assets
│   ├── assets/logos/             # IMS logo files
│   ├── assets/weather_icons/    # Weather emoji PNGs
│   └── fonts/                    # Open Sans variable font
│
├── 📁 Development
│   └── exploration/              # Test & development scripts
│
└── 📚 Documentation
    ├── README.md                 # Project README
    ├── GEMINI.md                 # This file
    └── docs/                     # Additional documentation
```

## Core Modules

The project is built around a set of core Python modules:

*   **`forecast_workflow.py`:** This is the main entry point of the application. It orchestrates the entire workflow by calling the other modules in the correct order. It also handles command-line arguments and logging.
*   **`download_forecast.py`:** This module is responsible for downloading the XML forecast data from the IMS website. It includes features like retry logic, timeout handling, and encoding conversion (from ISO-8859-8 to UTF-8). It also manages an archive of historical forecast data.
*   **`extract_forecast.py`:** This module parses the XML data and extracts the weather forecast for each of the 15 target cities. It then sorts the cities by latitude (from north to south) and validates the extracted data.
*   **`generate_forecast_image.py`:** This module uses the `Pillow` library to generate the final forecast image. It includes extensive configuration options for fonts, colors, and layout. It also handles the rendering of right-to-left (RTL) Hebrew text.
*   **`utils.py`:** This module contains a collection of utility functions that are shared across the other modules. This includes functions for logging, date handling, file management, and data validation.

## Key Features

*   **Automated Workflow:** The entire process of downloading, processing, and generating the forecast image is fully automated.
*   **Robust Error Handling:** The application includes comprehensive error handling, including retry logic for network requests and fallback to archived data.
*   **Hebrew Language Support:** The application correctly handles Hebrew text, including right-to-left (RTL) rendering in the generated image.
*   **Configurable Design:** The visual design of the forecast image is highly configurable, with constants for fonts, colors, and layout defined at the top of the `generate_forecast_image.py` script.
*   **Modular Architecture:** The project is well-structured and modular, making it easy to understand, maintain, and extend.

## Usage

### Prerequisites

*   Python 3.13+
*   An internet connection

### Installation

1.  Clone the repository.
2.  Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the complete workflow, execute the `forecast_workflow.py` script:

```bash
python forecast_workflow.py
```

This will download the latest forecast, extract the data, and generate a new forecast image in the `output` directory.

You can also run the workflow in "dry-run" mode, which will simulate the process without creating or modifying any files:

```bash
python forecast_workflow.py --dry-run
```