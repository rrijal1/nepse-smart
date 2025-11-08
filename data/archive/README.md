# Data Archive - Backup Storage

## Purpose

This directory contains **archived JSON data files** that are kept as **backup only**. These files are **NOT** actively used by the application.

## Data Sources

### Primary: PostgreSQL Database

- All historical market data is stored in PostgreSQL Cloud SQL
- Backend queries the database for historical data
- Database contains complete trading history since 2024

### Secondary: Active JSON Files

- Last 7 business days of data in `../daily/` and `../lookup/`
- Used as fallback when database is unavailable
- Automatically archived here after 7 business days

### Backup: Archive (This Directory)

- Historical JSON files organized by year/month
- **Not queried by the application**
- Kept for disaster recovery and auditing purposes
- Can be used to repopulate PostgreSQL if needed

## Structure

```
archive/
├── 2024/
│   ├── 10/
│   ├── 11/
│   └── 12/
└── 2025/
    ├── 01/
    ├── 02/
    ├── ...
    └── 11/
```

## Automated Maintenance

- **Cleanup Script**: `data-scraper/cleanup_and_archive_old_data.py`
- **Schedule**: Runs daily via GitHub Actions after data collection
- **Retention**: Keeps last 7 business days active, archives older files
- **Git Exclusion**: Archive directory excluded via `.gitignore`

## File Formats

Both date formats are supported:

- `YYYY-MM-DD_<data_type>.json` (current format with hyphens)
- `YYYY_MM_DD_<data_type>.json` (legacy format with underscores)

## Recovery Process

If PostgreSQL data needs to be restored:

```bash
# Run the migration script
cd backend
python data_manager.py

# Or programmatically
from backend.data_manager import DataManager
manager = DataManager()
result = manager.migrate_json_to_postgres()
```

## Storage Size

- Archive not tracked in Git (reduces repo size)
- Current size: ~34 MB (250 files)
- Grows ~1-2 MB per trading day

## Notes

- ✅ Archive provides backup redundancy
- ✅ PostgreSQL is the source of truth
- ✅ Active JSON files provide immediate fallback
- ⚠️ Archive is NOT queried by the backend
- ⚠️ Do NOT delete archive without database backup confirmation
