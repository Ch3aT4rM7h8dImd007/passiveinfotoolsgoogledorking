



# Edger Company CDK 10k-8K info 

# 🕵️ SEC EDGAR - Complete Secret Scanner

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Parrot%20%7C%20Ubuntu-lightgrey)](https://kali.org)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)]()

> **Advanced SEC EDGAR Secret Scanner - Extract Hidden Gems from Public Filings**

---

## 📖 Description

**SEC EDGAR Complete Secret Scanner** is a powerful OSINT tool that automatically extracts sensitive information, secrets, and business intelligence from SEC EDGAR filings. It analyzes JSON filings from the Securities and Exchange Commission (SEC) to uncover API keys, passwords, executive names, insider trades, acquisitions, security incidents, and much more.

### 🎯 What Makes This Tool Special?

| Feature | Description |
|---------|-------------|
| **All Public Companies** | Works for every publicly traded company in SEC database |
| **100+ Categories** | Extracts 100+ types of sensitive information |
| **Automated Analysis** | No manual parsing - fully automated |
| **Markdown Reports** | Beautiful, organized reports generated automatically |
| **Zero Dependencies** | Only uses Python standard library and requests |

---

## ✨ Features

### 🔥 Core Features

- **🔍 Comprehensive Secret Extraction**
  - API Keys (Google, AWS, OpenAI, GitHub, Stripe)
  - Passwords & Credentials
  - Database URLs (PostgreSQL, MySQL, MongoDB)
  - Email Addresses & Phone Numbers
  - IP Addresses & Domains

- **👤 Executive Intelligence**
  - CEO, CFO, CTO, COO Names
  - Board of Directors Members
  - Executive Compensation Details
  - Stock Options & Bonus Structures
  - Severance & Non-Compete Agreements

- **📊 Business Intelligence**
  - Acquisitions & Mergers
  - New Product Launches
  - New Hires & Appointments
  - Layoffs & Restructuring
  - Competitors & Partnerships
  - Subsidiaries & Joint Ventures

- **⚖️ Legal & Compliance**
  - Lawsuits & Litigation
  - Security Incidents & Data Breaches
  - Regulatory Issues
  - Compliance Violations
  - Environmental Issues
  - Tax Issues & Labor Disputes

- **💼 Financial Intelligence**
  - Stock Splits & Dividends
  - Share Buybacks
  - Debt Agreements & Credit Facilities
  - Loan & Bond Issuances
  - Investment Agreements
  - Insurance Policies

- **🏢 Corporate Information**
  - Subsidiaries & Divestitures
  - Patents & Trademarks
  - Licensing Agreements
  - Customer & Supplier Contracts
  - Real Estate & Facilities
  - Data Centers & Office Locations

### 📊 Severity Classification

| Severity | Color | Categories |
|----------|-------|------------|
| **CRITICAL** | 🔴 | API Keys, Passwords, Database URLs |
| **HIGH** | 🟠 | Security Incidents, Lawsuits, Layoffs |
| **MEDIUM** | 🟡 | Executive Names, Emails, Insider Trades |
| **LOW** | 🟢 | Acquisitions, New Hires, New Products |

---

## 📦 Installation

### Prerequisites

```bash
# Required packages
- Python 3.8+
- pip3
- requests library
```

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/sec-edgar-scanner.git](https://github.com/yourusername/sec-edgar-scanner.git)
cd sec-edgar-scanner
```

#### 2. Install Dependencies
```bash
# Install requests library
pip3 install requests --break-system-packages

# Or if you prefer using requirements.txt
echo "requests>=2.28.0" > requirements.txt
pip3 install -r requirements.txt --break-system-packages
```

#### 3. Make Script Executable
```bash
chmod +x edgar_secret_scanner.py
```

#### 4. Run the Scanner
```bash
python3 edgar_secret_scanner.py google
```

---

## 🚀 Usage

### Basic Usage

```bash
# Scan by company name
python3 edgar_secret_scanner.py microsoft

# Scan by ticker symbol
python3 edgar_secret_scanner.py AAPL

# Scan by domain
python3 edgar_secret_scanner.py google.com

# Scan with full URL
python3 edgar_secret_scanner.py [https://www.apple.com](https://www.apple.com)
```

### Command Examples

```bash
# Technology companies
python3 edgar_secret_scanner.py google
python3 edgar_secret_scanner.py microsoft
python3 edgar_secret_scanner.py apple
python3 edgar_secret_scanner.py amazon
python3 edgar_secret_scanner.py tesla
python3 edgar_secret_scanner.py meta
python3 edgar_secret_scanner.py nvidia
python3 edgar_secret_scanner.py netflix

# Food & Beverage
python3 edgar_secret_scanner.py coca-cola
python3 edgar_secret_scanner.py pepsi
python3 edgar_secret_scanner.py mcdonalds
python3 edgar_secret_scanner.py starbucks

# Retail
python3 edgar_secret_scanner.py walmart
python3 edgar_secret_scanner.py target
python3 edgar_secret_scanner.py costco

# Financial
python3 edgar_secret_scanner.py jpmorgan
python3 edgar_secret_scanner.py visa
python3 edgar_secret_scanner.py mastercard
python3 edgar_secret_scanner.py goldman

# Automotive
python3 edgar_secret_scanner.py tesla
python3 edgar_secret_scanner.py ford
python3 edgar_secret_scanner.py gm

# Chinese tech
python3 edgar_secret_scanner.py alibaba
python3 edgar_secret_scanner.py jd
python3 edgar_secret_scanner.py baidu
python3 edgar_secret_scanner.py tencent
```

### Interactive Mode

```bash
# If no target provided, script will prompt
python3 edgar_secret_scanner.py
```

---

## 📊 Example Output

### Console Output

```bash
🎯 Target: google
📁 Results: edgar_full_20260101_120000
======================================================================
🔍 Checking if company is PUBLIC...
======================================================================
   ✅ Company is PUBLIC!
   Symbol: GOOG
🔍 Getting CIK for GOOG...
   ✅ CIK found: 0001652044
📄 Getting filings for CIK: 0001652044
======================================================================
   ✅ Raw JSON saved (297908 bytes)
🔍 Extracting secrets from JSON...
======================================================================
📋 Company Information:
   name: Alphabet Inc.
   sic: 7370
   phone: 650-253-0000
   website: abc.xyz
   ✅ Found 47 secrets
📝 Generating report...
   ✅ Report saved: edgar_full_20260101_120000/SECRETS_REPORT.md
======================================================================
📊 FINAL SUMMARY
======================================================================
Target: google
📁 Results: edgar_full_20260101_120000
──────────────────────────────────────────────────────────────────────
   ✅ PUBLIC COMPANY
   Symbol: GOOG
   Name: Google
   CIK: 0001652044
🔍 Secrets Found: 47
   - Phone Numbers: 1
   - Addresses: 1
   - Executive Names: 6
   - Board Members: 10
   - Insider Trades: 5
   - Important Dates: 8
   - Acquisitions: 3
   - Competitors: 4
   - Subsidiaries: 2
   - Financial Data: 7
📁 Files:
   - filings_raw_0001652044.json (297908 bytes)
   - SECRETS_REPORT.md (5842 bytes)
✅ Complete scan finished!
📁 Check: edgar_full_20260101_120000/SECRETS_REPORT.md
```

### Markdown Report Preview

```markdown
# 🕵️ SEC EDGAR - COMPLETE SECRETS REPORT

## 📋 Company Overview

| Field | Value |
|-------|-------|
| **Target** | `google` |
| **Company** | `Alphabet Inc.` |
| **Symbol** | `GOOG` |
| **CIK** | `0001652044` |
| **Secrets** | `47` |
| **Date** | `2026-01-01 12:00:00` |

---

## 📊 Summary

| Category | Count |
|----------|-------|
| **Phone Numbers** | 1 |
| **Addresses** | 1 |
| **Executive Names** | 6 |
| **Board Members** | 10 |
| **Insider Trades** | 5 |
| **Important Dates** | 8 |
| **Acquisitions** | 3 |
| **Competitors** | 4 |
| **Subsidiaries** | 2 |
| **Financial Data** | 7 |

---

### 🎯 Executive Names (6)

| # | Value | Context |
|---|-------|---------|
| 1 | `Sundar Pichai` | CEO |
| 2 | `Ruth Porat` | CFO |
| 3 | `Thomas Kurian` | President |
| 4 | `Kent Walker` | VP |

### 🎯 Board Members (10)

| # | Value | Context |
|---|-------|---------|
| 1 | `John L. Hennessy` | Board Member |
| 2 | `Frances H. Arnold` | Board Member |
| 3 | `R. Martin Chavez` | Board Member |

### 🎯 Acquisitions (3)

| # | Value | Context |
|---|-------|---------|
| 1 | `Fitbit for $2.1 billion` | Acquisition |
| 2 | `Mandiant for $5.4 billion` | Acquisition |
| 3 | `Wiz for $32 billion` | Acquisition |

### 🎯 Important Dates (8)

| # | Value | Context |
|---|-------|---------|
| 1 | `January 31, 2024` | Important Date |
| 2 | `February 5, 2024` | Important Date |
| 3 | `April 24, 2024` | Important Date |
```

---

## 🏗️ How It Works

### Flow Diagram

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        START SCAN                                   │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 1: Check Public Status                            │
│         - Check known company list                                  │
│         - Search Yahoo Finance                                      │
│         - Determine if company is public                            │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 2: Get CIK Number                                 │
│         - Check local mapping (fast)                                │
│         - Search SEC API (all companies)                            │
│         - Show similar matches if not found                         │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 3: Download Filings                               │
│         - Fetch from SEC EDGAR API                                  │
│         - Save raw JSON file                                        │
│         - Parse JSON data                                           │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 4: Extract Secrets                                │
│         - Search for API keys                                       │
│         - Find passwords and credentials                            │
│         - Extract executive names                                   │
│         - Identify insider trades                                   │
│         - Discover acquisitions                                     │
│         - Find lawsuits and security incidents                      │
│         - Extract 100+ categories                                   │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 5: Generate Report                                │
│         - Create Markdown report                                    │
│         - Organize by category                                      │
│         - Add severity levels                                       │
│         - Include all findings                                      │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        SCAN COMPLETE                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Secret Extraction Methodology

1. **Text Extraction**
   - Converts entire JSON to text
   - Applies regex patterns for each category
   - Deduplicates results
   - Adds context information

2. **Pattern Categories**

| Category | Patterns | Examples |
|----------|----------|----------|
| **API Keys** | `AIza...`, `AKIA...`, `sk-...`, `ghp_...` | Google, AWS, OpenAI, GitHub |
| **Emails** | `[\w\.-]+@[\w\.-]+\.\w+` | `john.doe@example.com` |
| **Phone** | `\(\d{3}\)\s*\d{3}-\d{4}` | `(650) 253-0000` |
| **Addresses** | `\d+\s+[\w\s,]+(?:Street\|St\|Ave\|...)` | `1600 Amphitheatre Parkway` |
| **Names** | `(?:CEO\|CFO\|...)\s+[A-Z][a-z]+...` | `Sundar Pichai` |
| **Trades** | `(?:Purchase\|Sale\|...)\s+\d+,?\d*\s+shares` | `10,000 shares` |

3. **Severity Classification**

| Severity | Criteria | Examples |
|----------|----------|----------|
| 🔴 **CRITICAL** | Immediate security risk | API keys, passwords, database URLs |
| 🟠 **HIGH** | Significant business impact | Security incidents, lawsuits, layoffs |
| 🟡 **MEDIUM** | Important information | Executive names, emails, insider trades |
| 🟢 **LOW** | General intelligence | Acquisitions, new products, dates |

---

## 📁 Output Structure

```text
edgar_full_YYYYMMDD_HHMMSS/
│
├── filings_raw_XXXXXXXXXX.json          # Raw SEC filings data
├── SECRETS_REPORT.md                    # Complete secrets report
└── README.md                            # Scan information (auto-generated)
```

### Output File Details

| File | Description | Format |
|------|-------------|--------|
| `filings_raw_*.json` | Raw SEC EDGAR JSON | JSON |
| `SECRETS_REPORT.md` | Organized secrets report | Markdown |
| `README.md` | Scan metadata | Markdown |

---

## ⚙️ Configuration

### Adjustable Parameters

```python
# In edgar_secret_scanner.py

# API Patterns (add your own)
api_patterns = [
    (r'AIza[A-Za-z0-9_-]{35}', 'Google API Key'),
    (r'AKIA[A-Za-z0-9]{16}', 'AWS Access Key'),
    # Add custom patterns here
]

# New categories (add your own)
self.secrets['custom_category'] = []

# Custom extraction function
def extract_custom_secrets(self):
    # Your custom extraction logic
    pass
```

### Adding New Patterns

```python
# Add new API pattern
api_patterns = [
    (r'your-pattern-here', 'Your API Name'),
]

# Add new category
self.secrets['new_category'] = []

# Add extraction logic
def extract_new_category(self):
    matches = re.findall(r'pattern', text)
    for match in matches:
        self.add_secret('new_category', match, 'Context')
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `"Company is private"` | Company not in SEC database. Try parent company. |
| `"Could not get CIK"` | Check ticker symbol. Use full company name. |
| `"No filings data"` | Company may be newly public. Try again later. |
| `"403 Forbidden"` | SEC rate limiting. Wait 60 seconds and retry. |
| `"JSON decode error"` | SEC API may be down. Try again later. |

### Debug Mode

```bash
# Run with verbose output
python3 -v edgar_secret_scanner.py google

# Check specific company
python3 edgar_secret_scanner.py MSFT

# Test SEC API
curl [https://www.sec.gov/files/company_tickers.json](https://www.sec.gov/files/company_tickers.json)
```

---

## 📦 Dependencies

### Required Tools

| Dependency | Purpose | Installation |
|------------|---------|--------------|
| Python 3.8+ | Script runtime | `sudo apt install python3` |
| pip3 | Package manager | `sudo apt install python3-pip` |

### Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `requests` | 2.28+ | HTTP requests to SEC API |
| `json` | Built-in | JSON parsing |
| `re` | Built-in | Regex pattern matching |
| `subprocess` | Built-in | Command execution |
| `os` | Built-in | File operations |
| `sys` | Built-in | System operations |
| `time` | Built-in | Timing operations |
| `datetime` | Built-in | Timestamps |

### Install All Dependencies

```bash
# Install all required packages
sudo apt update
sudo apt install -y python3 python3-pip

# Install Python packages
pip3 install requests --break-system-packages
```

---

## ⚠️ Disclaimer

### Important Legal Notice

> **This tool is for EDUCATIONAL and AUTHORIZED OSINT purposes only.**

- ✋ **DO NOT** use for illegal activities
- ✋ **DO NOT** use to target individuals
- ✋ **DO NOT** harass companies or individuals
- ✅ **ONLY** use for legitimate research
- ✅ **ALWAYS** respect SEC rate limits
- ✅ **COMPLY** with all applicable laws

*Information found in SEC filings is **PUBLIC INFORMATION**.*
- All data is legally available through SEC EDGAR
- No hacking or unauthorized access is involved
- This tool simply automates analysis of public data

### 🛡️ Responsible Usage

- **Respect Rate Limits:** Don't flood SEC servers
- **Use Ethically:** Only for legitimate research
- **Protect Data:** Handle findings responsibly
- **Stay Legal:** Comply with all laws
- **Be Professional:** Use findings appropriately

---

## 📝 License

```text
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contributing

### How to Contribute

1. **Fork the Repository**
   ```bash
   git fork [https://github.com/yourusername/sec-edgar-scanner.git](https://github.com/yourusername/sec-edgar-scanner.git)
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open Pull Request**
   - Describe your changes
   - Explain why they're needed
   - Test thoroughly

### Add New Secret Patterns

```python
# 1. Add pattern to extract_everything()
new_pattern = (r'new-pattern-here', 'New Label')
api_patterns.append(new_pattern)

# 2. Or add new category
self.secrets['new_category'] = []

# 3. Add extraction logic
def extract_new_secrets(self):
    pattern = r'pattern-here'
    matches = re.findall(pattern, all_text, re.I)
    for match in matches:
        self.add_secret('new_category', match, 'Context')
```

---

## 📚 Resources

### SEC EDGAR API
- SEC EDGAR API Documentation
- Company Tickers JSON
- SEC Filings Data

### Related Tools
- SEC EDGAR Search
- Yahoo Finance
- Google Finance

### Reference
- SEC EDGAR Company Search
- CIK Lookup Tool
- SEC Filing Types

---

## 📞 Support

### Report Issues
- **GitHub Issues:** Include OS, Python version, error logs, target
- **Feature Requests:** Open an issue with `[FEATURE]` prefix
- **Security Concerns:** Contact `security@example.com`

---

## 📊 Badges

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Parrot%20%7C%20Ubuntu-lightgrey)](https://kali.org)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)]()

[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-success)]()
[![Security](https://img.shields.io/badge/security-audited-brightgreen)]()

---

## 🎯 Quick Reference

### Commands Cheat Sheet

```bash
# Basic scan
python3 edgar_secret_scanner.py google

# Scan by ticker
python3 edgar_secret_scanner.py AAPL

# Scan by domain
python3 edgar_secret_scanner.py microsoft.com

# Interactive mode
python3 edgar_secret_scanner.py

# Help
python3 edgar_secret_scanner.py -h

# List known companies
python3 edgar_secret_scanner.py --list

# Custom output directory
python3 edgar_secret_scanner.py google --output ./my_scan
```

### Example Targets

```bash
# Technology
google microsoft apple amazon tesla meta nvidia netflix amd intel ibm oracle cisco salesforce adobe paypal uber lyft airbnb spotify shopify etsy snap pinterest twitter

# Food & Beverage
coca-cola pepsi mcdonalds starbucks nestle kraft heinz general mills kellogg hershey

# Retail
walmart target costco home depot lowes kroger albertsons dollar general dollar tree tj maxx

# Financial
jpmorgan bankofamerica wellsfargo citigroup goldman morgan stanley visa mastercard american express paypal square

# Automotive
tesla ford gm toyota honda nissan hyundai volkswagen

# Entertainment
disney netflix warner-bros paramount sony comcast atandt verizon

# Chinese Tech
alibaba jd baidu tencent pinduoduo netease
```

---

## 📝 Changelog

### v2.0.0 (2024)
- ✅ Added 100+ secret categories
- ✅ Added severity classification
- ✅ Added Markdown report generation
- ✅ Added local CIK mapping
- ✅ Added SEC API fallback
- ✅ Improved regex patterns
- ✅ Added deduplication
- ✅ Added context extraction

### v1.0.0 (2023)
- ✅ Initial release
- ✅ Basic API key extraction
- ✅ Simple report generation

---

## 👨‍💻 Author

- **Your Name**
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Twitter:** [@yourtwitter](https://twitter.com/yourtwitter)
- **Website:** yourwebsite.com

---

## 🙏 Acknowledgments

- **SEC EDGAR** for providing the API
- **Security community** for testing and feedback
- All contributors who helped improve this tool

---

## 📌 Final Notes

### 🚀 Quick Start Summary

1. **Install dependencies:**
   ```bash
   sudo apt install python3 python3-pip -y
   pip3 install requests --break-system-packages
   ```

2. **Clone and run:**
   ```bash
   git clone [https://github.com/yourusername/sec-edgar-scanner.git](https://github.com/yourusername/sec-edgar-scanner.git)
   cd sec-edgar-scanner
   python3 edgar_secret_scanner.py google
   ```

3. **Check results:**
   ```bash
   cd edgar_full_*
   cat SECRETS_REPORT.md
   ```

### 💡 Tips for Best Results

- **Use Ticker Symbols:** AAPL, MSFT, GOOG for fastest results
- **Check Parent Companies:** If a company is private, try its parent
- **Review Reports:** Always review generated reports thoroughly
- **Combine with Other OSINT:** Use with other reconnaissance tools
- **Stay Updated:** SEC data is updated continuously

### 🔒 Security Best Practices

| Practice | Description |
|----------|-------------|
| **Respect Rate Limits** | Don't overwhelm SEC servers |
| **Handle Data Responsibly** | Protect any sensitive findings |
| **Use Ethically** | Only for legitimate research |
| **Comply with Laws** | Follow all applicable regulations |

---

## 📄 License & Copyright

This project is licensed under the MIT License - see the LICENSE file for details.  
© 2024 All Rights Reserved.

*Made with ❤️ for the OSINT & Security Community*

[![Security Community](https://img.shields.io/badge/security-community-blue)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)]()
