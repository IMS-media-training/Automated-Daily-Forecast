# Milestone 3 Fixes & Refinements Plan

**Status:** Implementation Updates Applied (Dec 10, 2025)
**Agent:** Gemini 3.0 Pro (Architect/Visuals)

## 1. Analysis of Issues
- **Coordinate Offset:** Cities were rendering at the top-left.
  - *Root Cause:* `CITY_POSITIONS` were relative to the Map component (258, 288) but rendered as absolute canvas coordinates.
  - *Fix:* Applied `MAP_X` and `MAP_Y` offsets in `render_cities`.
- **Logos:** IMS logo (SVG) was missing, breaking the centered layout.
  - *Fix:* Implemented robust placeholder logic. If a logo fails to load, a labeled gray box is drawn to maintain layout structure.
- **Layouts:** User reported all cities using same layout.
  - *Verification:* Logs confirm correct layouts (RTL/TTB/LTR) are being assigned based on `CITY_NAME_MAPPING`.

## 2. Implemented Changes
- Modified `generate_forecast_map.py`:
  - Added coordinate offset logic.
  - Added debug logging for name mapping.
  - Added `IMS_PH` and `MoT_PH` placeholder generation.

## 3. Verification
- generated `output/debug_fix_02.png`.
- **Zefat Y:** 307px (Correct: 19px relative + 288px map offset).
- **Eilat Y:** 1548px (Correct: 1260px relative + 288px map offset).
- **Logos:** Both slots filled (IMS Placeholder + MoT Real).

## 4. Next Steps (Milestone 4: Polish)
1.  **IMS Logo:** Convert `assets/logos/ims_logo.svg` to PNG and save as `assets/logos/ims_logo.png`.
2.  **Weather Description:** Verify description rendering with fresh XML data (currently using stale fallback data which lacks description).
3.  **Visual QA:** Check font weights and specific positioning against Figma design.
