# Adaptive Attack Surface Mapper

**Professional Cybersecurity Web Application for Network Security Assessment**

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-Educational-orange)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Performance](#performance)
- [Security](#security)
- [Testing](#testing)
- [Changelog](#changelog)
- [Contributing](#contributing)

---

## 🎯 Overview

The **Adaptive Attack Surface Mapper** is a professional cybersecurity tool designed to perform comprehensive network security assessments. It scans open ports, identifies services, assesses security risks, simulates attack scenarios, and generates detailed reports.

### Purpose
- Identify exposed services and vulnerabilities
- Generate security assessments with professional reports
- Educate about network security risks
- Provide actionable mitigation recommendations

### Target Audience
- Security professionals
- Network administrators
- Educational institutions
- Authorized penetration testers

---

## ✨ Features

### Core Capabilities

#### 1. **Multithreaded Port Scanning**
- Scans ports 1-65535 on target IP
- 200 concurrent threads for optimal performance
- 0.5-second timeout per port
- Customizable port ranges via API
- Service name identification (40+ common services)
- ~418 ports/second scanning speed

#### 2. **Risk Assessment Engine**
- Automatic risk level assignment (HIGH/MEDIUM/LOW)
- 40+ service-specific risk profiles
- Detailed vulnerability explanations
- Professional mitigation recommendations
- Security scoring algorithm (0-100 scale)

#### 3. **Attack Simulation**
- Realistic attacker behavior simulation
- Exploitation path analysis
- Lateral movement vectors
- Data breach scenarios
- Service-specific attack vectors
- 4-7 detailed attack scenarios per scan

#### 4. **Executive Summary**
- Overall security rating system
- Risk breakdown (HIGH/MEDIUM/LOW counts)
- Priority action items
- Color-coded risk indicators
- Professional security assessment

#### 5. **Report Export**
- Comprehensive JSON report generation
- Timestamped filenames
- Complete scan metadata
- Executive summary inclusion
- Attack simulation inclusion
- Actionable recommendations

#### 6. **Web Dashboard**
- Professional cybersecurity UI
- Real-time scanning interface
- Interactive results visualization
- Security score visualization
- Risk breakdown display
- Responsive design (desktop/mobile)

---

## 🏗️ Architecture

### Project Structure

```
p1/
├── app.py                    # Flask backend with routes
├── scanner.py                # Multithreaded port scanner
├── risk_engine.py            # Risk assessment engine
├── templates/
│   └── index.html            # Dashboard UI
├── static/
│   └── style.css             # Professional styling
├── PROJECT_SPEC.md           # Original specifications
└── README.md                 # This file
```

### Component Diagram

```
┌─────────────────────────────────────────────────┐
│         WEB DASHBOARD (index.html)              │
│    Professional Cybersecurity UI Interface      │
└────────────────┬────────────────────────────────┘
                 │ HTTP Requests (JSON)
                 ▼
┌─────────────────────────────────────────────────┐
│         FLASK BACKEND (app.py)                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Route: /          (Dashboard)            │  │
│  │ Route: /scan      (Port Scanning)        │  │
│  │ Route: /export    (Report Generation)    │  │
│  └──────────────────────────────────────────┘  │
└────────┬────────────────────────────────┬───────┘
         │                                │
         ▼                                ▼
   ┌──────────────┐            ┌──────────────────┐
   │ SCANNER.PY   │            │ RISK_ENGINE.PY   │
   ├──────────────┤            ├──────────────────┤
   │ • 200 threads│            │ • Risk scoring   │
   │ • 0.5s timeout           │ • Mitigation     │
   │ • Service ID │            │ • Attack sim     │
   │ • Thread safe│            │ • Report gen     │
   └──────────────┘            └──────────────────┘
```

### Data Flow

```
User Input (IP, Port Range)
    │
    ▼
Input Validation
    │
    ▼
Multithreaded Port Scan (200 threads)
    │
    ▼
Service Identification (Socket library)
    │
    ▼
Risk Assessment (Risk profiles)
    │
    ▼
Security Score Calculation
    │
    ▼
Attack Simulation
    │
    ▼
Executive Summary Generation
    │
    ▼
JSON Response to Frontend
    │
    ▼
Dashboard Display + Export Option
```

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Windows, Linux, or macOS
- 50 MB disk space
- 256 MB RAM minimum

### Step 1: Install Python Dependencies

```bash
pip install flask
```

### Step 2: Navigate to Project Directory

```bash
cd d:\FY_Project\cyberFolder\p1
```

### Step 3: Verify Project Files

Ensure all files are present:
```
✓ app.py
✓ scanner.py
✓ risk_engine.py
✓ templates/index.html
✓ static/style.css
✓ PROJECT_SPEC.md
```

### Step 4: Start the Server

```bash
python app.py
```

### Step 5: Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

You should see the **Adaptive Attack Surface Mapper** dashboard.

---

## 🚀 Usage

### Basic Scanning

1. **Enter Target IP**
   - Input field accepts IPv4 addresses (e.g., 192.168.1.1)
   - Validation ensures proper format

2. **Set Port Range (Optional)**
   - Start Port: 1 (minimum)
   - End Port: 1024 (default), up to 65535
   - Default scans common services (1-1024)

3. **Initiate Scan**
   - Click "Scan Network" button
   - Loading indicator shows scan progress
   - Scanning takes 2-5 seconds for 1024 ports

4. **Review Results**
   - Security Score displayed (0-100)
   - Risk breakdown shown (HIGH/MEDIUM/LOW)
   - Open ports listed with details
   - Attack scenarios displayed

5. **Export Report**
   - Click "Export Report" button
   - JSON file downloads automatically
   - Filename format: `security_report_<IP>_<timestamp>.json`

### Advanced Usage

#### Custom Port Range Scanning

For faster scans of specific services:
```
Start Port: 8000
End Port: 8100
(Scans only ports 8000-8100)
```

#### Testing Safe Targets

**Localhost (Your Machine):**
```
IP: 127.0.0.1
Ports: 1-1024
```

**Home Router:**
```
IP: 192.168.1.1
Ports: 1-1024
```

**Specific Service Scan:**
```
IP: 192.168.1.100
Ports: 22-22 (SSH only)
```

---

## 📡 API Documentation

### Endpoint 1: Dashboard

```http
GET /
```

Returns the main dashboard interface (index.html).

**Response:** HTML page with dashboard UI

---

### Endpoint 2: Port Scan

```http
POST /scan
Content-Type: application/json

{
  "ip": "192.168.1.1",
  "start_port": 1,
  "end_port": 1024
}
```

**Parameters:**
- `ip` (required): Target IPv4 address
- `start_port` (optional): Starting port (default: 1, min: 1)
- `end_port` (optional): Ending port (default: 1024, max: 65535)

**Response:**
```json
{
  "success": true,
  "ip": "192.168.1.1",
  "scan_metadata": {
    "start_port": 1,
    "end_port": 1024,
    "total_ports_scanned": 1024,
    "open_ports_count": 5
  },
  "security_score": 85,
  "executive_summary": {
    "rating": "GOOD",
    "rating_description": "Secure with minor improvements needed",
    "high_risk_count": 0,
    "medium_risk_count": 1,
    "low_risk_count": 4,
    "priority_actions": [
      "Review 1 MEDIUM risk service(s)",
      "Maintain current security posture"
    ]
  },
  "attack_simulation": [
    "HIGH: Web Service Exploitation - Detected web services...",
    "ATTACK SURFACE SUMMARY: System has 1 moderate vulnerabilities..."
  ],
  "scan_results": [
    {
      "port": 22,
      "service": "SSH",
      "risk_level": "LOW",
      "reason": "Secure but requires proper configuration",
      "mitigation": "Disable password auth. Use key-based authentication..."
    },
    ...
  ]
}
```

**Error Responses:**

Invalid IP:
```json
{
  "success": false,
  "error": "Invalid IP address format"
}
```

Invalid port range:
```json
{
  "success": false,
  "error": "start_port (1025) must be less than end_port (2000)"
}
```

---

### Endpoint 3: Export Report

```http
POST /export-report
Content-Type: application/json

{
  "ip": "192.168.1.1",
  "security_score": 85,
  "executive_summary": {...},
  "scan_results": [...]
}
```

**Parameters:**
- Complete scan response from `/scan` endpoint

**Response:**
- Binary file download (application/json)
- Filename: `security_report_192.168.1.1_20260211_120530.json`

**File Format:**
```json
{
  "report_metadata": {
    "generated_at": "2026-02-11T12:05:30...",
    "tool_name": "Adaptive Attack Surface Mapper",
    "tool_version": "1.0"
  },
  "scan_information": {...},
  "security_assessment": {...},
  "threat_analysis": {...},
  "detailed_findings": {...},
  "recommendations_summary": {...}
}
```

---

## ⚙️ Configuration

### Scanner Configuration

#### Default Settings (Optimized)
```python
num_threads = 200      # Concurrent scanning threads
timeout = 0.5          # Connection timeout (seconds)
start_port = 1         # Default starting port
end_port = 1024        # Default ending port
```

#### Custom Configuration

Modify in `scanner.py`:
```python
# For slower networks, increase timeout
scanner = PortScanner(num_threads=100, timeout=2.0)

# For faster networks, maintain aggressive settings
scanner = PortScanner(num_threads=200, timeout=0.5)
```

### Risk Profile Customization

Edit service risk mappings in `risk_engine.py`:
```python
SERVICE_RISKS = {
    'CustomService': {
        'risk': 'HIGH',
        'reason': 'Description of vulnerability',
        'mitigation': 'Recommended fix'
    },
    ...
}
```

### Logging Configuration

Modify in `app.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
logging.basicConfig(level=logging.WARNING)  # Less verbose
```

---

## 🚄 Performance

### Scanning Performance

**Metrics (Baseline):**
- **Threads:** 200 concurrent
- **Timeout:** 0.5 seconds
- **Port Range:** 1-1024 (1024 ports)
- **Duration:** ~2.5 seconds
- **Throughput:** ~418 ports/second

### Performance Optimization Timeline

| Feature | Before | After | Improvement |
|---------|--------|-------|-------------|
| Threads | 100 | 200 | +100% concurrency |
| Timeout | 1.0s | 0.5s | -50% response time |
| Speed | ~200 ports/sec | ~418 ports/sec | 2x faster |

### Optimization Techniques

1. **Multithreading**
   - Queue-based work distribution
   - Thread pool for port scanning
   - Efficient context switching

2. **Aggressive Timeout**
   - 0.5-second connection timeout
   - Prevents hanging on dead services
   - Fast failure detection

3. **Thread Safety**
   - Lock mechanism for concurrent writes
   - No race conditions
   - Safe for 200+ threads

### Logged Performance Metrics

Example log output:
```
Scan duration: 2.45 seconds | Performance: 418.37 ports/sec
Thread safety: Lock mechanism maintained for 15 concurrent port discoveries
```

---

## 🔒 Security

### Security Features

1. **Input Validation**
   - IP address format validation
   - Port range validation (1-65535)
   - JSON input sanitization

2. **Thread Safety**
   - Lock mechanisms for concurrent operations
   - No race conditions
   - Safe multi-threading

3. **Error Handling**
   - Comprehensive exception handling
   - User-friendly error messages
   - Stack trace logging for debugging

4. **Educational Disclaimer**
   - Prominent warning on startup
   - Legal notice in UI
   - Authorization reminder

### Important Security Notes

⚠️ **LEGAL DISCLAIMER:**

This tool is for **EDUCATIONAL AND AUTHORIZED USE ONLY**.

- **DO scan:** Your own systems, test environments, authorized networks
- **DO NOT scan:** Systems without explicit permission (ILLEGAL)
- **User Responsibility:** Ensure all scans are authorized
- **Unauthorized scanning violates:** CFAA (Computer Fraud and Abuse Act)

### Best Practices

1. **Obtain Written Permission**
   - Get explicit authorization before scanning
   - Document permission
   - Keep audit trail

2. **Responsible Disclosure**
   - Report vulnerabilities ethically
   - Allow time for remediation
   - Don't exploit findings

3. **Protect Reports**
   - Keep exported reports confidential
   - Restrict access to authorized personnel
   - Follow organizational policies

---

## 🧪 Testing

### Test Scenarios

#### Test 1: Localhost (No Services Running)

```
IP: 127.0.0.1
Port Range: 1-1024
Expected Results:
- No open ports
- Security Score: 100
- Rating: EXCELLENT
```

#### Test 2: Localhost with Service

```bash
# Terminal 1: Start HTTP server
python -m http.server 8888

# Terminal 2: Run scanner
IP: 127.0.0.1
Port Range: 8000-9000
Expected Results:
- Port 8888 found
- HTTP service identified
- Risk assessment displayed
```

#### Test 3: Custom Port Range

```
IP: 127.0.0.1
Port Range: 22-22
Expected Results:
- SSH port (if running)
- Quick scan (< 1 second)
- Limited results
```

#### Test 4: Report Export

```
1. Perform scan
2. Click "Export Report"
3. Verify JSON file downloads
4. Check file contains all data
5. Validate JSON format
```

### Testing Checklist

- [ ] Frontend loads correctly
- [ ] Port range validation works
- [ ] Scan completes successfully
- [ ] Results display correctly
- [ ] Attack scenarios generated
- [ ] Export button appears
- [ ] Report downloads correctly
- [ ] JSON file is valid
- [ ] Error handling works
- [ ] Logging shows correct metrics

### Safe Test Targets

```
127.0.0.1              - Your machine (safest)
localhost              - Same as above
192.168.1.1            - Your router (if authorized)
8.8.8.8 (DNS)          - Educational scanning (with caution)
1.1.1.1 (Cloudflare)   - Educational scanning (with caution)
```

---

## 📝 Changelog

### Version 1.0 (February 11, 2026)

#### Initial Release Features

**✅ Core Components**
- Flask-based web application
- Multithreaded port scanner (200 threads)
- Risk assessment engine
- Attack simulation module
- Professional dashboard UI

**✅ Scanning Features**
- Ports 1-65535 support
- Service identification (40+ services)
- Customizable port ranges
- 0.5s timeout
- ~418 ports/second throughput

**✅ Risk Assessment**
- 40+ service risk profiles
- HIGH/MEDIUM/LOW risk levels
- Detailed mitigation recommendations
- Security scoring (0-100)
- Executive summary generation

**✅ Attack Simulation**
- Realistic attack scenario generation
- Exploitation path analysis
- Lateral movement vectors
- Service-specific attack vectors
- 4-7 detailed scenarios per scan

**✅ Reporting**
- JSON report export
- Timestamped filenames
- Comprehensive metadata
- Actionable recommendations

**✅ User Interface**
- Professional cybersecurity dashboard
- Real-time scanning interface
- Interactive results visualization
- Security score display
- Risk breakdown display
- Responsive design
- Export button integration

**✅ Performance**
- 200 concurrent threads
- 0.5-second timeout per port
- 2-3 second scan time (1-1024 ports)
- Thread-safe operations
- Performance metrics logging

**✅ Security**
- Input validation
- Error handling
- Educational disclaimer
- Thread safety
- Logging support

---

## 🔄 Development Timeline

### Phase 1: Backend Development ✅
- Flask application setup
- Port scanner implementation
- Risk engine development
- API endpoint creation

### Phase 2: Frontend Development ✅
- Dashboard UI design
- Form input implementation
- Results visualization
- Export button integration

### Phase 3: Integration ✅
- Backend-frontend communication
- JSON response handling
- File download functionality
- Error handling

### Phase 4: Optimization ✅
- Thread count increased (100 → 200)
- Timeout reduced (1.0s → 0.5s)
- Performance metrics logging
- Thread safety verification

### Phase 5: Documentation ✅
- README creation
- API documentation
- Configuration guide
- Testing instructions

---

## 🤝 Contributing

### Guidelines

1. **Code Quality**
   - Follow PEP 8 style guide
   - Add comprehensive comments
   - Include docstrings
   - Maintain thread safety

2. **Testing**
   - Test all new features
   - Verify thread safety
   - Check performance impact
   - Document test results

3. **Documentation**
   - Update README for changes
   - Document new endpoints
   - Add configuration options
   - Include examples

4. **Security**
   - Validate all inputs
   - Handle errors gracefully
   - Maintain educational focus
   - Include legal disclaimers

---

## 📞 Support

### Troubleshooting

**Issue: Flask won't start**
```bash
# Ensure Flask is installed
pip install flask

# Check Python version
python --version  # Should be 3.7+
```

**Issue: Port already in use**
```bash
# Flask uses port 5000 by default
# Either:
# 1. Stop other services on port 5000
# 2. Modify port in app.py: app.run(port=5001)
```

**Issue: Permission denied (scanning)**
```
Ensure you only scan authorized systems
Windows may require elevated privileges for some operations
```

**Issue: Slow scanning**
```
# Check network connectivity
# Increase timeout for slow networks
# Reduce thread count if system is overloaded
```

---

## 📚 Additional Resources

### Related Technologies
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Cybersecurity Basics](https://www.nist.gov/)
- [OWASP Top 10](https://owasp.org/)

### Learning Path
1. Understand network basics
2. Learn about port scanning
3. Study risk assessment
4. Explore attack vectors
5. Review mitigation strategies

---

## ⚖️ Legal Notice

This tool is provided for **EDUCATIONAL PURPOSES ONLY**.

**Use responsibly:**
- Obtain written authorization before scanning
- Only test systems you own or have permission to test
- Unauthorized network scanning is illegal in most jurisdictions
- Violates Computer Fraud and Abuse Act (CFAA) and similar laws

**By using this tool, you agree to:**
- Only use on authorized systems
- Comply with all applicable laws
- Respect privacy and security
- Report findings responsibly

---

## 📄 License

Educational Tool - Provided as-is for learning purposes.

**Author:** Security Assessment Team  
**Version:** 1.0  
**Last Updated:** February 11, 2026

---

## 🎓 Educational Objective

The Adaptive Attack Surface Mapper teaches:
- Network security fundamentals
- Vulnerability assessment
- Risk analysis methodologies
- Mitigation strategies
- Professional reporting practices

---

**Thank you for using the Adaptive Attack Surface Mapper!**

For questions or improvements, refer to PROJECT_SPEC.md or review the source code comments.
