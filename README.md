# Crochet Management

A personal project management system for tracking handcrafted crochet work.

## Overview

This system helps manage a crochet hobby business by tracking three core entities:

- **Items** - Finished pieces (shawls, scarves, blankets, etc.) with dimensions, work hours, pricing, and sale status
- **Yarns** - Material inventory with specs, care instructions, and purchase info
- **Stitches** - Technique library with descriptions and tutorial links

## Structure

```
crochet/
├── data/           # JSON databases and schemas
├── images/         # Photos organized by entity
│   ├── items/      # Finished item photos
│   ├── yarns/      # Yarn/material photos
│   ├── stitches/   # Stitch samples/diagrams
│   └── marketing/  # Logos, banners, sale materials
├── docs/           # Care instructions, templates
└── scripts/        # Management utilities
```

## Data Model

Items link to yarns used and stitches applied, enabling tracking of materials per project and technique usage across pieces.

```
Item (shawl, scarf...) ──uses──► Yarn (cotton, wool...)
                       ──uses──► Stitch (dc, shell...)
```

## Documentation

See [CLAUDE.md](CLAUDE.md) for complete field definitions, naming conventions, and usage examples.

## License

Personal project - All rights reserved.
