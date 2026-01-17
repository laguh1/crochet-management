# Crochet Project Manager

A personal project management system for tracking handcrafted crochet work including shawls, scarves, bed throws, and similar pieces.

## Project Overview

This system tracks three main entities:
1. **Crochet Pieces** - Finished handcrafted pieces
2. **Yarns** - Materials used in projects
3. **Stitches** - Techniques/patterns used

## Project Structure

```
crochet/
├── CLAUDE.md              # This file - project documentation
├── data/
│   ├── pieces.json         # Crochet pieces database
│   ├── yarns.json         # Yarn inventory database
│   ├── stitches.json      # Stitch library database
│   └── schemas/
│       ├── piece.schema.json
│       ├── yarn.schema.json
│       └── stitch.schema.json
├── images/
│   ├── pieces/             # Photos of finished pieces
│   │   └── {PIECE-001}/    # Subfolder per piece (multiple photos)
│   ├── yarns/             # Photos of yarn balls/skeins
│   │   └── {YARN-001}/    # Subfolder per yarn (multiple photos)
│   ├── stitches/          # Photos/diagrams of stitches
│   │   └── {STITCH-001}/  # Subfolder per stitch (multiple photos)
│   └── marketing/         # Marketing materials
│       ├── logos/         # Brand logos
│       ├── banners/       # Sale banners, headers
│       └── text/          # Sale descriptions, templates
├── docs/
│   └── care-instructions/ # Care instruction templates
└── scripts/
    └── manager.py         # Optional: Python management script
```

---

## Data Models

### 1. Crochet Piece

Represents a finished handcrafted piece.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., "PIECE-001") |
| `name` | string | Yes | Item name (e.g., "Ocean Wave Shawl") |
| `type` | enum | Yes | Type: shawl, scarf, bed_throw, blanket, other |
| `dimensions` | object | Yes | Width, length, (optional) depth in cm |
| `date_started` | date | Yes | When work began (YYYY-MM-DD) |
| `date_finished` | date | No | When completed (YYYY-MM-DD) |
| `work_hours` | number | No | Approximate total hours worked |
| `photos` | array | No | List of photo filenames |
| `price` | number | No | Price to sell (in EUR) |
| `work_status` | enum | Yes | in_progress, finished, ready |
| `destination` | enum | Yes | for_sale, sold, for_gift, gifted, for_self, in_use |
| `gift_recipient` | string | No | If gifted, to whom |
| `sale_platform` | string | No | Where listed for sale |
| `sale_link` | string | No | URL if listed online |
| `sold_date` | date | No | When sold (if applicable) |
| `sold_price` | number | No | Actual sale price |
| `yarns_used` | array | Yes | List of yarn IDs used |
| `stitches_used` | array | Yes | List of stitch IDs used |
| `notes` | string | No | Additional notes |
| `archived` | boolean | No | True if record is archived (default: false) |
| `archived_date` | date | No | When archived (YYYY-MM-DD) |
| `archived_reason` | string | No | Why archived (e.g., "sold", "gifted", "damaged") |
| `created_at` | datetime | Auto | Record creation timestamp |
| `updated_at` | datetime | Auto | Last update timestamp |

**Example:**
```json
{
  "id": "PIECE-001",
  "name": "Ocean Wave Shawl",
  "type": "shawl",
  "dimensions": {
    "width_cm": 180,
    "length_cm": 60
  },
  "date_started": "2026-01-10",
  "date_finished": "2026-01-15",
  "work_hours": 25,
  "photos": ["front.jpg", "detail.jpg", "folded.jpg"],
  "price": 45.00,
  "status": "available",
  "sale_platform": "Etsy",
  "sale_link": "https://etsy.com/listing/...",
  "yarns_used": ["YARN-001", "YARN-003"],
  "stitches_used": ["STITCH-001", "STITCH-005"],
  "notes": "First attempt at wave pattern, very happy with result"
}
```

---

### 2. Yarn

Represents yarn material in inventory.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., "YARN-001") |
| `name` | string | Yes | Yarn name (e.g., "Natura Just Cotton") |
| `brand` | string | No | Brand name (e.g., "DMC") |
| `color` | string | Yes | Color name or code |
| `color_code` | string | No | Manufacturer color code |
| `material` | enum | Yes | Primary fiber: cotton, wool, acrylic, silk, blend, other |
| `material_composition` | string | No | Detailed composition (e.g., "100% Cotton") |
| `material_specs` | string | No | Quality/characteristics description |
| `weight_category` | enum | No | lace, fingering, sport, dk, worsted, aran, bulky, super_bulky |
| `ball_weight_g` | number | No | Weight per ball in grams |
| `ball_length_m` | number | No | Length per ball in meters |
| `price_paid` | number | No | Price paid per ball (EUR) |
| `purchase_location` | string | No | Store or website name |
| `purchase_link` | string | No | URL if bought online |
| `purchase_date` | date | No | When purchased |
| `quantity_owned` | number | No | Number of balls in inventory |
| `hook_size_mm` | number | No | Recommended crochet hook size (mm) |
| `needle_size_mm` | string | No | Recommended knitting needle size range |
| `gauge` | string | No | Tension/gauge information |
| `care_instructions` | object | No | Washing and maintenance info |
| `notes` | string | No | Additional notes |
| `archived` | boolean | No | True if record is archived (default: false) |
| `archived_date` | date | No | When archived (YYYY-MM-DD) |
| `archived_reason` | string | No | Why archived (e.g., "used up", "discontinued") |
| `created_at` | datetime | Auto | Record creation timestamp |
| `updated_at` | datetime | Auto | Last update timestamp |

**Care Instructions Object:**
```json
{
  "wash_temp": "30",
  "machine_washable": true,
  "tumble_dry": false,
  "iron_temp": "low",
  "bleach": false,
  "dry_clean": false,
  "special_notes": "Wash with similar colors"
}
```

**Example:**
```json
{
  "id": "YARN-001",
  "name": "Natura Just Cotton",
  "brand": "DMC",
  "color": "Light Blue",
  "color_code": "N56",
  "material": "cotton",
  "material_composition": "100% Cotton",
  "material_specs": "Matte finish, soft texture, suitable for baby pieces",
  "weight_category": "dk",
  "ball_weight_g": 50,
  "ball_length_m": 155,
  "price_paid": 3.50,
  "purchase_location": "Las Tijeras Magicas",
  "purchase_link": "https://www.lastijerasmagicas.com/en/yarns/natura-dmc-2231.html",
  "purchase_date": "2026-01-05",
  "quantity_owned": 5,
  "hook_size_mm": 3.0,
  "needle_size_mm": "2.5-3.5",
  "care_instructions": {
    "wash_temp": "30",
    "machine_washable": true,
    "tumble_dry": false,
    "iron_temp": "medium"
  },
  "notes": "Great for spring/summer projects"
}
```

---

### 3. Stitch

Represents a crochet stitch/technique.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., "STITCH-001") |
| `name` | string | Yes | Standardized name from Hookfully directory |
| `name_aliases` | array | No | Alternative names used by bloggers/tutorials |
| `abbreviation` | string | No | Common abbreviation (e.g., "sc") |
| `category` | enum | No | basic, textured, lace, colorwork, specialty |
| `difficulty` | enum | No | beginner, intermediate, advanced |
| `description` | string | Yes | Main characteristic/description |
| `hookfully_link` | string | No | URL to Hookfully's tutorial for this stitch |
| `instruction_link` | string | No | URL to tutorial user learned from |
| `video_link` | string | No | URL to video tutorial |
| `photos` | array | No | List of photo filenames (diagrams, samples) |
| `notes` | string | No | Personal notes about the stitch |
| `archived` | boolean | No | True if record is archived (default: false) |
| `archived_date` | date | No | When archived (YYYY-MM-DD) |
| `archived_reason` | string | No | Why archived (e.g., "duplicate", "merged") |
| `created_at` | datetime | Auto | Record creation timestamp |
| `updated_at` | datetime | Auto | Last update timestamp |

**Stitch Naming Source of Truth:**
```
https://hookfully.com/a-z-crochet-stitch-directory/
```
Always use Hookfully's standardized name. Store blogger/tutorial names in `name_aliases`.

**Example:**
```json
{
  "id": "STITCH-001",
  "name": "V-Stitch",
  "name_aliases": ["V Stitch", "Vee Stitch"],
  "abbreviation": "v-st",
  "category": "lace",
  "difficulty": "beginner",
  "description": "Creates an open, lacy fabric with V-shaped pattern. Work (dc, ch 1, dc) in same stitch.",
  "hookfully_link": "https://hookfully.com/v-stitch/",
  "instruction_link": "https://www.youtube.com/watch?v=example",
  "video_link": "https://www.youtube.com/watch?v=kFAw3hpTDkU",
  "photos": ["STITCH-001_tutorial.png", "STITCH-001_sample.jpg"],
  "notes": "Great for shawls and lightweight scarves"
}
```

---

## Relationships

```
┌─────────────────┐
│  Crochet Piece   │
│    (PIECE-001)   │
└────────┬────────┘
         │
         │ uses (many-to-many)
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐  ┌─────────┐
│ Yarn  │  │ Stitch  │
│(YARN-)│  │(STITCH-)│
└───────┘  └─────────┘
```

- **Piece → Yarns**: One piece can use multiple yarns; one yarn can be used in multiple pieces
- **Piece → Stitches**: One piece can use multiple stitches; one stitch can be used in multiple pieces

---

## Piece Types

| Type | Description |
|------|-------------|
| `shawl` | Triangular or rectangular wrap worn over shoulders |
| `scarf` | Long narrow piece worn around neck |
| `bed_throw` | Decorative blanket for beds |
| `blanket` | Full-size blanket or afghan |
| `cowl` | Tube-shaped neck warmer |
| `poncho` | Pullover cape-style garment |
| `cardigan` | Open-front sweater |
| `hat` | Head covering |
| `bag` | Tote, purse, or bag |
| `home_decor` | Pillows, coasters, wall hangings |
| `other` | Any other type |

---

## Yarn Weight Categories

| Category | Also Known As | Hook Size (mm) | Typical Uses |
|----------|---------------|----------------|--------------|
| `lace` | Thread, Cobweb | 1.5-2.25 | Doilies, fine shawls |
| `fingering` | Sock, Baby | 2.25-3.25 | Socks, baby pieces |
| `sport` | Baby | 3.25-3.75 | Light garments |
| `dk` | Light Worsted | 3.75-4.5 | Garments, accessories |
| `worsted` | Medium, Aran | 4.5-5.5 | Most projects |
| `aran` | Heavy Worsted | 5.5-6.5 | Sweaters, blankets |
| `bulky` | Chunky | 6.5-9 | Quick projects |
| `super_bulky` | Roving | 9+ | Very quick projects |

---

## Piece Status Flow

Items have two status dimensions: **work status** and **destination**.

### Work Status (progress)
```
[in_progress] ──finish──► [finished] ──prepare──► [ready]
```

| Status | Description |
|--------|-------------|
| `in_progress` | Currently being worked on |
| `finished` | Crocheting complete, but may need blocking, washing, or tagging |
| `ready` | Ready for use, sale, or gifting |

### Destination (intent/outcome)
```
[for_sale] ──sell──► [sold]
[for_gift] ──give──► [gifted]
[for_self] ──use───► [in_use]
```

| Status | Description |
|--------|-------------|
| `for_sale` | Intended to be sold |
| `sold` | Has been sold |
| `for_gift` | Intended as a gift for someone |
| `gifted` | Has been given as gift |
| `for_self` | For personal use |
| `in_use` | Currently being used by self |

### Combined Status Examples
| Work Status | Destination | Meaning |
|-------------|-------------|---------|
| `in_progress` | `for_sale` | Making it to sell |
| `finished` | `for_gift` | Done crocheting, preparing as gift |
| `ready` | `for_sale` | Listed and ready to ship |
| `ready` | `sold` | Sale completed |
| `ready` | `for_self` | Ready to use personally |
| `ready` | `in_use` | Currently using it |

---

## Sale Platforms

Common platforms for selling handmade crochet:
- **Etsy** - etsy.com
- **Wallapop** - wallapop.com (Spain)
- **Milanuncios** - milanuncios.com (Spain)
- **Amazon Handmade** - amazon.com/handmade
- **Local Markets** - "local"
- **Instagram** - instagram.com
- **Facebook Marketplace** - facebook.com/marketplace

---

## File Naming Conventions

### Piece Photos
```
images/pieces/{PIECE-ID}/{descriptor}.{ext}
```
Examples:
- `images/pieces/PIECE-001/front.jpg`
- `images/pieces/PIECE-001/detail-stitch.jpg`
- `images/pieces/PIECE-001/worn.jpg`
- `images/pieces/PIECE-001/packaging.jpg`

### Yarn Photos
```
images/yarns/{YARN-ID}/{descriptor}.{ext}
```
Examples:
- `images/yarns/YARN-001/ball.jpg`
- `images/yarns/YARN-001/label.jpg`
- `images/yarns/YARN-001/texture-closeup.jpg`
- `images/yarns/YARN-001/color-comparison.jpg`

### Stitch Photos
```
images/stitches/{STITCH-ID}/{descriptor}.{ext}
```
Examples:
- `images/stitches/STITCH-005/sample.jpg`
- `images/stitches/STITCH-005/diagram.png`
- `images/stitches/STITCH-005/step-by-step.jpg`

### Marketing Materials
```
images/marketing/{type}/{name}.{ext}
```
Examples:
- `images/marketing/logos/brand-logo.png`
- `images/marketing/logos/brand-logo-dark.png`
- `images/marketing/banners/etsy-shop-banner.jpg`
- `images/marketing/banners/instagram-highlight.png`
- `images/marketing/text/product-description-template.md`
- `images/marketing/text/care-card-template.md`

### Data Files
- Use lowercase with hyphens: `pieces.json`, `yarns.json`, `stitches.json`
- Backups: `pieces.backup.2026-01-16.json`

---

## ID Conventions

| Entity | Format | Example |
|--------|--------|---------|
| Piece | `PIECE-{NNN}` | PIECE-001, PIECE-042 |
| Yarn | `YARN-{NNN}` | YARN-001, YARN-015 |
| Stitch | `STITCH-{NNN}` | STITCH-001, STITCH-008 |
| Style | `STYLE-{NNN}` | STYLE-001, STYLE-008 |

**ID Rules:**
- **Padding:** 3 digits (001-999) - sufficient for personal inventory
- **Assignment:** Sequential by entry order (not chronological by date)
- **Gaps:** Never reuse IDs - leave gaps if pieces are archived
- **Starting point:** Begin at 001
- **Immutability:** IDs should never change once assigned (used in folders, filenames, cross-references)

**Why sequential, not date-based:**
- Use `date_started`, `purchase_date`, or `created_at` fields for chronological queries
- Keeps IDs short and clean for folder/file naming
- Avoids complexity in ID generation

---

## Archived Records

Instead of deleting records, mark them as `archived: true`. This preserves:
- Historical data and relationships
- Photo references (files remain in place)
- Sales/gift history

**Archived field** (applies to all entities):

```json
{
  "id": "YARN-005",
  "archived": true,
  "archived_date": "2026-01-17",
  "archived_reason": "Discontinued by manufacturer"
}
```

**Common archive reasons:**
- Items: "sold", "gifted", "damaged", "unraveled for yarn reuse"
- Yarns: "used up", "discontinued", "gave away"
- Stitches: "duplicate entry", "merged with STITCH-XXX"
- Styles: "discontinued", "merged with STYLE-XXX"

**Filtering archived records:**
- By default, queries/displays should filter out `archived: true`
- Include archived records only when explicitly requested

---

## Quick Reference: Common Stitches

| Abbreviation | Name | Spanish |
|--------------|------|---------|
| ch | Chain | Cadena |
| sl st | Slip Stitch | Punto deslizado |
| sc | Single Crochet | Punto bajo |
| hdc | Half Double Crochet | Media vareta |
| dc | Double Crochet | Vareta/Punto alto |
| tr | Treble Crochet | Punto alto doble |

---

## Session Log

### 2026-01-16: Project Created
- Initial project setup
- Created folder structure: data/, images/, docs/
- Defined data models for Item, Yarn, Stitch
- Created JSON schemas
- Added sample data files
- Documented relationships and conventions

### 2026-01-16: Image Recognition Testing
- Tested stitch pattern recognition with reference V-stitch image
- Successfully identified 5/10 pieces using V-stitch pattern
- Accuracy confirmed for distinguishing V-stitch, Puff, Shell, Granny patterns

### 2026-01-16: Photo Grouping & Planning
- Grouped 17 photos into 8 distinct pieces
- Identified need for Style → Item hierarchy
- Created `PLAN.md` with implementation roadmap
- Created `src/` folder for Python automation scripts
- Created `images/pieces/inbox/` for unsorted photos

**Items identified from photos:**
| ID | Style | Color | Photos |
|----|-------|-------|--------|
| PIECE-001 | V-Stitch Cowl | Yellow | 2 |
| PIECE-002 | V-Stitch Scarf w/Fringe | Beige | 4 |
| PIECE-003 | Puff Stitch Scarf | White | 4 |
| PIECE-004 | V-Stitch Scarf | Green | 2 |
| PIECE-005 | Triangle Shawl | Orange | 2 |
| PIECE-006 | Granny Squares | Peach | 1 |
| PIECE-007 | Chunky Puff Scarf | Grey | 1 |
| PIECE-008 | Shell Stitch Scarf | Red | 1 |

**Next session:** Implement Phase 1 (stitches → styles → pieces → photo rename)

---

## Inbox Processing Instructions

When images are present in any inbox folder, they need to be processed to extract metadata, create/update database entries, and organize files.

### Photo Matching (Same Entity Detection)

Multiple photos may belong to the same entity (yarn, stitch, or piece). Before creating new entries, detect if photos should be grouped together.

**Matching signals by entity type:**

| Entity | Signal | How to Detect |
|--------|--------|---------------|
| **Yarn** | Same product | Brand name, color code, product name match |
| | Shop + Physical | Same color, same label visible, same brand |
| | Color match | RGB/visual color similarity |
| | Texture pattern | Similar fiber texture in closeups |
| **Stitch** | Same pattern | Visual pattern structure matches |
| | Same name | Tutorial title mentions same stitch name |
| | Same source | Same URL/website visible |
| **Piece** | Same work | Same stitch pattern, same color, same shape |
| | Multiple angles | Same dimensions, edges, fringe visible |
| | WIP + Finished | Same stitch, same yarn color, progressive stages |

**Grouping workflow:**
```
1. READ all images in inbox
2. ANALYZE each image for identifying features:
   - Colors (dominant RGB values)
   - Text visible (brand, labels, URLs)
   - Pattern structure (for stitches/pieces)
   - Shape/dimensions (for pieces)
3. GROUP images that share identifying features
4. CONFIRM groupings with user before processing
5. PROCESS each group as a single entity
```

**Example: Yarn matching**
```
Inbox contains:
  - screenshot_tienda.png (shop page showing "DMC Natura N56 Azul")
  - IMG_20260117.jpg (physical yarn ball, blue color, DMC label visible)

Detection:
  - Both show "DMC" brand
  - Both show blue color
  - Screenshot shows "N56", label in photo shows "N56"
  → GROUP as same yarn → Create single YARN-XXX entry
```

**Example: Piece matching**
```
Inbox contains:
  - 20251213_photo1.jpg (beige scarf, V-stitch pattern, partial view)
  - 20251213_photo2.jpg (beige scarf, V-stitch pattern, full view)
  - 20251215_photo3.jpg (beige scarf with fringe, worn on mannequin)

Detection:
  - All show same beige color
  - All show V-stitch pattern
  - Same fringe style visible
  → GROUP as same piece → Create single PIECE-XXX entry with 3 photos
```

---

### Yarns Inbox Processing

**Location:** `images/yarns/inbox/`

**Two purchase scenarios:**

#### Scenario A: Online Purchase
**Input files:**
1. **Shop screenshot** - Screengrab of online product page (usually in Spanish → translate to English)
2. **Physical photo** - User's photo of yarn at home (ball, label, texture)

**Metadata extraction:** Most fields can be extracted from shop screenshot.

#### Scenario B: Physical Shop Purchase
**Input files:**
1. **Physical photo only** - User's photo of yarn (ball, label)
2. No shop screenshot available

**Metadata extraction:** Limited to what's visible on label. **Must prompt user for:**
- `price_paid` - "How much did you pay for this yarn?"
- `purchase_location` - "Which shop did you buy this from?"
- `purchase_date` - "When did you purchase this?"
- `quantity_owned` - "How many balls did you buy?"
- Any fields not visible on label

**How to detect scenario:**
- If inbox contains screenshot with web browser UI → Online purchase
- If inbox contains only photos of physical yarn → Physical shop purchase

---

**Metadata to extract:**

| Field | Online Source | Physical Shop Source | Ask User If Missing |
|-------|---------------|---------------------|---------------------|
| `name` | Shop screenshot | Label | Yes |
| `brand` | Shop screenshot | Label | Yes |
| `color` | Both images | Photo / label | Yes |
| `color_code` | Shop / label | Label | No (optional) |
| `material` | Shop screenshot | Label | Yes |
| `material_composition` | Shop / label | Label | No (optional) |
| `material_specs` | Shop screenshot | - | No (optional) |
| `weight_category` | Shop screenshot | Label / infer | Yes if unclear |
| `ball_weight_g` | Shop / label | Label | Yes |
| `ball_length_m` | Shop / label | Label | Yes |
| `price_paid` | Shop screenshot | **ASK USER** | **Required** |
| `purchase_location` | Shop screenshot | **ASK USER** | **Required** |
| `purchase_link` | Shop URL | N/A | No |
| `purchase_date` | Filename / ask | **ASK USER** | **Required** |
| `quantity_owned` | Ask user | **ASK USER** | Yes |
| `hook_size_mm` | Shop / label | Label | No (optional) |
| `needle_size_mm` | Shop / label | Label | No (optional) |
| `gauge` | Shop / label | Label | No (optional) |
| `care_instructions` | Shop / label | Label (symbols) | No (optional) |

**Processing workflow:**
```
1. READ images in images/yarns/inbox/
2. DETECT purchase scenario:
   - Screenshot with browser UI present → Online purchase (Scenario A)
   - Only physical yarn photos → Physical shop purchase (Scenario B)
3. EXTRACT metadata:
   - Scenario A: Extract from shop screenshot (translate Spanish → English)
   - Scenario B: Extract from label only
4. PROMPT USER for missing required fields (especially for Scenario B):
   - price_paid, purchase_location, purchase_date, quantity_owned
5. DETERMINE next YARN-ID (check yarns.json for max ID)
6. CREATE yarn entry in yarns.json
7. CREATE folder: images/yarns/YARN-XXX/
8. RENAME & MOVE images:
   - Shop screenshot → YARN-XXX_shop.png (if exists)
   - Physical photo → YARN-XXX_ball.jpg (or _label.jpg, _texture.jpg)
9. UPDATE yarn entry with photo references
10. CONFIRM with user before saving
```

**Spanish → English common translations:**
- Algodón = Cotton
- Lana = Wool
- Acrílico = Acrylic
- Mezcla = Blend
- Ovillo = Ball
- Agujas = Needles
- Ganchillo = Crochet hook
- Lavado = Washing
- Planchar = Iron
- No usar secadora = Do not tumble dry
- Lavar a mano = Hand wash
- Lavar a máquina = Machine wash

---

### Stitches Inbox Processing

**Location:** `images/stitches/inbox/`

**Source of Truth for Stitch Names:**
```
https://hookfully.com/a-z-crochet-stitch-directory/
```
This directory contains 200+ standardized crochet stitch names (A-Z) in USA terminology.

**IMPORTANT:** Do NOT pre-populate all stitches from the directory. Only add stitches to `stitches.json` as they are actually used.

**Expected input files:**
- Tutorial screenshots (from YouTube, blogs, pattern sites)
- Stitch diagrams or charts
- Sample photos showing the stitch pattern

**Metadata to extract:**

| Field | Source | Notes |
|-------|--------|-------|
| `name` | **Hookfully directory** | Standardized name (NOT blogger's custom name) |
| `name_aliases` | Tutorial | Alternative names used by bloggers/tutorials |
| `abbreviation` | Hookfully / Tutorial | Common abbreviation (sc, dc, hdc, etc.) |
| `category` | Infer from pattern | basic, textured, lace, colorwork, specialty |
| `difficulty` | Infer / tutorial | beginner, intermediate, advanced |
| `description` | Tutorial | Brief description of the stitch technique |
| `hookfully_link` | Hookfully directory | Link to Hookfully's tutorial for this stitch |
| `instruction_link` | Screenshot URL | Link to the tutorial user learned from |
| `video_link` | Screenshot URL | Link to video tutorial (YouTube, etc.) |
| `notes` | User input | Personal notes about using this stitch |

**Processing workflow:**
```
1. READ images in images/stitches/inbox/
2. IDENTIFY the stitch from visual pattern or tutorial title
3. CROSS-REFERENCE with Hookfully directory:
   - Fetch https://hookfully.com/a-z-crochet-stitch-directory/
   - Find matching stitch by visual pattern or name similarity
   - Use Hookfully's standardized name (not blogger's name)
   - If blogger uses different name, store in name_aliases
4. EXTRACT source URL if visible in screenshot
5. CHECK if stitch already exists in stitches.json (by Hookfully name)
   - If exists: Update with new reference images/aliases
   - If new: Create new entry with standardized name
6. DETERMINE next STITCH-ID (if new)
7. CREATE/UPDATE stitch entry in stitches.json
8. CREATE folder: images/stitches/STITCH-XXX/
9. RENAME & MOVE images:
   - Tutorial screenshot → STITCH-XXX_tutorial.png
   - Diagram → STITCH-XXX_diagram.png
   - Sample photo → STITCH-XXX_sample.jpg
10. CONFIRM with user before saving
```

**Example: Name normalization**
```
Tutorial says: "Suzette Stitch" or "Lemon Peel Stitch"
Hookfully says: "Suzette Stitch"
→ Use: "Suzette Stitch"
→ Store alias: ["Lemon Peel Stitch"] if tutorial used different name
```

**If stitch not found in Hookfully:**
- Ask user to confirm the name
- Note in `notes` field: "Not in Hookfully directory"
- May be a variation or composite stitch

**Pattern identification use:**
- Stitch reference images can be compared against piece photos
- Helps identify which stitches were used in a finished piece
- Build visual library for future classification
- Standardized naming ensures consistency across pieces

---

### Pieces Inbox Processing

**Location:** `images/pieces/inbox/`

**Expected input files:**
- Work-in-progress photos
- Finished piece photos (multiple angles)
- Detail shots (stitch closeups, fringe, edges)

**Metadata to extract:**

| Field | Source | Notes |
|-------|--------|-------|
| `name` | User input / style | Item name with color |
| `type` | Visual identification | shawl, scarf, blanket, cowl, etc. |
| `style_id` | Match to existing style | Link to STYLE-XXX |
| `color` | Photo analysis | Primary color(s) |
| `dimensions` | User input | Width, length in cm |
| `date_started` | Filename date | Extract from photo filename |
| `stitches_used` | Visual comparison | Match against stitch library |
| `yarns_used` | User input / visual | Link to YARN-XXX entries |

**Processing workflow:**
```
1. READ images in images/pieces/inbox/
2. GROUP photos by piece (same piece, different angles)
3. IDENTIFY stitch pattern (compare to stitch library)
4. MATCH to existing style OR flag for new style creation
5. EXTRACT date from filename (YYYYMMDD pattern)
6. DETERMINE next PIECE-ID
7. CREATE piece entry in pieces.json
8. CREATE folder: images/pieces/PIECE-XXX/
9. RENAME & MOVE images:
   - PIECE-XXX_01_wip.jpg
   - PIECE-XXX_02_finished.jpg
   - PIECE-XXX_03_detail.jpg
10. UPDATE piece entry with photo references
11. CONFIRM with user before saving
```

---

### General Inbox Check Command

At the start of each session, check for pending inbox files:

```bash
# Check all inboxes for unprocessed files
ls -la images/pieces/inbox/
ls -la images/yarns/inbox/
ls -la images/stitches/inbox/
```

If files exist, prompt user: "I found X files in [inbox]. Would you like me to process them now?"

---

## Future Enhancements

- [ ] Web interface for browsing inventory
- [ ] Photo gallery generator
- [ ] Price calculator based on materials + time
- [ ] Pattern tracking (PDF storage)
- [ ] Customer/recipient database
- [ ] Sales analytics and reporting
- [ ] Yarn inventory alerts (low stock)
- [ ] Project cost tracking
