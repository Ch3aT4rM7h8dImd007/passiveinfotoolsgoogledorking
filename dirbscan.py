#!/usr/bin/env python3
"""
DIRB - Hybrid Scanner with SecLists Optimization
Quick Scan + Deep Scan + Verification
Uses modern SecLists wordlists
"""

import subprocess
import os
import sys
import re
import time
import json
import shutil
from datetime import datetime
from urllib.request import urlretrieve

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class DirbHybrid:
    def __init__(self, target):
        self.target = target
        self.clean_target = self.clean_url(target)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"dirb_hybrid_results_{self.timestamp}"
        self.found_items = []
        self.all_wordlists = []
        self.scan_count = 0
        self.total_found = 0
        self.quick_found = []
        self.deep_found = []
        self.verified = []
        self.verified_failed = []
        self.scan_results = {}
        self.wordlist_downloaded = []
        
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(f"{self.results_dir}/wordlists", exist_ok=True)
        os.makedirs(f"{self.results_dir}/quick_scan", exist_ok=True)
        os.makedirs(f"{self.results_dir}/deep_scan", exist_ok=True)
        print(f"{Colors.CYAN}📁 Results folder: {self.results_dir}{Colors.RESET}")

    def clean_url(self, url):
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0]
        return url

    def check_dirb(self):
        """DIRB ইনস্টল চেক"""
        print(f"\n{Colors.CYAN}📦 Checking DIRB...{Colors.RESET}")
        try:
            subprocess.run(['dirb', '-h'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{Colors.GREEN}✅ DIRB is installed{Colors.RESET}")
            return True
        except:
            print(f"{Colors.YELLOW}⚠️ Installing DIRB...{Colors.RESET}")
            subprocess.run("sudo apt install dirb -y", shell=True, check=False)
            try:
                subprocess.run(['dirb', '-h'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{Colors.GREEN}✅ DIRB installed successfully{Colors.RESET}")
                return True
            except:
                print(f"{Colors.RED}❌ DIRB installation failed{Colors.RESET}")
                return False

    def check_seclists(self):
        """SecLists ইনস্টল চেক এবং ডাউনলোড"""
        print(f"\n{Colors.CYAN}📦 Checking SecLists...{Colors.RESET}")
        
        # Check if SecLists exists
        seclists_paths = [
            "/usr/share/seclists",
            "/usr/share/wordlists/seclists",
            "/opt/seclists"
        ]
        
        seclists_found = False
        for path in seclists_paths:
            if os.path.exists(path):
                print(f"{Colors.GREEN}✅ SecLists found at: {path}{Colors.RESET}")
                seclists_found = True
                break
        
        if not seclists_found:
            print(f"{Colors.YELLOW}⚠️ SecLists not found. Installing...{Colors.RESET}")
            
            # Try apt install first
            try:
                print(f"{Colors.CYAN}📥 Installing SecLists via apt...{Colors.RESET}")
                result = subprocess.run("sudo apt install seclists -y", shell=True, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    print(f"{Colors.GREEN}✅ SecLists installed via apt{Colors.RESET}")
                    return True
            except:
                pass
            
            # If apt fails, download manually
            try:
                print(f"{Colors.CYAN}📥 Downloading SecLists from GitHub...{Colors.RESET}")
                subprocess.run("sudo rm -rf /usr/share/seclists", shell=True, check=False)
                clone_cmd = "sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists"
                result = subprocess.run(clone_cmd, shell=True, capture_output=True, text=True, timeout=600)
                if result.returncode == 0:
                    print(f"{Colors.GREEN}✅ SecLists downloaded from GitHub{Colors.RESET}")
                    return True
            except:
                pass
            
            # If still fails, download from local directory
            print(f"{Colors.YELLOW}⚠️ Creating fallback wordlists...{Colors.RESET}")
            self.create_fallback_wordlists()
            return False
        
        return True

    def create_fallback_wordlists(self):
        """ফলব্যাক ওয়ার্ডলিস্ট তৈরি"""
        fallback_dir = f"{self.results_dir}/wordlists"
        os.makedirs(fallback_dir, exist_ok=True)
        
        wordlists = {
            "common.txt": ["admin", "login", "test", "dev", "api", "blog", "shop", "backup", "old", "new"],
            "medium.txt": ["admin", "login", "test", "dev", "api", "blog", "shop", "backup", "old", "new",
                          "images", "css", "js", "files", "download", "upload", "wp-admin", "wp-content"],
            "large.txt": ["admin", "login", "test", "dev", "api", "blog", "shop", "backup", "old", "new",
                         "images", "css", "js", "files", "download", "upload", "wp-admin", "wp-content",
                         "includes", "config", "database", "logs", "tmp", "temp", "public", "private"]
        }
        
        for name, words in wordlists.items():
            filepath = f"{fallback_dir}/{name}"
            with open(filepath, 'w') as f:
                for word in words:
                    f.write(f"{word}\n")
            print(f"{Colors.GREEN}   ✅ Created fallback: {name}{Colors.RESET}")

    def get_wordlists(self):
        """SecLists থেকে আপডেটেড ওয়ার্ডলিস্ট সংগ্রহ করুন"""
        print(f"\n{Colors.CYAN}📂 Collecting SecLists wordlists...{Colors.RESET}")
        
        # SecLists paths
        seclists_base = "/usr/share/seclists/Discovery/Web-Content/"
        seclists_alt = "/usr/share/wordlists/seclists/Discovery/Web-Content/"
        
        # Determine which path exists
        base_path = seclists_base if os.path.exists(seclists_base) else seclists_alt
        
        # Modern wordlists from SecLists
        wordlists = [
            # ============ QUICK SCAN (Priority 1) ============
            {
                'name': 'common.txt',
                'path': f"{base_path}common.txt",
                'size': 'tiny',
                'priority': 1,
                'words': 0,
                'desc': 'Most common directories (~4.6k words)'
            },
            {
                'name': 'quickhits.txt',
                'path': f"{base_path}quickhits.txt",
                'size': 'tiny',
                'priority': 1,
                'words': 0,
                'desc': 'Quick hits for fast scanning'
            },
            
            # ============ STANDARD SCAN (Priority 2) ============
            {
                'name': 'directory-list-2.3-small.txt',
                'path': f"{base_path}directory-list-2.3-small.txt",
                'size': 'small',
                'priority': 2,
                'words': 0,
                'desc': 'Small directory list (~87k words)'
            },
            {
                'name': 'PHP.fuzz.txt',
                'path': f"{base_path}PHP.fuzz.txt",
                'size': 'medium',
                'priority': 2,
                'words': 0,
                'desc': 'PHP specific files and directories'
            },
            {
                'name': 'api-endpoints.txt',
                'path': f"{base_path}api/api-endpoints.txt",
                'size': 'medium',
                'priority': 2,
                'words': 0,
                'desc': 'API endpoints discovery'
            },
            
            # ============ DEEP SCAN (Priority 3) ============
            {
                'name': 'directory-list-2.3-medium.txt',
                'path': f"{base_path}directory-list-2.3-medium.txt",
                'size': 'large',
                'priority': 3,
                'words': 0,
                'desc': 'Medium directory list (~220k words)'
            },
            {
                'name': 'combined_words.txt',
                'path': f"{base_path}combined_words.txt",
                'size': 'large',
                'priority': 3,
                'words': 0,
                'desc': 'Combined wordlist (recommended)'
            },
            {
                'name': 'raft-large-directories.txt',
                'path': f"{base_path}raft-large-directories.txt",
                'size': 'large',
                'priority': 3,
                'words': 0,
                'desc': 'Raft large directories'
            },
            
            # ============ EXTRA DEEP SCAN (Priority 4) ============
            {
                'name': 'directory-list-2.3-big.txt',
                'path': f"{base_path}directory-list-2.3-big.txt",
                'size': 'huge',
                'priority': 4,
                'words': 0,
                'desc': 'Big directory list (~1M+ words)'
            },
            {
                'name': 'raft-large-files.txt',
                'path': f"{base_path}raft-large-files.txt",
                'size': 'huge',
                'priority': 4,
                'words': 0,
                'desc': 'Raft large files'
            },
            {
                'name': 'combined_directories.txt',
                'path': f"{base_path}combined_directories.txt",
                'size': 'huge',
                'priority': 4,
                'words': 0,
                'desc': 'Combined directories (comprehensive)'
            },
            
            # ============ TECHNOLOGY SPECIFIC (Priority 2) ============
            {
                'name': 'wordpress.txt',
                'path': f"{base_path}wordpress.txt",
                'size': 'medium',
                'priority': 2,
                'words': 0,
                'desc': 'WordPress specific'
            },
            {
                'name': 'joomla.txt',
                'path': f"{base_path}joomla.txt",
                'size': 'medium',
                'priority': 2,
                'words': 0,
                'desc': 'Joomla specific'
            },
            {
                'name': 'drupal.txt',
                'path': f"{base_path}drupal.txt",
                'size': 'medium',
                'priority': 2,
                'words': 0,
                'desc': 'Drupal specific'
            },
            {
                'name': 'iis.txt',
                'path': f"{base_path}iis.txt",
                'size': 'small',
                'priority': 2,
                'words': 0,
                'desc': 'IIS specific'
            },
            {
                'name': 'apache.txt',
                'path': f"{base_path}apache.txt",
                'size': 'small',
                'priority': 2,
                'words': 0,
                'desc': 'Apache specific'
            },
            {
                'name': 'nginx.txt',
                'path': f"{base_path}nginx.txt",
                'size': 'small',
                'priority': 2,
                'words': 0,
                'desc': 'Nginx specific'
            },
            {
                'name': 'tomcat.txt',
                'path': f"{base_path}tomcat.txt",
                'size': 'small',
                'priority': 2,
                'words': 0,
                'desc': 'Tomcat specific'
            }
        ]
        
        # Check which exist and get word counts
        available = []
        for wl in wordlists:
            if os.path.exists(wl['path']):
                try:
                    with open(wl['path'], 'r', errors='ignore') as f:
                        count = sum(1 for line in f if line.strip())
                    wl['words'] = count
                except:
                    wl['words'] = 0
                available.append(wl)
                print(f"{Colors.GREEN}   ✅ {wl['name']} ({wl['words']:,} words){Colors.RESET}")
        
        # If not enough wordlists, use fallbacks
        if len(available) < 3:
            print(f"{Colors.YELLOW}⚠️ Not enough wordlists. Creating fallbacks...{Colors.RESET}")
            self.create_fallback_wordlists()
            fallback_dir = f"{self.results_dir}/wordlists"
            available.append({
                'name': 'common_fb.txt',
                'path': f"{fallback_dir}/common.txt",
                'size': 'tiny',
                'priority': 1,
                'words': 10,
                'desc': 'Fallback common'
            })
            available.append({
                'name': 'medium_fb.txt',
                'path': f"{fallback_dir}/medium.txt",
                'size': 'medium',
                'priority': 2,
                'words': 20,
                'desc': 'Fallback medium'
            })
        
        self.all_wordlists = available
        print(f"\n{Colors.GREEN}✅ Total wordlists: {len(available)}{Colors.RESET}")
        return available

    def test_protocol(self):
        """প্রটোকল টেস্ট"""
        print(f"\n{Colors.CYAN}📡 Testing connection...{Colors.RESET}")
        
        try:
            import requests
            try:
                response = requests.get(f"http://{self.clean_target}", timeout=10, allow_redirects=False)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}   ✅ HTTP works{Colors.RESET}")
                    return ['http']
                elif response.status_code in [301, 302, 307, 308]:
                    if 'Location' in response.headers and 'https' in response.headers['Location'].lower():
                        print(f"{Colors.GREEN}   ✅ Redirecting to HTTPS{Colors.RESET}")
                        return ['https']
            except:
                pass
            
            try:
                response = requests.get(f"https://{self.clean_target}", timeout=10)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}   ✅ HTTPS works{Colors.RESET}")
                    return ['https']
            except:
                pass
        except:
            pass
        
        print(f"{Colors.YELLOW}   ⚠️ Trying both HTTP and HTTPS{Colors.RESET}")
        return ['https', 'http']

    # ==================== PHASE 1: QUICK SCAN ====================
    def run_quick_scan(self, protocol, wordlist, delay_ms=300):
        """দ্রুত স্ক্যান - ০.৩ সেকেন্ড ডেলে"""
        wordlist_path = wordlist['path']
        wordlist_name = wordlist['name']
        word_count = wordlist.get('words', 0)
        
        output_file = f"{self.results_dir}/quick_scan/quick_{protocol}_{wordlist_name}.txt"
        
        print(f"\n{Colors.CYAN}⚡ Quick: {protocol}://{self.clean_target}{Colors.RESET}")
        print(f"{Colors.BLUE}   📂 {wordlist_name} ({word_count:,} words){Colors.RESET}")
        print(f"{Colors.BLUE}   📝 {wordlist.get('desc', '')}{Colors.RESET}")
        print(f"{Colors.YELLOW}   ⏱️ {delay_ms//1000}.{delay_ms%1000}s per word{Colors.RESET}")
        
        cmd = (f"dirb {protocol}://{self.clean_target} "
               f"{wordlist_path} "
               f"-o {output_file} "
               f"-a 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' "
               f"-b "
               f"-i -l -f -r "
               f"-z {delay_ms}")
        
        print(f"{Colors.CYAN}▶️ Running...{Colors.RESET}")
        print(f"{Colors.YELLOW}   {cmd[:150]}...{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
        
        found = []
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    line = line.rstrip()
                    if line:
                        if '+ ' in line:
                            print(f"{Colors.GREEN}   🟢 {line}{Colors.RESET}")
                            match = re.search(r'\+ (https?://[^\s]+)', line)
                            if match:
                                found.append(match.group(1))
                        elif 'ERROR' in line or 'error' in line.lower():
                            print(f"{Colors.RED}   ❌ {line}{Colors.RESET}")
                        elif 'WARNING' in line or 'warning' in line.lower():
                            print(f"{Colors.YELLOW}   ⚠️ {line}{Colors.RESET}")
                        elif '---' in line or 'Scanning' in line:
                            print(f"{Colors.CYAN}   📊 {line}{Colors.RESET}")
                        else:
                            print(f"   {line}")
            
            elapsed = time.time() - start_time
            print(f"\n{Colors.GREEN}   ✅ Found {len(found)} items in {elapsed:.1f}s{Colors.RESET}")
            
            if found:
                self.quick_found.extend(found)
                self.total_found += len(found)
                self.scan_results[f"quick_{wordlist_name}"] = {
                    'found': len(found),
                    'urls': found,
                    'time': f"{elapsed:.1f}s"
                }
            
            return found
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {str(e)[:100]}{Colors.RESET}")
            return None

    # ==================== PHASE 2: DEEP SCAN ====================
    def run_deep_scan(self, protocol, wordlist, delay_ms=800):
        """গভীর স্ক্যান - ০.৮ সেকেন্ড ডেলে (আরও নির্ভুল)"""
        wordlist_path = wordlist['path']
        wordlist_name = wordlist['name']
        word_count = wordlist.get('words', 0)
        
        output_file = f"{self.results_dir}/deep_scan/deep_{protocol}_{wordlist_name}.txt"
        
        print(f"\n{Colors.MAGENTA}🔍 Deep: {protocol}://{self.clean_target}{Colors.RESET}")
        print(f"{Colors.BLUE}   📂 {wordlist_name} ({word_count:,} words){Colors.RESET}")
        print(f"{Colors.BLUE}   📝 {wordlist.get('desc', '')}{Colors.RESET}")
        print(f"{Colors.YELLOW}   ⏱️ {delay_ms//1000}.{delay_ms%1000}s per word{Colors.RESET}")
        
        # Deep scan with all extensions
        extensions = ".php,.html,.htm,.txt,.bak,.old,.sql,.js,.css,.xml,.json,.env,.git,.svn,.log,.conf,.ini,.cfg,.yml,.yaml,.zip,.tar,.gz,.7z,.rar,.pdf,.doc,.xls,.ppt,.docx,.xlsx,.pptx,.csv,.tsv,.ts,.jsx,.vue,.svelte,.go,.rb,.py,.pl,.sh,.cgi,.jsp,.asp,.aspx,.do,.action"
        
        cmd = (f"dirb {protocol}://{self.clean_target} "
               f"{wordlist_path} "
               f"-o {output_file} "
               f"-a 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' "
               f"-b "
               f"-i -l -v -w -f -r -R 2 "
               f"-X {extensions} "
               f"-z {delay_ms}")
        
        print(f"{Colors.CYAN}▶️ Running...{Colors.RESET}")
        print(f"{Colors.YELLOW}   {cmd[:150]}...{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
        
        found = []
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    line = line.rstrip()
                    if line:
                        if '+ ' in line:
                            print(f"{Colors.GREEN}   🟢 {line}{Colors.RESET}")
                            match = re.search(r'\+ (https?://[^\s]+)', line)
                            if match:
                                found.append(match.group(1))
                        elif 'ERROR' in line or 'error' in line.lower():
                            print(f"{Colors.RED}   ❌ {line}{Colors.RESET}")
                        elif 'WARNING' in line or 'warning' in line.lower():
                            print(f"{Colors.YELLOW}   ⚠️ {line}{Colors.RESET}")
                        elif '---' in line or 'Scanning' in line:
                            print(f"{Colors.CYAN}   📊 {line}{Colors.RESET}")
                        else:
                            print(f"   {line}")
            
            elapsed = time.time() - start_time
            print(f"\n{Colors.GREEN}   ✅ Found {len(found)} items in {elapsed:.1f}s{Colors.RESET}")
            
            if found:
                self.deep_found.extend(found)
                self.total_found += len(found)
                self.scan_results[f"deep_{wordlist_name}"] = {
                    'found': len(found),
                    'urls': found,
                    'time': f"{elapsed:.1f}s"
                }
            
            return found
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {str(e)[:100]}{Colors.RESET}")
            return None

    # ==================== VERIFY RESULTS ====================
    def verify_results(self):
        """ফলাফল যাচাই করুন - গুরুত্বপূর্ণ ডিরেক্টরি ম্যানুয়ালি চেক"""
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}🔍 VERIFYING IMPORTANT DIRECTORIES{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        
        all_found = list(set(self.quick_found + self.deep_found))
        
        if not all_found:
            print(f"{Colors.YELLOW}⚠️ No items to verify{Colors.RESET}")
            return []
        
        # Important directories to check
        important = ['admin', 'login', 'wp-admin', 'cpanel', 'webmail', 'phpmyadmin', 
                     'config', 'backup', 'database', 'logs', 'uploads', 'downloads',
                     'manager', 'portal', 'dashboard', 'secure', 'auth', 'api',
                     'v2', 'v3', 'graphql', 'rest', 'soap', 'xmlrpc']
        
        verified = []
        failed = []
        
        for url in all_found[:30]:  # Check top 30
            dir_name = url.split('/')[-1] if url.endswith('/') else url.split('/')[-1]
            dir_name = dir_name.split('?')[0]  # Remove query params
            
            if any(imp in dir_name.lower() for imp in important):
                print(f"{Colors.CYAN}📝 Checking: {url}{Colors.RESET}")
                
                # Check if URL is accessible
                try:
                    import requests
                    response = requests.get(url, timeout=5, verify=False, allow_redirects=False)
                    status = response.status_code
                    
                    if status == 200:
                        print(f"{Colors.GREEN}   ✅ Verified: {url} (Status: {status}){Colors.RESET}")
                        verified.append(url)
                    elif status in [301, 302, 307, 308, 403, 401, 405]:
                        print(f"{Colors.YELLOW}   ⚠️ Found: {url} (Status: {status}){Colors.RESET}")
                        verified.append(url)
                    else:
                        print(f"{Colors.RED}   ❌ Failed: {url} (Status: {status}){Colors.RESET}")
                        failed.append(url)
                except requests.exceptions.Timeout:
                    print(f"{Colors.YELLOW}   ⏱️ Timeout: {url}{Colors.RESET}")
                    failed.append(url)
                except Exception as e:
                    print(f"{Colors.RED}   ❌ Error: {url} - {str(e)[:30]}{Colors.RESET}")
                    failed.append(url)
        
        self.verified = verified
        self.verified_failed = failed
        
        print(f"\n{Colors.GREEN}✅ Verified: {len(verified)} directories{Colors.RESET}")
        if verified:
            for v in verified[:10]:
                print(f"   {Colors.GREEN}• {v}{Colors.RESET}")
            if len(verified) > 10:
                print(f"   {Colors.YELLOW}... and {len(verified)-10} more{Colors.RESET}")
        
        if failed:
            print(f"{Colors.RED}❌ Failed: {len(failed)} directories{Colors.RESET}")
        
        # Save verified results
        if verified:
            with open(f"{self.results_dir}/verified.txt", 'w') as f:
                for v in verified:
                    f.write(f"{v}\n")
            print(f"{Colors.CYAN}📁 Verified results saved: {self.results_dir}/verified.txt{Colors.RESET}")
        
        return verified

    # ==================== MAIN HYBRID SCAN ====================
    def run_hybrid_scan(self):
        """হাইব্রিড স্ক্যান চালান - Quick + Deep + Verify"""
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}🚀 DIRB HYBRID SCAN (SecLists Optimized){Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")

        # STEP 1: Check DIRB
        if not self.check_dirb():
            print(f"{Colors.RED}❌ DIRB not available{Colors.RESET}")
            return

        # STEP 2: Check SecLists
        self.check_seclists()

        # STEP 3: Get wordlists
        all_wordlists = self.get_wordlists()
        if not all_wordlists:
            print(f"{Colors.RED}❌ No wordlists found{Colors.RESET}")
            return

        # STEP 4: Test protocol
        protocols = self.test_protocol()

        # ============ PHASE 1: QUICK SCAN ============
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 PHASE 1: QUICK SCAN (Priority 1-2){Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
        
        quick_wordlists = [wl for wl in all_wordlists if wl['priority'] <= 2]
        quick_found_total = 0
        
        for wl in quick_wordlists[:4]:  # First 4 quick wordlists
            for protocol in protocols:
                found = self.run_quick_scan(protocol, wl, delay_ms=300)
                if found:
                    quick_found_total += len(found)
                    if quick_found_total >= 15:
                        print(f"{Colors.GREEN}✅ Found 15+ items in quick scan! Moving to deep scan...{Colors.RESET}")
                        break
                if quick_found_total >= 15:
                    break
            if quick_found_total >= 15:
                break
        
        print(f"\n{Colors.CYAN}📊 Quick scan found: {quick_found_total} items{Colors.RESET}")

        # ============ PHASE 2: DEEP SCAN ============
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}📊 PHASE 2: DEEP SCAN (Priority 3-4){Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
        
        # If quick scan found less than 10, do deep scan
        if quick_found_total < 10:
            print(f"{Colors.YELLOW}⚠️ Quick scan found less than 10 items. Running deep scan...{Colors.RESET}")
            
            deep_wordlists = [wl for wl in all_wordlists if wl['priority'] >= 3]
            
            for wl in deep_wordlists[:3]:
                for protocol in protocols[:1]:  # Use only first protocol for deep scan
                    found = self.run_deep_scan(protocol, wl, delay_ms=800)
                    if found:
                        self.deep_found.extend(found)
                        if len(self.deep_found) >= 20:
                            print(f"{Colors.GREEN}✅ Found enough items in deep scan!{Colors.RESET}")
                            break
                if len(self.deep_found) >= 20:
                    break
        else:
            print(f"{Colors.GREEN}✅ Quick scan found enough results. Running one deep scan for verification...{Colors.RESET}")
            deep_wordlists = [wl for wl in all_wordlists if wl['priority'] >= 3]
            for wl in deep_wordlists[:1]:
                for protocol in protocols[:1]:
                    self.run_deep_scan(protocol, wl, delay_ms=800)

        # ============ PHASE 3: VERIFY ============
        self.verify_results()

        # ============ FINAL SUMMARY ============
        self.show_hybrid_summary()

    def show_hybrid_summary(self):
        """হাইব্রিড স্ক্যানের সারাংশ"""
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 HYBRID SCAN SUMMARY{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        
        all_found = list(set(self.quick_found + self.deep_found))
        print(f"{Colors.CYAN}Target:{Colors.RESET} {self.target}")
        print(f"{Colors.CYAN}Quick scan found:{Colors.RESET} {len(self.quick_found)} items")
        print(f"{Colors.CYAN}Deep scan found:{Colors.RESET} {len(self.deep_found)} items")
        print(f"{Colors.CYAN}Total unique items:{Colors.RESET} {len(all_found)}")
        print(f"{Colors.CYAN}Verified working:{Colors.RESET} {len(self.verified) if hasattr(self, 'verified') else 0}")
        print(f"{Colors.CYAN}📁 Results folder:{Colors.RESET} {self.results_dir}")
        
        # Scan performance
        if self.scan_results:
            print(f"\n{Colors.BOLD}📋 Scan performance:{Colors.RESET}")
            for name, data in self.scan_results.items():
                print(f"{Colors.GREEN}   ✅ {name}: {data['found']} items ({data['time']}){Colors.RESET}")
        
        # Save combined results
        if all_found:
            with open(f"{self.results_dir}/all_found.txt", 'w') as f:
                for item in sorted(all_found):
                    f.write(f"{item}\n")
            print(f"{Colors.CYAN}📁 All results: {self.results_dir}/all_found.txt{Colors.RESET}")
            
            print(f"\n{Colors.GREEN}📋 Found items ({len(all_found)}):{Colors.RESET}")
            for i, item in enumerate(sorted(all_found)[:20], 1):
                print(f"   {i}. {item}")
            if len(all_found) > 20:
                print(f"   {Colors.YELLOW}... and {len(all_found)-20} more{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠️ No items found!{Colors.RESET}")

    def run(self):
        """মেইন"""
        print()
        print(f"{Colors.BOLD}{Colors.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║         DIRB - HYBRID SCANNER (SECLISTS OPTIMIZED)          ║")
        print("║         Quick Scan + Deep Scan + Verification               ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print(Colors.RESET)

        print(f"{Colors.CYAN}🎯 Target: {self.target}{Colors.RESET}")
        print(f"{Colors.CYAN}📁 Results: {self.results_dir}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")

        self.run_hybrid_scan()

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        print(f"{Colors.YELLOW}📝 Enter target (e.g., foodnetwork.com): {Colors.RESET}")
        target = input().strip()
    
    if not target:
        print(f"{Colors.RED}❌ No target!{Colors.RESET}")
        sys.exit(1)

    scanner = DirbHybrid(target)
    scanner.run()

if __name__ == "__main__":
    main()