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
| `status` | enum | Yes | available, sold, gifted, keeping |
| `gift_recipient` | string | No | If gifted, to whom |
| `sale_platform` | string | No | Where listed for sale |
| `sale_link` | string | No | URL if listed online |
| `sold_date` | date | No | When sold (if applicable) |
| `sold_price` | number | No | Actual sale price |
| `yarns_used` | array | Yes | List of yarn IDs used |
| `stitches_used` | array | Yes | List of stitch IDs used |
| `notes` | string | No | Additional notes |
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
| `notes` | string | No | Personal notes about the stitch |
| `created_at` | datetime | Auto | Record creation timestamp |

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

```
[available] ──sell──► [sold]
     │
     └──gift──► [gifted]
     │
     └──keep──► [keeping]
```

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

## Future Enhancements

- [ ] Web interface for browsing inventory
- [ ] Photo gallery generator
- [ ] Price calculator based on materials + time
- [ ] Pattern tracking (PDF storage)
- [ ] Customer/recipient database
- [ ] Sales analytics and reporting
- [ ] Yarn inventory alerts (low stock)
- [ ] Project cost tracking
