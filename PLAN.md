# Crochet Project - Implementation Plan

**Created:** January 16, 2026
**Status:** Planning

---

## Data Model Hierarchy

To handle production growth with repeated pieces and variations, we need a **Style → Piece Instance** hierarchy:

```
STYLE (Design/Pattern)
  │
  ├── name: "V-Stitch Scarf with Fringe"
  ├── style_id: STYLE-001
  ├── base_stitch: STITCH-010 (V-stitch)
  ├── piece_type: scarf
  ├── has_fringe: true
  │
  └── ITEM INSTANCES (actual pieces made)
       │
       ├── PIECE-001: Beige, 180cm (sold)
       ├── PIECE-005: Navy Blue, 180cm (available)
       └── PIECE-012: Beige, 150cm (shorter variation)
```

### Entity Relationships

```
┌─────────────┐
│   STYLE     │ ◄─── Design/pattern template
│ (STYLE-001) │
└──────┬──────┘
       │ 1:many
       ▼
┌─────────────┐
│    ITEM     │ ◄─── Actual finished piece
│ (PIECE-001)  │
└──────┬──────┘
       │ many:many
       ▼
┌─────────────┐      ┌─────────────┐
│    YARN     │      │   STITCH    │
│ (YARN-001)  │      │ (STITCH-001)│
└─────────────┘      └─────────────┘
```

---

## Phase 1: Foundation Setup

### Task 1.1: Define Stitches
**Priority:** First (stitches are referenced by styles and pieces)

| Step | Action | Output |
|------|--------|--------|
| 1.1.1 | Review existing stitches in `stitches.json` | List of current stitches |
| 1.1.2 | Identify stitches used in current pieces (from photos) | V-stitch, Puff, Shell, Granny |
| 1.1.3 | Add missing stitches with proper IDs | Updated `stitches.json` |
| 1.1.4 | Assign final IDs: `STITCH-001` to `STITCH-NNN` | Confirmed stitch library |

**Current stitches to confirm:**
- V-Stitch (used in yellow cowl, beige scarf, green scarf, orange shawl)
- Puff/Bobble Stitch (used in white scarf, grey scarf)
- Shell/Fan Stitch (used in red scarf)
- Granny Square (used in peach squares)

---

### Task 1.2: Define Styles (NEW)
**Priority:** Second (styles group similar pieces)

| Step | Action | Output |
|------|--------|--------|
| 1.2.1 | Create `styles.json` schema | New schema file |
| 1.2.2 | Create `styles.json` data file | New data file |
| 1.2.3 | Define styles from grouped photos | Style entries |

**Styles to create from current pieces:**

| Style ID | Name | Type | Main Stitch |
|----------|------|------|-------------|
| STYLE-001 | V-Stitch Cowl | cowl | V-stitch |
| STYLE-002 | V-Stitch Scarf with Fringe | scarf | V-stitch |
| STYLE-003 | Puff Stitch Scarf | scarf | Puff stitch |
| STYLE-004 | V-Stitch Scarf (no fringe) | scarf | V-stitch |
| STYLE-005 | V-Stitch Triangle Shawl | shawl | V-stitch |
| STYLE-006 | Granny Square Blanket | blanket | Granny square |
| STYLE-007 | Chunky Puff Scarf | scarf | Puff stitch |
| STYLE-008 | Shell Stitch Scarf | scarf | Shell stitch |

---

### Task 1.3: Define Pieces with IDs
**Priority:** Third (pieces reference styles and stitches)

| Step | Action | Output |
|------|--------|--------|
| 1.3.1 | Assign piece IDs to each grouped set | ID assignments |
| 1.3.2 | Extract metadata from photo dates | date_started estimates |
| 1.3.3 | Link pieces to styles | style_id references |
| 1.3.4 | Update `pieces.json` with full data | Complete piece records |

**Items to create:**

| Item ID | Style | Color | Photos | Earliest Date |
|---------|-------|-------|--------|---------------|
| PIECE-001 | STYLE-001 | Yellow/Mustard | 2 | 2025-11-23 |
| PIECE-002 | STYLE-002 | Beige/Taupe | 4 | 2025-12-13 |
| PIECE-003 | STYLE-003 | White/Cream | 4 | 2025-12-19 |
| PIECE-004 | STYLE-004 | Green | 2 | 2025-12-23 |
| PIECE-005 | STYLE-005 | Orange/Peach | 2 | 2026-01-01 |
| PIECE-006 | STYLE-006 | Peach | 1 | 2025-11-22 |
| PIECE-007 | STYLE-007 | Grey | 1 | 2025-12-20 |
| PIECE-008 | STYLE-008 | Red/Magenta | 1 | 2025-12-29 |

---

### Task 1.4: Rename Photos
**Priority:** Fourth (after pieces have IDs)

| Step | Action | Output |
|------|--------|--------|
| 1.4.1 | Create photo naming convention | Documented standard |
| 1.4.2 | Create Python script for batch rename | `src/rename_photos.py` |
| 1.4.3 | Execute rename for all pieces | Renamed files |
| 1.4.4 | Move photos to piece subfolders | Organized folders |

**Naming Convention:**
```
{PIECE-ID}_{sequence}_{descriptor}.{ext}

Examples:
PIECE-001_01_wip.jpg
PIECE-001_02_finished.jpg
PIECE-002_01_wip.jpg
PIECE-002_02_detail.jpg
PIECE-002_03_worn.jpg
PIECE-002_04_flat.jpg
```

---

## Phase 2: Automation Scripts

### Task 2.1: Photo Metadata Extractor
**Script:** `src/extract_metadata.py`

| Function | Input | Output |
|----------|-------|--------|
| Extract date from filename | `20251123_193645.jpg` | `2025-11-23` |
| Extract EXIF data (if available) | Photo file | Date, dimensions |
| Generate piece stub | Photo files | Draft piece JSON |

---

### Task 2.2: Photo Renamer
**Script:** `src/rename_photos.py`

| Function | Input | Output |
|----------|-------|--------|
| Batch rename by mapping | Old names + piece IDs | Renamed files |
| Create piece subfolders | Item IDs | Folder structure |
| Update references | Old paths | New paths in JSON |

---

### Task 2.3: Piece Creator
**Script:** `src/create_piece.py`

| Function | Input | Output |
|----------|-------|--------|
| Create new piece from template | Style ID, color, date | New piece in JSON |
| Auto-assign next ID | Current max ID | `PIECE-NNN` |
| Link to style | Style ID | Populated fields |

---

### Task 2.4: Stitch Classifier (Future)
**Script:** `src/classify_stitch.py`

| Function | Input | Output |
|----------|-------|--------|
| Compare photo to reference | Item photo + stitch refs | Suggested stitch |
| Confidence scoring | Comparison results | Match percentage |

---

### Task 2.5: Price Calculator
**Script:** `src/calculate_price.py`

**Formula:**
```
material_cost = Σ (yarn.price_paid × balls_used)
labor_cost = work_hours_actual × hourly_rate
suggested_price = (material_cost + labor_cost) × (1 + profit_margin)
```

| Function | Input | Output |
|----------|-------|--------|
| Calculate material cost | Item yarns_used | Total material EUR |
| Calculate labor cost | Hours + rate | Labor EUR |
| Suggest price | Costs + margin | Suggested price |
| Compare to market | Style history | Price range |

**Configuration (in settings or per-user):**
```json
{
  "hourly_rate": 8.00,
  "profit_margin": 0.20,
  "min_margin": 0.10,
  "round_to": 5
}
```

**Example:**
```
Item: V-Stitch Scarf - Beige
├── Material: 3 balls × €3.50 = €10.50
├── Labor: 15 hours × €8.00 = €120.00
├── Subtotal: €130.50
├── Margin (20%): €26.10
├── Total: €156.60
└── Suggested (rounded): €155.00
```

**Learning features:**
- Track `price_sold` vs `suggested_price` to adjust recommendations
- Compare similar styles to suggest competitive pricing
- Flag if suggested price differs significantly from market (style avg)

---

## Phase 3: Data Population

### Task 3.1: Populate Stitches
- [ ] Confirm V-Stitch entry
- [ ] Confirm Puff Stitch entry
- [ ] Confirm Shell Stitch entry
- [ ] Confirm Granny Square entry
- [ ] Add instruction links

### Task 3.2: Populate Styles
- [ ] Create all 8 styles from current pieces
- [ ] Link to primary stitches
- [ ] Add base dimensions and characteristics

### Task 3.3: Populate Pieces
- [ ] Create all 8 pieces with full metadata
- [ ] Extract dates from photo filenames
- [ ] Estimate work hours
- [ ] Set initial status (available/sold/gifted)
- [ ] Link to styles and stitches

### Task 3.4: Organize Photos
- [ ] Rename all photos
- [ ] Move to piece subfolders
- [ ] Remove duplicates
- [ ] Update JSON references

---

## Workflow for New Items (Future)

When creating a new piece:

```
1. PHOTO INTAKE
   └── Add photos to images/pieces/inbox/

2. CLASSIFY (manual or assisted)
   ├── Identify stitch → STITCH-ID
   ├── Match to existing style OR create new → STYLE-ID
   └── Extract date from filename

3. CREATE ITEM
   ├── Run: python src/create_piece.py --style STYLE-002 --color "Navy Blue"
   ├── Auto-assigns: PIECE-009
   └── Creates stub in pieces.json

4. RENAME & ORGANIZE PHOTOS
   ├── Run: python src/rename_photos.py --piece PIECE-009
   └── Moves to images/pieces/PIECE-009/

5. COMPLETE DATA
   └── Fill in: dimensions, work_hours, price, status
```

---

## File Structure (Updated)

```
crochet/
├── CLAUDE.md
├── PLAN.md                    # This file
├── README.md
├── data/
│   ├── pieces.json
│   ├── yarns.json
│   ├── stitches.json
│   ├── styles.json            # NEW
│   └── schemas/
│       ├── piece.schema.json
│       ├── yarn.schema.json
│       ├── stitch.schema.json
│       └── style.schema.json  # NEW
├── images/
│   ├── pieces/
│   │   ├── inbox/             # NEW - for unsorted photos
│   │   ├── PIECE-001/
│   │   ├── PIECE-002/
│   │   └── ...
│   ├── yarns/
│   ├── stitches/
│   └── marketing/
├── src/                       # NEW
│   ├── __init__.py
│   ├── extract_metadata.py
│   ├── rename_photos.py
│   ├── create_piece.py
│   └── classify_stitch.py
└── docs/
```

---

## Tomorrow's Session Checklist

### Morning: Foundation
- [ ] Review and confirm stitch definitions
- [ ] Create `styles.json` schema and initial data
- [ ] Assign piece IDs to all 8 pieces
- [ ] Map photos to pieces

### Afternoon: Data Entry
- [ ] Update `pieces.json` with full metadata
- [ ] Extract dates from photo filenames
- [ ] Link pieces → styles → stitches

### Scripts (if time permits)
- [ ] Create `src/rename_photos.py`
- [ ] Execute photo renaming
- [ ] Organize into folders

---

## Decisions Made

1. **Naming for variations:** Item names INCLUDE color
   - Example: "V-Stitch Scarf with Fringe - Beige"
   - Style name stays generic, piece name includes color

2. **ID sequence:** Sequential by entry (not chronological)
   - Simpler to manage
   - Use `date_started` field for chronological queries
   - Note: Changing IDs later is difficult (photo renames, JSON refs)

3. **Work hours tracking:** Track ALL for learning/prediction
   - `work_hours_estimated`: Initial estimate before starting
   - `work_sessions`: Array of {date, hours} for per-session tracking
   - `work_hours_actual`: Calculated sum of sessions (actual time spent)
   - Over time, compare estimated vs actual to improve predictions
   - Style can store `avg_hours` based on completed pieces

4. **Pricing strategy:** Per ITEM (not per style)
   - Each piece has its own `price` field
   - Style can have `base_price` as suggestion only

---

## Schema Updates Needed

### New: style.schema.json
```json
{
  "id": "STYLE-001",
  "name": "V-Stitch Scarf with Fringe",
  "piece_type": "scarf",
  "primary_stitch_id": "STITCH-010",
  "secondary_stitches": [],
  "has_fringe": true,
  "base_dimensions": { "width_cm": 25, "length_cm": 180 },
  "difficulty": "beginner",
  "estimated_hours": 15,
  "avg_hours_actual": null,
  "pieces_completed": 0,
  "base_price": 35.00,
  "notes": "Classic design, very popular"
}
```

**Time Prediction Learning:**
- `estimated_hours`: Initial estimate for this style
- `avg_hours_actual`: Auto-calculated average from completed pieces
- `pieces_completed`: Count of finished pieces (for averaging)
- Formula: `avg_hours_actual = sum(piece.work_hours_actual) / pieces_completed`
- Over time, use `avg_hours_actual` instead of `estimated_hours` for predictions

### Update: piece.schema.json
Add fields:
```json
"style_id": {
  "type": "string",
  "pattern": "^STYLE-[0-9]{3}$",
  "description": "Reference to parent style"
},
"color": {
  "type": "string",
  "description": "Primary color of the piece"
},
"work_hours_estimated": {
  "type": "number",
  "description": "Initial estimate before starting (for prediction learning)"
},
"work_sessions": {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "date": { "type": "string", "format": "date" },
      "hours": { "type": "number" }
    }
  },
  "description": "Individual work sessions"
},
"work_hours_actual": {
  "type": "number",
  "description": "Actual total (sum of sessions)"
},
"yarns_used": {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "yarn_id": { "type": "string", "pattern": "^YARN-[0-9]{3}$" },
      "balls_used": { "type": "number" }
    }
  },
  "description": "Yarns with quantity (for cost calculation)"
},
"material_cost": {
  "type": "number",
  "description": "Calculated cost of materials (EUR)"
},
"suggested_price": {
  "type": "number",
  "description": "Auto-calculated suggested price"
},
"price": {
  "type": "number",
  "description": "Actual selling price set by user"
}
```

---

**End of Plan**
