# Plan: Precise Figma Replication (V2 Production)

## Prologue: Codebase Maintenance
*Note: This section outlines strictly maintenance tasks to clean up the workspace before the new implementation. Do not execute these immediately.*
1.  **Archive Legacy Plans:** Move `docs/plans/fix_city_coordinates.md` to `archive/v1/docs/plans/`.
2.  **Archive Prototype Code:** Move `generate_forecast_map.py` (current iterative version) to `archive/v1/generate_forecast_map_v2_alpha.py` to preserve the logic while clearing the path for the clean implementation.
3.  **Git Status:** Ensure a clean working tree before starting the "Rebuild" phase.

---

## Core Objective
Recreate the Figma design with pixel-perfect precision using the `Pillow` library, strictly adhering to the coordinate systems, hierarchy, and styling properties extracted from the Figma React/Tailwind code.

## 1. Technical Architecture: "Container-Based Layout"
Instead of absolute coordinates for every element, we will define **Layout Containers** that mimic Figma's Frame structure. This allows us to use the relative coordinates directly from the design data without manual recalculation errors.

### 1.1 Coordinate System Hierarchy
1.  **Root Canvas:** `1080x1920`
2.  **Background:** Global Layer
3.  **Map Layer:** Absolute Position `(258, 288.3)`
4.  **Header Frame:** `(0, 0)` (Content starts at `top-[57px]`)
5.  **Forecast Data Frame:** Origin `(128, 248)`
    *   *All cities will be positioned relative to this origin.*
6.  **Description Frame:** Right-aligned anchor at `(851, 986)` (approx, needs logic adjustment for RTL text flow).
7.  **Logos Frame:** Origin `(633, 1709)`

## 2. Data Constants (Extracted from Figma)
*These values must be hardcoded as constants in the new script.*

### 2.1 Gradient
*   **Angle:** `-23.236` degrees (CSS standard).
    *   *Conversion:* $360 - 23.236 = 336.764$ degrees (approx).
*   **Stops:**
    *   `#DCFF57` (RGBA 220, 255, 87) at `62.599%`
    *   `#22B2FF` (RGBA 34, 178, 255) at `112.14%`

### 2.2 Typography
*   **Font Family:** `Noto Sans Hebrew` (Variable or Static).
*   **Styles:**
    *   **Header Date:** Size `36px`, Weight `900` (Black), Color `White`.
    *   **City Name:** Size `24px`, Weight `900` (Black), Color `Black`.
    *   **Temperature:** Size `20px`, Weight `600` (SemiBold), Color `Black`.
    *   **Description:** Size `24px`, Weight `600` (SemiBold), Color `Black`.
    *   **IMS Label:** Size `18px`, Weight `400` (Regular), Condensed Width `62.5`.

### 2.3 City "Auto-Layout" Logic
We must implement a mini-layout engine to replicate Figma's Flexbox behavior for cities.

*   **Common Padding:** `10px` (surrounding the content).
*   **Icon Size:** `50x50px`.
*   **Layout Types:**
    *   **RTL (Coastal/Western):**
        *   Flex Direction: Row (reversed).
        *   Gap: `16px`.
        *   Alignment: `items-center` (Vertical center).
        *   *Structure:* `[Icon] --16px-- [TextGroup(RightAligned)]`
    *   **TTB (Inland/Southern):**
        *   Flex Direction: Column.
        *   Gap: `0px` (or minimal, Figma shows `pb-px` padding hack).
        *   Alignment: `items-center` (Horizontal center).
        *   *Structure:* `[Icon] (centered) 
 [TextGroup(Centered)]`
    *   **LTR (Eastern - Ein Gedi):**
        *   Flex Direction: Row.
        *   Gap: `16px`.
        *   *Structure:* `[TextGroup(RightAligned?)] --16px-- [Icon]`

### 2.4 City Coordinates (Relative to `Forecast Data Frame` at `128, 248`)
| City | X (left) | Y (top) | Layout |
| :--- | :--- | :--- | :--- |
| Zefat | 335 | 19 | RTL |
| Nazareth | 424 | 180 | RTL |
| Katzrin | 681 | 170 | TTB |
| Tiberias | 588 | 331 | RTL |
| Haifa | 159 | 224 | RTL |
| Afula | 424 | 289 | TTB |
| Tel Aviv | 99 | 421 | RTL |
| Lod | 337 | 457 | TTB |
| Beit Shean | 574 | 490 | TTB |
| Ashdod | 75 | 567 | RTL |
| Jerusalem | 328 | 623 | RTL |
| Ein Gedi | 571 | 702 | LTR |
| Beer Sheva | 300 | 738 | TTB |
| Mitzpe Ramon | 265 | 981 | TTB |
| Eilat | 315 | 1260 | TTB |

## 3. Implementation Phases

### Phase 1: Foundation
1.  Create `generate_forecast_map_v2.py`.
2.  Implement `draw_gradient(canvas, angle, stops)` with precise math.
3.  Load fonts with correct variation settings (`wdth` axis support is crucial for IMS logo).

### Phase 2: The "Renderer" Class
Create a class `FigmaRenderer` to handle the coordinate offsets.
```python
class FigmaRenderer:
    def __init__(self, base_x, base_y):
        self.origin = (base_x, base_y)
    
    def draw_element(self, relative_x, relative_y, element):
        # Calculates absolute pos and pastes/draws
```

### Phase 3: Component Implementation
1.  **Header:** Implement text centering logic + separator line (`h-[7px]`, `w-full` inside `px-[100px]`).
2.  **Map:** Paste `israel_map.png` at `(258, 288)`.
3.  **Cities:**
    *   Implement `render_city_component(canvas, x, y, layout, data)`.
    *   This function MUST handle the internal padding (`10px`) and gap (`16px`) calculation to determine where the text lands relative to the icon.
4.  **Description:** Implement text wrapping for the description box.
5.  **Logos:** Implement the specific layout for IMS/MoT logos.

## 4. Verification Steps
1.  **Dry Run:** Generate `output/test/v2_precision_test_01.png`.
2.  **Overlay Check:** (Manual) Drag result into Figma or overlay with reference screenshot to check alignment.
3.  **Data Validation:** Ensure all 15 cities appear at the exact coordinates listed in section 2.4.

## 5. Execution Command
*To be executed after plan approval:*
```bash
python generate_forecast_map_v2.py --date "2025-12-17" --output "output/test/v2_final.png"
```
