# Development Guide

## Getting Started

### Development Environment

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python forecast_workflow.py --dry-run`

## Project Structure

```
├── Core scripts (project root)
├── assets/           # Images, fonts, icons
├── docs/             # Documentation
├── exploration/      # Test and development scripts
├── output/           # Generated images
├── logs/             # Application logs
└── archive/v1/       # Archived v1 code
```

## Code Style

- Use `pathlib` for all file paths
- Use `setup_logging()` from utils.py
- UTF-8 encoding everywhere
- Absolute paths preferred

## Making Changes

### Image Design

Visual parameters are in constants at the top of the generator script:

```python
# Configuration
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
ROW_PADDING = 160
# etc.
```

### Adding Data Fields

1. Update `extract_forecast.py` to extract new fields
2. Pass data to generator
3. Update tests

### Testing

```bash
# Full workflow test
python forecast_workflow.py --dry-run

# Image generation only
python generate_forecast_map.py

# Email test
python send_email_smtp.py --dry-run
```

## Logging

Use the shared logging system:

```python
from utils import setup_logging
logger = setup_logging()

logger.info("Normal operation")
logger.warning("Recoverable issue")
logger.error("Critical failure")
```

Logs are written to both console and `logs/forecast_automation.log`.

## Critical Implementation Notes

### XML Encoding
Always convert IMS XML from ISO-8859-8 to UTF-8 before parsing.

### Hebrew Text
Use python-bidi for RTL text rendering, or Pillow's `direction='rtl'` with Raqm.

### Variable Fonts
Axis order matters! For Noto Sans Hebrew: `[width, weight]`

```python
font.set_variation_by_axes([100, 600])  # width=100, weight=600
```

## Version Control

### Branching
- `main` - Production code
- Feature branches for development

### Tags
- `v1.0-final` - Archived v1 code
- `v2.0.0` - V2 release (when complete)

---

*This documentation will be expanded as V2 development progresses.*
