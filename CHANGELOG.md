# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Map-based geographic layout with Israel silhouette
- Textual weather description from IMS country forecast
- Hebrew calendar dates alongside Gregorian (using pyluach)
- Noto Sans Hebrew variable font
- New weather icon set (weather_icons 2.0)
- Dual logos: IMS + Ministry of Transport
- City-specific layouts (RTL/TTB/LTR) based on map position

### Changed
- Complete visual redesign from vertical list to geographic map
- Background: gradient overlaid with map vs. simple gradient
- Font: Open Sans → Noto Sans Hebrew
- Documentation: lean CLAUDE.md + detailed docs/ structure

### Removed
- Vertical list layout (preserved in archive/v1/)

---

## [1.0.0] - 2025-11-17

**Version 1 - List-Based Layout** (Archived)

Production release with automated daily forecasts via GitHub Actions.

### Features
- Download forecast data from IMS (isr_cities.xml)
- Extract weather for 15 Israeli cities, sorted north-to-south
- Generate 1080x1920px Instagram story image with vertical list layout
- Open Sans variable font with Hebrew RTL support
- Weather icons (Twemoji) covering all 23 IMS codes
- SMTP email delivery with professional HTML template
- Multi-recipient support via recipients.txt
- GitHub Actions automation (daily at 6 AM Israel time)
- Dry-run mode for safe testing

### Technical Details
- Python 3.8+ compatible
- ISO-8859-8 to UTF-8 encoding conversion
- Archive management with 14-day retention
- Smart date detection for IMS publishing schedule

---

## Version 1.x History (Summarized)

| Version | Date | Milestone |
|---------|------|-----------|
| 1.0.0 | 2025-11-17 | Phase 4c: Multi-recipient GitHub Actions |
| 4.2.0 | 2025-11-13 | External email template with IMS branding |
| 4.1.0 | 2025-11-10 | Daily random gradients |
| 4.0.0 | 2025-11-05 | GitHub Actions automation |
| 3.5.0 | 2025-11-03 | Complete Twemoji icon set (23 codes) |
| 3.0.0 | 2025-10-30 | All 15 cities image generation |
| 2.0.0 | 2025-10-16 | Single city POC with variable fonts |
| 1.0.0 | 2025-10-15 | XML download and data extraction |

For detailed v1 history, see `archive/v1/docs/` or checkout tag `v1.0-final`.

---

## Versioning Strategy

- **Major (x.0.0):** Breaking changes, major redesigns
- **Minor (x.y.0):** New features, backward compatible
- **Patch (x.y.z):** Bug fixes, minor improvements

---

**Maintained by:** Noam W, IMS Design Team
