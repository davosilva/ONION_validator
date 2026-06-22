# 🌐 Onion URL Validator - Tor Network Service Checker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/Requests-2.28.0+-orange.svg)](https://requests.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Overview

**Onion URL Validator** is a Python tool that validates if a `.onion` hidden service is reachable through the Tor network. It automatically detects your Tor proxy (supports both Tor Browser and Tor daemon), tests both HTTP and HTTPS protocols in parallel, and provides detailed information about the service including page metadata and statistics.

## 🎯 Features

- ✅ **Automatic Tor detection** - Detects Tor on ports 9050 (daemon) or 9150 (Tor Browser)
- ✅ **Parallel protocol testing** - Tests HTTP and HTTPS simultaneously for speed
- ✅ **Detailed page information** - Extracts title, description, metadata, and page statistics
- ✅ **Fast validation** - Quick response with configurable timeout
- ✅ **Interactive and CLI modes** - Use interactively or from command line
- ✅ **Detailed results** - Shows response time, headers, and page content information
- ✅ **No external dependencies** - Only requires `requests` and `pysocks`

## 📊 Example Output
======================================================================
VALIDATION RESULTS
======================================================================

URL: http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
Status: REACHABLE
Message: Reachable with HTTP (HTTP 200)

Details:
Tor Port: 9150
Protocol: HTTP
HTTP Status: 200
Response Time: 0.76s
Total Time: 0.76s

Extra Information:
Content Size: 12.34 KB (12634 bytes)
Content Type: text/html
Server: nginx

Page Information:
Title: Example Onion Service
Description: This is a sample hidden service running on Tor network
Keywords: onion, tor, hidden service, example
Language: en
Main Heading (H1): Welcome to the Onion Service

Page Statistics:
Links: 15
Images: 3
Scripts: 2
Forms: 1
Login Form: YES

Headers:
Content-Type: text/html; charset=utf-8
Content-Length: 12634
Server: nginx
Date: Wed, 21 Jun 2026 10:30:45 GMT

Attempts:
FAILED HTTPS: Connection error
SUCCESS HTTP: HTTP 200 (0.76s)
======================================================================

text

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Tor service running (Tor Browser or Tor daemon)

### Step 1: Clone the Repository

```bash
git clone https://github.com/davosilva/onion-validator.git
cd onion-validator
Step 2: Create Virtual Environment (Optional)
bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Start Tor Service
bash
# Windows: Run Tor Browser
# Linux:
sudo systemctl start tor

# macOS:
brew services start tor
💻 Usage
Interactive Mode
bash
python onion_validator.py
Then enter the .onion URL when prompted:

text
Enter the .onion URL to validate
   Example: http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
   Type 'exit' to quit
----------------------------------------------------------------------

URL: http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
Command Line Mode
bash
python onion_validator.py http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
Examples
bash
# Validate with http://
python onion_validator.py http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion

# Validate with https://
python onion_validator.py https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/

# Without protocol (automatically adds http://)
python onion_validator.py juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
📦 Requirements
requirements.txt
txt
# requirements.txt - Dependencies for .onion validator

# Core dependencies for HTTP requests and Tor SOCKS5 proxy
requests>=2.28.0
pysocks>=1.7.0

# Optional - for better performance and additional features
urllib3>=1.26.0
certifi>=2022.12.07

# Optional - for development and testing
pytest>=7.0.0
Install Dependencies
bash
pip install -r requirements.txt
🔧 How It Works
Tor Detection: Scans ports 9050 and 9150 to detect running Tor service

Protocol Testing: Tests both HTTP and HTTPS simultaneously using ThreadPoolExecutor

Page Analysis: If successful, extracts page title, description, metadata, and statistics

Results Display: Shows detailed information including response time, headers, and page content

🛡️ Security Features
✅ No data storage - Does not save any URLs or content

✅ SSL verification disabled - Handles self-signed certificates common on .onion services

✅ Connection close - Closes connections immediately after request

✅ Stream mode - Streams content to avoid memory issues

📊 Extracted Page Information
Information	Description
Title	Page title from <title> tag
Description	Meta description
Keywords	Meta keywords
OG Title	Open Graph title
OG Description	Open Graph description
OG Site Name	Open Graph site name
Author	Meta author
Language	HTML language attribute
H1 Heading	First heading on page
Links	Number of links
Images	Number of images
Scripts	Number of scripts
Forms	Number of forms
Login Form	Whether login form is present
🧪 Testing with Known Onion Services
bash
# DuckDuckGo
python onion_validator.py https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/

# Facebook
python onion_validator.py https://facebookcorewwwi.onion/

# The Hidden Wiki (example)
python onion_validator.py http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6osjiys62w3o6x2ad.onion/
🔧 Troubleshooting
Issue	Solution
Tor not detected	Start Tor Browser or Tor service
Connection timeout	Service may be slow or down, try increasing timeout
SSL errors	Try using http:// instead of https://
SOCKS errors	Check that Tor proxy is running on correct port
📁 Project Structure
text
onion-validator/
├── onion_validator.py   # Main application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── LICENSE             # MIT License
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Disclaimer
This tool is for legitimate security research and testing purposes only. Use responsibly and respect the terms of service of any onion services you validate.

🙏 Acknowledgments
Tor Project - For providing the anonymity network

Requests - For the excellent HTTP library

pysocks - For SOCKS5 proxy support

📧 Contact
Author: davosilva

GitHub: https://github.com/davosilva

🚀 Quick Start
bash
# Clone repository
git clone https://github.com/davosilva/onion-validator.git
cd onion-validator

# Install dependencies
pip install -r requirements.txt

# Start Tor (Linux)
sudo systemctl start tor

# Run validator
python onion_validator.py http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
Built with ❤️ for the Tor community
