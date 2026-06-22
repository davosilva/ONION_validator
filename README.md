# 🌐 Onion URL Validator - Tor Network Service Checker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/Requests-2.28.0+-orange.svg)](https://requests.readthedocs.io/)

## 📋 Overview

**Onion URL Validator** is a Python tool that validates whether a `.onion` hidden service is reachable through the Tor network. It automatically detects your Tor proxy (supports both Tor Browser and Tor daemon), tests both HTTP and HTTPS protocols in parallel, and provides detailed information about the service, including page metadata and statistics.

---

## 🎯 Features

* ✅ Automatic Tor detection (ports 9050 and 9150)
* ✅ Parallel HTTP/HTTPS testing
* ✅ Detailed page information extraction
* ✅ Fast validation with configurable timeout
* ✅ Interactive and CLI modes
* ✅ Detailed response metrics
* ✅ Minimal dependencies (`requests` and `pysocks`)

---

## 📊 Example Output

```text
======================================================================
VALIDATION RESULTS
======================================================================

URL: http://example.onion
Status: REACHABLE
Message: Reachable with HTTP (HTTP 200)

Details:
Tor Port: 9150
Protocol: HTTP
HTTP Status: 200
Response Time: 0.76s

Page Information:
Title: Example Onion Service
Description: Sample hidden service

Page Statistics:
Links: 15
Images: 3
Scripts: 2
Forms: 1

Attempts:
FAILED HTTPS: Connection error
SUCCESS HTTP: HTTP 200 (0.76s)
======================================================================
```

---

## 🚀 Installation

### Prerequisites

* Python 3.8+
* Tor Browser or Tor daemon running

### 1. Clone the Repository

```bash
git clone https://github.com/davosilva/onion-validator.git
cd onion-validator
```

### 2. Create a Virtual Environment (Optional)

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Tor Service

#### Linux

```bash
sudo systemctl start tor
```

#### macOS

```bash
brew services start tor
```

#### Windows

Run Tor Browser.

---

## 💻 Usage

### Interactive Mode

```bash
python onion_validator.py
```

Example:

```text
Enter the .onion URL to validate
Example: http://example.onion
Type 'exit' to quit
```

### Command Line Mode

```bash
python onion_validator.py http://example.onion
```

### Examples

```bash
# Validate with HTTP
python onion_validator.py http://example.onion

# Validate with HTTPS
python onion_validator.py https://example.onion

# Without protocol (auto-adds HTTP)
python onion_validator.py example.onion
```

---

## 📦 Requirements

### requirements.txt

```txt
requests>=2.28.0
pysocks>=1.7.0

# Optional
urllib3>=1.26.0
certifi>=2022.12.07

# Development
pytest>=7.0.0
```

Install:

```bash
pip install -r requirements.txt
```

---

## 🔧 How It Works

1. **Tor Detection** – Detects Tor on ports 9050 and 9150.
2. **Protocol Testing** – Tests HTTP and HTTPS in parallel.
3. **Page Analysis** – Extracts metadata and statistics.
4. **Results Display** – Shows response details and timing.

---

## 🛡️ Security Features

* ✅ No data storage
* ✅ Supports self-signed certificates
* ✅ Automatic connection cleanup
* ✅ Stream-based requests

---

## 📊 Extracted Page Information

| Information    | Description            |
| -------------- | ---------------------- |
| Title          | HTML page title        |
| Description    | Meta description       |
| Keywords       | Meta keywords          |
| OG Title       | Open Graph title       |
| OG Description | Open Graph description |
| Author         | Meta author            |
| Language       | HTML language          |
| H1 Heading     | First H1 tag           |
| Links          | Number of links        |
| Images         | Number of images       |
| Scripts        | Number of scripts      |
| Forms          | Number of forms        |
| Login Form     | Login form detected    |

---

## 🧪 Testing

```bash
# DuckDuckGo
python onion_validator.py https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/

# Facebook
python onion_validator.py https://facebookcorewwwi.onion/
```

---

## 🔧 Troubleshooting

| Issue              | Solution                         |
| ------------------ | -------------------------------- |
| Tor not detected   | Start Tor Browser or Tor service |
| Connection timeout | Increase timeout value           |
| SSL errors         | Try HTTP instead of HTTPS        |
| SOCKS errors       | Verify Tor proxy is running      |

---

## 📁 Project Structure

```text
onion-validator/
├── onion_validator.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/AmazingFeature
```

3. Commit changes

```bash
git commit -m "Add AmazingFeature"
```

4. Push changes

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request

---

## ⚠️ Disclaimer

This tool is intended for legitimate security research, accessibility testing, and educational purposes. Users are responsible for ensuring compliance with applicable laws and the terms of service of any systems they access.

---

## 🙏 Acknowledgments

* Tor Project
* Requests
* PySocks

---

## 📧 Contact

- **Author**: [David Silva]
- **GitHub**: [@davosilva](https://github.com/davosilva)
- **Website**: [zioNETMX](https://www.zionet.com.mx)

---

## 🚀 Quick Start

```bash
git clone https://github.com/davosilva/onion-validator.git
cd onion-validator

pip install -r requirements.txt

sudo systemctl start tor

python onion_validator.py http://example.onion
```

Built with ❤️ for the Tor community.

