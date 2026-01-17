# Crochet Project Manager - Development Plan

**Created:** January 16, 2026
**Last Updated:** January 17, 2026
**Version:** 2.0

---

## Table of Contents

1. [Current Implementation Status](#current-implementation-status)
2. [Data Model](#data-model)
3. [Phase 1: Data Foundation](#phase-1-data-foundation) ✅ COMPLETE
4. [Phase 2: Python Backend Core](#phase-2-python-backend-core) ✅ COMPLETE
5. [Phase 3: Pricing Algorithm](#phase-3-pricing-algorithm) ✅ COMPLETE
6. [Phase 4: File Management Automation](#phase-4-file-management-automation) ✅ COMPLETE
7. [Phase 5: Standalone Desktop Application](#phase-5-standalone-desktop-application)
8. [Phase 6: Online Deployment (Optional)](#phase-6-online-deployment-optional)
9. [Technical Architecture](#technical-architecture)
10. [File Structure](#file-structure)

---

## Current Implementation Status

### ✅ Completed

| Feature | Status | Date | Notes |
|---------|--------|------|-------|
| Project structure | ✅ Done | Jan 16 | Folders, schemas, CLAUDE.md |
| Data models defined | ✅ Done | Jan 16 | Pieces, Yarns, Stitches |
| ID conventions | ✅ Done | Jan 16 | PIECE-XXX, YARN-XXX, STITCH-XXX |
| Photo naming convention | ✅ Done | Jan 16 | {ID}_{seq}_{descriptor}.{ext} |
| Inbox processing workflow | ✅ Done | Jan 17 | Documented in CLAUDE.md |
| Stitches populated | ✅ Done | Jan 17 | 15 stitches with photos |
| Yarns populated | ✅ Done | Jan 17 | 14 yarns with metadata |
| Pieces populated | ✅ Done | Jan 17 | 13 pieces with photos |
| Photos organized | ✅ Done | Jan 17 | Moved to entity folders |
| Crochet hooks reference | ✅ Done | Jan 17 | 11 sizes documented |
| Python models | ✅ Done | Jan 17 | piece.py, yarn.py, stitch.py |
| Data service | ✅ Done | Jan 17 | CRUD for all entities |
| Price service | ✅ Done | Jan 17 | Full pricing algorithm |
| Time service | ✅ Done | Jan 17 | Session tracking, estimation |
| Utils module | ✅ Done | Jan 17 | ID gen, date, photo utils |
| CLI module | ✅ Done | Jan 17 | main, rename, data entry, inbox |

### 📋 Planned

| Feature | Priority | Phase |
|---------|----------|-------|
| React frontend | Medium | Phase 5 |
| Desktop app (Electron) | Medium | Phase 5 |
| Online deployment | Low | Phase 6 |

---

## Data Model

### Entity Relationships

```
┌─────────────┐
│   STYLE     │ ◄─── Design/pattern template (future)
│ (STYLE-001) │
└──────┬──────┘
       │ 1:many
       ▼
┌─────────────┐
│   PIECE     │ ◄─── Actual finished piece
│ (PIECE-001) │
└──────┬──────┘
       │ many:many
       ▼
┌─────────────┐      ┌─────────────┐
│    YARN     │      │   STITCH    │
│ (YARN-001)  │      │(STITCH-001) │
└─────────────┘      └─────────────┘
       │                    │
       └──────────┬─────────┘
                  ▼
            ┌──────────┐
            │  PHOTOS  │ ◄─── All entities have photos arrays
            └──────────┘
```

### Photos Field (All Entities)

Every entity (Piece, Yarn, Stitch) has a `photos` array field:

```json
{
  "photos": ["ENTITY-ID_01_descriptor.jpg", "ENTITY-ID_02_descriptor.jpg"]
}
```

This enables:
- Frontend image galleries
- Visual inventory browsing
- Photo-based search/filtering

---

## Phase 1: Data Foundation ✅ COMPLETE

### 1.1 Stitches Library ✅
- [x] Define stitch schema
- [x] Populate 15 stitches (basic + specialty)
- [x] Add tutorial screenshots as photos
- [x] Link to Hookfully reference

### 1.2 Yarns Inventory ✅
- [x] Define yarn schema
- [x] Populate 14 yarns with full metadata
- [x] Shop screenshots + physical photos
- [x] Price, weight, purchase info

### 1.3 Pieces Collection ✅
- [x] Define piece schema with work_status + destination
- [x] Populate 13 pieces
- [x] Organize photos into folders
- [x] Link yarns_used and stitches_used

### 1.4 Photo Organization ✅
- [x] Create inbox folders for each entity type
- [x] Define naming convention
- [x] Process all inbox files
- [x] Move to organized folders

---

## Phase 2: Python Backend Core ✅ COMPLETE

### 2.1 Project Structure

```
src/
├── __init__.py
├── config.py              # Configuration and constants
├── models/
│   ├── __init__.py
│   ├── piece.py           # Piece data class
│   ├── yarn.py            # Yarn data class
│   └── stitch.py          # Stitch data class
├── services/
│   ├── __init__.py
│   ├── data_service.py    # JSON CRUD operations
│   ├── file_service.py    # File management
│   ├── price_service.py   # Pricing calculations
│   └── time_service.py    # Time calculations
├── utils/
│   ├── __init__.py
│   ├── id_generator.py    # ID generation utilities
│   ├── date_utils.py      # Date parsing/formatting
│   └── photo_utils.py     # Photo metadata extraction
└── cli/
    ├── __init__.py
    └── main.py            # Command-line interface
```

### 2.2 Core Modules

#### 2.2.1 Data Service (`services/data_service.py`)
```python
class DataService:
    """CRUD operations for JSON data files."""

    def load_pieces() -> List[Piece]
    def save_pieces(pieces: List[Piece])
    def get_piece_by_id(piece_id: str) -> Piece
    def create_piece(piece: Piece) -> str  # Returns new ID
    def update_piece(piece: Piece)
    def delete_piece(piece_id: str)  # Archives, doesn't delete

    # Same pattern for yarns and stitches
    def load_yarns() -> List[Yarn]
    def load_stitches() -> List[Stitch]
    # ... etc
```

#### 2.2.2 ID Generator (`utils/id_generator.py`)
```python
def get_next_id(entity_type: str) -> str:
    """
    Generate next sequential ID for entity type.

    Args:
        entity_type: 'PIECE', 'YARN', or 'STITCH'

    Returns:
        Next ID like 'PIECE-014', 'YARN-015', etc.
    """
```

#### 2.2.3 Photo Utilities (`utils/photo_utils.py`)
```python
def extract_date_from_filename(filename: str) -> Optional[date]:
    """Extract date from filename like '20251123_193645.jpg'"""

def extract_exif_date(filepath: str) -> Optional[datetime]:
    """Extract date from photo EXIF metadata"""

def generate_photo_name(entity_id: str, sequence: int, descriptor: str, ext: str) -> str:
    """Generate standardized photo filename"""
```

---

## Phase 3: Pricing Algorithm ✅ COMPLETE

**Implementation:** `src/services/price_service.py`

### 3.1 Price Calculation Formula

```
SUGGESTED_PRICE = (MATERIAL_COST + LABOR_COST) × (1 + PROFIT_MARGIN) + COMPLEXITY_ADJUSTMENT

Where:
├── MATERIAL_COST = Σ (yarn.price_paid × balls_used)
├── LABOR_COST = work_hours_actual × hourly_rate
├── PROFIT_MARGIN = configurable (default 20%)
└── COMPLEXITY_ADJUSTMENT = stitch_complexity_factor × size_factor
```

### 3.2 Complexity Factors

| Stitch Category | Complexity Factor |
|-----------------|-------------------|
| basic | 1.0 |
| textured | 1.15 |
| lace | 1.25 |
| colorwork | 1.30 |
| specialty | 1.40 |

| Piece Type | Size Factor |
|------------|-------------|
| hat | 0.8 |
| cowl | 0.9 |
| scarf | 1.0 |
| shawl | 1.2 |
| blanket | 1.5 |

### 3.3 Price Service Implementation

**File:** `src/services/price_service.py`

```python
from dataclasses import dataclass
from typing import List, Optional
from decimal import Decimal

@dataclass
class PriceConfig:
    hourly_rate: Decimal = Decimal("8.00")
    profit_margin: Decimal = Decimal("0.20")
    min_margin: Decimal = Decimal("0.10")
    round_to: int = 5  # Round to nearest 5€

@dataclass
class PriceBreakdown:
    material_cost: Decimal
    labor_cost: Decimal
    subtotal: Decimal
    complexity_adjustment: Decimal
    profit_margin: Decimal
    suggested_price: Decimal
    rounded_price: Decimal

class PriceService:
    """Calculate suggested prices for pieces."""

    def __init__(self, config: PriceConfig = None):
        self.config = config or PriceConfig()

    def calculate_material_cost(self, piece_id: str) -> Decimal:
        """
        Calculate total material cost from yarns_used.

        Returns: Sum of (yarn.price_paid * balls_used) for each yarn
        """

    def calculate_labor_cost(self, piece_id: str) -> Decimal:
        """
        Calculate labor cost from work hours.

        Returns: work_hours_actual * hourly_rate
        """

    def get_complexity_factor(self, piece_id: str) -> Decimal:
        """
        Calculate complexity based on stitches used.

        Returns: Average complexity of all stitches used
        """

    def get_size_factor(self, piece_type: str) -> Decimal:
        """Get size adjustment factor for piece type."""

    def calculate_price(self, piece_id: str) -> PriceBreakdown:
        """
        Calculate full price breakdown for a piece.

        Returns: PriceBreakdown with all cost components
        """

    def suggest_price_range(self, piece_id: str) -> tuple[Decimal, Decimal]:
        """
        Suggest min/max price range based on similar pieces.

        Returns: (min_price, max_price) tuple
        """

    def compare_to_market(self, piece_id: str) -> dict:
        """
        Compare suggested price to similar sold pieces.

        Returns: Dict with avg_sold_price, price_difference, recommendation
        """
```

### 3.4 Example Price Calculation

```
Piece: PIECE-003 (V-Stitch Scarf with Fringe - Taupe)
├── Material Cost:
│   └── YARN-013: 1 ball × €5.00 = €5.00
├── Labor Cost:
│   └── 8 hours × €8.00 = €64.00
├── Subtotal: €69.00
├── Complexity:
│   └── V-Stitch (lace) = 1.25 factor
│   └── Scarf = 1.0 size factor
│   └── Adjustment: €69.00 × 0.25 = €17.25
├── Adjusted: €86.25
├── Profit (20%): €17.25
├── Total: €103.50
└── Suggested (rounded): €105.00
```

---

## Phase 4: File Management Automation ✅ COMPLETE

**Implementation:** `src/cli/` module with rename_files.py, data_entry.py, process_inbox.py

### 4.1 Purpose

Replace AI-dependent tasks with standalone Python scripts that can run without Claude API access.

### 4.2 Scripts to Implement

#### 4.2.1 File Renamer (`src/cli/rename_files.py`)

```python
"""
Rename files in inbox to standardized format.

Usage:
    python -m src.cli.rename_files --entity piece --id PIECE-014
    python -m src.cli.rename_files --entity yarn --id YARN-015 --files photo1.jpg photo2.jpg
"""

def rename_inbox_files(entity_type: str, entity_id: str, files: List[str] = None):
    """
    Rename files from inbox to entity folder with proper naming.

    1. Scan inbox folder for files (or use provided list)
    2. Generate new names: {ID}_{seq}_{descriptor}.{ext}
    3. Move to entity folder: images/{entity_type}/{entity_id}/
    4. Update JSON data with new photo references
    """
```

#### 4.2.2 Data Entry CLI (`src/cli/data_entry.py`)

```python
"""
Interactive CLI for creating/updating data entries.

Usage:
    python -m src.cli.data_entry create piece
    python -m src.cli.data_entry update yarn YARN-012
    python -m src.cli.data_entry list pieces --status for_sale
"""

def create_piece_interactive():
    """
    Interactive prompts to create a new piece entry.

    Prompts for:
    - Name, type, color
    - Yarns used (select from existing)
    - Stitches used (select from existing)
    - Work status, destination
    - Dimensions, hook size
    """

def create_yarn_interactive():
    """Interactive prompts for new yarn entry."""

def create_stitch_interactive():
    """Interactive prompts for new stitch entry."""
```

#### 4.2.3 Inbox Processor (`src/cli/process_inbox.py`)

```python
"""
Process all inbox folders and organize files.

Usage:
    python -m src.cli.process_inbox --all
    python -m src.cli.process_inbox --entity pieces
"""

def process_inbox(entity_type: str = None):
    """
    Scan inbox folders and process new files.

    1. List files in inbox
    2. Extract metadata (date from filename, EXIF)
    3. Prompt user for entity assignment
    4. Generate ID if new entity
    5. Rename and move files
    6. Update JSON data
    """
```

#### 4.2.4 Time Calculator (`src/services/time_service.py`)

```python
"""
Calculate work time from sessions and estimate total time.
"""

@dataclass
class WorkSession:
    date: date
    hours: float
    notes: Optional[str] = None

class TimeService:
    """Calculate and estimate work times."""

    def calculate_total_hours(self, sessions: List[WorkSession]) -> float:
        """Sum all session hours."""

    def estimate_remaining_hours(self, piece_id: str) -> float:
        """
        Estimate remaining hours based on:
        - Similar completed pieces
        - Current progress percentage
        - Style average hours
        """

    def get_style_average_hours(self, style_id: str) -> float:
        """Calculate average hours for all pieces of a style."""

    def predict_completion_date(self, piece_id: str, hours_per_week: float) -> date:
        """Predict when piece will be finished."""
```

### 4.3 Automation Summary

| Current (AI-Assisted) | Automated Script | Functionality |
|----------------------|------------------|---------------|
| Photo analysis | `process_inbox.py` | File metadata extraction |
| File renaming | `rename_files.py` | Standardized naming |
| Data creation | `data_entry.py` | Interactive CLI prompts |
| Price calculation | `price_service.py` | Algorithm-based pricing |
| Time estimation | `time_service.py` | Session-based calculation |

---

## Phase 5: Standalone Desktop Application

### 5.1 Technology Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| Frontend | React + TypeScript | Modern, component-based UI |
| Desktop Wrapper | Electron | Cross-platform desktop app |
| Backend | Python (embedded) | Existing logic reuse |
| Database | JSON files (local) | Simple, portable, no server |
| IPC | Electron IPC | Frontend ↔ Python communication |

### 5.2 Application Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Electron App                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │              React Frontend                       │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │   │
│  │  │ Pieces  │ │  Yarns  │ │Stitches │           │   │
│  │  │  View   │ │  View   │ │  View   │           │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘           │   │
│  │       └───────────┼───────────┘                 │   │
│  │                   ▼                             │   │
│  │           ┌─────────────┐                       │   │
│  │           │  API Layer  │ (Electron IPC)        │   │
│  │           └──────┬──────┘                       │   │
│  └──────────────────┼──────────────────────────────┘   │
│                     ▼                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Python Backend (Embedded)              │   │
│  │  ┌──────────────┐  ┌──────────────┐            │   │
│  │  │ Data Service │  │Price Service │            │   │
│  │  └──────────────┘  └──────────────┘            │   │
│  │  ┌──────────────┐  ┌──────────────┐            │   │
│  │  │ File Service │  │ Time Service │            │   │
│  │  └──────────────┘  └──────────────┘            │   │
│  └─────────────────────────────────────────────────┘   │
│                     ▼                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Local File System                   │   │
│  │  data/*.json          images/*/*                │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 5.3 Frontend Components

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── PhotoGallery.tsx
│   │   │   ├── EntityCard.tsx
│   │   │   ├── FilterBar.tsx
│   │   │   └── SearchInput.tsx
│   │   ├── pieces/
│   │   │   ├── PieceList.tsx
│   │   │   ├── PieceDetail.tsx
│   │   │   ├── PieceForm.tsx
│   │   │   └── PriceCalculator.tsx
│   │   ├── yarns/
│   │   │   ├── YarnList.tsx
│   │   │   ├── YarnDetail.tsx
│   │   │   └── YarnForm.tsx
│   │   └── stitches/
│   │       ├── StitchList.tsx
│   │       ├── StitchDetail.tsx
│   │       └── StitchForm.tsx
│   ├── hooks/
│   │   ├── useData.ts
│   │   ├── usePhotos.ts
│   │   └── usePricing.ts
│   ├── services/
│   │   └── ipcService.ts      # Electron IPC calls
│   ├── types/
│   │   ├── piece.ts
│   │   ├── yarn.ts
│   │   └── stitch.ts
│   └── App.tsx
```

### 5.4 Key Features

1. **Dashboard**
   - Overview of inventory counts
   - Recent pieces
   - Pieces by status (for_sale, in_progress)
   - Quick stats (total value, avg price)

2. **Pieces View**
   - Grid/list toggle with photo thumbnails
   - Filter by status, type, stitch, yarn
   - Sort by date, price, name
   - Detail view with full photo gallery
   - Inline price calculator

3. **Yarns View**
   - Inventory grid with color swatches
   - Stock levels (quantity_owned)
   - Filter by material, weight, color
   - "Used in" pieces linking

4. **Stitches View**
   - Tutorial reference gallery
   - Difficulty filtering
   - "Used in" pieces linking
   - Link to external tutorials

5. **Data Entry Forms**
   - Create/edit all entity types
   - Photo upload with drag-drop
   - Auto-rename on upload
   - Validation feedback

6. **Price Calculator**
   - Interactive price estimation
   - Breakdown visualization
   - Comparison to similar pieces
   - "What-if" scenarios

---

## Phase 6: Online Deployment (Optional)

### 6.1 Architecture Changes for Online

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │         React Frontend (Browser)                 │   │
│  │              ↓ HTTP/REST                         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     SERVER                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │         FastAPI Backend (Python)                 │   │
│  │  ┌──────────────────────────────────────────┐   │   │
│  │  │            REST API Endpoints             │   │   │
│  │  │  GET  /api/pieces                         │   │   │
│  │  │  POST /api/pieces                         │   │   │
│  │  │  GET  /api/pieces/{id}                    │   │   │
│  │  │  PUT  /api/pieces/{id}                    │   │   │
│  │  │  DELETE /api/pieces/{id}                  │   │   │
│  │  │  POST /api/pieces/{id}/calculate-price    │   │   │
│  │  │  ... same for yarns, stitches             │   │   │
│  │  └──────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Database (PostgreSQL)               │   │
│  │         or JSON files with file locking          │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           File Storage (S3 or local)             │   │
│  │                  images/*/*                      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 6.2 API Endpoints

```
# Pieces
GET    /api/pieces                    # List all pieces
GET    /api/pieces?status=for_sale    # Filter by status
GET    /api/pieces/{id}               # Get single piece
POST   /api/pieces                    # Create piece
PUT    /api/pieces/{id}               # Update piece
DELETE /api/pieces/{id}               # Archive piece
GET    /api/pieces/{id}/photos        # Get piece photos
POST   /api/pieces/{id}/photos        # Upload photo
POST   /api/pieces/{id}/calculate     # Calculate price

# Yarns
GET    /api/yarns
GET    /api/yarns/{id}
POST   /api/yarns
PUT    /api/yarns/{id}
DELETE /api/yarns/{id}

# Stitches
GET    /api/stitches
GET    /api/stitches/{id}
POST   /api/stitches
PUT    /api/stitches/{id}

# Utilities
POST   /api/inbox/process             # Process inbox files
GET    /api/stats                     # Get statistics
POST   /api/price/calculate           # Calculate price for params
```

### 6.3 Deployment Options

| Option | Pros | Cons |
|--------|------|------|
| **Vercel + Railway** | Easy deploy, free tier | Limited storage |
| **DigitalOcean** | Full control, affordable | More setup |
| **Self-hosted (Raspberry Pi)** | Free, local | Maintenance |
| **Heroku** | Easy, familiar | Cost for dynos |

### 6.4 Security Considerations

- Authentication (if multi-user)
- CORS configuration
- File upload validation
- Rate limiting
- HTTPS required

---

## Technical Architecture

### Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   INBOX     │────▶│  PROCESSOR  │────▶│    DATA     │
│  (photos)   │     │  (Python)   │     │   (JSON)    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   IMAGES    │
                    │ (organized) │
                    └─────────────┘
```

### Configuration File

**File:** `src/config.py`

```python
from pathlib import Path
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Config:
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    IMAGES_DIR: Path = BASE_DIR / "images"

    # Data files
    PIECES_FILE: Path = DATA_DIR / "pieces.json"
    YARNS_FILE: Path = DATA_DIR / "yarns.json"
    STITCHES_FILE: Path = DATA_DIR / "stitches.json"

    # Pricing defaults
    HOURLY_RATE: Decimal = Decimal("8.00")
    PROFIT_MARGIN: Decimal = Decimal("0.20")
    MIN_MARGIN: Decimal = Decimal("0.10")
    PRICE_ROUND_TO: int = 5

    # Complexity factors
    STITCH_COMPLEXITY = {
        "basic": Decimal("1.0"),
        "textured": Decimal("1.15"),
        "lace": Decimal("1.25"),
        "colorwork": Decimal("1.30"),
        "specialty": Decimal("1.40"),
    }

    SIZE_FACTORS = {
        "hat": Decimal("0.8"),
        "cowl": Decimal("0.9"),
        "scarf": Decimal("1.0"),
        "shawl": Decimal("1.2"),
        "blanket": Decimal("1.5"),
        "other": Decimal("1.0"),
    }
```

---

## File Structure

```
crochet/
├── CLAUDE.md                    # ✅ AI assistant documentation
├── PLAN.md                      # ✅ This file
├── README.md                    # Project overview
├── requirements.txt             # ✅ Python dependencies
│
├── data/
│   ├── pieces.json              # ✅ 13 pieces
│   ├── yarns.json               # ✅ 14 yarns
│   ├── stitches.json            # ✅ 15 stitches
│   ├── styles.json              # 📋 Planned
│   └── schemas/
│       ├── piece.schema.json
│       ├── yarn.schema.json
│       └── stitch.schema.json
│
├── images/
│   ├── pieces/
│   │   ├── inbox/               # ✅ For new photos
│   │   ├── PIECE-001/           # ✅ Organized
│   │   └── ...
│   ├── yarns/
│   │   ├── inbox/               # ✅ For new photos
│   │   ├── YARN-001/            # ✅ Organized
│   │   └── ...
│   ├── stitches/
│   │   ├── inbox/               # ✅ For new photos
│   │   ├── STITCH-001/          # ✅ Organized
│   │   └── ...
│   ├── reference/
│   │   └── tools/               # ✅ Crochet hooks
│   └── marketing/               # 📋 For sale images
│
├── src/                         # ✅ Python backend
│   ├── __init__.py              # ✅
│   ├── config.py                # ✅
│   ├── models/
│   │   ├── __init__.py          # ✅
│   │   ├── piece.py             # ✅
│   │   ├── yarn.py              # ✅
│   │   └── stitch.py            # ✅
│   ├── services/
│   │   ├── __init__.py          # ✅
│   │   ├── data_service.py      # ✅
│   │   ├── price_service.py     # ✅
│   │   └── time_service.py      # ✅
│   ├── utils/
│   │   ├── __init__.py          # ✅
│   │   ├── id_generator.py      # ✅
│   │   ├── date_utils.py        # ✅
│   │   └── photo_utils.py       # ✅
│   └── cli/
│       ├── __init__.py          # ✅
│       ├── main.py              # ✅
│       ├── rename_files.py      # ✅
│       ├── data_entry.py        # ✅
│       └── process_inbox.py     # ✅
│
├── frontend/                    # 📋 React app (Phase 5)
│   ├── package.json
│   ├── src/
│   └── public/
│
└── docs/
    └── care-instructions/
```

---

## Development Priority Order

1. ~~**Phase 2.2** - Core Python modules (data_service, models)~~ ✅ DONE
2. ~~**Phase 3** - Pricing algorithm implementation~~ ✅ DONE
3. ~~**Phase 4** - File automation scripts~~ ✅ DONE
4. ~~**Phase 2 complete** - Time service, all utilities~~ ✅ DONE
5. **Phase 5** - React frontend + Electron wrapper (NEXT)
6. **Phase 6** - Online deployment (optional)

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Jan 16 | Use JSON for data storage | Simple, portable, no DB setup |
| Jan 16 | Sequential IDs (001-999) | Clean, sufficient for personal use |
| Jan 16 | Photos in entity folders | Easy browsing, backup |
| Jan 17 | Rename Item → Piece | Clearer terminology |
| Jan 17 | Two-status system | work_status + destination |
| Jan 17 | Hookfully for stitch names | Standardized reference |
| Jan 17 | Archive instead of delete | Preserve history |
| Jan 17 | Python for backend | Existing skills, good for algorithms |
| Jan 17 | React for frontend | Modern, good ecosystem |
| Jan 17 | Electron for desktop | Cross-platform, web tech reuse |

---

**End of Plan**
