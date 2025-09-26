# NEPSE Unofficial API Library

[![Status](https://github.com/basic-bgnr/NepseUnofficialApi/actions/workflows/actions.yml/badge.svg)](https://github.com/basic-bgnr/NepseUnofficialApi/actions/workflows/actions.yml)

This directory contains the NepseUnofficialApi library - an unofficial Python library to interface with nepalstock.com that deciphers the authentication key to access the NEPSE API.

## 📁 Directory Structure

```
API/
├── nepse/                 # Core library package
│   ├── __init__.py       # Package initialization
│   ├── NepseLib.py       # Main NEPSE API library
│   ├── TokenUtils.py     # Authentication utilities
│   ├── DummyIDUtils.py   # ID generation utilities
│   ├── Errors.py         # Custom exception classes
│   └── data/             # Configuration and data files
│       ├── API_ENDPOINTS.json  # NEPSE API endpoints
│       ├── HEADERS.json        # HTTP headers
│       ├── DUMMY_DATA.json     # Sample data structures
│       └── css.wasm           # WebAssembly for token decryption
├── pyproject.toml        # Package configuration
├── Requirements.txt      # Dependencies
└── README.md            # This file
```

## 🚀 Installation

This library is installed as an editable package in the NEPSE Smart project:

```bash
# From the project root
cd API
pip install -e .
```

## 💻 Usage in NEPSE Smart Project

The library is integrated into the FastAPI backend and can be used as follows:

### Synchronous API Usage

```python
from nepse import Nepse

nepse = Nepse()
nepse.setTLSVerification(False)  # Temporary fix for NEPSE SSL issues

# Get market summary
summary = nepse.getSummary()

# Get company listings
companies = nepse.getCompanyList()

# Get live market data
live_data = nepse.getLiveMarket()
```

### Asynchronous API Usage

```python
from nepse import AsyncNepse

nepse = AsyncNepse()
nepse.setTLSVerification(False)

# Async operations
companies = await nepse.getCompanyList()
summary = await nepse.getSummary()
```

### CLI Tool Integration

The package includes `nepse-cli` command-line tool:

```bash
# Get help
nepse-cli --help

# Download floorsheet data
nepse-cli --get-floorsheet --output-file floor.json
nepse-cli --get-floorsheet --to-csv --output-file floor.csv

# Start standalone server
nepse-cli --start-server

# Show market status
nepse-cli --show-status
```

## 🛠️ Integration Notes

- **SSL Handling**: The library includes workarounds for NEPSE's SSL certificate issues
- **WebAssembly**: Uses `css.wasm` for token decryption and authentication
- **Rate Limiting**: Built-in handling for NEPSE API rate limits
- **Error Handling**: Custom exception classes for robust error management
- **HTTP/2 Support**: Optimized for fast API communication

## 🔧 Configuration Files

- **API_ENDPOINTS.json**: Contains all NEPSE API endpoint definitions
- **HEADERS.json**: HTTP headers required for NEPSE API access
- **DUMMY_DATA.json**: Sample data structures for testing
- **css.wasm**: WebAssembly module for authentication token processing

## 📝 Library Maintenance

This is a clean, streamlined version of the NepseUnofficialApi library integrated specifically for the NEPSE Smart project. Redundant files and examples have been removed to maintain focus on the core functionality.

For the original library documentation and development history, visit: https://github.com/basic-bgnr/NepseUnofficialApi

## ⚠️ Known Issues & Solutions

### SSL Certificate Issues

NEPSE's SSL certificate chain is incomplete, which can cause SSL verification errors:

```
requests.exceptions.SSLError: certificate verify failed: unable to get local issuer certificate
```

**Solution**: The library handles this by using `setTLSVerification(False)` as a temporary workaround.

### Rate Limiting

NEPSE API has built-in rate limiting. The library includes:

- Automatic retry logic
- HTTP/2 support for better performance
- Optimized request handling

## 🔄 Recent Updates in NEPSE Smart Integration

- ✅ Cleaned up redundant example files
- ✅ Streamlined package structure
- ✅ Removed build artifacts and system files
- ✅ Integrated as editable package for development
- ✅ Maintained all core functionality

## 📚 Reference

- **Original Repository**: https://github.com/basic-bgnr/NepseUnofficialApi
- **Python Version**: 3.11+ required
- **Key Dependencies**: httpx, pywasm, flask, tqdm

---

**Note**: This library is not officially affiliated with Nepal Stock Exchange (NEPSE). It provides unofficial access to publicly available data for educational and analytical purposes.

# Fix Details

## Fixed: SSL Error

Recently there was a [PR](https://github.com/basic-bgnr/NepseUnofficialApi/pull/3) in this repo by [@Prabesh01](https://github.com/Prabesh01) to merge few changes to fix SSL issue that he was facing.

```
requests.exceptions.SSLError:
HTTPSConnectionPool(host='www.nepalstock.com.np', port=443):
Max retries exceeded with url: /api/authenticate/prove
(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED]
certificate verify failed: unable to get local issuer certificate (_ssl.c:1002)')))
```

The day when I actually received that PR, I too was facing similar issue with Nepse's website, so I thought the issue was serverside and left it as it is.

Fast-forward today, upon diving a little deeper, It appears that the issue can be solved entirely from clientside. But it has nothing to do with code in this repository, it was because my linux distribution(and maybe others too, I haven't checked) doesn't have ca-certificate of Certificate Authority [GeoTrust](http://cacerts.geotrust.com/) that signs the ssl certificate of Nepse. The mistake is primarily due to Nepse as it means that the certificate chain used by Nepse is incomplete.

> ### Solution:

1. Find out the ssl [certificate details of Nepse](https://www.ssllabs.com/ssltest/analyze.html?d=nepalstock.com.np) using [ssllabs.com](https://www.ssllabs.com).
1. Copy the .pem file from the ssllabs and save it into your `/usr/local/share/ca-certificates/` folder using the following command[^1].

```
sudo curl -A "Mozilla Chrome Safari" "https://www.ssllabs.com/ssltest/getTestCertificate?d=nepalstock.com.np&cid=3a83c9a7e960f29b48e5719510e2e8582c37f72f3abf35e6f400eaacec38aad2&time=1695547628855" >> geotrust.pem
sudo curl -A "Mozilla Chrome Safari" "https://www.ssllabs.com/ssltest/getTestChain?d=nepalstock.com.np&cid=3a83c9a7e960f29b48e5719510e2e8582c37f72f3abf35e6f400eaacec38aad2&time=1695547628855" >> geotrust_alt.pem
```

3. and, finally you've to run the following command[^1] to include the added CA details into the system.  
   ` sudo update-ca-certificates`
   [^1]: The command uses root access so first verify before carrying out the operation.
