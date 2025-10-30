# NEPSE Official API Reference

This document provides a comprehensive reference for the NepseUnofficialApi library endpoints, including data types and representative samples.

## Overview
- **Library**: NepseUnofficialApi
- **Authentication**: Required for most endpoints
- **Data Format**: JSON-compatible Python objects (lists, dicts)

## API Endpoints Reference

### getCompanyList
- **Return Type**: list
- **Total Items**: 599
- **Sample Data**:
```json
[
  {
    "id": 131,
    "companyName": "Nabil Bank Limited",
    "symbol": "NABIL",
    "securityName": "Nabil Bank Limited",
    "status": "A",
    "companyEmail": "company.affairs@nabilbank.com",
    "website": "www.nabilbank.com",
    "sectorName": "Commercial Banks",
    "regulatoryBody": "Nepal Rastra Bank",
    "instrumentType": "Equity"
  },
  {
    "id": 132,
    "companyName": "Nepal Investment Mega Bank Limited",
    "symbol": "NIMB",
    "securityName": "Nepal Investment Mega Bank Limited",
    "status": "A",
    "companyEmail": "info@nimb.com.np",
    "website": "http://www.nimb.com.np",
    "sectorName": "Commercial Banks",
    "regulatoryBody": "Nepal Rastra Bank",
    "instrumentType": "Equity"
  },
  {
    "id": 133,
    "companyName": "Standard Chartered Bank  Nepal Limited",
    "symbol": "SCB",
    "securityName": "Standard Chartered Bank Limited",
    "status": "A",
    "companyEmail": "Legal.Nepal@sc.com",
    "website": "www.sc.com/np",
    "sectorName": "Commercial Banks",
    "regulatoryBody": "Nepal Rastra Bank",
    "instrumentType": "Equity"
  },
  {
    "id": 134,
    "companyName": "Himalayan Bank Limited",
    "symbol": "HBL",
    "securityName": "Himalayan Bank Limited",
    "status": "A",
    "companyEmail": "legal@himalayanbank.com",
    "website": "https://www.himalayanbank.com",
    "sectorName": "Commercial Banks",
    "regulatoryBody": "Nepal Rastra Bank",
    "instrumentType": "Equity"
  },
  {
    "id": 135,
    "companyName": "Nepal SBI Bank Limited",
    "symbol": "SBI",
    "securityName": "Nepal SBI Bank Limited",
    "status": "A",
    "companyEmail": "cs@nsbl.com.np",
    "website": "https://nsbl.statebank",
    "sectorName": "Commercial Banks",
    "regulatoryBody": "Nepal Rastra Bank",
    "instrumentType": "Equity"
  }
]
```

---

### getSecurityList
- **Return Type**: list
- **Total Items**: 529
- **Sample Data**:
```json
[
  {
    "id": 9192,
    "symbol": "USHL",
    "securityName": "Upper Syange Hydropower Limited",
    "name": "(USHL) Upper Syange Hydropower Limited",
    "activeStatus": "A"
  },
  {
    "id": 2790,
    "symbol": "ACLBSL",
    "securityName": "Aarambha Chautari Laghubitta Bittiya Sanstha Limited",
    "name": "(ACLBSL) Aarambha Chautari Laghubitta Bittiya Sanstha Limited",
    "activeStatus": "A"
  },
  {
    "id": 2791,
    "symbol": "ACLBSLP",
    "securityName": "Aarambha Chautari Laghubitta Bittiya Sanstha Limited Promoter Share",
    "name": "(ACLBSLP) Aarambha Chautari Laghubitta Bittiya Sanstha Limited Promoter Share",
    "activeStatus": "A"
  },
  {
    "id": 9161,
    "symbol": "ANLB",
    "securityName": "Aatmanirbhar Laghubitta Bittiya Sanstha Limited",
    "name": "(ANLB) Aatmanirbhar Laghubitta Bittiya Sanstha Limited",
    "activeStatus": "A"
  },
  {
    "id": 9164,
    "symbol": "ANLBP",
    "securityName": "Aatmanirbhar Laghubitta Bittiya Sanstha Limited Promoter Share",
    "name": "(ANLBP) Aatmanirbhar Laghubitta Bittiya Sanstha Limited Promoter Share",
    "activeStatus": "A"
  }
]
```

---

### getFloorSheet
- **Return Type**: list
- **Total Items**: 53112
- **Sample Data**:
```json
[
  {
    "contractId": 2025103005017614,
    "stockSymbol": "SIKLES",
    "buyerMemberId": "95",
    "sellerMemberId": "38",
    "contractQuantity": 200,
    "contractRate": 659.0,
    "contractAmount": 131800.0,
    "businessDate": "2025-10-30",
    "tradeBookId": 167823747,
    "stockId": 8126,
    "buyerBrokerName": "Magnet Securities and Investment Company Private Limited",
    "sellerBrokerName": "Dipshikha Dhitopatra Karobar Co. Pvt Ltd.",
    "tradeTime": "2025-10-30T14:59:59.956739",
    "securityName": "Sikles Hydropower Limited"
  },
  {
    "contractId": 2025103004016483,
    "stockSymbol": "RHPL",
    "buyerMemberId": "57",
    "sellerMemberId": "95",
    "contractQuantity": 190,
    "contractRate": 272.0,
    "contractAmount": 51680.0,
    "businessDate": "2025-10-30",
    "tradeBookId": 167823804,
    "stockId": 2841,
    "buyerBrokerName": "Aryatara Investment & Securities",
    "sellerBrokerName": "Magnet Securities and Investment Company Private Limited",
    "tradeTime": "2025-10-30T14:59:59.952437",
    "securityName": "RASUWAGADHI HYDROPOWER COMPANY LIMITED"
  },
  {
    "contractId": 2025103005017613,
    "stockSymbol": "PHCL",
    "buyerMemberId": "32",
    "sellerMemberId": "32",
    "contractQuantity": 10,
    "contractRate": 377.4,
    "contractAmount": 3774.0,
    "businessDate": "2025-10-30",
    "tradeBookId": 167823620,
    "stockId": 8133,
    "buyerBrokerName": "Premier Securities Company Ltd.",
    "sellerBrokerName": "Premier Securities Company Ltd.",
    "tradeTime": "2025-10-30T14:59:59.91382",
    "securityName": "Peoples Hydropower Company Limited"
  },
  {
    "contractId": 2025103004016482,
    "stockSymbol": "TRH",
    "buyerMemberId": "13",
    "sellerMemberId": "32",
    "contractQuantity": 50,
    "contractRate": 720.0,
    "contractAmount": 36000.0,
    "businessDate": "2025-10-30",
    "tradeBookId": 167823803,
    "stockId": 148,
    "buyerBrokerName": "Thrive Brokerage House Pvt. Ltd",
    "sellerBrokerName": "Premier Securities Company Ltd.",
    "tradeTime": "2025-10-30T14:59:59.909988",
    "securityName": "Taragaon Regency Hotel Limited"
  },
  {
    "contractId": 2025103004016481,
    "stockSymbol": "TRH",
    "buyerMemberId": "45",
    "sellerMemberId": "32",
    "contractQuantity": 20,
    "contractRate": 720.0,
    "contractAmount": 14400.0,
    "businessDate": "2025-10-30",
    "tradeBookId": 167823798,
    "stockId": 148,
    "buyerBrokerName": "Imperial Securities Company Pvt. Ltd.",
    "sellerBrokerName": "Premier Securities Company Ltd.",
    "tradeTime": "2025-10-30T14:59:59.909944",
    "securityName": "Taragaon Regency Hotel Limited"
  }
]
```

---

### getNepseIndex
- **Return Type**: list
- **Total Items**: 4
- **Sample Data**:
```json
[
  {
    "id": 57,
    "auditId": null,
    "exchangeIndexId": null,
    "generatedTime": "2025-10-30T15:18:27.15",
    "index": "Sensitive Index",
    "close": 447.41,
    "high": 453.3381,
    "low": 444.9194,
    "previousClose": 452.8135,
    "change": 5.4,
    "perChange": 1.2,
    "fiftyTwoWeekHigh": 518.6,
    "fiftyTwoWeekLow": 434.98,
    "currentValue": 452.81
  },
  {
    "id": 58,
    "auditId": null,
    "exchangeIndexId": null,
    "generatedTime": "2025-10-30T15:18:27.15",
    "index": "NEPSE Index",
    "close": 2566.16,
    "high": 2605.5078,
    "low": 2548.3936,
    "previousClose": 2600.3892,
    "change": 34.22,
    "perChange": 1.33,
    "fiftyTwoWeekHigh": 3002.08,
    "fiftyTwoWeekLow": 2487.18,
    "currentValue": 2600.38
  },
  {
    "id": 62,
    "auditId": null,
    "exchangeIndexId": null,
    "generatedTime": "2025-10-30T15:18:27.153",
    "index": "Float Index",
    "close": 175.86,
    "high": 178.4215,
    "low": 174.675,
    "previousClose": 178.2362,
    "change": 2.37,
    "perChange": 1.35,
    "fiftyTwoWeekHigh": 206.26,
    "fiftyTwoWeekLow": 170.58,
    "currentValue": 178.23
  },
  {
    "id": 63,
    "auditId": null,
    "exchangeIndexId": null,
    "generatedTime": "2025-10-30T15:18:27.153",
    "index": "Sensitive Float Index",
    "close": 152.05,
    "high": 154.1755,
    "low": 151.1663,
    "previousClose": 153.9858,
    "change": 1.93,
    "perChange": 1.27,
    "fiftyTwoWeekHigh": 177.31,
    "fiftyTwoWeekLow": 145.59,
    "currentValue": 153.98
  }
]
```

---

### getNepseSubIndices
- **Return Type**: list
- **Total Items**: 13
- **Sample Data**:
```json
[
  {
    "id": 64,
    "index": "Microfinance Index",
    "change": 77.34,
    "perChange": 1.6,
    "currentValue": 4902.23
  },
  {
    "id": 65,
    "index": "Life Insurance",
    "change": 226.6,
    "perChange": 1.8,
    "currentValue": 12775.16
  },
  {
    "id": 66,
    "index": "Mutual Fund",
    "change": -0.03,
    "perChange": -0.18,
    "currentValue": 20.22
  },
  {
    "id": 67,
    "index": "Investment Index",
    "change": 1.4,
    "perChange": 1.35,
    "currentValue": 105.3
  },
  {
    "id": 51,
    "index": "Banking SubIndex",
    "change": 4.59,
    "perChange": 0.33,
    "currentValue": 1370.18
  }
]
```

---

### getPriceVolume
- **Return Type**: list
- **Total Items**: 249
- **Sample Data**:
```json
[
  {
    "securityId": "2790",
    "securityName": "Aarambha Chautari Laghubitta Bittiya Sanstha Limited",
    "symbol": "ACLBSL",
    "indexId": 58,
    "totalTradeQuantity": 828,
    "lastTradedPrice": 1008.0,
    "percentageChange": 1.408450704,
    "previousClose": 994.0,
    "closePrice": 1008.0
  },
  {
    "securityId": "397",
    "securityName": "Agricultural Development Bank Limited",
    "symbol": "ADBL",
    "indexId": 58,
    "totalTradeQuantity": 28033,
    "lastTradedPrice": 313.5,
    "percentageChange": 0.480769231,
    "previousClose": 312.0,
    "closePrice": 313.5
  },
  {
    "securityId": "9150",
    "securityName": "Asian Hydropower Limited",
    "symbol": "AHL",
    "indexId": 58,
    "totalTradeQuantity": 5197,
    "lastTradedPrice": 628.0,
    "percentageChange": 0.159489633,
    "previousClose": 627.0,
    "closePrice": 628.0
  },
  {
    "securityId": "360",
    "securityName": "Arun Valley Hydropower Development Co. Ltd.",
    "symbol": "AHPC",
    "indexId": 58,
    "totalTradeQuantity": 216839,
    "lastTradedPrice": 286.9,
    "percentageChange": 2.099644128,
    "previousClose": 281.0,
    "closePrice": 286.9
  },
  {
    "securityId": "2788",
    "securityName": "Ankhu Khola Jalvidhyut Company Ltd",
    "symbol": "AKJCL",
    "indexId": 58,
    "totalTradeQuantity": 76960,
    "lastTradedPrice": 194.0,
    "percentageChange": 1.570680628,
    "previousClose": 191.0,
    "closePrice": 194.0
  }
]
```

---

### getTopGainers
- **Return Type**: list
- **Total Items**: 248
- **Sample Data**:
```json
[
  {
    "symbol": "GLBSL",
    "ltp": 2310.0,
    "cp": 2310.0,
    "pointChange": 210.0,
    "percentageChange": 10.0,
    "securityName": "Gurans Laghubitta Bittiya Sanstha Limited",
    "securityId": 2826
  },
  {
    "symbol": "USLB",
    "ltp": 2002.1,
    "cp": 2002.1,
    "pointChange": 182.0,
    "percentageChange": 10.0,
    "securityName": "Unnati Sahakarya Laghubitta Bittiya Sanstha Limited",
    "securityId": 2774
  },
  {
    "symbol": "SMHL",
    "ltp": 897.0,
    "cp": 897.0,
    "pointChange": 78.1,
    "percentageChange": 9.54,
    "securityName": "Super Madi Hydropower Limited",
    "securityId": 9146
  },
  {
    "symbol": "GMFBS",
    "ltp": 1620.0,
    "cp": 1620.0,
    "pointChange": 140.0,
    "percentageChange": 9.46,
    "securityName": "Ganapati Laghubitta Bittiya Sanstha Limited",
    "securityId": 2815
  },
  {
    "symbol": "PHCL",
    "ltp": 377.4,
    "cp": 377.4,
    "pointChange": 31.4,
    "percentageChange": 9.08,
    "securityName": "Peoples Hydropower Company Limited",
    "securityId": 8133
  }
]
```

---

### getTopLosers
- **Return Type**: list
- **Total Items**: 59
- **Sample Data**:
```json
[
  {
    "symbol": "NIBLSTF",
    "ltp": 8.44,
    "cp": 8.44,
    "pointChange": -0.51,
    "percentageChange": -5.7,
    "securityName": "NIBL Stable Fund",
    "securityId": 9244
  },
  {
    "symbol": "SAGF",
    "ltp": 9.05,
    "cp": 9.05,
    "pointChange": -0.5,
    "percentageChange": -5.24,
    "securityName": "Sanima Growth Fund",
    "securityId": 9139
  },
  {
    "symbol": "ALBSL",
    "ltp": 1014.0,
    "cp": 1014.0,
    "pointChange": -51.0,
    "percentageChange": -4.79,
    "securityName": "Asha Laghubitta Bittiya Sanstha Ltd",
    "securityId": 2807
  },
  {
    "symbol": "ULBSL",
    "ltp": 3770.6,
    "cp": 3770.6,
    "pointChange": -155.4,
    "percentageChange": -3.96,
    "securityName": "Upakar Laghubitta Bittiya Sanstha Limited",
    "securityId": 8063
  },
  {
    "symbol": "HPPL",
    "ltp": 539.0,
    "cp": 539.0,
    "pointChange": -21.0,
    "percentageChange": -3.75,
    "securityName": "Himalayan Power Partner Ltd.",
    "securityId": 2767
  }
]
```

---

### getTopTenTradeScrips
- **Return Type**: list
- **Total Items**: 319
- **Sample Data**:
```json
[
  {
    "symbol": "HBLPO",
    "shareTraded": 14006230,
    "closingPrice": 131.0,
    "securityName": "Himalayan Bank Ltd. Promoter",
    "securityId": 564
  },
  {
    "symbol": "RADHI",
    "shareTraded": 497142,
    "closingPrice": 767.0,
    "securityName": "Radhi Bidyut Company Ltd",
    "securityId": 2776
  },
  {
    "symbol": "UPCL",
    "shareTraded": 369523,
    "closingPrice": 384.0,
    "securityName": "UNIVERSAL POWER COMPANY LTD",
    "securityId": 2810
  },
  {
    "symbol": "NGPL",
    "shareTraded": 369374,
    "closingPrice": 388.0,
    "securityName": "Ngadi Group Power Ltd.",
    "securityId": 2743
  },
  {
    "symbol": "UNHPL",
    "shareTraded": 362817,
    "closingPrice": 513.0,
    "securityName": "Union Hydropower Limited",
    "securityId": 2831
  }
]
```

---

### getTopTenTransactionScrips
- **Return Type**: list
- **Total Items**: 319
- **Sample Data**:
```json
[
  {
    "securityId": 2776,
    "totalTrades": 1540,
    "lastTradedPrice": 767.0,
    "securityName": "Radhi Bidyut Company Ltd",
    "symbol": "RADHI"
  },
  {
    "securityId": 134,
    "totalTrades": 1410,
    "lastTradedPrice": 199.5,
    "securityName": "Himalayan Bank Limited",
    "symbol": "HBL"
  },
  {
    "securityId": 8021,
    "totalTrades": 1279,
    "lastTradedPrice": 674.6,
    "securityName": "Sahas Urja Limited",
    "symbol": "SAHAS"
  },
  {
    "securityId": 2881,
    "totalTrades": 1239,
    "lastTradedPrice": 1380.0,
    "securityName": "Nepal Reinsurance Company Limited",
    "symbol": "NRIC"
  },
  {
    "securityId": 9234,
    "totalTrades": 1102,
    "lastTradedPrice": 808.0,
    "securityName": "Himalayan Reinsurance Limited",
    "symbol": "HRL"
  }
]
```

---

### getTopTenTurnoverScrips
- **Return Type**: list
- **Total Items**: 319
- **Sample Data**:
```json
[
  {
    "symbol": "HBLPO",
    "turnover": 1665060622.4,
    "closingPrice": 131.0,
    "securityName": "Himalayan Bank Ltd. Promoter",
    "securityId": 564
  },
  {
    "symbol": "RADHI",
    "turnover": 376004605.3,
    "closingPrice": 767.0,
    "securityName": "Radhi Bidyut Company Ltd",
    "securityId": 2776
  },
  {
    "symbol": "NRIC",
    "turnover": 341036207.7,
    "closingPrice": 1380.0,
    "securityName": "Nepal Reinsurance Company Limited",
    "securityId": 2881
  },
  {
    "symbol": "SAHAS",
    "turnover": 206020094.5,
    "closingPrice": 674.6,
    "securityName": "Sahas Urja Limited",
    "securityId": 8021
  },
  {
    "symbol": "BPCL",
    "turnover": 201437343.2,
    "closingPrice": 779.0,
    "securityName": "Butwal Power Company Limited",
    "securityId": 153
  }
]
```

---

### getDailyNepseIndexGraph
- **Return Type**: list
- **Total Items**: 588
- **Sample Data**:
```json
[
  [
    1761800700,
    2568.41
  ],
  [
    1761800700,
    2568.41
  ],
  [
    1761800700,
    2568.41
  ],
  [
    1761800700,
    2568.41
  ],
  [
    1761800700,
    2568.41
  ]
]
```

---

### getDailySensitiveIndexGraph
- **Return Type**: list
- **Total Items**: 588
- **Sample Data**:
```json
[
  [
    1761800700,
    448.43
  ],
  [
    1761800700,
    448.43
  ],
  [
    1761800700,
    448.43
  ],
  [
    1761800700,
    448.43
  ],
  [
    1761800700,
    448.43
  ]
]
```

---

### getSummary
- **Return Type**: list
- **Total Items**: 6
- **Sample Data**:
```json
[
  {
    "detail": "Total Turnover Rs:",
    "value": 7513938473.45
  },
  {
    "detail": "Total Traded Shares",
    "value": 26010718.0
  },
  {
    "detail": "Total Transactions",
    "value": 53112.0
  },
  {
    "detail": "Total Scrips Traded",
    "value": 319.0
  },
  {
    "detail": "Total Market Capitalization Rs:",
    "value": 4347161313108.67
  }
]
```

---

### getMarketStatus
- **Return Type**: dict
- **Total Items**: 3
- **Sample Data**:
```json
{
  "isOpen": "CLOSE",
  "asOf": "2025-10-30T15:00:00",
  "id": 80
}
```

---

### getSectorScrips
- **Return Type**: dict
- **Total Items**: 14
- **Sample Data**:
```json
{
  "Hydro Power": [
    "USHL",
    "AKJCL",
    "API",
    "AKPL",
    "AHPC"
  ],
  "Microfinance": [
    "ACLBSL",
    "ANLB",
    "ALBSL",
    "AVYAN",
    "CBBL"
  ],
  "Promoter Share": [
    "ACLBSLP",
    "ANLBP",
    "ALBSLP",
    "ALICLP",
    "AVYANP"
  ],
  "Commercial Banks": [
    "ADBL",
    "ADBLD83",
    "ADBLB",
    "ADBLB86",
    "ADBLB87"
  ],
  "Manufacturing And Processing": [
    "AVU",
    "BSL",
    "BNL",
    "BNT",
    "BSM"
  ],
  "Life Insurance": [
    "ALICL",
    "CLI",
    "CREST",
    "GMLI",
    "HLI"
  ],
  "Finance": [
    "BFC",
    "CMB",
    "CFCL",
    "CFL",
    "GFCL"
  ],
  "Tradings": [
    "BBC",
    "NTL",
    "NWC",
    "STC"
  ],
  "Mutual Fund": [
    "CMF2",
    "GIBF1",
    "LUK",
    "NIBLGF",
    "NICBF"
  ],
  "Investment": [
    "CHDC",
    "CIT",
    "ENL",
    "HATHY",
    "HIDCL"
  ],
  "Hotels And Tourism": [
    "CGH",
    "CITY",
    "KDL",
    "OHL",
    "SHL"
  ],
  "Development Banks": [
    "CORBL",
    "EDBL",
    "GBBL",
    "GSY",
    "GBBD85"
  ],
  "Non Life Insurance": [
    "HEI",
    "IGI",
    "NIL",
    "NICL",
    "NMIC"
  ],
  "Others": [
    "HRL",
    "MKCL",
    "NTC",
    "NFD",
    "NRIC"
  ]
}
```

---

### getSupplyDemand
- **Return Type**: dict
- **Total Items**: 2
- **Sample Data**:
```json
{
  "supplyList": [
    {
      "totalQuantity": 1075,
      "totalOrder": 4,
      "securityId": 8098,
      "symbol": "SBLD89",
      "securityName": "10.75% SBL Debenture 2089"
    },
    {
      "totalQuantity": 27,
      "totalOrder": 2,
      "securityId": 2922,
      "symbol": "SBD87",
      "securityName": "8.5% Sanima Debenture 2087"
    },
    {
      "totalQuantity": 7,
      "totalOrder": 1,
      "securityId": 2936,
      "symbol": "NCCD86",
      "securityName": "9.5% NCC Debenture 2086"
    }
  ],
  "demandList": [
    {
      "totalQuantity": 100,
      "totalOrder": 1,
      "securityId": 2889,
      "symbol": "CIZBD86",
      "securityName": "10.25% Citizens Bank Debenture 2086"
    },
    {
      "totalQuantity": 100,
      "totalOrder": 1,
      "securityId": 2922,
      "symbol": "SBD87",
      "securityName": "8.5% Sanima Debenture 2087"
    },
    {
      "totalQuantity": 100,
      "totalOrder": 1,
      "securityId": 2936,
      "symbol": "NCCD86",
      "securityName": "9.5% NCC Debenture 2086"
    },
    {
      "totalQuantity": 100,
      "totalOrder": 1,
      "securityId": 9177,
      "symbol": "SCBD",
      "securityName": "10.30% Standard Chartered Bank Limited Debenture"
    }
  ]
}
```

---

### getCompanyIDKeyMap
- **Return Type**: dict
- **Total Items**: 599
- **Sample Data**:
```json
{
  "NABIL": 131,
  "NIMB": 132,
  "SCB": 133,
  "HBL": 134,
  "SBI": 135,
  "NBB": 136,
  "EBL": 137,
  "BOKL": 138,
  "NICA": 139,
  "MBL": 140,
  "LSL": 141,
  "KBL": 142,
  "LUBL": 143,
  "NCCB": 144,
  "SBL": 145,
  "YHL": 146,
  "SHL": 147,
  "TRH": 148,
  "OHL": 149,
  "ESC": 150,
  "NFD": 151,
  "NHPC": 152,
  "BPCL": 153,
  "CHCL": 154,
  "STC": 155,
  "BBC": 156,
  "NBCK": 157,
  "NTL": 158,
  "NWC": 159,
  "NIDC": 160,
  "NDB": 161,
  "GRAND": 162,
  "NUBL": 163,
  "CBBL": 164,
  "PDBL": 165,
  "DDBL": 166,
  "GDBL1": 167,
  "BUDBL": 168,
  "SDBL": 169,
  "BBBL": 170,
  "SANIMA": 171,
  "NABBC": 172,
  "BBBLN": 173,
  "SBBLJ": 174,
  "GDBNL": 175,
  "NICL": 176,
  "RBCL": 177,
  "NLICL": 178,
  "HEI": 179,
  "UAIL": 180,
  "EIC": 181,
  "SPIL": 182,
  "NIL": 183,
  "PRIN": 184,
  "SALICO": 185,
  "IGI": 186,
  "NLIC": 187,
  "LICN": 188,
  "PICL": 189,
  "LGIL": 190,
  "SICL": 192,
  "MSM": 193,
  "NFS": 194,
  "BNL": 195,
  "NCM": 196,
  "BJM": 197,
  "NLO": 198,
  "NNFC": 199,
  "NSM": 200,
  "NVG": 201,
  "KBBL": 202,
  "RJM": 203,
  "GUFL": 204,
  "BSM": 205,
  "PFCL": 206,
  "GRU": 207,
  "UFCL": 208,
  "JSM": 209,
  "CIT": 210,
  "AVU": 211,
  "NABB": 212,
  "BNT": 213,
  "NFL": 214,
  "HBT": 215,
  "ACEDBL": 216,
  "BSL": 217,
  "YFL": 218,
  "UNL": 219,
  "GFLK": 220,
  "SFC": 221,
  "NKU": 222,
  "UFLK": 223,
  "HTL": 224,
  "NHMF": 225,
  "SBPP": 226,
  "BFC": 227,
  "FHL": 228,
  "MFL": 229,
  "SRS": 230,
  "LFC": 231,
  "GFCL": 232,
  "NBBU": 233,
  "PFC": 234,
  "HDL": 235,
  "PFL": 236,
  "LFLC": 237,
  "NMB": 238,
  "SFL": 239,
  "AEFL": 240,
  "NBFL": 241,
  "UFL": 242,
  "ILFC": 243,
  "SIFC": 244,
  "CFCL": 245,
  "NSLMB": 246,
  "PFCLL": 247,
  "NDFL": 248,
  "SYFL": 249,
  "JFL": 250,
  "STFL": 251,
  "OFL": 252,
  "CMBF": 253,
  "FFCL": 254,
  "PRVU": 255,
  "SFCL": 256,
  "BJFL": 257,
  "EFL": 258,
  "CMB": 259,
  "PFIL": 260,
  "SFFIL": 261,
  "APEX": 262,
  "GMFIL": 263,
  "IMEFI": 264,
  "BFIL": 265,
  "PFLBS": 266,
  "SUPRME": 267,
  "SWBBL": 268,
  "NCMMF": 269,
  "IFIL": 270,
  "SODBL": 271,
  "CMBSL": 272,
  "ICFC": 273,
  "EDBL": 274,
  "MLBL1": 275,
  "EBLCP": 277,
  "NEFL": 278,
  "BLDBL": 279,
  "SIL": 280,
  "IDBL": 290,
  "CEFL": 296,
  "NTC": 307,
  "PRBBL": 308,
  "DBBL": 311,
  "LBFIL": 320,
  "SAFL": 321,
  "SUBBL": 331,
  "KAFIL": 332,
  "CEDBL": 336,
  "TBBL": 337,
  "PROFL": 338,
  "PGBL": 340,
  "GBIME": 341,
  "REDBL": 342,
  "AXIS": 344,
  "SBSL": 345,
  "CZBIL": 348,
  "BOAN": 349,
  "AFL": 356,
  "PCBL": 357,
  "LBBL": 358,
  "SRBL": 359,
  "AHPC": 360,
  "CFL": 361,
  "MGBL": 364,
  "PDB": 367,
  "MBBL": 370,
  "MDB": 371,
  "PBSL": 383,
  "RBSL": 384,
  "ALICL": 385,
  "KDBL": 388,
  "SEWA": 389,
  "HLI": 393,
  "NGBL": 394,
  "NMLBBL": 396,
  "ADBL": 397,
  "ODBL": 398,
  "MLBL": 401,
  "SJLIC": 403,
  "UBBL": 405,
  "ALDBL": 406,
  "SDFL": 407,
  "ZFL": 408,
  "SMF": 409,
  "SLFL": 411,
  "GSDBL": 412,
  "UFIL": 413,
  "PRDBL": 414,
  "SETI": 416,
  "GBBL": 417,
  "JBBL": 418,
  "KNBL": 419,
  "GDBL": 420,
  "HATH": 421,
  "KEBL": 427,
  "KRBL": 428,
  "HFL": 441,
  "TNBL": 442,
  "ARDBL": 443,
  "VFL": 444,
  "WDBL": 445,
  "PRBL": 446,
  "GLICL": 447,
  "CNDBL": 448,
  "CORBL": 450,
  "PURBL": 451,
  "KSBBL": 459,
  "RARA": 460,
  "HAMA": 470,
  "MPFL": 471,
  "SADBL": 472,
  "SHINE": 473,
  "MNBBL": 474,
  "BHBL": 487,
  "BGDBL": 489,
  "FMDBL": 490,
  "JBNL": 496,
  "SMFDB": 502,
  "TDBL": 503,
  "GULMI": 504,
  "KADBL": 505,
  "NCDBL": 506,
  "PADBL": 512,
  "METRO": 513,
  "RDBL": 514,
  "MFIL": 516,
  "NBL": 517,
  "SIGS1": 526,
  "INDB": 529,
  "KKBL": 531,
  "CBL": 532,
  "CIVIC": 533,
  "BRTBL": 535,
  "INDBL": 536,
  "KHDBL": 537,
  "NBF1": 538,
  "CTBNL": 539,
  "SLBBL": 545,
  "NLG": 559,
  "SINDU": 561,
  "MEGA": 562,
  "JHBL": 563,
  "MIDBL": 570,
  "NBSL": 571,
  "GABL": 572,
  "SKBBL": 574,
  "RMDC": 575,
  "HAMRO": 576,
  "JEFL": 577,
  "GBLBS": 583,
  "RLFL": 587,
  "MSBBL": 588,
  "SHPC": 591,
  "NSLB": 592,
  "KMCDB": 593,
  "MTBL": 595,
  "NCDB": 598,
  "CSDBL": 600,
  "MLBBL": 601,
  "NBBL": 602,
  "CCBL": 605,
  "TRHPR": 608,
  "RIDI": 610,
  "MMDBL": 614,
  "SEOS": 616,
  "EKBL": 617,
  "LLBS": 618,
  "SHBL": 625,
  "KCDBL": 627,
  "NMBSF1": 629,
  "NIBSF1": 636,
  "LVF1": 674,
  "RBBBL": 679,
  "BFCL": 680,
  "MMFDB": 682,
  "BARUN": 686,
  "VLBS": 687,
  "MSMBS": 691,
  "SBLD78": 692,
  "HLBSL": 693,
  "MATRI": 694,
  "JSLBB": 695,
  "API": 697,
  "NMBMF": 704,
  "GILB": 705,
  "SWMF": 706,
  "SKDBL": 1733,
  "SAJHA": 1735,
  "GIMES1": 1740,
  "MERO": 1741,
  "HIDCL": 2742,
  "NGPL": 2743,
  "GRDBL": 2744,
  "NMFBS": 2746,
  "RSDC": 2748,
  "SLBS": 2750,
  "KKHC": 2751,
  "NMBHF1": 2752,
  "NEF": 2753,
  "DHPL": 2754,
  "NIBLPF": 2755,
  "AKPL": 2757,
  "FOWAD": 2758,
  "SPDL": 2759,
  "UMHL": 2760,
  "SMATA": 2761,
  "SDESI": 2764,
  "LEMF": 2765,
  "CHL": 2766,
  "HPPL": 2767,
  "MSLB": 2768,
  "NHDL": 2769,
  "SEF": 2770,
  "SMB": 2771,
  "SAEF": 2773,
  "USLB": 2774,
  "RADHI": 2776,
  "AMFI": 2777,
  "NICGF": 2779,
  "CMF1": 2780,
  "WNLB": 2781,
  "RRHP": 2783,
  "NADEP": 2784,
  "PMHPL": 2786,
  "KPCL": 2787,
  "AKJCL": 2788,
  "JOSHI": 2789,
  "ACLBSL": 2790,
  "UPPER": 2792,
  "SLBSL": 2804,
  "GHL": 2806,
  "ALBSL": 2807,
  "SHIVM": 2809,
  "UPCL": 2810,
  "MHNL": 2811,
  "SPARS": 2812,
  "PPCL": 2813,
  "GMFBS": 2815,
  "NAGRO": 2816,
  "HURJA": 2824,
  "NICAD85/86": 2825,
  "GLBSL": 2826,
  "SAND2085": 2828,
  "SMFBS": 2829,
  "UNHPL": 2831,
  "ILBS": 2832,
  "SRD80": 2834,
  "NBF2": 2835,
  "GBD80/81": 2840,
  "RHPL": 2841,
  "SJCL": 2842,
  "SABSL": 2843,
  "AKBSL": 2845,
  "NMBD2085": 2850,
  "NIBD2082": 2851,
  "GGBSL": 2852,
  "NBBD2085": 2854,
  "TMDBL": 2855,
  "SIGS2": 2859,
  "SAPDBL": 2860,
  "CMF2": 2862,
  "NICBF": 2863,
  "SBLD83": 2864,
  "MBLD2085": 2866,
  "NMB50": 2867,
  "NICD83/84": 2868,
  "NICAD8283": 2869,
  "BOKD2079": 2870,
  "EBLD2078": 2871,
  "SBLD2082": 2872,
  "HBLD83": 2873,
  "PBLD86": 2875,
  "SFMF": 2877,
  "SRBLD83": 2878,
  "LBLD86": 2879,
  "HDHPC": 2880,
  "NRIC": 2881,
  "ICFCD83": 2882,
  "GWFD83": 2883,
  "KBLD86": 2885,
  "ADBLD83": 2886,
  "NICLBSL": 2887,
  "CIZBD86": 2889,
  "SBIBD86": 2890,
  "NBLD82": 2892,
  "AIL": 2893,
  "NICAD8182": 2895,
  "SMPDA": 2896,
  "NRN": 2898,
  "RLI": 2900,
  "LUK": 2902,
  "LEC": 2903,
  "PBLD84": 2904,
  "GIC": 2905,
  "SSHL": 2907,
  "SGIC": 2908,
  "SBLD84": 2912,
  "MEN": 2913,
  "UMRH": 2914,
  "PMLI": 2915,
  "CGH": 2917,
  "NIFRA": 2919,
  "SBD87": 2922,
  "SLCF": 2923,
  "GLH": 2924,
  "MLBSL": 2925,
  "JLI": 2929,
  "NIBD84": 2931,
  "MFLD85": 2932,
  "KEF": 2933,
  "SHEL": 2934,
  "RURU": 2935,
  "NCCD86": 2936,
  "SBCF": 2937,
  "CHDC": 3946,
  "PSF": 4947,
  "KSBBLD87": 4948,
  "NIBSF2": 4949,
  "JBLB": 4951,
  "MKLB": 4955,
  "ULI": 4956,
  "NBLD87": 4959,
  "ADBLB": 4960,
  "BOKD86": 4961,
  "PBLD87": 4962,
  "NMBD87/88": 4963,
  "NMBEB92/93": 4964,
  "SAMAJ": 4965,
  "NICSF": 4967,
  "RMF1": 4968,
  "MND84/85": 4969,
  "SRLI": 5982,
  "LBLD88": 5984,
  "PBD85": 6984,
  "SDBD87": 6985,
  "MBLD87": 7985,
  "NICD88": 7986,
  "RBBD83": 8003,
  "GBILD86/87": 8004,
  "MKJC": 8005,
  "MLBS": 8018,
  "JBBD87": 8020,
  "SAHAS": 8021,
  "TPC": 8022,
  "MMF1": 8023,
  "NBF3": 8024,
  "SPC": 8025,
  "NYADI": 8026,
  "NBLD85": 8027,
  "ADBLB86": 8029,
  "ADBLB87": 8030,
  "MBJC": 8031,
  "BNHC": 8032,
  "GBBD85": 8033,
  "ENL": 8034,
  "RULB": 8036,
  "JALPA": 8038,
  "NESDO": 8041,
  "CBLD88": 8043,
  "EBLD86": 8044,
  "GVL": 8045,
  "BHL": 8055,
  "ULBSL": 8063,
  "CYCL": 8065,
  "RFPL": 8066,
  "CCBD88": 8068,
  "DORDI": 8070,
  "ADLB": 8071,
  "NICFC": 8073,
  "KDBY": 8074,
  "BHDC": 8075,
  "HHL": 8076,
  "PBD88": 8097,
  "SBLD89": 8098,
  "UHEWA": 8099,
  "SGHC": 8100,
  "MHL": 8102,
  "USHEC": 8104,
  "NMBUR93/94": 8105,
  "GIBF1": 8106,
  "RHGCL": 8108,
  "SBD89": 8109,
  "SBID83": 8110,
  "PBD84": 8116,
  "AVYAN": 8117,
  "EBLD85": 8119,
  "SPHL": 8121,
  "PPL": 8122,
  "DLBS": 8123,
  "NSIF2": 8125,
  "SIKLES": 8126,
  "KBLD89": 8127,
  "KLBS": 8128,
  "EHPL": 8131,
  "SHLB": 8132,
  "PHCL": 8133,
  "BHPL": 9135,
  "BOKD86KA": 9136,
  "HBLD86": 9137,
  "NIBLGF": 9138,
  "SAGF": 9139,
  "UNLB": 9140,
  "NIFRAUR85/86": 9141,
  "SMHL": 9146,
  "SPL": 9147,
  "SMH": 9148,
  "MKHC": 9149,
  "AHL": 9150,
  "KDL": 9151,
  "EBLEB89": 9152,
  "SFEF": 9154,
  "TAMOR": 9156,
  "MHCL": 9158,
  "SMJC": 9159,
  "ANLB": 9161,
  "BPW": 9163,
  "MAKAR": 9166,
  "MKHL": 9167,
  "GBILD84/85": 9168,
  "DOLTI": 9170,
  "BEDC": 9171,
  "CITY": 9173,
  "PRSF": 9174,
  "MCHL": 9175,
  "IHL": 9176,
  "SCBD": 9177,
  "RMF2": 9178,
  "MEL": 9179,
  "NMBD89/90": 9180,
  "RAWA": 9181,
  "SIGS3": 9182,
  "NRM": 9183,
  "ILI": 9184,
  "C30MF": 9191,
  "USHL": 9192,
  "GCIL": 9193,
  "TSHL": 9194,
  "MLBLD89": 9195,
  "KBSH": 9196,
  "LBBLD89": 9197,
  "LVF2": 9198,
  "RNLI": 9199,
  "SNLI": 9201,
  "MEHL": 9203,
  "ULHC": 9208,
  "CLI": 9209,
  "SBID89": 9211,
  "MANDU": 9212,
  "HATHY": 9213,
  "BGWT": 9214,
  "MSHL": 9215,
  "SONA": 9216,
  "MMKJL": 9217,
  "TVCL": 9218,
  "KBLD90": 9220,
  "H8020": 9221,
  "VLUCL": 9225,
  "MKCL": 9230,
  "CIZBD90": 9231,
  "CKHL": 9232,
  "NWCL": 9233,
  "HRL": 9234,
  "NICGF2": 9236,
  "NABILD87": 9238,
  "KSY": 9241,
  "SARBTM": 9242,
  "NIMBD90": 9243,
  "NIBLSTF": 9244,
  "MNMF1": 9245,
  "GMLI": 9246,
  "GSY": 9248,
  "ICFCD88": 9249,
  "NMIC": 9250,
  "CREST": 9252,
  "NMBHF2": 9254,
  "EBLD91": 9255,
  "OMPL": 9256,
  "MBLEF": 9257,
  "PURE": 9258,
  "RSY": 9259,
  "NIFRAGED": 9261,
  "TTL": 9262,
  "SANVI": 9263,
  "RBBD2088": 9264,
  "NICAD2091": 9266,
  "BHCL": 9267,
  "GBIMESY2": 9269,
  "HIMSTAR": 9270,
  "SBLD2091": 9271
}
```

---

### getSecurityIDKeyMap
- **Return Type**: dict
- **Total Items**: 529
- **Sample Data**:
```json
{
  "USHL": 9192,
  "ACLBSL": 2790,
  "ACLBSLP": 2791,
  "ANLB": 9161,
  "ANLBP": 9164,
  "ADBL": 397,
  "ADBLD83": 2886,
  "ADBLB": 4960,
  "ADBLB86": 8029,
  "ADBLB87": 8030,
  "AKJCL": 2788,
  "API": 697,
  "AKPL": 2757,
  "AHPC": 360,
  "AVU": 211,
  "ALBSL": 2807,
  "ALBSLP": 2808,
  "AHL": 9150,
  "ALICLP": 599,
  "ALICL": 385,
  "AVYAN": 8117,
  "AVYANP": 8120,
  "BHL": 8055,
  "BOKD86": 4961,
  "BOKD86KA": 9136,
  "BHPL": 9135,
  "BARUN": 686,
  "BFC": 227,
  "BFCPO": 339,
  "BGWT": 9214,
  "BEDC": 9171,
  "BHCL": 9267,
  "BHDC": 8075,
  "BSL": 217,
  "BBC": 156,
  "BNL": 195,
  "BNT": 213,
  "BNHC": 8032,
  "BPCL": 153,
  "BSM": 205,
  "CMB": 259,
  "CMF2": 2862,
  "CHDC": 3946,
  "CFCL": 245,
  "CFCLPO": 676,
  "CCBD88": 8068,
  "CGH": 2917,
  "CBBLPO": 698,
  "CBBL": 164,
  "CHL": 2766,
  "CHCL": 154,
  "CKHL": 9232,
  "CIT": 210,
  "CITPO": 9219,
  "CLI": 9209,
  "CLIP": 9210,
  "C30MF": 9191,
  "CIZBD90": 9231,
  "CZBILP": 493,
  "CZBIL": 348,
  "CIZBD86": 2889,
  "CITY": 9173,
  "CBLD88": 8043,
  "PSDBLP": 387,
  "CORBL": 450,
  "CORBLP": 2763,
  "CREST": 9252,
  "CRESTP": 9253,
  "CFL": 361,
  "CYCL": 8065,
  "CYCLP": 8067,
  "DDBL": 166,
  "DDBLPO": 607,
  "DLBS": 8123,
  "DHPL": 2754,
  "DOLTI": 9170,
  "DORDI": 8070,
  "EHPL": 8131,
  "ENL": 8034,
  "EBL": 137,
  "EBLPO": 594,
  "EBLD85": 8119,
  "EBLEB89": 9152,
  "EBLD86": 8044,
  "EBLD91": 9255,
  "EDBLPO": 612,
  "EDBL": 274,
  "FMDBL": 490,
  "FMDBLP": 722,
  "FHL": 228,
  "FOWAD": 2758,
  "FOWADP": 2921,
  "GMFBS": 2815,
  "GMFBSP": 2818,
  "GBBL": 417,
  "GBBLPO": 623,
  "GSY": 9248,
  "GBBD85": 8033,
  "GHL": 2806,
  "GCIL": 9193,
  "GIBF1": 8106,
  "GBIME": 341,
  "GBIMEP": 511,
  "GBIMESY2": 9269,
  "GBILD86/87": 8004,
  "GBILD84/85": 9168,
  "GILBPO": 731,
  "GILB": 705,
  "GFCL": 232,
  "GFCLPO": 355,
  "GWFD83": 2883,
  "GRU": 207,
  "GBLBS": 583,
  "PDBLPO": 346,
  "GBLBSP": 712,
  "GRDBL": 2744,
  "GRDBLP": 2745,
  "GVL": 8045,
  "GLH": 2924,
  "GMLI": 9246,
  "GMLIP": 9247,
  "GMFIL": 263,
  "GMFILP": 613,
  "GLBSL": 2826,
  "GUFL": 204,
  "GUFLPO": 315,
  "HBT": 215,
  "HATHY": 9213,
  "HDHPC": 2880,
  "HURJA": 2824,
  "HBLD86": 9137,
  "H8020": 9221,
  "HBLD83": 2873,
  "HBL": 134,
  "HBLPO": 564,
  "HDL": 235,
  "HEI": 179,
  "HEIP": 700,
  "HFL": 441,
  "HHL": 8076,
  "HLBSL": 693,
  "HLBSLP": 725,
  "HLI": 393,
  "HLIPO": 701,
  "HPPL": 2767,
  "HRL": 9234,
  "HRLP": 9235,
  "HIMSTAR": 9270,
  "HIDCL": 2742,
  "HIDCLP": 8111,
  "ILI": 9184,
  "ILIP": 9185,
  "ICFC": 273,
  "ICFCPO": 400,
  "ICFCD83": 2882,
  "ICFCD88": 9249,
  "IGIPO": 635,
  "IGI": 186,
  "ILBS": 2832,
  "ILBSP": 2833,
  "IHL": 9176,
  "JFL": 250,
  "JFLPO": 292,
  "JSLBB": 695,
  "JSLBBP": 719,
  "JBLBP": 4950,
  "JBLB": 4951,
  "JOSHI": 2789,
  "JBBD87": 8020,
  "JBBLPO": 579,
  "JBBL": 418,
  "JSM": 209,
  "KMCDB": 593,
  "KMCDBP": 678,
  "KPCL": 2787,
  "KDL": 9151,
  "KDLP": 9153,
  "KSBBLP": 677,
  "KSBBL": 459,
  "KSBBLD87": 4948,
  "KRBL": 428,
  "KRBLPO": 1739,
  "KKHC": 2751,
  "KEF": 2933,
  "KBLD86": 2885,
  "KBLPO": 283,
  "KBL": 142,
  "KBLD89": 8127,
  "KDBY": 8074,
  "KBLD90": 9220,
  "KSY": 9241,
  "KBSH": 9196,
  "LUK": 2902,
  "LLBSPO": 644,
  "LLBS": 618,
  "LBLD88": 5984,
  "LVF2": 9198,
  "LSL": 141,
  "LSLPO": 286,
  "SFMF": 2877,
  "LBLD86": 2879,
  "LEC": 2903,
  "LICN": 188,
  "LICNPO": 696,
  "LBBLD89": 9197,
  "LBBL": 358,
  "LBBLPO": 626,
  "MBLD2085": 2866,
  "MBLPO": 281,
  "MBL": 140,
  "MBLEF": 9257,
  "MBLD87": 7985,
  "MBJC": 8031,
  "MLBLD89": 9195,
  "MLBL": 401,
  "MLBLPO": 620,
  "MDBLPO": 291,
  "MLBSL": 2925,
  "MLBSLP": 2926,
  "MSLB": 2768,
  "MSLBP": 2928,
  "MKHL": 9167,
  "MKJC": 8005,
  "MAKAR": 9166,
  "MEHL": 9203,
  "MHL": 8102,
  "MANDU": 9212,
  "MFILPO": 730,
  "MFLD85": 2932,
  "MFIL": 516,
  "MLBS": 8018,
  "MLBSP": 8019,
  "MMKJL": 9217,
  "MATRIP": 733,
  "MATRI": 694,
  "MKHC": 9149,
  "MMF1": 8023,
  "MCHL": 9175,
  "MERO": 1741,
  "MEROPO": 1742,
  "MSHL": 9215,
  "MDB": 371,
  "MDBPO": 609,
  "MLBBLP": 707,
  "MLBBL": 601,
  "MEL": 9179,
  "MHCL": 9158,
  "MEN": 2913,
  "MHNL": 2811,
  "MND84/85": 4969,
  "MNMF1": 9245,
  "MNBBL": 474,
  "MNBBLP": 640,
  "MKCL": 9230,
  "MPFL": 471,
  "MPFLPO": 1737,
  "NABIL": 131,
  "NABILP": 282,
  "NBF2": 2835,
  "NBLD82": 2892,
  "NBF3": 8024,
  "NBLD85": 8027,
  "NABILD87": 9238,
  "NADEP": 2784,
  "NADEPP": 2785,
  "NABBCP": 8037,
  "NABBC": 172,
  "NMFBS": 2746,
  "NMFBSP": 2747,
  "NHPC": 152,
  "NLICLP": 582,
  "NLICL": 178,
  "NIL": 183,
  "NILPO": 615,
  "NBBD2085": 2854,
  "NBL": 517,
  "NBLP": 9239,
  "NBLD87": 4959,
  "NBBU": 233,
  "NCCD86": 2936,
  "NTC": 307,
  "NFD": 151,
  "NFSPO": 651,
  "NFS": 194,
  "NHDL": 2769,
  "NIFRA": 2919,
  "NIFRAP": 2920,
  "NIFRAGED": 9261,
  "NIFRAUR85/86": 9141,
  "NICL": 176,
  "NICLPO": 689,
  "NIMBD90": 9243,
  "NIBLSTF": 9244,
  "NIBSF2": 4949,
  "NIBD84": 2931,
  "NIBD2082": 2851,
  "NIMB": 132,
  "NIMBPO": 469,
  "NKU": 222,
  "NLIC": 187,
  "NLICP": 589,
  "NLO": 198,
  "NMIC": 9250,
  "NMICP": 9251,
  "NRIC": 2881,
  "NRICP": 2884,
  "NRM": 9183,
  "SBI": 135,
  "SBIPO": 347,
  "SBIBD86": 2890,
  "SBID89": 9211,
  "SBID83": 8110,
  "NSM": 200,
  "NSMPO": 313,
  "NTL": 158,
  "NVG": 201,
  "NWCL": 9233,
  "NWC": 159,
  "NMLBBLP": 661,
  "NMLBBL": 396,
  "NESDO": 8041,
  "NESDOP": 8042,
  "NGPL": 2743,
  "NIBLGF": 9138,
  "NICD88": 7986,
  "NICFC": 8073,
  "NICAD2091": 9266,
  "NICGF2": 9236,
  "NICA": 139,
  "NICAP": 309,
  "NICD83/84": 2868,
  "NICAD85/86": 2825,
  "NICBF": 2863,
  "NICSF": 4967,
  "NICLBSL": 2887,
  "NICLBSLP": 2888,
  "NUBL": 163,
  "NUBLPO": 672,
  "NLGPO": 684,
  "NLG": 559,
  "NMBMF": 704,
  "NMBMFP": 723,
  "NMBPO": 391,
  "NMB": 238,
  "NMBD2085": 2850,
  "NMBHF2": 9254,
  "NMBUR93/94": 8105,
  "NMBD87/88": 4963,
  "NMBEB92/93": 4964,
  "NMBD89/90": 9180,
  "NSIF2": 8125,
  "NMB50": 2867,
  "NRN": 2898,
  "NYADI": 8026,
  "OMPL": 9256,
  "OHL": 149,
  "PMHPL": 2786,
  "PPCL": 2813,
  "PHCL": 8133,
  "PPL": 8122,
  "PFL": 236,
  "PFLPO": 390,
  "PRVU": 255,
  "PRFLPO": 488,
  "PRVUPO": 632,
  "PBLD86": 2875,
  "PBLD84": 2904,
  "PBLD87": 4962,
  "PSF": 4947,
  "PRSF": 9174,
  "PRINPO": 590,
  "PRIN": 184,
  "PMLI": 2915,
  "PMLIP": 9237,
  "PCBLP": 544,
  "PCBL": 357,
  "PBD84": 8116,
  "PBD85": 6984,
  "PBD88": 8097,
  "PROFL": 338,
  "PROFLP": 354,
  "PURE": 9258,
  "RADHI": 2776,
  "RJM": 203,
  "RHGCL": 8108,
  "RBBD83": 8003,
  "RBBD2088": 9264,
  "RBCL": 177,
  "RBCLPO": 634,
  "RHPL": 2841,
  "RAWA": 9181,
  "RMF1": 4968,
  "RMF2": 9178,
  "RSY": 9259,
  "RNLI": 9199,
  "RNLIP": 9200,
  "RLFLPO": 650,
  "RLFL": 587,
  "RIDI": 610,
  "RFPL": 8066,
  "RSDC": 2748,
  "RSDCP": 2749,
  "RURU": 2935,
  "SABSLPO": 2844,
  "SMJC": 9159,
  "SALICO": 185,
  "SALICOPO": 619,
  "SAHAS": 8021,
  "STC": 155,
  "SAMAJ": 4965,
  "SAMAJP": 4966,
  "SMATA": 2761,
  "SMATAP": 2762,
  "SFC": 221,
  "SPC": 8025,
  "SMPDA": 2896,
  "SMPDAP": 2897,
  "SFCL": 256,
  "SFCLP": 298,
  "SLBSL": 2804,
  "SLBSLPO": 2805,
  "SKBBL": 574,
  "SKBBLP": 671,
  "SNMAPO": 362,
  "SANIMA": 171,
  "SAND2085": 2828,
  "SBD87": 2922,
  "SLCF": 2923,
  "SBD89": 8109,
  "SGIC": 2908,
  "SGICP": 2909,
  "SAGF": 9139,
  "SHPC": 591,
  "TAMOR": 9156,
  "SRLI": 5982,
  "SRLIP": 5983,
  "SJCL": 2842,
  "SANVI": 9263,
  "SAPDBL": 2860,
  "SAPDBLP": 2861,
  "SARBTM": 9242,
  "SPHL": 8121,
  "SADBLP": 708,
  "SADBL": 472,
  "SDBD87": 6985,
  "SICL": 192,
  "SICLPO": 606,
  "SHINEP": 669,
  "SHINE": 473,
  "SSHL": 2907,
  "SHIVM": 2809,
  "SBPP": 226,
  "SIFC": 244,
  "SIFCPO": 456,
  "SRS": 230,
  "SHLB": 8132,
  "SHLBP": 8134,
  "SPL": 9147,
  "SBLD89": 8098,
  "SIGS3": 9182,
  "SBLD2091": 9271,
  "SBL": 145,
  "SEOS": 616,
  "SBLPO": 449,
  "SBLD83": 2864,
  "SBLD84": 2912,
  "SBLD2082": 2872,
  "SIGS2": 2859,
  "SEF": 2770,
  "SPIL": 182,
  "SPILPO": 713,
  "SIKLES": 8126,
  "SINDU": 561,
  "SINDUP": 652,
  "SHEL": 2934,
  "SHL": 147,
  "SONA": 9216,
  "SCB": 133,
  "SCBPO": 655,
  "SCBD": 9177,
  "SNLI": 9201,
  "SNLIP": 9202,
  "SRBLD83": 2878,
  "SBCF": 2937,
  "SFEF": 9154,
  "SMHL": 9146,
  "SMH": 9148,
  "SMB": 2771,
  "SMBPO": 2772,
  "SJLICP": 581,
  "SJLIC": 403,
  "SWMF": 706,
  "SWMFPO": 720,
  "SWBBL": 268,
  "SWBBLP": 314,
  "SMFBS": 2829,
  "SMFBSP": 2830,
  "SLBBL": 545,
  "SLBBLP": 721,
  "SGHC": 8100,
  "SPDL": 2759,
  "TRH": 148,
  "TPC": 8022,
  "TSHL": 9194,
  "TTL": 9262,
  "TVCL": 9218,
  "UNL": 219,
  "UNHPL": 2831,
  "UNLB": 9140,
  "UNLBP": 9142,
  "UAILPO": 726,
  "UAIL": 180,
  "UMRH": 2914,
  "UMHL": 2760,
  "UPCL": 2810,
  "USLB": 2774,
  "USLBP": 2775,
  "ULBSL": 8063,
  "ULBSLPO": 8064,
  "UHEWA": 8099,
  "ULHC": 9208,
  "USHEC": 8104,
  "UPPER": 2792,
  "VLBS": 687,
  "VLBSPO": 716,
  "VLUCL": 9225,
  "WNLB": 2781,
  "WNLBP": 2782,
  "YHL": 146
}
```

---

