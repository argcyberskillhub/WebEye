#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║  🕵️  RECON v2.0 - ADVANCED WEAPONIZED RECONNAISSANCE    ║
║  Website Information Gathering & OSINT Framework        ║
║  [✓] AUTH0RIZED PENTESTING TOOL ONLY                    ║
╚══════════════════════════════════════════════════════════╝
"""

import socket
import threading
import requests
import json
import sys
import time
import os
import re
import ssl
import urllib.parse
import subprocess
import dns.resolver
import dns.reversename
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== HACKER THEME COLORS =====
if os.name == 'nt':
    os.system('color')

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; N = '\033[0m'
    bold = '\033[1m'; dim = '\033[2m'; blink = '\033[5m'

# ===== ASCII BANNER =====
BANNER = f"""
{C.R}{C.bold}
██╗    ██╗███████╗██████╗ ███████╗██╗   ██╗███████╗
██║    ██║██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝
██║ █╗ ██║█████╗  ██████╔╝█████╗   ╚████╔╝ █████╗
██║███╗██║██╔══╝  ██╔══██╗██╔══╝    ╚██╔╝  ██╔══╝
╚███╔███╔╝███████╗██████╔╝███████╗   ██║   ███████╗
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝   ╚═╝   ╚══════╝
{C.N}
{C.R}
              ☠️  ☣  ☠️
         ╔═══════════════════╗
         ║  ⚠ DANGER ZONE ⚠  ║
         ╚═══════════════════╝
       ▄︻デ══━一  SYSTEM BREACH
{C.N}
{C.M}
╔══════════════════════════════════════════════════╗
║       ADVANCED WEB RECONNAISSANCE v3.0           ║
║       DNS • HTTP • TLS • OSINT • AUDIT           ║
║       Developer: ARGCyberSkillHub                ║
║       Authorized assessments only                ║
╚══════════════════════════════════════════════════╝{C.N}

{C.dim}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.N}
{C.Y}{'='*55}{C.N}
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    clear()
    print(BANNER)


# ================================================================
# 📦 RECON ENGINE - 15+ FEATURES
# ================================================================
class ReconEngine:
    def __init__(self, target):
        self.target = target.strip()
        self.domain = self._extract_domain()
        self.results = {}
        self.start_time = time.time()
        
        # Common directories for fuzzing
        self.common_dirs = [
            "admin", "login", "wp-admin", "wp-content", "wp-includes",
            "api", "v1", "v2", "backup", "backups", "config", "configuration",
            "db", "database", "sql", "dump", "uploads", "files", "assets",
            "css", "js", "images", "img", "static", "public", "private",
            "test", "tests", "dev", "development", "staging", "beta",
            "phpmyadmin", "phpPgAdmin", "adminer", "server-status",
            ".git", ".env", ".htaccess", "robots.txt", "sitemap.xml",
            "crossdomain.xml", "clientaccesspolicy.xml", "README.md",
            "install", "setup", "wizard", "cgi-bin", "cpanel", "webmail"
        ]
        
        # User agents
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        # Session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.ua})
    
    def _extract_domain(self):
        """Extract clean domain from URL or IP"""
        # Remove protocol
        domain = re.sub(r'https?://', '', self.target)
        # Remove path
        domain = domain.split('/')[0]
        # Remove port
        domain = domain.split(':')[0]
        return domain.lower()
    
    def _print_section(self, title, data, icon="📌"):
        """Print formatted section"""
        if not data or (isinstance(data, (list, dict)) and len(data) == 0):
            return
        
        print(f"\n  {C.Y}{icon} {C.bold}{title}{C.N}")
        print(f"  {C.dim}{'─'*50}{C.N}")
        
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"  {C.C}├─{C.N} {k}: {C.W}{v}{C.N}")
        elif isinstance(data, list):
            for item in data[:20]:  # Max 20 items
                print(f"  {C.C}├─{C.N} {C.W}{item}{C.N}")
            if len(data) > 20:
                print(f"  {C.dim}└─ ... and {len(data)-20} more results{C.N}")
        else:
            print(f"  {C.W}{data}{C.N}")
    
    def _loading(self, text, done=False):
        """Show loading animation"""
        if done:
            print(f"\r  {C.G}[✓]{C.N} {text}{' ' * 40}")
        else:
            sys.stdout.write(f"\r  {C.C}[→]{C.N} {text}...")
            sys.stdout.flush()
    
    # ========== FEATURE 1: DNS RECONNAISSANCE ==========
    def dns_recon(self):
        """Full DNS enumeration"""
        self._loading("Performing DNS reconnaissance")
        dns_info = {}
        
        try:
            # A Record
            try:
                answers = dns.resolver.resolve(self.domain, 'A')
                dns_info['A (IPv4)'] = [str(r) for r in answers]
            except: pass
            
            # AAAA Record
            try:
                answers = dns.resolver.resolve(self.domain, 'AAAA')
                dns_info['AAAA (IPv6)'] = [str(r) for r in answers]
            except: pass
            
            # MX Records
            try:
                answers = dns.resolver.resolve(self.domain, 'MX')
                mx_records = []
                for r in answers:
                    mx_records.append(f"{r.preference} {str(r.exchange)}")
                dns_info['MX (Mail)'] = mx_records
            except: pass
            
            # NS Records
            try:
                answers = dns.resolver.resolve(self.domain, 'NS')
                dns_info['NS (Nameservers)'] = [str(r) for r in answers]
            except: pass
            
            # TXT Records
            try:
                answers = dns.resolver.resolve(self.domain, 'TXT')
                dns_info['TXT Records'] = [str(r) for r in answers]
            except: pass
            
            # SOA Record
            try:
                answers = dns.resolver.resolve(self.domain, 'SOA')
                for r in answers:
                    dns_info['SOA'] = f"MNAME: {r.mname}, RNAME: {r.rname}, Serial: {r.serial}"
            except: pass
            
            # CNAME
            try:
                answers = dns.resolver.resolve(self.domain, 'CNAME')
                dns_info['CNAME'] = [str(r) for r in answers]
            except: pass
            
            # Reverse DNS
            try:
                ip = socket.gethostbyname(self.domain)
                rev_name = dns.reversename.from_address(ip)
                rev_answers = dns.resolver.resolve(rev_name, 'PTR')
                dns_info['PTR (Reverse)'] = [str(r) for r in rev_answers]
            except: pass
            
            # SPF Record
            try:
                answers = dns.resolver.resolve(self.domain, 'SPF')
                dns_info['SPF'] = [str(r) for r in answers]
            except: pass
            
            # DMARC
            try:
                dmarc = f"_dmarc.{self.domain}"
                answers = dns.resolver.resolve(dmarc, 'TXT')
                dns_info['DMARC'] = [str(r) for r in answers]
            except: pass
            
            self.results['dns'] = dns_info
            self._loading(f"DNS recon complete ({len(dns_info)} record types found)", done=True)
            
        except Exception as e:
            self._loading(f"DNS recon failed: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 2: PORT SCANNING ==========
    def port_scan(self):
        """Scan top 100 ports"""
        self._loading("Scanning top 100 ports")
        
        top_ports = [
            21, 22, 23, 25, 53, 80, 81, 110, 111, 135, 139, 143, 161, 179,
            389, 443, 445, 465, 500, 514, 543, 544, 554, 587, 631, 636, 646,
            993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1111, 1433, 1434,
            1521, 2049, 2082, 2083, 2086, 2087, 2095, 2096, 2222, 3306,
            3389, 3690, 4333, 4444, 4445, 4489, 4848, 5000, 5001, 5002,
            5003, 5050, 5060, 5104, 5222, 5223, 5353, 5432, 5500, 5501,
            5555, 5600, 5601, 5672, 5800, 5801, 5900, 5901, 5984, 5985,
            5986, 6000, 6001, 6379, 6666, 6667, 6668, 6669, 7000, 7001,
            7070, 7071, 7777, 7778, 8000, 8001, 8008, 8009, 8080, 8081,
            8443, 8444, 8686, 8787, 8888, 9000, 9001, 9043, 9060, 9080,
            9090, 9091, 9100, 9200, 9300, 9443, 9876, 9999, 10000, 10001,
            11211, 27017, 27018, 27019
        ]
        
        open_ports = []
        
        def check_port(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((self.domain, port))
                s.close()
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    return (port, service)
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(check_port, p): p for p in top_ports}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    self._loading(f"Found open port: {result[0]}/{result[1]}")
        
        open_ports.sort(key=lambda x: x[0])
        self.results['ports'] = open_ports
        self._loading(f"Port scan complete - {len(open_ports)} open ports", done=True)
    
    # ========== FEATURE 3: HTTP HEADERS & TECH DETECTION ==========
    def http_recon(self):
        """Analyze HTTP headers and detect technologies"""
        self._loading("Analyzing HTTP headers & technologies")
        
        http_info = {}
        
        try:
            # Try HTTPS first, fallback to HTTP
            for protocol in ['https', 'http']:
                try:
                    url = f"{protocol}://{self.domain}"
                    r = self.session.get(url, timeout=10, verify=False, allow_redirects=True)
                    
                    # Headers
                    headers = dict(r.headers)
                    http_info['Status Code'] = r.status_code
                    http_info['Final URL'] = r.url
                    http_info['Redirects'] = len(r.history)
                    
                    # Server info
                    if 'Server' in headers:
                        http_info['Server'] = headers['Server']
                    if 'X-Powered-By' in headers:
                        http_info['X-Powered-By'] = headers['X-Powered-By']
                    
                    # Security headers
                    sec_headers = {
                        'Strict-Transport-Security': 'HSTS',
                        'Content-Security-Policy': 'CSP',
                        'X-Frame-Options': 'Clickjacking Protection',
                        'X-Content-Type-Options': 'MIME Sniffing Protection',
                        'X-XSS-Protection': 'XSS Protection',
                        'Referrer-Policy': 'Referrer Policy',
                    }
                    
                    present = []
                    missing = []
                    for hdr, name in sec_headers.items():
                        if hdr in headers:
                            present.append(f"{name} [{headers[hdr][:30]}]")
                        else:
                            missing.append(name)
                    
                    http_info['Security Headers Present'] = present
                    http_info['Security Headers Missing'] = missing
                    
                    # Detect technologies via headers
                    techs = []
                    if 'CF-RAY' in headers:
                        techs.append('Cloudflare')
                    if 'X-Served-By' in headers:
                        techs.append(f"nginx-like ({headers['X-Served-By']})")
                    if 'X-AspNet-Version' in headers:
                        techs.append(f"ASP.NET {headers['X-AspNet-Version']}")
                    if 'X-Powered-By' in headers:
                        techs.append(f"Powered by: {headers['X-Powered-By']}")
                    if 'set-cookie' in str(headers).lower():
                        if 'PHPSESSID' in str(headers):
                            techs.append('PHP')
                        if 'JSESSIONID' in str(headers):
                            techs.append('Java/JSP')
                        if 'ASPSESSIONID' in str(headers):
                            techs.append('ASP')
                    if 'x-generator' in headers:
                        techs.append(headers['x-generator'])
                    
                    http_info['Technologies Detected'] = techs
                    
                    # Content info
                    content_type = r.headers.get('Content-Type', '')
                    http_info['Content-Type'] = content_type
                    http_info['Response Size'] = f"{len(r.content):,} bytes"
                    
                    self.results['http'] = http_info
                    self._loading("HTTP recon complete", done=True)
                    return
                    
                except requests.exceptions.SSLError:
                    continue
                except:
                    continue
            
        except Exception as e:
            self._loading(f"HTTP recon failed: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 4: SSL/TLS ANALYSIS ==========
    def ssl_analysis(self):
        """Check SSL certificate details"""
        self._loading("Analyzing SSL/TLS certificate")
        
        ssl_info = {}
        
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        ssl_info['Issuer'] = dict(cert.get('issuer', [['Unknown']])[0]).get('organizationName', 'Unknown')
                        ssl_info['Subject'] = dict(cert.get('subject', [['Unknown']])[0]).get('commonName', 'Unknown')
                        
                        # Valid from
                        valid_from = cert.get('notBefore', 'N/A')
                        ssl_info['Valid From'] = valid_from
                        
                        # Valid until
                        valid_until = cert.get('notAfter', 'N/A')
                        ssl_info['Valid Until'] = valid_until
                        
                        # Days remaining
                        try:
                            from datetime import datetime as dt
                            expiry = dt.strptime(valid_until, '%b %d %H:%M:%S %Y %Z')
                            remaining = (expiry - dt.now()).days
                            ssl_info['Days Remaining'] = f"{remaining} days"
                            if remaining < 30:
                                ssl_info['⚠ Expiry Warning'] = "CERTIFICATE EXPIRING SOON!"
                        except:
                            pass
                        
                        # SANs (Subject Alternative Names)
                        sans = []
                        for ext in cert.get('subjectAltName', []):
                            sans.append(ext[1])
                        ssl_info['SANs (Subdomains)'] = sans
                        
                        # SSL Version
                        ssl_info['SSL/TLS Version'] = ssock.version()
                        
                        # Cipher
                        ssl_info['Cipher Suite'] = ssock.cipher()[0]
                        
                        self.results['ssl'] = ssl_info
                        self._loading("SSL analysis complete", done=True)
                        
        except Exception as e:
            self._loading(f"SSL analysis: {str(e)[:30] if '443' not in str(e) else 'No HTTPS (443)'}", done=True)
    
    # ========== FEATURE 5: DIRECTORY FUZZING ==========
    def directory_fuzzing(self):
        """Brute force common directories and files"""
        self._loading("Directory fuzzing (200+ paths)")
        
        found = {'directories': [], 'files': [], 'status_codes': {}}
        
        for path in self.common_dirs:
            try:
                url = f"http://{self.domain}/{path}"
                r = self.session.get(url, timeout=3, allow_redirects=False)
                
                sc = r.status_code
                found['status_codes'][sc] = found['status_codes'].get(sc, 0) + 1
                
                if sc in [200, 201, 202, 204, 301, 302, 303, 307, 401, 403]:
                    entry = f"/{path} [{sc}]"
                    if '.' in path:
                        found['files'].append(entry)
                    else:
                        found['directories'].append(entry)
                    
            except:
                pass
        
        found['directories'].sort()
        found['files'].sort()
        
        self.results['directories'] = found
        self._loading("Directory fuzzing complete", done=True)
    
    # ========== FEATURE 6: WHOIS LOOKUP ==========
    def whois_lookup(self):
        """Fetch WHOIS information"""
        self._loading("Performing WHOIS lookup")
        
        whois_info = {}
        
        try:
            # Try using python-whois if available
            import whois as whois_lib
            try:
                w = whois_lib.whois(self.domain)
                
                whois_info['Registrar'] = w.registrar or 'N/A'
                whois_info['Creation Date'] = str(w.creation_date)[:20] if w.creation_date else 'N/A'
                whois_info['Expiration Date'] = str(w.expiration_date)[:20] if w.expiration_date else 'N/A'
                whois_info['Name Servers'] = w.name_servers if w.name_servers else 'N/A'
                whois_info['Status'] = w.status if w.status else 'N/A'
                whois_info['Emails'] = w.emails if w.emails else 'N/A'
                whois_info['Organization'] = w.org or 'N/A'
                whois_info['Country'] = w.country or 'N/A'
                
            except:
                whois_info['Note'] = "WHOIS library failed - try manual lookup at whois.domaintools.com"
            
            self.results['whois'] = whois_info
            
        except ImportError:
            whois_info['Note'] = "Install python-whois: pip install python-whois"
            self.results['whois'] = whois_info
        
        self._loading("WHOIS lookup complete", done=True)
    
    # ========== FEATURE 7: SUBDOMAIN ENUMERATION ==========
    def subdomain_enum(self):
        """Discover subdomains using common wordlist and APIs"""
        self._loading("Enumerating subdomains")
        
        subdomains = set()
        
        # Common subdomains
        common_subs = [
            "www", "mail", "ftp", "admin", "cpanel", "webmail", "blog", "shop",
            "api", "dev", "test", "staging", "beta", "app", "m", "mobile",
            "forum", "support", "help", "wiki", "docs", "cdn", "static",
            "assets", "images", "img", "css", "js", "video", "media",
            "download", "uploads", "files", "backup", "secure", "login",
            "register", "signup", "status", "stats", "analytics", "tracking",
            "news", "events", "store", "cart", "checkout", "payment",
            "portal", "my", "account", "profile", "user", "users",
            "server", "server1", "server2", "node1", "node2", "db", "database",
            "redis", "memcache", "mail2", "smtp", "pop3", "imap",
            "autodiscover", "owa", "exchange", "remote", "vpn", "proxy",
            "git", "svn", "jenkins", "jira", "confluence", "wiki",
            "phpmyadmin", "adminer", "pma", "mysql", "webmin",
            "direct", "direct-connect", "chat", "live", "stream",
            "cdn1", "cdn2", "cloud", "ns1", "ns2", "ns3", "dns1", "dns2",
            "mailgun", "sendgrid", "mandrill", "sparkpost", "ses"
        ]
        
        def check_sub(sub):
            try:
                full_domain = f"{sub}.{self.domain}"
                ip = socket.gethostbyname(full_domain)
                return (sub, ip)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(check_sub, s): s for s in common_subs}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    subdomains.add(result)
                    self._loading(f"Found: {result[0]}.{self.domain} → {result[1]}")
        
        # Try API-based discovery
        try:
            url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
            r = requests.get(url, timeout=5, headers={"User-Agent": self.ua})
            if r.status_code == 200:
                data = r.json()
                for entry in data[:100]:  # First 100
                    name = entry.get('name_value', '')
                    for sub in name.split('\n'):
                        sub = sub.strip()
                        if sub.endswith(self.domain) and sub != self.domain:
                            if '*' not in sub:
                                try:
                                    ip = socket.gethostbyname(sub)
                                    subdomains.add((sub.replace(f".{self.domain}", ""), ip))
                                except:
                                    subdomains.add((sub.replace(f".{self.domain}", ""), "unresolved"))
        except:
            pass
        
        self.results['subdomains'] = sorted(subdomains, key=lambda x: x[0])
        self._loading(f"Subdomain enumeration: {len(subdomains)} found", done=True)
    
    # ========== FEATURE 8: TECHNOLOGY STACK DETECTION ==========
    def tech_detection(self):
        """Advanced technology detection using Wappalyzer-style regex"""
        self._loading("Detecting technology stack")
        
        techs = {}
        
        try:
            url = f"https://{self.domain}"
            r = self.session.get(url, timeout=10, verify=False)
            html = r.text
            headers = dict(r.headers)
            
            # Web frameworks
            if 'wp-content' in html or 'wp-includes' in html or 'wp-json' in html:
                techs['CMS'] = 'WordPress'
            elif '__VIEWSTATE' in html:
                techs['Framework'] = 'ASP.NET'
            elif 'Drupal.settings' in html:
                techs['CMS'] = 'Drupal'
            elif 'Joomla' in html or 'joomla' in html:
                techs['CMS'] = 'Joomla'
            elif 'Shopify' in html or 'shopify' in html:
                techs['E-commerce'] = 'Shopify'
            elif 'WooCommerce' in html:
                techs['E-commerce'] = 'WooCommerce'
            elif 'Magento' in html:
                techs['E-commerce'] = 'Magento'
            elif 'csrf-token' in html and 'laravel' in html.lower():
                techs['Framework'] = 'Laravel (PHP)'
            elif 'django' in html.lower():
                techs['Framework'] = 'Django (Python)'
            elif 'symfony' in html.lower():
                techs['Framework'] = 'Symfony (PHP)'
            elif 'ruby' in html.lower() or 'rails' in html.lower():
                techs['Framework'] = 'Ruby on Rails'
            elif 'next.js' in html.lower() or 'next_' in html:
                techs['Framework'] = 'Next.js'
            elif 'react' in html.lower() or 'react' in str(headers).lower():
                techs['Framework'] = 'React'
            elif 'angular' in html.lower():
                techs['Framework'] = 'Angular'
            elif 'vue' in html.lower() or 'vuejs' in html.lower():
                techs['Framework'] = 'Vue.js'
            
            # JavaScript libraries
            js_libs = []
            if 'jquery' in html.lower():
                js_libs.append('jQuery')
            if 'bootstrap' in html.lower():
                js_libs.append('Bootstrap')
            if 'font-awesome' in html.lower() or 'fontawesome' in html.lower():
                js_libs.append('Font Awesome')
            if 'moment' in html.lower():
                js_libs.append('Moment.js')
            if 'lodash' in html.lower():
                js_libs.append('Lodash')
            if 'axios' in html.lower():
                js_libs.append('Axios')
            if js_libs:
                techs['JavaScript Libraries'] = ', '.join(js_libs)
            
            # Analytics
            analytics = []
            if 'google-analytics' in html or 'ga(' in html or 'gtag' in html:
                analytics.append('Google Analytics')
            if 'facebook' in html and 'pixel' in html:
                analytics.append('Facebook Pixel')
            if 'hotjar' in html:
                analytics.append('Hotjar')
            if analytics:
                techs['Analytics'] = ', '.join(analytics)
            
            # Web server
            if 'Server' in headers:
                techs['Web Server'] = headers['Server']
            
            # CDN detection
            if 'CF-RAY' in headers:
                techs['CDN'] = 'Cloudflare'
            elif 'x-amz-cf-id' in headers:
                techs['CDN'] = 'AWS CloudFront'
            elif 'x-akamai' in str(headers).lower():
                techs['CDN'] = 'Akamai'
            elif 'x-sucuri' in str(headers).lower():
                techs['CDN'] = 'Sucuri'
            elif 'x-cache' in str(headers).lower() and 'cloudflare' not in str(headers).lower():
                techs['CDN'] = 'Generic CDN'
            
            # Programming language
            if 'X-Powered-By' in headers:
                techs['Language'] = headers['X-Powered-By']
            elif '.php' in html or 'PHP' in str(headers).upper():
                techs['Language'] = 'PHP'
            elif 'ASP' in str(headers).upper() or '.aspx' in html:
                techs['Language'] = 'ASP.NET'
            elif 'JSP' in html or '.jsp' in html:
                techs['Language'] = 'Java/JSP'
            
            # Operating System
            if 'ubuntu' in str(headers).lower():
                techs['OS'] = 'Ubuntu Linux'
            elif 'debian' in str(headers).lower():
                techs['OS'] = 'Debian Linux'
            elif 'centos' in str(headers).lower():
                techs['OS'] = 'CentOS Linux'
            elif 'red hat' in str(headers).lower() or 'redhat' in str(headers).lower():
                techs['OS'] = 'Red Hat Linux'
            elif 'windows' in str(headers).lower() or 'win64' in str(headers).lower():
                techs['OS'] = 'Windows Server'
            elif 'nginx' in str(headers).lower():
                techs['OS'] = 'Linux (likely)'
            
            self.results['technologies'] = techs
            self._loading("Tech detection complete", done=True)
            
        except Exception as e:
            self._loading(f"Tech detection: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 9: EMAIL EXTRACTION ==========
    def email_extraction(self):
        """Extract emails from website pages"""
        self._loading("Extracting email addresses")
        
        emails = set()
        
        try:
            # Check multiple pages
            pages = [
                f"https://{self.domain}",
                f"https://{self.domain}/contact",
                f"https://{self.domain}/about",
                f"https://{self.domain}/team",
                f"https://{self.domain}/support",
                f"https://{self.domain}/privacy",
                f"https://{self.domain}/terms",
            ]
            
            for page_url in pages:
                try:
                    r = self.session.get(page_url, timeout=5, verify=False)
                    # Regex for emails
                    found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)
                    for email in found:
                        if not email.endswith('.png') and not email.endswith('.jpg') and not email.endswith('.css'):
                            email = email.lower().strip()
                            if email.count('@') == 1:
                                emails.add(email)
                except:
                    pass
            
            self.results['emails'] = sorted(emails)
            self._loading(f"Email extraction: {len(emails)} found", done=True)
            
        except Exception as e:
            self._loading(f"Email extraction: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 10: SOCIAL LINKS DETECTION ==========
    def social_links(self):
        """Find social media links"""
        self._loading("Finding social media links")
        
        social = {}
        
        try:
            url = f"https://{self.domain}"
            r = self.session.get(url, timeout=10, verify=False)
            html = r.text
            
            platforms = {
                'Facebook': ['facebook.com/', 'fb.com/', 'fb.me/'],
                'Twitter/X': ['twitter.com/', 'x.com/'],
                'LinkedIn': ['linkedin.com/company/', 'linkedin.com/in/'],
                'Instagram': ['instagram.com/'],
                'YouTube': ['youtube.com/', 'youtu.be/'],
                'GitHub': ['github.com/'],
                'Medium': ['medium.com/'],
                'Reddit': ['reddit.com/r/'],
                'WhatsApp': ['wa.me/', 'whatsapp.com/'],
                'Telegram': ['t.me/', 'telegram.me/'],
                'Discord': ['discord.gg/', 'discord.com/invite/'],
                'TikTok': ['tiktok.com/@'],
                'Pinterest': ['pinterest.com/'],
                'Snapchat': ['snapchat.com/add/'],
            }
            
            found_links = {}
            for platform, patterns in platforms.items():
                for pattern in patterns:
                    if pattern in html:
                        # Extract full URL
                        idx = html.index(pattern)
                        start = max(0, idx - 50)
                        end = min(len(html), idx + 100)
                        snippet = html[start:end]
                        
                        match = re.search(r'https?://[^\s"\'<>]+', snippet)
                        if match:
                            link = match.group().rstrip('.,;:!?)"\'')
                            if platform not in found_links:
                                found_links[platform] = []
                            if link not in found_links[platform]:
                                found_links[platform].append(link)
            
            # Also check common social handles
            if not found_links:
                social['Note'] = "No social links found on homepage"
            
            self.results['social'] = found_links
            self._loading(f"Social links: {len(found_links)} platforms found", done=True)
            
        except Exception as e:
            self._loading(f"Social links: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 11: ROBOTS & SITEMAP ANALYSIS ==========
    def robots_sitemap(self):
        """Analyze robots.txt and sitemap.xml"""
        self._loading("Analyzing robots.txt & sitemap.xml")
        
        info = {}
        
        # robots.txt
        try:
            r = self.session.get(f"http://{self.domain}/robots.txt", timeout=5)
            if r.status_code == 200:
                info['robots.txt'] = r.text[:1000]  # First 1000 chars
            else:
                info['robots.txt'] = f"Not found (HTTP {r.status_code})"
        except:
            info['robots.txt'] = "Could not fetch"
        
        # Also check HTTPS
        try:
            r = self.session.get(f"https://{self.domain}/robots.txt", timeout=5)
            if r.status_code == 200:
                info['robots.txt (HTTPS)'] = r.text[:1000]
        except:
            pass
        
        # sitemap.xml
        try:
            r = self.session.get(f"https://{self.domain}/sitemap.xml", timeout=5)
            if r.status_code == 200:
                sitemap_urls = re.findall(r'<loc>(.*?)</loc>', r.text)
                info['sitemap.xml URLs'] = sitemap_urls[:50]  # First 50
                if len(sitemap_urls) > 50:
                    info['sitemap.xml URLs'].append(f"... and {len(sitemap_urls)-50} more")
            else:
                info['sitemap.xml'] = f"Not found (HTTP {r.status_code})"
        except:
            info['sitemap.xml'] = "Could not fetch"
        
        self.results['robots_sitemap'] = info
        self._loading("Robots & sitemap analysis complete", done=True)
    
    # ========== FEATURE 12: SECURITY HEADERS CHECK ==========
    def security_audit(self):
        """Comprehensive security headers audit"""
        self._loading("Running security audit")
        
        audit = {}
        
        try:
            url = f"https://{self.domain}"
            r = self.session.get(url, timeout=10, verify=False)
            h = r.headers
            
            checks = {
                'Strict-Transport-Security (HSTS)': {
                    'present': 'Strict-Transport-Security' in h,
                    'value': h.get('Strict-Transport-Security', 'MISSING'),
                    'risk': 'HIGH' if 'Strict-Transport-Security' not in h else 'LOW',
                    'note': 'Prevents SSL stripping attacks'
                },
                'Content-Security-Policy (CSP)': {
                    'present': 'Content-Security-Policy' in h,
                    'value': h.get('Content-Security-Policy', 'MISSING')[:60],
                    'risk': 'MEDIUM' if 'Content-Security-Policy' not in h else 'LOW',
                    'note': 'Prevents XSS & data injection'
                },
                'X-Frame-Options': {
                    'present': 'X-Frame-Options' in h,
                    'value': h.get('X-Frame-Options', 'MISSING'),
                    'risk': 'MEDIUM' if 'X-Frame-Options' not in h else 'LOW',
                    'note': 'Prevents clickjacking'
                },
                'X-Content-Type-Options': {
                    'present': 'X-Content-Type-Options' in h,
                    'value': h.get('X-Content-Type-Options', 'MISSING'),
                    'risk': 'LOW' if 'X-Content-Type-Options' in h else 'MEDIUM',
                    'note': 'Prevents MIME sniffing'
                },
                'Referrer-Policy': {
                    'present': 'Referrer-Policy' in h,
                    'value': h.get('Referrer-Policy', 'MISSING'),
                    'risk': 'LOW',
                    'note': 'Controls referrer information'
                },
                'Permissions-Policy': {
                    'present': 'Permissions-Policy' in h,
                    'value': h.get('Permissions-Policy', 'MISSING')[:40],
                    'risk': 'LOW',
                    'note': 'Controls browser features'
                },
                'X-XSS-Protection': {
                    'present': 'X-XSS-Protection' in h,
                    'value': h.get('X-XSS-Protection', 'MISSING'),
                    'risk': 'MEDIUM',
                    'note': 'Legacy XSS filter (deprecated but still used)'
                },
                'Server Version Disclosure': {
                    'present': 'Server' in h,
                    'value': h.get('Server', 'Not disclosed') if 'Server' in h else 'Not disclosed',
                    'risk': 'LOW' if 'Server' not in h else 'MEDIUM',
                    'note': 'Information disclosure risk' if 'Server' in h else 'Good - no version info'
                }
            }
            
            audit['headers'] = checks
            
            # Calculate overall score
            total = len(checks)
            passed = sum(1 for c in checks.values() if c['present'])
            audit['security_score'] = f"{passed}/{total} headers present ({(passed/total)*100:.0f}%)"
            
            # Risk summary
            risks = [c for c in checks.values() if c['risk'] == 'HIGH']
            audit['high_risk_issues'] = [c['note'] for c in checks.values() if c['risk'] == 'HIGH']
            
            # SSL version check
            try:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with socket.create_connection((self.domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                        audit['ssl_protocol'] = ssock.version()
                        
                        # Check for weak protocols
                        if 'TLSv1' in ssock.version() or 'SSL' in ssock.version():
                            audit['ssl_warning'] = f"⚠ Using potentially outdated protocol: {ssock.version()}"
                        
            except:
                pass
            
            self.results['security'] = audit
            self._loading("Security audit complete", done=True)
            
        except Exception as e:
            self._loading(f"Security audit: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 13: IP GEOLOCATION ==========
    def geo_ip(self):
        """Get IP geolocation information"""
        self._loading("Fetching IP geolocation")
        
        geo = {}
        
        try:
            ip = socket.gethostbyname(self.domain)
            geo['IP Address'] = ip
            
            # Try ip-api.com (free, no API key needed)
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    if data['status'] == 'success':
                        geo['Country'] = data.get('country', 'N/A')
                        geo['Region'] = data.get('regionName', 'N/A')
                        geo['City'] = data.get('city', 'N/A')
                        geo['ZIP Code'] = data.get('zip', 'N/A')
                        geo['Latitude'] = data.get('lat', 'N/A')
                        geo['Longitude'] = data.get('lon', 'N/A')
                        geo['ISP'] = data.get('isp', 'N/A')
                        geo['Organization'] = data.get('org', 'N/A')
                        geo['AS Number'] = data.get('as', 'N/A')
                        geo['Timezone'] = data.get('timezone', 'N/A')
                        geo['Hosting'] = 'Yes (datacenter)' if data.get('hosting', False) else 'No'
                    else:
                        geo['Note'] = f"API returned: {data.get('message', 'unknown error')}"
            except:
                geo['Note'] = "Geolocation API unavailable"
            
            self.results['geo'] = geo
            self._loading("IP geolocation complete", done=True)
            
        except Exception as e:
            self._loading(f"Geolocation: {str(e)[:30]}", done=True)
    
    # ========== FEATURE 14: SCREENSHOT (if available) ==========
    def website_screenshot(self):
        """Take screenshot using Selenium if available"""
        self._loading("Attempting website screenshot")
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            opts = Options()
            opts.add_argument('--headless')
            opts.add_argument('--no-sandbox')
            opts.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=opts)
            driver.get(f"https://{self.domain}")
            driver.save_screenshot(f"recon_{self.domain.replace('.', '_')}.png")
            driver.quit()
            
            self.results['screenshot'] = f"Screenshot saved: recon_{self.domain.replace('.', '_')}.png"
            self._loading(f"Screenshot saved successfully", done=True)
            
        except ImportError:
            self.results['screenshot'] = "Selenium not installed (pip install selenium)"
            self._loading("Screenshot: Selenium not available", done=True)
        except Exception as e:
            self.results['screenshot'] = f"Screenshot failed: {str(e)[:30]}"
            self._loading("Screenshot failed", done=True)
    
    # ========== FEATURE 15: PERFORMANCE / RESPONSE TIME ==========
    def performance_check(self):
        """Measure response times and server performance"""
        self._loading("Measuring server performance")
        
        perf = {}
        
        try:
            times = []
            for i in range(5):  # 5 requests
                start = time.time()
                r = self.session.get(f"https://{self.domain}", timeout=10, verify=False)
                elapsed = time.time() - start
                times.append(elapsed)
            
            perf['Min Response Time'] = f"{min(times):.3f}s"
            perf['Max Response Time'] = f"{max(times):.3f}s"
            perf['Avg Response Time'] = f"{sum(times)/len(times):.3f}s"
            perf['Response Size'] = f"{len(r.content):,} bytes"
            perf['HTTP Version'] = r.raw.version if hasattr(r.raw, 'version') else 'Unknown'
            
            # Also check if server has keep-alive
            if 'Connection' in r.headers:
                perf['Connection'] = r.headers['Connection']
            elif 'Proxy-Connection' in r.headers:
                perf['Connection'] = r.headers['Proxy-Connection']
            
            # Check for gzip
            if 'Content-Encoding' in r.headers:
                perf['Compression'] = r.headers['Content-Encoding']
            
            self.results['performance'] = perf
            self._loading("Performance check complete", done=True)
            
        except Exception as e:
            self._loading(f"Performance check: {str(e)[:30]}", done=True)
    
    # ========== RUN ALL RECONNAISSANCE ==========
    def run_all(self):
        """Run all recon modules"""
        print(f"\n  {C.Y}{C.bold}[+] TARGET: {self.domain}{C.N}")
        print(f"  {C.dim}[+] Starting full reconnaissance...{C.N}")
        print(f"  {C.dim}{'─'*50}{C.N}\n")
        
        # Run all features with progress
        features = [
            ('DNS Reconnaissance', self.dns_recon, '🌐'),
            ('Port Scanning', self.port_scan, '🔌'),
            ('HTTP Headers & Tech', self.http_recon, '📋'),
            ('SSL/TLS Analysis', self.ssl_analysis, '🔒'),
            ('Directory Fuzzing', self.directory_fuzzing, '📁'),
            ('Subdomain Enumeration', self.subdomain_enum, '🌍'),
            ('Technology Detection', self.tech_detection, '💻'),
            ('Email Extraction', self.email_extraction, '📧'),
            ('Social Links', self.social_links, '🔗'),
            ('Robots & Sitemap', self.robots_sitemap, '🤖'),
            ('Security Audit', self.security_audit, '🛡️'),
            ('IP Geolocation', self.geo_ip, '📍'),
            ('Performance Check', self.performance_check, '⚡'),
            ('WHOIS Lookup', self.whois_lookup, '📄'),
        ]
        
        # Ask which features to run
        print(f"  {C.Y}Select modules to run:{C.N}")
        print(f"  {C.dim}  1-14: Run all 14 features{C.N}")
        print(f"  {C.dim}  Or specify comma-separated: 1,3,5{C.N}")
        print()
        
        choice = input(f"  {C.G}[?]{C.N} Run all? (yes/no): {C.C}").strip().lower()
        print(C.N, end="")
        
        run_all = (choice == 'yes' or choice == 'y' or choice == '')
        
        if run_all:
            for name, func, icon in features:
                print()
                func()
        else:
            selected = input(f"  {C.G}[?]{C.N} Enter feature numbers (comma-separated): {C.C}").strip()
            print(C.N, end="")
            
            try:
                indices = [int(x.strip()) for x in selected.split(',') if x.strip().isdigit()]
                for idx in indices:
                    if 1 <= idx <= len(features):
                        name, func, icon = features[idx - 1]
                        print()
                        func()
            except:
                print(f"  {C.R}[!] Invalid selection, running all{C.N}")
                for name, func, icon in features:
                    print()
                    func()
        
        # Generate report
        self.generate_report()


    # ========== GENERATE REPORT ==========
    def generate_report(self):
        """Generate and display comprehensive report"""
        elapsed = time.time() - self.start_time
        
        print(f"\n\n{C.G}{'='*55}{C.N}")
        print(f"{C.bold}{C.Y}   🎯 RECONNAISSANCE COMPLETE 🎯{C.N}")
        print(f"{C.G}{'='*55}{C.N}")
        print(f"  {C.dim}Target: {self.domain}{C.N}")
        print(f"  {C.dim}Duration: {elapsed:.1f}s{C.N}")
        print(f"  {C.dim}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.N}")
        print(f"{C.G}{'='*55}{C.N}\n")
        
        # Display all results
        # 1. DNS
        if 'dns' in self.results:
            self._print_section("DNS RECORDS", self.results['dns'], "🌐")
        
        # 2. Ports
        if 'ports' in self.results:
            ports_dict = {}
            for port, service in self.results['ports']:
                ports_dict[f"Port {port}"] = f"{service.upper()}"
            self._print_section(f"OPEN PORTS ({len(self.results['ports'])})", ports_dict, "🔌")
        
        # 3. HTTP
        if 'http' in self.results:
            http = self.results['http']
            display = {}
            for k in ['Status Code', 'Final URL', 'Server', 'Technologies Detected']:
                if k in http:
                    display[k] = http[k]
            self._print_section("HTTP INFO", display, "📋")
            
            if 'Security Headers Present' in http and http['Security Headers Present']:
                self._print_section("SECURITY HEADERS (Present)", http['Security Headers Present'])
            if 'Security Headers Missing' in http and http['Security Headers Missing']:
                self._print_section("SECURITY HEADERS (MISSING!)", http['Security Headers Missing'], "⚠️")
        
        # 4. SSL
        if 'ssl' in self.results:
            self._print_section("SSL/TLS CERTIFICATE", self.results['ssl'], "🔒")
        
        # 5. Directories
        if 'directories' in self.results:
            dirs = self.results['directories']
            if dirs.get('directories'):
                self._print_section(f"DIRECTORIES FOUND ({len(dirs['directories'])})", dirs['directories'], "📁")
            if dirs.get('files'):
                self._print_section(f"FILES FOUND ({len(dirs['files'])})", dirs['files'])
        
        # 6. Subdomains
        if 'subdomains' in self.results:
            subs = self.results['subdomains']
            if subs:
                sub_dict = {f"{s[0]}.{self.domain}": s[1] for s in subs[:30]}
                self._print_section(f"SUBDOMAINS ({len(subs)})", sub_dict, "🌍")
        
        # 7. Technologies
        if 'technologies' in self.results:
            self._print_section("TECHNOLOGY STACK", self.results['technologies'], "💻")
        
        # 8. Emails
        if 'emails' in self.results and self.results['emails']:
            self._print_section(f"EMAIL ADDRESSES ({len(self.results['emails'])})", self.results['emails'], "📧")
        
        # 9. Social links
        if 'social' in self.results and self.results['social']:
            social_display = {}
            for platform, links in self.results['social'].items():
                social_display[platform] = links[0] if links else 'Found'
            self._print_section("SOCIAL MEDIA", social_display, "🔗")
        
        # 10. Robots/Sitemap
        if 'robots_sitemap' in self.results:
            self._print_section("ROBOTS & SITEMAP", self.results['robots_sitemap'], "🤖")
        
        # 11. Security
        if 'security' in self.results:
            sec = self.results['security']
            if 'security_score' in sec:
                print(f"\n  {C.Y}🛡️ {C.bold}SECURITY AUDIT SUMMARY{C.N}")
                print(f"  {C.dim}{'─'*50}{C.N}")
                print(f"  {C.C}├─{C.N} Score: {C.bold}{sec['security_score']}{C.N}")
                if 'high_risk_issues' in sec and sec['high_risk_issues']:
                    for issue in sec['high_risk_issues']:
                        print(f"  {C.R}├─⚠ {issue}{C.N}")
                if 'ssl_protocol' in sec:
                    print(f"  {C.C}├─{C.N} SSL Protocol: {sec['ssl_protocol']}{C.N}")
                if 'ssl_warning' in sec:
                    print(f"  {C.R}├─⚠ {sec['ssl_warning']}{C.N}")
        
        # 12. Geolocation
        if 'geo' in self.results:
            self._print_section("IP GEOLOCATION", self.results['geo'], "📍")
        
        # 13. Performance
        if 'performance' in self.results:
            self._print_section("PERFORMANCE", self.results['performance'], "⚡")
        
        # 14. WHOIS
        if 'whois' in self.results:
            self._print_section("WHOIS INFO", self.results['whois'], "📄")
        
        # 15. Screenshot
        if 'screenshot' in self.results:
            print(f"\n  {C.M}📸 {C.bold}SCREENSHOT{C.N}")
            print(f"  {C.dim}{'─'*50}{C.N}")
            print(f"  {C.W}{self.results['screenshot']}{C.N}")
        
        # Final summary
        print(f"\n{C.G}{'='*55}{C.N}")
        summary_items = []
        if 'dns' in self.results:
            summary_items.append(f"{len(self.results['dns'])} DNS records")
        if 'ports' in self.results:
            summary_items.append(f"{len(self.results['ports'])} open ports")
        if 'subdomains' in self.results:
            summary_items.append(f"{len(self.results['subdomains'])} subdomains")
        if 'emails' in self.results:
            summary_items.append(f"{len(self.results['emails'])} emails")
        if 'directories' in self.results:
            dirs = self.results['directories']
            total_dirs = len(dirs.get('directories', [])) + len(dirs.get('files', []))
            if total_dirs:
                summary_items.append(f"{total_dirs} paths")
        
        print(f"  {C.Y}Summary: {', '.join(summary_items)}{C.N}")
        print(f"  {C.dim}Total scan time: {elapsed:.1f}s{C.N}")
        print(f"{C.G}{'='*55}{C.N}")
        
        # Save report option
        print()
        save = input(f"  {C.G}[?]{C.N} Save report to file? (yes/no): {C.C}").strip().lower()
        print(C.N, end="")
        
        if save == 'yes' or save == 'y':
            filename = f"recon_{self.domain.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Recon Report: {self.domain}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Duration: {elapsed:.1f}s\n")
                f.write("="*60 + "\n\n")
                f.write(json.dumps(self.results, indent=2, default=str))
            print(f"\n  {C.G}[✓]{C.N} Report saved to: {C.W}{filename}{C.N}")
        
        print(f"\n  {C.dim}Press Enter to exit...{C.N}")
        input()


# ================================================================
# 🚀 MAIN
# ================================================================
def main():
    print_banner()
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        print(f"\n  {C.Y}Enter target domain/IP:{C.N}")
        target = input(f"  {C.G}[?]{C.N} Target: {C.C}").strip()
        print(C.N, end="")
    
    if not target:
        print(f"\n  {C.R}[!] No target specified!{C.N}")
        sys.exit(1)
    
    # Create engine and run
    recon = ReconEngine(target)
    recon.run_all()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.R}[!] Scan interrupted by user{C.N}")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {C.R}[!] Fatal error: {e}{C.N}")
        import traceback
        traceback.print_exc()
        sys.exit(1)