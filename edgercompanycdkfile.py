#!/usr/bin/env python3
"""
SEC EDGAR - COMPLETE SECRET SCANNER (FIXED)
Works for ALL public companies
Extracts EVERYTHING from SEC filings
"""

import subprocess
import os
import sys
import time
import re
import json
import requests
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class EdgarFullScanner:
    def __init__(self, target):
        self.target = target
        self.clean_target = self.clean_name(target)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"edgar_full_{self.timestamp}"
        
        self.is_public = False
        self.stock_symbol = None
        self.company_name = None
        self.cik = None
        self.filings_data = None
        self.secret_count = 0
        
        # Complete secrets dictionary
        self.secrets = {
            'api_keys': [],
            'tokens': [],
            'passwords': [],
            'database_urls': [],
            'security_incidents': [],
            'lawsuits': [],
            'layoffs': [],
            'executive_names': [],
            'board_members': [],
            'insider_trades': [],
            'emails': [],
            'phone_numbers': [],
            'addresses': [],
            'ip_addresses': [],
            'domains': [],
            'acquisitions': [],
            'new_hires': [],
            'new_products': [],
            'competitors': [],
            'important_dates': [],
            'financial_data': [],
            'risk_factors': [],
            'subsidiaries': [],
            'partnerships': [],
            'facilities': [],
            'stock_splits': [],
            'dividends': [],
            'executive_compensation': [],
            'stock_options': [],
            'bonus_structures': [],
            'severance_agreements': [],
            'pension_plans': [],
            'employee_benefits': [],
            'regulatory_issues': [],
            'compliance_issues': [],
            'environmental_issues': [],
            'tax_issues': [],
            'labor_disputes': [],
            'product_recalls': [],
            'safety_incidents': [],
            'real_estate': [],
            'debt_agreements': [],
            'credit_facilities': [],
            'loan_agreements': [],
            'bond_issuances': [],
            'equity_financings': [],
            'investment_agreements': [],
            'insurance_policies': [],
            'corporate_governance': [],
            'social_responsibility': [],
            'divestitures': [],
            'patents': [],
            'trademarks': [],
            'licensing_agreements': [],
            'customer_contracts': [],
            'supplier_contracts': [],
            'data_centers': [],
            'office_locations': [],
            'share_buybacks': [],
            'joint_ventures': [],
            'mergers': [],
            'new_services': [],
        }
        
        os.makedirs(self.results_dir, exist_ok=True)

    def clean_name(self, name):
        name = re.sub(r'^https?://', '', name)
        name = re.sub(r'^www\.', '', name)
        name = name.split('/')[0]
        if '.' in name:
            parts = name.split('.')
            if len(parts) > 2:
                name = parts[-2]
            else:
                name = parts[0]
        return name

    def print_header(self, text):
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{text}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")

    def check_public_status(self):
        print(f"\n{Colors.CYAN}🔍 Checking if company is PUBLIC...{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
        
        known = {
            'google': 'GOOG', 'microsoft': 'MSFT', 'apple': 'AAPL',
            'amazon': 'AMZN', 'tesla': 'TSLA', 'meta': 'META',
            'nvidia': 'NVDA', 'netflix': 'NFLX', 'amd': 'AMD',
        }
        
        search_term = self.clean_target.lower()
        for company, symbol in known.items():
            if company in search_term or search_term in company:
                self.is_public = True
                self.stock_symbol = symbol
                self.company_name = company.title()
                print(f"{Colors.GREEN}   ✅ Company is PUBLIC!{Colors.RESET}")
                print(f"{Colors.BLUE}   Symbol: {symbol}{Colors.RESET}")
                return True
        
        try:
            url = f"https://query1.finance.yahoo.com/v1/finance/search?q={self.clean_target}"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('quotes', []):
                    if quote.get('typeDisp') == 'Equity' and quote.get('exchange'):
                        self.is_public = True
                        self.stock_symbol = quote.get('symbol')
                        self.company_name = quote.get('longname')
                        print(f"{Colors.GREEN}   ✅ Company is PUBLIC!{Colors.RESET}")
                        print(f"{Colors.BLUE}   Symbol: {self.stock_symbol}{Colors.RESET}")
                        return True
        except:
            pass
        
        print(f"{Colors.YELLOW}   ⚠️ Not found as public company{Colors.RESET}")
        return False

    def get_cik(self):
        print(f"\n{Colors.CYAN}🔍 Getting CIK for {self.stock_symbol}...{Colors.RESET}")
        
        ticker_to_cik = {
            'AAPL': '0000320193', 'MSFT': '0000789019',
            'GOOG': '0001652044', 'GOOGL': '0001652044',
            'AMZN': '0001018724', 'TSLA': '0001318605',
            'META': '0001326801', 'NVDA': '0001045810',
            'NFLX': '0001065280', 'AMD': '0000002488',
        }
        
        if self.stock_symbol.upper() in ticker_to_cik:
            self.cik = ticker_to_cik[self.stock_symbol.upper()]
            print(f"{Colors.GREEN}   ✅ CIK found: {self.cik}{Colors.RESET}")
            return True
        
        try:
            url = "https://www.sec.gov/files/company_tickers.json"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.values():
                    if item.get('ticker', '').upper() == self.stock_symbol.upper():
                        self.cik = str(item.get('cik_str', '')).zfill(10)
                        print(f"{Colors.GREEN}   ✅ CIK found via SEC: {self.cik}{Colors.RESET}")
                        return True
        except:
            pass
        
        print(f"{Colors.RED}   ❌ Could not find CIK{Colors.RESET}")
        return False

    def get_filings(self):
        if not self.cik:
            return False
        
        print(f"\n{Colors.CYAN}📄 Getting filings for CIK: {self.cik}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
        
        url = f"https://data.sec.gov/submissions/CIK{self.cik}.json"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                self.filings_data = response.json()
                
                with open(f"{self.results_dir}/filings_raw_{self.cik}.json", 'w') as f:
                    json.dump(self.filings_data, f, indent=2)
                print(f"{Colors.GREEN}   ✅ Raw JSON saved{Colors.RESET}")
                return True
        except Exception as e:
            print(f"{Colors.RED}   ❌ Error: {str(e)[:50]}{Colors.RESET}")
        
        return False

    def add_secret(self, category, value, context=""):
        if not value or len(str(value)) < 2:
            return
        
        for item in self.secrets[category]:
            if item.get('value') == value:
                return
        
        self.secrets[category].append({
            'value': str(value),
            'context': str(context)
        })

    def extract_everything(self):
        """Extract EVERYTHING from JSON"""
        print(f"\n{Colors.CYAN}🔍 Extracting secrets from JSON...{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
        
        if not self.filings_data:
            print(f"{Colors.RED}❌ No filings data{Colors.RESET}")
            return
        
        data = self.filings_data
        all_text = json.dumps(data, indent=2)
        
        # Company info
        print(f"\n{Colors.CYAN}📋 Company Information:{Colors.RESET}")
        company_info = {
            'name': data.get('name', 'N/A'),
            'sic': data.get('sic', 'N/A'),
            'phone': data.get('phone', 'N/A'),
            'website': data.get('website', 'N/A'),
        }
        for key, value in company_info.items():
            if value != 'N/A':
                print(f"{Colors.BLUE}   {key}: {value}{Colors.RESET}")

        # API Keys
        api_patterns = [
            (r'AIza[A-Za-z0-9_-]{35}', 'Google API Key'),
            (r'AKIA[A-Za-z0-9]{16}', 'AWS Access Key'),
            (r'sk-[A-Za-z0-9]{32,}', 'OpenAI Key'),
            (r'ghp_[A-Za-z0-9]{36}', 'GitHub Token'),
        ]
        for pattern, label in api_patterns:
            try:
                matches = re.findall(pattern, all_text)
                for match in matches:
                    if len(match) > 15:
                        self.add_secret('api_keys', match, label)
            except:
                pass

        # Passwords
        password_patterns = [
            (r'password[=:]\s*["\']?([A-Za-z0-9@#$%^&*!]{8,})["\']?', 'Password'),
            (r'secret[=:]\s*["\']?([A-Za-z0-9@#$%^&*!]{8,})["\']?', 'Secret'),
        ]
        for pattern, label in password_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    if len(match) > 5:
                        self.add_secret('passwords', match, label)
            except:
                pass

        # Emails
        email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
        try:
            matches = re.findall(email_pattern, all_text)
            for match in matches:
                if '@example' not in match and len(match) > 5:
                    self.add_secret('emails', match, 'Email')
        except:
            pass

        # Phone Numbers
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}',
            r'\+\d{1,3}\s*\d{3}\s*\d{3}\s*\d{4}',
        ]
        for pattern in phone_patterns:
            try:
                matches = re.findall(pattern, all_text)
                for match in matches:
                    self.add_secret('phone_numbers', match, 'Phone')
            except:
                pass

        # Addresses
        address_pattern = r'\d{1,5}\s+[A-Za-z0-9\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Parkway|Pkwy)'
        try:
            matches = re.findall(address_pattern, all_text, re.I)
            for match in matches:
                if len(match) > 20:
                    self.add_secret('addresses', match, 'Address')
        except:
            pass

        # Executive Names
        exec_patterns = [
            r'(?:CEO|CFO|CTO|COO|President|Chairman|Director|VP)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        for pattern in exec_patterns:
            try:
                matches = re.findall(pattern, all_text)
                for match in matches:
                    if len(match) > 5:
                        self.add_secret('executive_names', match, 'Executive')
            except:
                pass

        # Board Members
        board_pattern = r'(?:Board of Directors|Board Member|Director)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        try:
            matches = re.findall(board_pattern, all_text)
            for match in matches:
                if len(match) > 5:
                    self.add_secret('board_members', match, 'Board Member')
        except:
            pass

        # Insider Trades
        trade_patterns = [
            r'(?:Purchase|Sale|Acquired|Disposed)\s+(?:of\s+)?(\d+(?:,\d+)?)\s+(?:shares|stock)',
        ]
        for pattern in trade_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    self.add_secret('insider_trades', match, 'Insider Trade')
            except:
                pass

        # Acquisitions
        acq_patterns = [
            r'(?:acquired|purchased|buying|bought)\s+([A-Za-z0-9\s]+)\s+(?:for|at)\s+\$(\d+(?:,\d+)?(?:\.\d+)?)\s+(?:million|billion)',
        ]
        for pattern in acq_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    if len(str(match)) > 5:
                        self.add_secret('acquisitions', str(match), 'Acquisition')
            except:
                pass

        # Lawsuits
        lawsuit_patterns = [
            r'(?:lawsuit|litigation|legal proceeding|class action)\s+(?:against|involving)\s+([A-Za-z0-9\s,]+)',
        ]
        for pattern in lawsuit_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    if len(match) > 5:
                        self.add_secret('lawsuits', match, 'Lawsuit')
            except:
                pass

        # Security Incidents
        security_patterns = [
            r'(?:security|cyber|data)\s+(?:breach|incident)\s+(?:involving|affecting)\s+([A-Za-z0-9\s,]+)',
        ]
        for pattern in security_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    if len(match) > 5:
                        self.add_secret('security_incidents', match, 'Security Incident')
            except:
                pass

        # Layoffs
        layoff_patterns = [
            r'(?:layoff|downsizing|restructuring)\s+(?:of\s+)?(\d+(?:,\d+)?)\s+(?:employees|staff)',
        ]
        for pattern in layoff_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    self.add_secret('layoffs', match, 'Layoff')
            except:
                pass

        # New Hires
        hire_patterns = [
            r'(?:hired|appointed|new hire|joins)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+as\s+([A-Za-z\s]+)',
        ]
        for pattern in hire_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    if len(str(match)) > 3:
                        self.add_secret('new_hires', str(match), 'New Hire')
            except:
                pass

        # New Products
        product_patterns = [
            r'(?:launching|launched|introducing|introduced|new)\s+([A-Za-z0-9\s]+)\s+(?:product|service|platform)',
        ]
        for pattern in product_patterns:
            try:
                matches = re.findall(pattern, all_text, re.I)
                for match in matches:
                    if len(match) > 3:
                        self.add_secret('new_products', match, 'New Product')
            except:
                pass

        # Competitors
        comp_pattern = r'(?:competitors?|competition|rivals?)\s+(?:include|are|such as)\s+([A-Za-z0-9\s,]+)'
        try:
            matches = re.findall(comp_pattern, all_text, re.I)
            for match in matches:
                if len(match) > 5:
                    self.add_secret('competitors', match, 'Competitor')
        except:
            pass

        # Important Dates
        date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b'
        try:
            matches = re.findall(date_pattern, all_text)
            for match in matches:
                if match:
                    self.add_secret('important_dates', match, 'Important Date')
        except:
            pass

        # Count
        for key in self.secrets:
            self.secret_count += len(self.secrets[key])
        
        print(f"{Colors.GREEN}   ✅ Found {self.secret_count} secrets{Colors.RESET}")

    def generate_report(self):
        print(f"\n{Colors.CYAN}📝 Generating report...{Colors.RESET}")
        
        report_lines = []
        report_lines.append(f"# 🕵️ SEC EDGAR - COMPLETE SECRETS REPORT")
        report_lines.append(f"")
        report_lines.append(f"## 📋 Company Overview")
        report_lines.append(f"")
        report_lines.append(f"| Field | Value |")
        report_lines.append(f"|-------|-------|")
        report_lines.append(f"| **Target** | `{self.target}` |")
        report_lines.append(f"| **Company** | `{self.company_name}` |")
        report_lines.append(f"| **Symbol** | `{self.stock_symbol}` |")
        report_lines.append(f"| **CIK** | `{self.cik}` |")
        report_lines.append(f"| **Secrets** | `{self.secret_count}` |")
        report_lines.append(f"| **Date** | `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}` |")
        report_lines.append(f"")
        report_lines.append(f"---")
        report_lines.append(f"")
        
        # Summary
        report_lines.append(f"## 📊 Summary")
        report_lines.append(f"")
        report_lines.append(f"| Category | Count |")
        report_lines.append(f"|----------|-------|")
        for category, items in sorted(self.secrets.items(), key=lambda x: len(x[1]), reverse=True):
            if items:
                report_lines.append(f"| **{category.replace('_', ' ').title()}** | {len(items)} |")
        report_lines.append(f"")
        report_lines.append(f"---")
        report_lines.append(f"")
        
        # Details
        for category, items in sorted(self.secrets.items(), key=lambda x: len(x[1]), reverse=True):
            if items:
                report_lines.append(f"### 🎯 {category.replace('_', ' ').title()} ({len(items)})")
                report_lines.append(f"")
                report_lines.append(f"| # | Value | Context |")
                report_lines.append(f"|---|-------|---------|")
                for i, item in enumerate(items, 1):
                    report_lines.append(f"| {i} | `{item.get('value')}` | {item.get('context')} |")
                report_lines.append(f"")
        
        # Files
        report_lines.append(f"---")
        report_lines.append(f"")
        report_lines.append(f"## 📁 Generated Files")
        report_lines.append(f"")
        for file in os.listdir(self.results_dir):
            size = os.path.getsize(f"{self.results_dir}/{file}")
            report_lines.append(f"- `{file}` ({size} bytes)")
        
        report_content = "\n".join(report_lines)
        report_file = f"{self.results_dir}/SECRETS_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"{Colors.GREEN}   ✅ Report saved{Colors.RESET}")

    def print_summary(self):
        self.print_header("📊 FINAL SUMMARY")
        
        print(f"{Colors.CYAN}Target: {self.target}{Colors.RESET}")
        print(f"{Colors.CYAN}📁 Results: {self.results_dir}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'─'*70}{Colors.RESET}")
        
        if self.is_public:
            print(f"{Colors.GREEN}   ✅ PUBLIC COMPANY{Colors.RESET}")
            print(f"{Colors.BLUE}   Symbol: {self.stock_symbol}{Colors.RESET}")
            print(f"{Colors.BLUE}   Name: {self.company_name}{Colors.RESET}")
            if self.cik:
                print(f"{Colors.BLUE}   CIK: {self.cik}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}🔍 Secrets Found: {self.secret_count}{Colors.RESET}")
        for category, items in sorted(self.secrets.items(), key=lambda x: len(x[1]), reverse=True):
            if items:
                print(f"{Colors.BLUE}   - {category.replace('_', ' ').title()}: {len(items)}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}📁 Files:{Colors.RESET}")
        for file in sorted(os.listdir(self.results_dir)):
            size = os.path.getsize(f"{self.results_dir}/{file}")
            print(f"{Colors.BLUE}   - {file} ({size} bytes){Colors.RESET}")

    def run(self):
        print(f"""
{Colors.BOLD}{Colors.MAGENTA}
╔═══════════════════════════════════════════════════════════════════╗
║           SEC EDGAR - COMPLETE SECRET SCANNER                   ║
║           Works for ALL public companies                        ║
║           Extracts EVERYTHING from SEC filings                  ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
        """)

        print(f"{Colors.CYAN}🎯 Target: {self.target}{Colors.RESET}")
        print(f"{Colors.CYAN}📁 Results: {self.results_dir}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")

        if not self.check_public_status():
            print(f"\n{Colors.YELLOW}⚠️ Company is private. No SEC filings.{Colors.RESET}")
            return

        if not self.get_cik():
            print(f"\n{Colors.RED}❌ Could not get CIK. Exiting.{Colors.RESET}")
            return

        if not self.get_filings():
            print(f"\n{Colors.RED}❌ Could not get filings. Exiting.{Colors.RESET}")
            return

        # ============ FIX: এটা যোগ করতে হবে! ============
        self.extract_everything()
        # ==============================================

        self.generate_report()
        self.print_summary()
        
        print(f"\n{Colors.GREEN}✅ Complete scan finished!{Colors.RESET}")
        print(f"{Colors.CYAN}📁 Check: {self.results_dir}/SECRETS_REPORT.md{Colors.RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{Colors.YELLOW}Usage: python3 {sys.argv[0]} <company>{Colors.RESET}")
        print(f"{Colors.YELLOW}Example: python3 {sys.argv[0]} google{Colors.RESET}")
        print(f"{Colors.YELLOW}Example: python3 {sys.argv[0]} microsoft{Colors.RESET}")
        print(f"{Colors.YELLOW}Example: python3 {sys.argv[0]} apple{Colors.RESET}")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = EdgarFullScanner(target)
    scanner.run()

if __name__ == "__main__":
    main()