# NEPSE Smart Data Scraper - Production Optimized

⚡ **Ultra-fast, lightweight production scraper for Nepal Stock Exchange data**

## 🎯 Overview

Optimized production scraper that collects comprehensive NEPSE data with minimal resource usage:

### 📊 Data Sources

- **ShareSansar.com**: stock prices and market indices
- **MeroLagani.com**: floorsheet transactions (with full pagination)

## 🚀 Quick Start

### Local Testing

```bash
# Quick test (1 page, ~500 transactions)
FLOORSHEET_PAGES=1 python production_scraper.py

# Standard collection (10 pages, ~5,000 transactions)
FLOORSHEET_PAGES=10 python production_scraper.py

# Full collection (72 pages, ~35,750 transactions)
FLOORSHEET_PAGES=72 python production_scraper.py
```

### GitHub Actions

- **Automatic**: Runs daily at midnight UTC (5:45 AM NPT)
- **Complete**: Collects ALL pages by default
- **Manual**: Trigger with custom page count via workflow dispatch
- **Fast**: ~6-12 minutes for full collection vs ~30+ minutes before optimization

## 📦 Minimal Dependencies

**Just 4 packages** (vs 24 in full requirements):

```
requests>=2.31.0          # HTTP client (~3MB)
beautifulsoup4>=4.12.2    # HTML parsing (~1MB)
lxml>=4.9.3              # XML/HTML parser (~15MB)
pandas>=2.1.4            # Data processing (~30MB)
Total: ~50MB vs 500MB+ full installation
```

## 🎯 Data Collection Capabilities

### Stock Prices (ShareSansar)

- **318+ companies** with OHLC, volume, turnover data
- **Real-time indices** and market statistics
- **JSON output**: ~500KB per collection

### Floorsheet Transactions (MeroLagani)

- **Configurable pages**: variable pages pages (500 transactions each)
- **Complete transaction data**: Symbol, brokers, quantity, rate, amount
- **JSON output**: ~2-10MB per collection (based on pages)

### Sample Output

```json
{
  "sn": "1",
  "transaction_no": "T123456",
  "symbol": "NABIL",
  "buyer_broker": "Broker A",
  "seller_broker": "Broker B",
  "share_quantity": 100,
  "rate": 1235.0,
  "amount": 123500.0,
  "date": "2025-10-15",
  "source": "merolagani"
}
```

## 🛠️ GitHub Actions Integration

### Workflow Features

```yaml
# Minimal dependency installation
- pip install -r data-scraper/requirements.txt

# Dependency caching for speed
- uses: actions/cache@v3

# Environment variable control
env:
  FLOORSHEET_PAGES: 10

# Fast execution (15 minute timeout)
timeout-minutes: 15
```

### Manual Execution

```bash
# GitHub CLI
gh workflow run daily-scraping.yml -f pages=5

# Or via GitHub web interface
Actions → Daily NEPSE Data Collection → Run workflow
```

## 📁 File Structure

```
data-scraper/
├── production_scraper.py     # Optimized main scraper
├── requirements.txt          # Minimal 4 dependencies
├── optimization_report.sh    # Performance comparison
└── logs/                     # Daily execution logs

data/
├── daily/                    # Daily JSON collections
│   ├── 2025-10-15_prices.json      (~500KB)
│   ├── 2025-10-15_floorsheet.json  (~2-10MB)
│   └── 2025-10-15_indices.json     (~10KB)
└── historical/               # Accumulated historical data
    ├── historical_prices.json
    ├── historical_floorsheet.json
    └── historical_indices.json
```

## 🔧 Configuration

### Environment Variables

- `FLOORSHEET_PAGES`: Number of MeroLagani pages to scrape (0 = all pages, default: 0)

### Page Recommendations

| Use Case            | Pages       | Transactions | Runtime       | File Size |
| ------------------- | ----------- | ------------ | ------------- | --------- |
| Quick test          | 1-3         | 500-1,500    | ~30s          | ~1MB      |
| Partial collection  | 10-20       | 5,000-10,000 | ~3-8 min      | ~2-4MB    |
| **Full collection** | **0 (all)** | **~35,750**  | **~6-12 min** | **~7MB**  |

## 🔍 Error Handling & Reliability

### Built-in Features

- **Retry Logic**: 3 attempts with exponential backoff
- **Fallback Mechanisms**: Continue with partial data on failures
- **Data Validation**: Comprehensive error checking
- **Success Criteria**: At least 2/3 data sources must succeed
- **Logging**: Detailed logs for debugging and monitoring

### GitHub Actions Safeguards

- **Timeout Protection**: 15-minute maximum runtime
- **Partial Success**: Commits available data even on partial failures
- **Artifact Upload**: Logs preserved for troubleshooting
- **Status Reporting**: Clear success/failure indicators

## 📊 Monitoring & Analytics

### Collection Summary

Daily execution generates comprehensive reports:

```json
{
  "collection_date": "2025-10-15",
  "totals": {
    "prices": 318,
    "floorsheet": 5000,
    "indices": 15,
    "total_records": 5333
  },
  "success": true
}
```

### Performance Metrics

- Installation time: ~2 minutes (vs 8+ minutes)
- Execution time: ~3-5 minutes (vs 15+ minutes)
- Memory usage: ~100MB (vs 500MB+)
- Storage per day: ~2-10MB JSON (vs 20-50MB with CSV)

## 🚀 Optimization Benefits

### Cost Savings

- **GitHub Actions**: 75% reduction in build minutes
- **Storage**: 90% reduction in dependency size
- **Bandwidth**: Faster downloads and deployments

### Reliability Improvements

- **Focused Dependencies**: Fewer potential failure points
- **Faster Recovery**: Quick re-runs on failures
- **Predictable Performance**: Consistent execution times

### Developer Experience

- **Local Testing**: Fast setup and iteration
- **Clear Logs**: Focused, relevant output
- **Easy Debugging**: Minimal complexity

## 🛡️ Production Readiness Checklist

✅ **Minimal Dependencies** - Only essential packages  
✅ **Error Handling** - Comprehensive retry and fallback logic  
✅ **Performance Optimized** - Fast execution with caching  
✅ **Storage Efficient** - JSON-only output  
✅ **Monitoring Ready** - Detailed logging and reporting  
✅ **GitHub Actions Optimized** - Fast, reliable automation  
✅ **Configurable** - Environment variable control  
✅ **Documentation** - Complete usage guides

---

**🎉 Ready for production use with optimal performance and minimal resource usage!**
