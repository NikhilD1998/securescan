# 🔒 SecureScan

> A modular, multi-threaded network reconnaissance and HTTP security scanner built in Python.

SecureScan is a Python-based security scanner designed to perform fast TCP port scanning, service enumeration, HTTP analysis, technology fingerprinting, and basic web security assessment. It combines low-level socket programming with application-layer reconnaissance to provide a comprehensive overview of exposed services on a target.

> **Disclaimer:** This tool is intended for educational purposes and authorized security testing only. Do not scan systems without explicit permission.

---

# Features

## Network Scanning

- Multi-threaded TCP Connect Port Scanner
- Configurable thread pool
- Custom timeout support
- Fast concurrent scanning
- Service identification using well-known ports

---

## Banner Grabbing

Supports banner collection from common services including:

- HTTP
- HTTPS
- FTP
- SSH
- SMTP
- POP3
- IMAP
- IMAPS
- POP3S

Extracts:

- Protocol
- Software
- Version
- Platform (when available)

---

## HTTP Enumeration

Automatically performs HTTP enumeration for web servers.

Collects:

- Page Title
- Server Header
- X-Powered-By
- Cookies
- Redirect Location
- Response Headers
- HTML Body

---

## Security Header Analysis

Checks for missing security headers including:

- Strict-Transport-Security (HSTS)
- Content-Security-Policy (CSP)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

Generates findings with:

- Severity
- Description
- Recommendation

---

## Technology Fingerprinting

Detects common technologies used by the target.

### Web Servers

- Nginx
- Apache
- IIS
- LiteSpeed
- Caddy
- OpenResty
- Gunicorn
- Uvicorn
- Tomcat

### Backend Frameworks

- Express.js
- Django
- Flask
- Laravel
- Spring Boot
- ASP.NET
- PHP

### Frontend Frameworks

- React
- Vue
- Angular
- Next.js
- Nuxt
- Gatsby
- Svelte

### CMS Detection

- WordPress
- Joomla
- Drupal
- Ghost

### CDN Detection

- Cloudflare
- CloudFront
- Fastly
- Akamai
- Vercel
- Netlify
- BunnyCDN
- Azure Front Door

---

## Web Reconnaissance

Performs lightweight reconnaissance including:

### Interesting Paths

Attempts discovery of:

- robots.txt
- security.txt
- sitemap.xml
- favicon.ico
- /admin
- /login
- /dashboard
- /api
- /graphql
- /phpmyadmin

---

### HTTP Methods

Discovers supported HTTP methods using:

- OPTIONS
- Allow Header
- Public Header

---

### Redirect Detection

Checks for:

- HTTP Redirects
- Redirect Location
- Redirect Status Code

---

### Header Enumeration

Extracts important response headers including:

- Server
- Content-Type
- Content-Length
- Cache-Control
- Last-Modified
- ETag
- HSTS
- CSP
- CORS Headers

---

### Favicon Analysis

Collects:

- MD5 Hash
- SHA1 Hash
- SHA256 Hash
- File Size

---

## Reporting

Generates structured JSON reports containing:

- Target Information
- Scan Statistics
- Open Ports
- Service Details
- HTTP Enumeration
- Security Findings
- Fingerprinting Results
- Web Recon Results

---

# Architecture

```text
                     +----------------+
                     |     CLI        |
                     +-------+--------+
                             |
                             |
                     +-------v--------+
                     | Port Scanner   |
                     +-------+--------+
                             |
               +-------------+-------------+
               |                           |
      +--------v-------+          +--------v--------+
      | Worker Threads |          | Banner Grabber  |
      +--------+-------+          +--------+--------+
               |                           |
               +-------------+-------------+
                             |
                     +-------v--------+
                     | Banner Parser  |
                     +-------+--------+
                             |
             +---------------+----------------+
             |                                |
      +------v------+                  +-------v-------+
      | HTTP Enum   |                  | Service Info  |
      +------+------+
             |
      +------+-------------------------------+
      |                                      |
+-----v------+                     +----------v---------+
| Analyzer   |                     | Fingerprinting     |
+-----+------+                     +----------+---------+
      |                                        |
      +----------------------+-----------------+
                             |
                      +------v-------+
                      | Web Recon    |
                      +------+-------+
                             |
                      +------v-------+
                      | JSON Report  |
                      +--------------+
```

---

# Project Structure

```text
SecureScan/

├── main.py
├── requirements.txt
│
├── scanner/
│   ├── cli.py
│   ├── config.py
│   ├── port_scanner.py
│   ├── worker.py
│   ├── enumerator.py
│   ├── services.py
│   ├── utils.py
│   │
│   ├── http/
│   │   ├── client.py
│   │   └── response.py
│   │
│   ├── parser/
│   │   ├── banner_parser.py
│   │   ├── http_parser.py
│   │   └── ssh_parser.py
│   │
│   ├── analyzers/
│   │   └── http_analyzer.py
│   │
│   ├── fingerprint/
│   │   ├── detector.py
│   │   ├── servers.py
│   │   ├── frameworks.py
│   │   ├── frontend.py
│   │   ├── cms.py
│   │   └── cdn.py
│   │
│   ├── recon/
│   │   ├── detector.py
│   │   ├── paths.py
│   │   ├── methods.py
│   │   ├── redirects.py
│   │   ├── headers.py
│   │   └── favicon.py
│   │
│   ├── reports/
│   │   ├── json.py
│   │   ├── html.py
│   │   └── markdown.py
│   │
│   └── models/
│       └── finding.py
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/securescan.git
```

Navigate into the project

```bash
cd securescan
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

Scan common ports

```bash
python main.py example.com
```

Scan a custom range

```bash
python main.py example.com -p 1-1024
```

Scan a single port

```bash
python main.py example.com -p 80
```

---

# Example Output

```text
Target : example.com
Resolved IP : 93.184.216.34

Open Ports

80/tcp   HTTP
443/tcp  HTTPS

Technology

Server      : Nginx
Backend     : Express.js
Frontend    : React

Security Findings

[Medium] Missing HSTS
[Medium] Missing CSP
[Low] Missing X-Content-Type-Options
```

---

# JSON Report

A JSON report is generated after every scan.

Example:

```json
{
  "target": "example.com",
  "ip": "93.184.216.34",
  "scan_time": 2.31,
  "open_ports": [
    {
      "port": 80,
      "service": "http"
    }
  ]
}
```

---

# Technologies Used

- Python 3
- Socket Programming
- ThreadPoolExecutor
- SSL
- Dataclasses
- Rich
- JSON

---

# Future Improvements

- HTTPS Enumeration
- TLS Certificate Analysis
- SSL Cipher Detection
- UDP Scanning
- SYN Scan
- OS Fingerprinting
- HTML Reports
- Markdown Reports
- XML Export
- CLI Improvements
- Plugin System
- CVE Detection
- Vulnerability Database Integration

---

# Learning Objectives

This project was built to gain hands-on experience with:

- Network Programming
- TCP/IP
- HTTP Protocol
- Socket Programming
- Concurrent Programming
- Security Enumeration
- Web Reconnaissance
- Technology Fingerprinting
- Report Generation
- Software Architecture

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

SecureScan was inspired by industry-standard reconnaissance tools including:

- Nmap
- Netcat
- WhatWeb
- Wappalyzer
- httpx
- Nikto

The project is an educational implementation designed to understand how network scanners and reconnaissance tools work internally rather than to replace them.

---

# Author

**Nikhil Dada**

Backend Developer • React Native Developer • Cybersecurity Enthusiast

If you found this project useful, consider giving it a ⭐ on GitHub.
