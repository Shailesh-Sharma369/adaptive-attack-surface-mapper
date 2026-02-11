# ARCHITECTURE DOCUMENT

## Adaptive Attack Surface Mapper - System Architecture

**Version:** 1.0  
**Date:** February 11, 2026  
**Purpose:** Technical overview of system design and implementation

---

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Technology Stack](#technology-stack)
5. [Module Descriptions](#module-descriptions)
6. [API Design](#api-design)
7. [Database/Storage](#databasestorage)
8. [Scalability](#scalability)
9. [Deployment](#deployment)
10. [Error Handling](#error-handling)

---

## SYSTEM OVERVIEW

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│              USER INTERFACE (Browser)               │
│        HTML5 + CSS3 + JavaScript (Vanilla)          │
│       Professional Cybersecurity Dashboard          │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/JSON
                   ▼
┌─────────────────────────────────────────────────────┐
│          FLASK WEB APPLICATION SERVER               │
│  (Python Flask - http://127.0.0.1:5000)            │
│  ┌───────────────────────────────────────────────┐ │
│  │ Routes:                                       │ │
│  │  • GET  /              (Dashboard HTML)      │ │
│  │  • POST /scan          (Port scanning)       │ │
│  │  • POST /export-report (Report generation)  │ │
│  └───────────────────────────────────────────────┘ │
└───┬────────────────────────────────────────┬────────┘
    │                                        │
    ▼                                        ▼
┌──────────────────┐            ┌───────────────────┐
│  SCANNER MODULE  │            │  RISK ENGINE      │
│  (scanner.py)    │            │  (risk_engine.py) │
├──────────────────┤            ├───────────────────┤
│ • 200 threads    │            │ • Risk profiles   │
│ • 0.5s timeout   │            │ • Scoring algo    │
│ • Service ID     │            │ • Mitigation DB   │
│ • Queue-based    │            │ • Attack sims     │
│ • Thread-safe    │            │ • Reporting       │
└──────────────────┘            └───────────────────┘
```

### System Components

| Component | Type | Purpose |
|-----------|------|---------|
| Frontend | Web UI | User interaction and visualization |
| Flask App | Web Server | Request routing and API endpoints |
| Scanner | Python Module | Multithreaded port scanning |
| Risk Engine | Python Module | Security assessment and scoring |
| Templates | HTML/CSS/JS | User interface files |
| Static Assets | CSS/Images | Styling and design |

---

## COMPONENT ARCHITECTURE

### 1. Frontend Component (Client-Side)

**File:** `templates/index.html` + `static/style.css`

**Responsibilities:**
- Display dashboard interface
- Collect user input (IP, port range)
- Send scan requests
- Display results with visualizations
- Handle file downloads

**Technologies:**
- HTML5 (semantic markup)
- CSS3 (responsive styling)
- JavaScript (ES6, vanilla)
- Fetch API (HTTP requests)

**Key Features:**
- Form validation
- Loading indicators
- Real-time feedback
- Error handling
- Report export button

**Dependencies:**
- None (pure client-side)

---

### 2. Flask Web Application (Server)

**File:** `app.py`

**Responsibilities:**
- HTTP request routing
- Input validation
- Orchestrate scanning workflow
- Generate JSON responses
- Handle file downloads

**Technologies:**
- Python 3.7+
- Flask web framework
- JSON processing
- File I/O

**Key Functions:**

```python
@app.route('/')
def index():
    """Serve dashboard HTML"""
    
@app.route('/scan', methods=['POST'])
def scan():
    """Execute port scan and risk assessment"""
    
@app.route('/export-report', methods=['POST'])
def export_report():
    """Generate and download JSON report"""
```

**Flow:**
```
Request → Validation → Scanner → Risk Engine → Response
```

---

### 3. Port Scanner Module

**File:** `scanner.py`

**Responsibilities:**
- Multithreaded TCP port scanning
- Service identification
- Result aggregation
- Performance monitoring

**Architecture:**

```
Main Thread
    │
    ├─ Create 200 worker threads
    │
    ├─ Queue ports (1 to N)
    │
    ├─ Each worker:
    │   ├─ Get port from queue
    │   ├─ Attempt TCP connection
    │   ├─ Record if open
    │   └─ Next port
    │
    └─ Collect results
        └─ Sort by port number
```

**Key Classes:**

```python
class PortScanner:
    def __init__(self, num_threads=200, timeout=0.5)
    def scan_port(ip, port) -> bool
    def get_service_name(port) -> str
    def worker(ip)
    def scan(ip, start_port, end_port) -> List[Dict]
```

**Thread Safety:**

```python
self.lock = threading.Lock()  # Protects concurrent writes
with self.lock:
    self.open_ports.append({...})  # Safe concurrent append
```

**Performance:**
- 200 concurrent threads
- 0.5-second timeout
- ~418 ports/second
- Thread-safe with locks

---

### 4. Risk Assessment Engine

**File:** `risk_engine.py`

**Responsibilities:**
- Risk level assignment
- Mitigation recommendations
- Security scoring
- Attack simulation
- Report generation

**Key Classes:**

```python
class RiskEngine:
    # Constants
    RISK_LEVELS = {'HIGH': {...}, 'MEDIUM': {...}, 'LOW': {...}}
    SERVICE_RISKS = {40+ service profiles...}
    
    # Methods
    def get_risk_profile(service) -> Dict
    def assess_risks(open_ports) -> List[Dict]
    def calculate_security_score(risk_results) -> int
    def get_security_rating(score) -> Dict
    def generate_executive_summary(risk_results, score) -> Dict
    def simulate_attack_scenarios(risk_results) -> List[str]
```

**Risk Assessment Flow:**

```
Open Ports
    │
    ├─ For each port:
    │   ├─ Get service name
    │   ├─ Look up risk profile
    │   ├─ Assign risk level
    │   └─ Add mitigation
    │
    ├─ Count risks by level
    │
    ├─ Calculate score (0-100)
    │
    ├─ Generate rating
    │
    ├─ Create summary
    │
    └─ Simulate attacks
```

**Service Risk Profiles:**

```python
SERVICE_RISKS = {
    'SSH': {'risk': 'LOW', 'reason': '...', 'mitigation': '...'},
    'Telnet': {'risk': 'HIGH', 'reason': '...', 'mitigation': '...'},
    'HTTP': {'risk': 'MEDIUM', 'reason': '...', 'mitigation': '...'},
    # ... 40+ services
}
```

---

## DATA FLOW

### Request/Response Flow

```
1. CLIENT REQUEST
   ├─ Input: IP address, port range
   ├─ Method: POST /scan
   └─ Format: JSON

2. SERVER VALIDATION
   ├─ Validate IP format
   ├─ Validate port range
   └─ Check bounds (1-65535)

3. PORT SCANNING
   ├─ Create 200 worker threads
   ├─ Distribute ports via queue
   ├─ Each thread: TCP connect
   ├─ Collect open ports
   └─ Duration: 2-5 seconds

4. RISK ASSESSMENT
   ├─ For each open port:
   │  ├─ Identify service
   │  ├─ Lookup risk profile
   │  └─ Assign risk level
   ├─ Calculate security score
   └─ Duration: <100ms

5. ATTACK SIMULATION
   ├─ Analyze risk patterns
   ├─ Generate scenarios
   └─ Create recommendations

6. RESPONSE GENERATION
   ├─ Compile results
   ├─ Create JSON response
   ├─ Include metadata
   └─ Send to client

7. CLIENT DISPLAY
   ├─ Parse JSON
   ├─ Render results
   ├─ Show visualizations
   └─ Enable export button
```

### Data Structures

**Scan Request:**
```json
{
  "ip": "192.168.1.1",
  "start_port": 1,
  "end_port": 1024
}
```

**Port Result (Internal):**
```python
{
    'port': 22,
    'service': 'SSH'
}
```

**Risk Result:**
```python
{
    'port': 22,
    'service': 'SSH',
    'risk_level': 'LOW',
    'risk_color': '#28a745',
    'reason': 'Secure but requires proper configuration',
    'mitigation': 'Disable password auth...'
}
```

**Scan Response:**
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
    "high_risk_count": 0,
    "medium_risk_count": 1,
    "low_risk_count": 4
  },
  "attack_simulation": [
    "HIGH: Web Service Exploitation...",
    "..."
  ],
  "scan_results": [...]
}
```

---

## TECHNOLOGY STACK

### Backend

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web Framework | Flask | HTTP routing and request handling |
| Language | Python 3.7+ | Backend logic implementation |
| Networking | Socket library | TCP port scanning |
| Threading | threading module | Concurrent scanning (200 threads) |
| Data Format | JSON | API communication |
| File I/O | BytesIO | In-memory file generation |
| Logging | logging module | Debug and audit trails |
| Time | time module | Performance metrics |

### Frontend

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Markup | HTML5 | Semantic structure |
| Styling | CSS3 | Professional design |
| Scripts | Vanilla JavaScript | Client-side logic |
| HTTP | Fetch API | Server communication |
| Data | JSON | Request/response format |

### Infrastructure

| Component | Specification |
|-----------|---------------|
| Server | Single-threaded Flask dev server |
| Port | 5000 (configurable) |
| Protocol | HTTP (not HTTPS) |
| Database | None (in-memory only) |
| Storage | File system for exports |

---

## MODULE DESCRIPTIONS

### Module: app.py

**Size:** 340+ lines  
**Purpose:** Flask web application and API endpoints  
**Dependencies:** Flask, scanner, risk_engine, datetime, json, io

**Key Exports:**
```python
Flask application instance: app
Routes: /, /scan, /export-report
```

**Responsibilities:**
- Route HTTP requests
- Validate input parameters
- Orchestrate scanner and risk engine
- Format JSON responses
- Handle file downloads
- Manage error handling
- Provide logging

---

### Module: scanner.py

**Size:** 216+ lines  
**Purpose:** Multithreaded TCP port scanner  
**Dependencies:** socket, threading, queue, logging, time

**Key Exports:**
```python
class PortScanner:
    def scan(ip, start_port, end_port) -> List[Dict]
```

**Responsibilities:**
- Perform TCP port scanning
- Identify services
- Maintain thread safety
- Collect results
- Calculate performance metrics

**Performance Characteristics:**
- Throughput: 418 ports/second
- Concurrency: 200 threads
- Timeout: 0.5 seconds
- Typical duration: 2-5 seconds for 1024 ports

---

### Module: risk_engine.py

**Size:** 434+ lines  
**Purpose:** Risk assessment and security scoring  
**Dependencies:** logging

**Key Exports:**
```python
class RiskEngine:
    def assess_risks(open_ports) -> List[Dict]
    def calculate_security_score(risk_results) -> int
    def generate_executive_summary(risk_results, score) -> Dict
    def simulate_attack_scenarios(risk_results) -> List[str]
```

**Responsibilities:**
- Assess security risks
- Generate scores
- Create recommendations
- Simulate attack paths
- Format reports

**Service Profiles:** 40+ unique services covered

---

### Module: templates/index.html

**Size:** 610+ lines  
**Purpose:** Dashboard user interface  
**Dependencies:** CSS file, JavaScript, Fetch API

**Key Features:**
- Form input collection
- Loading indicators
- Results visualization
- Export functionality
- Error handling
- Responsive design

**JavaScript Functions:**
```javascript
function validateIP(ip)
function validatePortRange(start, end)
function renderResults(data)
function updateSecurityScore(score)
function createPortCard(portData)
function exportReport()
```

---

### Module: static/style.css

**Size:** 924+ lines  
**Purpose:** Professional styling and layout  
**Dependencies:** None

**Key Sections:**
- CSS variables (theme)
- Global styles
- Layout components
- Form styling
- Button styles
- Card layouts
- Animations
- Responsive breakpoints
- Scrollbar styling

---

## API DESIGN

### REST Endpoints

#### 1. GET /

**Purpose:** Serve dashboard  
**Method:** GET  
**Authentication:** None  
**Request Body:** None  

**Response:**
```
Content-Type: text/html
Body: index.html content
```

---

#### 2. POST /scan

**Purpose:** Execute port scan and assessment  
**Method:** POST  
**Authentication:** None  
**Content-Type:** application/json  

**Request:**
```json
{
  "ip": "192.168.1.1",
  "start_port": 1,
  "end_port": 1024
}
```

**Validation:**
```
✓ ip: Required, valid IPv4 format
✓ start_port: Optional, ≥ 1
✓ end_port: Optional, ≤ 65535, > start_port
```

**Response (Success - 200):**
```json
{
  "success": true,
  "ip": "...",
  "scan_metadata": {...},
  "security_score": 85,
  "executive_summary": {...},
  "attack_simulation": [...],
  "scan_results": [...]
}
```

**Response (Error - 400/500):**
```json
{
  "success": false,
  "error": "Error message"
}
```

**Error Cases:**
- `400`: Invalid IP format
- `400`: Missing required fields
- `400`: Port range validation failure
- `500`: Scan execution error

---

#### 3. POST /export-report

**Purpose:** Generate downloadable report  
**Method:** POST  
**Authentication:** None  
**Content-Type:** application/json  

**Request:**
```json
{
  "ip": "192.168.1.1",
  "security_score": 85,
  "executive_summary": {...},
  "scan_results": [...]
}
```

**Response (Success - 200):**
```
Content-Type: application/json
Content-Disposition: attachment; filename="security_report_192.168.1.1_20260211_120530.json"
Body: JSON report file
```

**Response (Error - 400/500):**
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## DATABASE/STORAGE

### Current Implementation

**Type:** In-Memory  
**Persistence:** None  
**Data Retention:** Session only

### Storage Locations

1. **Scan Results**
   - Stored in memory during scan
   - Cleared on new scan
   - Sent to client in JSON response

2. **Exported Reports**
   - Generated in memory (BytesIO)
   - Sent to client as file download
   - Not persisted on server

### Future Enhancement

For production deployment, consider:

```python
# Option 1: SQLite (lightweight)
database = 'scans.db'
tables = ['scans', 'ports', 'risks']

# Option 2: PostgreSQL (scalable)
connection = 'postgresql://localhost/aasm'
tables = ['scans', 'ports', 'risks', 'users']

# Option 3: MongoDB (document-based)
database = 'aasm'
collections = ['scans', 'reports']
```

---

## SCALABILITY

### Current Limitations

| Aspect | Limitation | Impact |
|--------|-----------|--------|
| Users | Single user | Concurrent requests blocked |
| Storage | In-memory | Results lost on restart |
| Threads | 200 max | Limited by OS |
| IPs | One at a time | Sequential scanning |
| History | None | No persistence |

### Scalability Improvements

#### Horizontal Scaling
```
Load Balancer
    ├─ Instance 1 (app.py + scanner)
    ├─ Instance 2 (app.py + scanner)
    └─ Instance 3 (app.py + scanner)
    
+ Shared database
+ Message queue (Redis/RabbitMQ)
+ Cache layer (Redis)
```

#### Vertical Scaling
```
Current:
- Single Flask instance
- Single process
- In-memory storage

Improved:
- Multiple worker processes
- Database backend
- Cache layer
- Async task queue
```

#### Threading Optimization
```
Current:
- 200 threads per scan
- One scan at a time

Improved:
- Thread pool (1000+)
- Concurrent scans
- Job queue
- Worker threads
```

---

## DEPLOYMENT

### Development Environment

```bash
# Install dependencies
pip install flask

# Run server
python app.py

# Access
http://127.0.0.1:5000
```

### Production Deployment

```
Option 1: Gunicorn + Nginx
Option 2: Docker container
Option 3: Cloud platform (AWS/GCP/Azure)
```

### Docker Deployment (Example)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Configuration

**Environment Variables:**
```
FLASK_ENV=production
FLASK_DEBUG=0
FLASK_PORT=5000
LOG_LEVEL=INFO
THREAD_COUNT=200
TIMEOUT=0.5
```

---

## ERROR HANDLING

### Error Hierarchy

```
Exception
├─ ValueError (Invalid input)
├─ socket.error (Network error)
├─ threading.error (Thread error)
└─ Exception (General error)
```

### Error Handling Strategy

```python
try:
    # Main operation
    result = perform_operation()
except ValueError as e:
    # Input validation error
    logger.warning(f"Invalid input: {e}")
    return error_response(400, str(e))
except socket.error as e:
    # Network error
    logger.error(f"Network error: {e}")
    return error_response(500, "Network error")
except Exception as e:
    # Unexpected error
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return error_response(500, "Internal error")
```

### Logging Levels

```
DEBUG   - Detailed diagnostic info
INFO    - General informational messages
WARNING - Warning messages (issues but continuing)
ERROR   - Error messages (problem occurred)
CRITICAL- Critical error (service failure)
```

### Error Response Format

```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

---

## SUMMARY

The Adaptive Attack Surface Mapper is a well-architected, modular security assessment tool featuring:

✅ Clean separation of concerns  
✅ Efficient multithreaded scanning  
✅ Comprehensive risk assessment  
✅ Professional web interface  
✅ Robust error handling  
✅ Detailed logging  
✅ Performance optimization  
✅ Extensible design  

**Status:** Production-ready for educational use

---

*Document Version: 1.0*  
*Last Updated: February 11, 2026*
