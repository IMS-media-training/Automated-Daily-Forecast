# V2 Roadmap

## Vision

Transform the IMS Weather Forecast from a simple vertical list to a **geographic map-based design** where cities are positioned on an actual map of Israel, creating a more visually engaging and intuitive Instagram story.

### Design Reference
**Figma:** https://www.figma.com/design/YVPUc24KCJIFrHpoXKrHz7/Story-Layout-V2.0?node-id=1-2

### Key Visual Changes

| Element | V1 | V2 |
|---------|----|----|
| Layout | Vertical list (north to south) | Geographic map positioning |
| Background | Sky blue → white gradient | Cyan → magenta gradient with Israel map |
| Font | Open Sans | Noto Sans Hebrew |
| Date | Gregorian only | Hebrew + Gregorian + Jewish calendar |
| Content | Cities + temperatures | + Textual weather description |
| Logos | IMS only | IMS + Ministry of Transport |
| City display | Uniform rows | Adaptive layouts (RTL/TTB/LTR) |

---

## New Features in V2

### 1. Geographic City Positioning
Cities positioned on Israel map at their actual geographic locations using manual x,y coordinates from Figma design.

### 2. Textual Weather Description
Daily forecast text from `isr_country.xml` displayed on the image, providing context beyond just temperatures.

### 3. Hebrew Calendar Dates
Full date display: "17/11/2025 כ"ו בחשוון התשפ"ו"
- Gregorian date (DD/MM/YYYY)
- Hebrew calendar date using pyluach library

### 4. Adaptive City Layouts
Different component layouts based on map position:
- **RTL** (icon left, text right): Coastal cities (Haifa, Tel Aviv, Ashdod)
- **TTB** (icon top, text below): Inland cities (Afula, Lod, Beer Sheva)
- **LTR** (text left, icon right): Eastern cities (Ein Gedi)

### 5. Enhanced Visual Design
- Cyan-to-magenta gradient background
- Israel map silhouette with effects (shadow, texture)
- Dual logos: IMS + Ministry of Transport
- New weather icon set (weather_icons 2.0)

---

## Milestones

### Milestone 1: Data Pipeline Update
**Status:** Not Started

**Objectives:**
- Download and parse `isr_country.xml` for textual forecast
- Add Hebrew calendar conversion with pyluach
- Update extraction to include weather description
- Test complete data pipeline

**New Data Source:**
- URL: `https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_country.xml`
- Content: Daily textual weather description in Hebrew
- Same encoding handling as cities XML (ISO-8859-8 → UTF-8)

**Deliverables:**
- [ ] `download_country_forecast.py` or update to existing download script
- [ ] Hebrew calendar utility in `utils.py`
- [ ] Updated `extract_forecast.py` with description field
- [ ] Tested data pipeline

---

### Milestone 2: Asset Preparation
**Status:** Not Started

**Objectives:**
- Export Israel map from Figma (PNG with effects)
- Download Noto Sans Hebrew variable font
- Define city coordinate mapping from Figma
- Organize new assets structure

**Assets to Prepare:**
- [ ] Israel map PNG (with inner shadow, drop shadow, texture baked in)
- [ ] Noto Sans Hebrew variable font
- [ ] City coordinates dictionary (15 cities with x, y, layout type)
- [ ] Ministry of Transport logo

**City Coordinates (from Figma):**
```python
CITY_POSITIONS = {
    'Zefat': {'x': 335, 'y': 19, 'layout': 'RTL'},
    'Nazareth': {'x': 424, 'y': 180, 'layout': 'RTL'},
    'Katzrin': {'x': 681, 'y': 170, 'layout': 'TTB'},
    'Tiberias': {'x': 588, 'y': 331, 'layout': 'RTL'},
    'Haifa': {'x': 159, 'y': 224, 'layout': 'RTL'},
    'Afula': {'x': 424, 'y': 289, 'layout': 'TTB'},
    'Tel Aviv': {'x': 99, 'y': 421, 'layout': 'RTL'},
    'Lod': {'x': 337, 'y': 457, 'layout': 'TTB'},
    'Beit Shean': {'x': 574, 'y': 490, 'layout': 'TTB'},
    'Ashdod': {'x': 75, 'y': 567, 'layout': 'RTL'},
    'Jerusalem': {'x': 328, 'y': 623, 'layout': 'RTL'},
    'Ein Gedi': {'x': 571, 'y': 702, 'layout': 'LTR'},
    'Beer Sheva': {'x': 300, 'y': 738, 'layout': 'TTB'},
    'Mitzpe Ramon': {'x': 265, 'y': 981, 'layout': 'TTB'},
    'Eilat': {'x': 315, 'y': 1260, 'layout': 'TTB'},
}
```

---

### Milestone 3: Map-Based Image Generator
**Status:** Not Started

**Objectives:**
- Build new `generate_forecast_map.py`
- Implement gradient background (cyan → magenta)
- Add map overlay positioning
- Create city components with adaptive layouts
- Position weather icons at geographic locations

**Technical Approach:**
1. Create canvas (1080x1920)
2. Draw gradient background
3. Overlay Israel map PNG
4. Position each city component at coordinates
5. Render with appropriate layout (RTL/TTB/LTR)

**Deliverables:**
- [ ] `generate_forecast_map.py` with full city rendering
- [ ] Adaptive layout system for city components
- [ ] Weather icon positioning on map

---

### Milestone 4: Complete Visual Design
**Status:** Not Started

**Objectives:**
- Add header with trilingual date (Hebrew + Gregorian + Jewish)
- Add textual weather description panel
- Add dual logos (IMS + Ministry of Transport)
- Fine-tune typography and spacing

**Design Elements:**
- Header: Date with Hebrew calendar
- Description: Right-aligned text panel on image
- Footer: Logo row with IMS and Ministry of Transport

**Deliverables:**
- [ ] Complete header with date formatting
- [ ] Weather description text rendering
- [ ] Logo positioning and sizing
- [ ] Visual polish and spacing adjustments

---

### Milestone 5: Integration & Deployment
**Status:** Not Started

**Objectives:**
- Update `forecast_workflow.py` to use new generator
- Test end-to-end workflow
- Update all documentation
- Deploy to GitHub Actions

**Testing:**
- [ ] Dry-run mode works correctly
- [ ] Email delivery with new image format
- [ ] Both remotes updated (origin + ims-production)

**Documentation Updates:**
- [ ] CLAUDE.md with new commands and patterns
- [ ] README.md with V2 features
- [ ] CHANGELOG.md with 2.0.0 release
- [ ] docs/ with updated architecture

---

## Technical Decisions

### Map Asset: Export from Figma
**Decision:** Export Israel map as PNG with all effects baked in
**Rationale:** Recreating inner shadow + drop shadow + texture in Pillow would add significant complexity for diminishing returns. Can revisit later if needed.

### City Coordinates: Manual from Figma
**Decision:** Use manual x,y positions from Figma design
**Rationale:** More accurate and visually appealing than calculating from lat/long. We have the exact positions from the Figma export.

### Font: Noto Sans Hebrew
**Decision:** Switch from Open Sans to Noto Sans Hebrew
**Rationale:** Better fit for the new design aesthetic. Still a variable font with weight/width axes.

### Repository Structure: In-Place Replacement
**Decision:** Replace V1 code in-place, archive old code
**Rationale:** Team doesn't need V1 running in parallel. Git tag preserves V1 for recovery if needed.

---

## Timeline Estimate

| Milestone | Estimated Sessions | Notes |
|-----------|-------------------|-------|
| M1: Data Pipeline | 1 session | Follows v1 patterns |
| M2: Asset Prep | 0.5 session | Mostly export/download |
| M3: Map Generator | 2-3 sessions | Core new code |
| M4: Visual Design | 1-2 sessions | Polish and details |
| M5: Integration | 1 session | Testing and docs |
| **Total** | **5-7 sessions** | |

---

## Resources

### Data Sources
- Cities: `https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_cities.xml`
- Country: `https://ims.gov.il/sites/default/files/ims_data/xml_files/isr_country.xml`

### Design
- Figma: https://www.figma.com/design/YVPUc24KCJIFrHpoXKrHz7/Story-Layout-V2.0

### Libraries
- pyluach - Hebrew calendar conversion
- Pillow - Image generation
- python-bidi - Hebrew RTL text

---

## Version History

- **2025-11-24:** V2 Roadmap created, Milestone 1 ready to start
- **2025-11-17:** V1 completed and tagged (v1.0-final)

---

*This document will be updated as milestones are completed.*
