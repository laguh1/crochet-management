# Crochet Project Manager

A personal project management system for tracking handcrafted crochet work including shawls, scarves, bed throws, and similar items.

## Project Overview

This system tracks three main entities:
1. **Crochet Items** - Finished handcrafted pieces
2. **Yarns** - Materials used in projects
3. **Stitches** - Techniques/patterns used

## Project Structure

```
crochet/
├── CLAUDE.md              # This file - project documentation
├── data/
│   ├── items.json         # Crochet items database
│   ├── yarns.json         # Yarn inventory database
│   ├── stitches.json      # Stitch library database
│   └── schemas/
│       ├── item.schema.json
│       ├── yarn.schema.json
│       └── stitch.schema.json
├── images/
│   ├── items/             # Photos of finished items
│   │   └── {ITEM-001}/    # Subfolder per item (multiple photos)
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

### 1. Crochet Item

Represents a finished handcrafted piece.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., "ITEM-001") |
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
  "id": "ITEM-001",
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
  "material_specs": "Matte finish, soft texture, suitable for baby items",
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
| `name` | string | Yes | Stitch name (e.g., "Single Crochet") |
| `abbreviation` | string | No | Common abbreviation (e.g., "sc") |
| `category` | enum | No | basic, textured, lace, colorwork, specialty |
| `difficulty` | enum | No | beginner, intermediate, advanced |
| `description` | string | Yes | Main characteristic/description |
| `instruction_link` | string | No | URL to tutorial/instructions |
| `video_link` | string | No | URL to video tutorial |
| `photos` | array | No | List of photo filenames (diagrams, samples) |
| `notes` | string | No | Personal notes about the stitch |
| `archived` | boolean | No | True if record is archived (default: false) |
| `archived_date` | date | No | When archived (YYYY-MM-DD) |
| `archived_reason` | string | No | Why archived (e.g., "duplicate", "merged") |
| `created_at` | datetime | Auto | Record creation timestamp |
| `updated_at` | datetime | Auto | Last update timestamp |

**Example:**
```json
{
  "id": "STITCH-001",
  "name": "Single Crochet",
  "abbreviation": "sc",
  "category": "basic",
  "difficulty": "beginner",
  "description": "Basic stitch creating a tight, dense fabric. Insert hook, yarn over, pull through, yarn over, pull through both loops.",
  "instruction_link": "https://www.youtube.com/watch?v=example",
  "video_link": "https://www.youtube.com/watch?v=kFAw3hpTDkU",
  "notes": "Foundation for most projects"
}
```

---

## Relationships

```
┌─────────────────┐
│  Crochet Item   │
│    (ITEM-001)   │
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

- **Item → Yarns**: One item can use multiple yarns; one yarn can be used in multiple items
- **Item → Stitches**: One item can use multiple stitches; one stitch can be used in multiple items

---

## Item Types

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
| `fingering` | Sock, Baby | 2.25-3.25 | Socks, baby items |
| `sport` | Baby | 3.25-3.75 | Light garments |
| `dk` | Light Worsted | 3.75-4.5 | Garments, accessories |
| `worsted` | Medium, Aran | 4.5-5.5 | Most projects |
| `aran` | Heavy Worsted | 5.5-6.5 | Sweaters, blankets |
| `bulky` | Chunky | 6.5-9 | Quick projects |
| `super_bulky` | Roving | 9+ | Very quick projects |

---

## Item Status Flow

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

### Item Photos
```
images/items/{ITEM-ID}/{descriptor}.{ext}
```
Examples:
- `images/items/ITEM-001/front.jpg`
- `images/items/ITEM-001/detail-stitch.jpg`
- `images/items/ITEM-001/worn.jpg`
- `images/items/ITEM-001/packaging.jpg`

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
- Use lowercase with hyphens: `items.json`, `yarns.json`, `stitches.json`
- Backups: `items.backup.2026-01-16.json`

---

## ID Conventions

| Entity | Format | Example |
|--------|--------|---------|
| Item | `ITEM-{NNN}` | ITEM-001, ITEM-042 |
| Yarn | `YARN-{NNN}` | YARN-001, YARN-015 |
| Stitch | `STITCH-{NNN}` | STITCH-001, STITCH-008 |
| Style | `STYLE-{NNN}` | STYLE-001, STYLE-008 |

**ID Rules:**
- **Padding:** 3 digits (001-999) - sufficient for personal inventory
- **Assignment:** Sequential by entry order (not chronological by date)
- **Gaps:** Never reuse IDs - leave gaps if items are archived
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
- Successfully identified 5/10 items using V-stitch pattern
- Accuracy confirmed for distinguishing V-stitch, Puff, Shell, Granny patterns

### 2026-01-16: Photo Grouping & Planning
- Grouped 17 photos into 8 distinct items
- Identified need for Style → Item hierarchy
- Created `PLAN.md` with implementation roadmap
- Created `src/` folder for Python automation scripts
- Created `images/items/inbox/` for unsorted photos

**Items identified from photos:**
| ID | Style | Color | Photos |
|----|-------|-------|--------|
| ITEM-001 | V-Stitch Cowl | Yellow | 2 |
| ITEM-002 | V-Stitch Scarf w/Fringe | Beige | 4 |
| ITEM-003 | Puff Stitch Scarf | White | 4 |
| ITEM-004 | V-Stitch Scarf | Green | 2 |
| ITEM-005 | Triangle Shawl | Orange | 2 |
| ITEM-006 | Granny Squares | Peach | 1 |
| ITEM-007 | Chunky Puff Scarf | Grey | 1 |
| ITEM-008 | Shell Stitch Scarf | Red | 1 |

**Next session:** Implement Phase 1 (stitches → styles → items → photo rename)

---

## Inbox Processing Instructions

When images are present in any inbox folder, they need to be processed to extract metadata, create/update database entries, and organize files.

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

**Expected input files:**
- Tutorial screenshots (from YouTube, blogs, pattern sites)
- Stitch diagrams or charts
- Sample photos showing the stitch pattern

**Metadata to extract:**

| Field | Source | Notes |
|-------|--------|-------|
| `name` | Tutorial / diagram | Full stitch name in English |
| `abbreviation` | Tutorial | Common abbreviation (sc, dc, hdc, etc.) |
| `category` | Infer from pattern | basic, textured, lace, colorwork, specialty |
| `difficulty` | Infer / tutorial | beginner, intermediate, advanced |
| `description` | Tutorial | Brief description of the stitch technique |
| `instruction_link` | Screenshot URL | Link to written tutorial |
| `video_link` | Screenshot URL | Link to video tutorial (YouTube, etc.) |
| `notes` | User input | Personal notes about using this stitch |

**Processing workflow:**
```
1. READ images in images/stitches/inbox/
2. IDENTIFY the stitch from visual pattern or tutorial title
3. EXTRACT source URL if visible in screenshot
4. CHECK if stitch already exists in stitches.json
   - If exists: Update with new reference images
   - If new: Create new entry
5. DETERMINE next STITCH-ID (if new)
6. CREATE/UPDATE stitch entry in stitches.json
7. CREATE folder: images/stitches/STITCH-XXX/
8. RENAME & MOVE images:
   - Tutorial screenshot → STITCH-XXX_tutorial.png
   - Diagram → STITCH-XXX_diagram.png
   - Sample photo → STITCH-XXX_sample.jpg
9. CONFIRM with user before saving
```

**Pattern identification use:**
- Stitch reference images can be compared against item photos
- Helps identify which stitches were used in a finished item
- Build visual library for future classification

---

### Items Inbox Processing

**Location:** `images/items/inbox/`

**Expected input files:**
- Work-in-progress photos
- Finished item photos (multiple angles)
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
1. READ images in images/items/inbox/
2. GROUP photos by item (same piece, different angles)
3. IDENTIFY stitch pattern (compare to stitch library)
4. MATCH to existing style OR flag for new style creation
5. EXTRACT date from filename (YYYYMMDD pattern)
6. DETERMINE next ITEM-ID
7. CREATE item entry in items.json
8. CREATE folder: images/items/ITEM-XXX/
9. RENAME & MOVE images:
   - ITEM-XXX_01_wip.jpg
   - ITEM-XXX_02_finished.jpg
   - ITEM-XXX_03_detail.jpg
10. UPDATE item entry with photo references
11. CONFIRM with user before saving
```

---

### General Inbox Check Command

At the start of each session, check for pending inbox items:

```bash
# Check all inboxes for unprocessed files
ls -la images/items/inbox/
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
