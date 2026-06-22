#!/usr/bin/env python3
"""
.onion URL Validator through Tor Network
Validates if a .onion hidden service is reachable
"""
import sys
import time
import socket
import warnings
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try to import dependencies
try:
    import requests
    import socks
except ImportError as e:
    print(f"Error: Missing dependency - {e}")
    print("\nInstall dependencies:")
    print("   pip install -r requirements.txt")
    print("   or")
    print("   pip install requests pysocks")
    sys.exit(1)

warnings.filterwarnings('ignore')

# ============================================
# .ONION URL VALIDATOR THROUGH TOR NETWORK
# ============================================

def is_valid_onion_url(url):
    """Check if a given URL appears to be a valid .onion address."""
    try:
        parsed = urlparse(url)
        if not parsed.hostname:
            return False
        return parsed.hostname.endswith('.onion')
    except Exception:
        return False

def get_tor_port():
    """Get the working Tor port."""
    for port in [9150, 9050]:
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(0.5)
            result = test_socket.connect_ex(('127.0.0.1', port))
            test_socket.close()
            if result == 0:
                return port
        except Exception:
            continue
    return None

def extract_page_info(html_content):
    """Extract title, description, and other meta information from HTML."""
    info = {
        'title': 'Not found',
        'description': 'Not found',
        'keywords': 'Not found',
        'author': 'Not found',
        'language': 'Not found',
        'robots': 'Not found',
        'og_title': 'Not found',
        'og_description': 'Not found',
        'og_site_name': 'Not found',
        'h1_heading': 'Not found',
        'links_count': 0,
        'images_count': 0,
        'scripts_count': 0,
        'forms_count': 0,
        'has_login_form': False
    }
    
    if not html_content:
        return info
    
    # Extract title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        info['title'] = title_match.group(1).strip()[:200]
    
    # Extract meta description
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if desc_match:
        info['description'] = desc_match.group(1).strip()[:300]
    else:
        desc_match2 = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\'][^>]*>', html_content, re.IGNORECASE)
        if desc_match2:
            info['description'] = desc_match2.group(1).strip()[:300]
    
    # Extract meta keywords
    keywords_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if keywords_match:
        info['keywords'] = keywords_match.group(1).strip()[:200]
    
    # Extract meta author
    author_match = re.search(r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if author_match:
        info['author'] = author_match.group(1).strip()
    
    # Extract language
    lang_match = re.search(r'<html[^>]*lang=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if lang_match:
        info['language'] = lang_match.group(1).strip()
    
    # Extract robots
    robots_match = re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if robots_match:
        info['robots'] = robots_match.group(1).strip()
    
    # Extract Open Graph title
    og_title_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if og_title_match:
        info['og_title'] = og_title_match.group(1).strip()[:200]
    
    # Extract Open Graph description
    og_desc_match = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if og_desc_match:
        info['og_description'] = og_desc_match.group(1).strip()[:300]
    
    # Extract Open Graph site name
    og_site_match = re.search(r'<meta[^>]*property=["\']og:site_name["\'][^>]*content=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE)
    if og_site_match:
        info['og_site_name'] = og_site_match.group(1).strip()
    
    # Extract first H1 heading
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        info['h1_heading'] = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()[:200]
    
    # Count links
    info['links_count'] = len(re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE))
    
    # Count images
    info['images_count'] = len(re.findall(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*>', html_content, re.IGNORECASE))
    
    # Count scripts
    info['scripts_count'] = len(re.findall(r'<script[^>]*>', html_content, re.IGNORECASE))
    
    # Count forms
    info['forms_count'] = len(re.findall(r'<form[^>]*>', html_content, re.IGNORECASE))
    
    # Check for login forms
    if re.search(r'<form[^>]*>.*?(?:password|login|signin|user|email).*?</form>', html_content, re.IGNORECASE | re.DOTALL):
        info['has_login_form'] = True
    
    return info

def try_protocol(url, proxy, timeout=15):
    """Try a single protocol with short timeout."""
    try:
        start_time = time.time()
        
        response = requests.get(
            url,
            proxies=proxy,
            timeout=timeout,
            verify=False,
            allow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Connection': 'close',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            },
            stream=True
        )
        
        end_time = time.time()
        
        # Get content
        content = response.content
        
        if response.status_code < 500:
            # Extract page info
            page_info = extract_page_info(content.decode('utf-8', errors='ignore'))
            
            return {
                'success': True,
                'protocol': urlparse(url).scheme,
                'status_code': response.status_code,
                'response_time': round(end_time - start_time, 2),
                'headers': dict(response.headers),
                'final_url': response.url,
                'content_length': len(content),
                'content_type': response.headers.get('Content-Type', 'unknown'),
                'server': response.headers.get('Server', 'unknown'),
                'page_info': page_info
            }
        else:
            return {
                'success': False,
                'protocol': urlparse(url).scheme,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }
            
    except requests.exceptions.ConnectTimeout:
        return {'success': False, 'protocol': urlparse(url).scheme, 'error': 'Connection timeout'}
    except requests.exceptions.ReadTimeout:
        return {'success': False, 'protocol': urlparse(url).scheme, 'error': 'Read timeout'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'protocol': urlparse(url).scheme, 'error': 'Connection error'}
    except requests.exceptions.SSLError:
        return {'success': False, 'protocol': urlparse(url).scheme, 'error': 'SSL error'}
    except Exception as e:
        return {'success': False, 'protocol': urlparse(url).scheme, 'error': str(e)}

def validate_onion_url(onion_url, timeout=20):
    """
    Validate .onion URL by trying both HTTP and HTTPS.
    Auto-detects Tor port.
    """
    if not is_valid_onion_url(onion_url):
        return False, f"Invalid .onion URL format: {onion_url}", {}

    # Get Tor port
    tor_port = get_tor_port()
    if tor_port is None:
        return False, "Tor not running. Please start Tor Browser or Tor service.", {}
    
    tor_proxy = f"socks5h://127.0.0.1:{tor_port}"
    
    proxies = {
        'http': tor_proxy,
        'https': tor_proxy,
    }

    details = {
        'url': onion_url,
        'proxy': tor_proxy,
        'tor_port': tor_port,
        'attempts': [],
        'response_time': None,
        'status_code': None,
        'protocol_used': None,
        'final_url': None,
        'content_length': None,
        'content_type': None,
        'server': None,
        'headers': None,
        'page_info': None
    }

    parsed = urlparse(onion_url)
    
    # Build URLs to try (both HTTP and HTTPS)
    urls_to_try = []
    if parsed.scheme == 'https':
        urls_to_try.append(onion_url)
        urls_to_try.append(onion_url.replace('https://', 'http://'))
    else:
        urls_to_try.append(onion_url)
        urls_to_try.append(onion_url.replace('http://', 'https://'))

    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_url = {
            executor.submit(try_protocol, url, proxies, timeout): url 
            for url in urls_to_try
        }
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                details['attempts'].append(result)
                
                if result.get('success'):
                    details['protocol_used'] = result['protocol']
                    details['status_code'] = result['status_code']
                    details['response_time'] = result['response_time']
                    details['headers'] = result.get('headers', {})
                    details['final_url'] = result.get('final_url')
                    details['content_length'] = result.get('content_length')
                    details['content_type'] = result.get('content_type')
                    details['server'] = result.get('server')
                    details['page_info'] = result.get('page_info')
                    
                    end_total = time.time()
                    details['total_time'] = round(end_total - start_total, 2)
                    
                    return True, f"Reachable with {result['protocol'].upper()} (HTTP {result['status_code']})", details
                    
            except Exception:
                continue
    
    end_total = time.time()
    details['total_time'] = round(end_total - start_total, 2)
    
    if details['attempts']:
        for attempt in details['attempts']:
            if attempt.get('error'):
                return False, f"Failed: {attempt.get('error')}", details
        return False, "All connection attempts failed", details
    
    return False, "All connection attempts failed", details

def print_results(url, reachable, message, details):
    """Print results in a formatted way with more details."""
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    
    print(f"\nURL: {url}")
    print(f"Status: {'REACHABLE' if reachable else 'NOT REACHABLE'}")
    print(f"Message: {message}")
    
    if details:
        print("\nDetails:")
        if details.get('tor_port'):
            print(f"   Tor Port: {details['tor_port']}")
        if details.get('protocol_used'):
            print(f"   Protocol: {details['protocol_used'].upper()}")
        if details.get('status_code'):
            print(f"   HTTP Status: {details['status_code']}")
        if details.get('response_time'):
            print(f"   Response Time: {details['response_time']}s")
        if details.get('total_time'):
            print(f"   Total Time: {details['total_time']}s")
        
        # Show extra details when successful
        if reachable:
            print("\n   Extra Information:")
            if details.get('final_url') and details['final_url'] != url:
                print(f"      Final URL: {details['final_url']}")
            if details.get('content_length'):
                size_kb = details['content_length'] / 1024
                if size_kb > 1024:
                    print(f"      Content Size: {size_kb/1024:.2f} MB ({details['content_length']} bytes)")
                else:
                    print(f"      Content Size: {size_kb:.2f} KB ({details['content_length']} bytes)")
            if details.get('content_type'):
                print(f"      Content Type: {details['content_type']}")
            if details.get('server') and details['server'] != 'unknown':
                print(f"      Server: {details['server']}")
            
            # Print page information
            page_info = details.get('page_info')
            if page_info:
                print("\n   Page Information:")
                if page_info.get('title') and page_info['title'] != 'Not found':
                    print(f"      Title: {page_info['title']}")
                if page_info.get('description') and page_info['description'] != 'Not found':
                    print(f"      Description: {page_info['description']}")
                if page_info.get('keywords') and page_info['keywords'] != 'Not found':
                    print(f"      Keywords: {page_info['keywords']}")
                if page_info.get('og_title') and page_info['og_title'] != 'Not found':
                    print(f"      OG Title: {page_info['og_title']}")
                if page_info.get('og_description') and page_info['og_description'] != 'Not found':
                    print(f"      OG Description: {page_info['og_description']}")
                if page_info.get('og_site_name') and page_info['og_site_name'] != 'Not found':
                    print(f"      Site Name: {page_info['og_site_name']}")
                if page_info.get('author') and page_info['author'] != 'Not found':
                    print(f"      Author: {page_info['author']}")
                if page_info.get('language') and page_info['language'] != 'Not found':
                    print(f"      Language: {page_info['language']}")
                if page_info.get('h1_heading') and page_info['h1_heading'] != 'Not found':
                    print(f"      Main Heading (H1): {page_info['h1_heading']}")
                
                # Show statistics
                print(f"\n   Page Statistics:")
                print(f"      Links: {page_info.get('links_count', 0)}")
                print(f"      Images: {page_info.get('images_count', 0)}")
                print(f"      Scripts: {page_info.get('scripts_count', 0)}")
                print(f"      Forms: {page_info.get('forms_count', 0)}")
                if page_info.get('has_login_form'):
                    print(f"      Login Form: YES")
                else:
                    print(f"      Login Form: NO")
            
            if details.get('headers'):
                print("\n   Headers:")
                for key, value in list(details['headers'].items())[:8]:
                    print(f"      {key}: {value}")
        
        # Show attempts
        if details.get('attempts'):
            print("\n   Attempts:")
            for attempt in details['attempts']:
                status = "SUCCESS" if attempt.get('success') else "FAILED"
                protocol = attempt.get('protocol', 'unknown').upper()
                error = attempt.get('error', '')
                status_code = attempt.get('status_code', '')
                response_time = attempt.get('response_time', '')
                if status_code:
                    print(f"      {status} {protocol}: HTTP {status_code} ({response_time}s)")
                elif error:
                    print(f"      {status} {protocol}: {error}")
                else:
                    print(f"      {status} {protocol}")
    print("="*70)

def main():
    """Main function."""
    print("\n" + "="*70)
    print(".ONION URL VALIDATOR - TOR NETWORK")
    print("="*70)
    
    # Check Tor
    print("\nChecking Tor...")
    tor_port = get_tor_port()
    
    if tor_port:
        print(f"Tor detected on port {tor_port}")
        if tor_port == 9150:
            print("   Using Tor Browser port (recommended)")
        else:
            print("   Using Tor daemon port")
    else:
        print("Tor is NOT running on ports 9050 or 9150")
        print("\nStart Tor with:")
        print("   - Windows: Run Tor Browser (port 9150) - RECOMMENDED")
        print("   - Linux:   sudo systemctl start tor (port 9050)")
        print("   - macOS:   brew services start tor (port 9050)")
        return
    
    print("\n" + "="*70)
    print("\nEnter the .onion URL to validate")
    print("   Example: http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion")
    print("   Type 'exit' to quit")
    print("-"*70)
    
    while True:
        url = input("\nURL: ").strip()
        
        if url.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye! Stay safe on the dark web.")
            break
        
        if not url:
            print("No URL entered.")
            continue
            
        if not url.startswith(('http://', 'https://')):
            print("Adding 'http://' automatically...")
            url = 'http://' + url
        
        print("\nValidating...")
        reachable, message, details = validate_onion_url(url)
        print_results(url, reachable, message, details)
        
        if not reachable:
            print("\nTips:")
            print("  1. Make sure Tor Browser is running (port 9150)")
            print("  2. Try http:// instead of https://")
            print("  3. Service might be temporarily down")
            print("  4. Some .onion services are very slow")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        print(f"\nValidating: {url}")
        print("="*50)
        
        reachable, message, details = validate_onion_url(url)
        print_results(url, reachable, message, details)
        
        if not reachable:
            print("\nTry: http:// instead of https://")
            print("   Make sure Tor Browser is running on port 9150")
    else:
        main()
