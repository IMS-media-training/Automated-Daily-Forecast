# Version 1.0 Archive

This directory contains the archived code and documentation from Version 1.0 of the IMS Weather Forecast Automation project.

## What Was V1?

Version 1.0 featured a **vertical list-based layout** with all 15 Israeli cities arranged in a single column, sorted north to south by latitude.

### Key Characteristics

- **Layout**: Vertical list (1080x1920px Instagram story)
- **Font**: Open Sans Variable
- **Background**: Sky blue to white gradient
- **Cities**: Displayed in a centered vertical list
- **Design**: Simple, clean, functional

### Archived Files

- `generate_forecast_image.py` - Main image generator for list layout
- `generate_image.py` - Single-city POC (from exploration/)
- `CLAUDE.md` - Original Claude Code instructions
- `docs/` - Original documentation

### Why Archived?

Version 2.0 introduces a completely new **map-based geographic layout** where cities are positioned on an actual map of Israel. This required a complete redesign of the image generation system.

### Recovery

To restore v1 code completely:

```bash
git checkout v1.0-final
```

This tag preserves the exact state of the repository before the v2 transition.

## Timeline

- **Development**: October - November 2025
- **Production**: November 17, 2025
- **Archived**: November 24, 2025
