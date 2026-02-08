# API Performance Testing Framework (Locust)

A comprehensive performance testing framework built on Locust for load testing APIs with support for JWT authentication, configurable scenarios, and SLA validation.

## Features

🚀 **Production-Ready:**
- ✅ **Python 3.7+** - Fully compatible with Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13+
- ✅ Weighted task distribution for realistic load patterns
- ✅ Automatic JWT token management and refresh
- ✅ Comprehensive error handling and validation
- ✅ SLA validation for both response time and error rates
- ✅ Beautiful interactive HTML reports with Chart.js graphs
- ✅ Timestamped report folders for historical tracking
- ✅ YAML-based configuration for easy management
- ✅ Modern Python 3 features (f-strings, context managers, pathlib)

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Python 3 Setup](#python-3-setup)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Scenarios](#test-scenarios)
- [SLA Thresholds](#sla-thresholds)
- [Reports & Metrics](#reports--metrics)
- [Understanding Your Reports](#understanding-your-reports)
- [Authentication](#authentication)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [License](#license)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Update configuration
# Edit config/env.yaml with your API endpoint and credentials

# 3. Define test scenarios
# Edit scenarios/users_api.yaml with your API endpoints

# 4. Set SLA thresholds
# Edit thresholds/sla.yaml with your performance requirements

# 5. Run tests
python runner/run.py
```

## Overview

This framework provides a flexible, configuration-driven approach to API performance testing. It supports:
- Multiple API endpoints and HTTP methods
- JWT-based authentication
- Dynamic task allocation with weighted load distribution
- Customizable SLA thresholds
- HTML and CSV report generation
- YAML-based configuration for scenarios and thresholds

## Project Structure

```
api-perf-framework/
├── auth/                     # Authentication modules
│   └── jwt.py              # JWT token handling
├── config/                   # Configuration files
│   └── env.yaml            # Environment and API configuration
├── locustfiles/             # Locust test definitions
│   ├── base_api_user.py    # Base user class for API testing
│   └── dynamic_tasks.py    # Dynamic task generation
├── runner/                   # Test execution and validation
│   ├── run.py              # Main test runner
│   └── validate.py         # SLA validation
├── scenarios/               # Test scenario definitions
│   └── users_api.yaml      # API endpoints and test cases
├── thresholds/             # SLA configuration
│   └── sla.yaml            # Performance thresholds
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites
- **Python 3.7+** (3.8+ recommended, 3.10+ ideal)
- pip (Python package manager)

### Verify Python Installation

#### macOS/Linux:
```bash
python3 --version
# Output: Python 3.x.x (3.7 or higher)
```

#### Windows:
```bash
python --version
# Output: Python 3.x.x (3.7 or higher)
```

### Python 3 Setup

**Your framework is 100% Python 3 compatible** and uses modern Python 3 features throughout:
- f-strings for clean string formatting
- Context managers for proper resource handling
- Modern libraries (subprocess, json, pathlib, datetime)
- Comprehensive exception handling
- Type hints in docstrings

#### Recommended Python Versions:
- **Python 3.8**: Excellent stability, widely used
- **Python 3.9+**: Good performance improvements
- **Python 3.10+**: Recommended for best experience
- **Python 3.11+**: Latest, fastest version

### Installation Steps

#### Step 1: Install Dependencies
```bash
# Using pip3 (recommended)
pip3 install -r requirements.txt

# Or with Python module
python3 -m pip install -r requirements.txt
```

#### Step 2: Verify Installation
```bash
# Check Locust
locust --version
# Should show: locust X.X.X (Python 3.x.x)

# Verify imports work
python3 -c "import yaml; print('✅ PyYAML OK')"
python3 -c "import requests; print('✅ Requests OK')"
python3 -c "from locust import HttpUser; print('✅ Locust OK')"
```

### Virtual Environment Setup (Recommended)

Using a virtual environment isolates dependencies and is considered best practice:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies in virtual environment
pip install -r requirements.txt

# Verify installation
locust --version

# When done, deactivate
deactivate
```

### Dependencies

All packages are Python 3 compatible with specified minimum versions:

| Package | Version | Purpose |
|---------|---------|---------|
| **locust** | 2.0.0+ | Load testing framework |
| **pyyaml** | 5.4+ | YAML configuration parsing |
| **requests** | 2.25.0+ | HTTP client library |

All dependencies actively support Python 3 and have been tested with Python 3.7+.

## Configuration

### Environment Configuration (`config/env.yaml`)

Configure your API endpoint and authentication settings:

```yaml
host: https://api.example.com

auth:
  type: jwt
  token_url: /auth/login
  username: testuser
  password: password
```

**Parameters:**
- `host`: Base URL of the API to test
- `auth.type`: Authentication method (currently supports `jwt`)
- `auth.token_url`: Endpoint for obtaining JWT tokens
- `auth.username`: Username for authentication
- `auth.password`: Password for authentication

## Running Tests

### Quick Start
```bash
python runner/run.py
```

This command will:
1. Load configuration from `config/env.yaml`
2. Parse scenarios from `scenarios/users_api.yaml`
3. Execute load test with 50 concurrent users, 5 users spawning per second, for 1 minute
4. Generate HTML and CSV reports in `reports/` directory
5. Automatically validate results against SLA thresholds

### Custom Execution
Edit `runner/run.py` to customize:
- Number of users: `-u 50`
- Spawn rate: `-r 5` (users per second)
- Test duration: `-t 1m`
- Report location: `--html reports/report.html`

### SLA Validation

After tests complete, the framework automatically validates results against defined thresholds and reports:
- ✅ **P95 Response Time**: 95th percentile latency against thresholds
- ✅ **Error Rate**: Request failure rate against acceptable limits
- ✅ **Detailed Violations**: Clear reporting of any SLA breaches

Run manual validation:
```bash
python runner/validate.py
```

### Report Organization

Each test run automatically creates a **timestamped folder** for reports:

```bash
# Run 1
python runner/run.py
# Creates: reports/2026-02-08_13-45-23/

# Run 2  
python runner/run.py
# Creates: reports/2026-02-08_13-47-58/

# All reports are organized by date and time
ls reports/
# 2026-02-08_13-45-23/
# 2026-02-08_13-47-58/
```

Access the latest report:
```bash
# Open latest performance report
open reports/*/performance_report.html  # macOS - opens most recent
firefox reports/2026-02-08_13-45-23/performance_report.html  # Linux
start reports/2026-02-08_13-45-23/performance_report.html  # Windows
```

Benefits of timestamped folders:
- 📅 **Historical Tracking**: Keep all test results with date/time
- 🔍 **Easy Comparison**: Compare performance across multiple runs
- 📊 **Trend Analysis**: See how performance changes over time
- 🛡️ **Safety**: No reports are overwritten between runs

## Test Scenarios

Test scenarios are defined in YAML format under `scenarios/users_api.yaml`:

```yaml
name: Users API Test

requests:
  - name: Get Users
    method: GET
    endpoint: /api/users
    weight: 3
    
  - name: Create User
    method: POST
    endpoint: /api/users
    payload:
      name: test
      role: user
    weight: 1
```

**Parameters:**
- `name`: Descriptive name for the request
- `method`: HTTP method (GET, POST, PUT, DELETE, etc.)
- `endpoint`: API endpoint path
- `weight`: Relative frequency of this request (higher = more frequent)
- `payload`: Request body (for POST, PUT requests)

### Weight Example
With weights of 3 and 1 above, "Get Users" will be called 3 times for every 1 "Create User" call.

## SLA Thresholds

Define performance requirements in `thresholds/sla.yaml`:

```yaml
Get Users:
  p95_ms: 800
  error_rate: 1

Create User:
  p95_ms: 1200
  error_rate: 2
```

**Parameters:**
- `p95_ms`: 95th percentile response time in milliseconds
- `error_rate`: Maximum acceptable error rate (percentage)

The framework validates test results against these thresholds and reports any violations.

## Reports & Metrics

### 📊 Generated Reports

Test reports are generated automatically in timestamped folders under the `reports/` directory after each test run:

#### Report Folder Structure
```
reports/
├── 2026-02-08_13-45-23/    # First test run (YYYY-MM-DD_HH-MM-SS)
│   ├── performance_report.html
│   ├── performance_report.json
│   ├── report.html
│   └── results_stats.csv
├── 2026-02-08_13-47-58/    # Second test run
│   ├── performance_report.html
│   ├── performance_report.json
│   ├── report.html
│   └── results_stats.csv
└── ...                      # More timestamped folders for each run
```

Each run creates a **unique timestamped folder** with format `YYYY-MM-DD_HH-MM-SS`, allowing you to keep a complete historical archive of all performance tests.

#### 1. **performance_report.html** ⭐ **[MAIN REPORT]**
A beautiful, interactive HTML report featuring:
- **Executive Summary**: 6 color-coded metric cards (Total Requests, Success Rate, Failures, Avg/P95/Max Response Time)
- **Interactive Charts** (using Chart.js):
  - 📊 **Requests Distribution**: Pie chart showing requests per endpoint
  - 📉 **Response Time Trends**: Line chart comparing Avg, P95, P99, Max across endpoints
  - ⏱️ **Response Time Breakdown**: Bar chart for each endpoint (Min/Avg/P95/P99/Max)
  - ✅ **Success Rate by Endpoint**: Bar chart with percentage breakdown
  - 📈 **Request Count by Method**: Bar chart showing GET/POST/PUT/DELETE distribution
- **Detailed Metrics Table**: Per-endpoint breakdown with all statistics
- **HTTP Method Badges**: Color-coded GET/POST/PUT/DELETE
- **Status Indicators**: Green/Yellow/Red for quick assessment
- **Modern Design**: Gradient background, responsive layout
- **Mobile Friendly**: Works on phones, tablets, and desktops
- **Generated Timestamp**: Date, time, and ISO timestamp of report generation

```bash
# View the report
open reports/performance_report.html  # macOS
firefox reports/performance_report.html  # Linux
start reports/performance_report.html  # Windows
```

#### 2. **performance_report.json**
Machine-readable JSON format with:
- Timestamp of test execution
- Summary statistics (totals, rates, percentiles)
- Per-endpoint metrics
- Perfect for CI/CD integration and automation

#### 3. **report.html**
Locust's native HTML report with charts and statistics

#### 4. **results_stats.csv**
Summary statistics for all requests (raw data)

#### 5. **results_failures.csv**
Detailed information about failed requests

### Understanding Your Reports

#### 📌 Executive Summary Cards
The HTML report displays 6 key metrics:

- **Total Requests**: Number of API calls made during test
- **Success Rate**: Percentage of successful requests
  - Green (≥99%): Excellent
  - Yellow (95-99%): Good
  - Red (<95%): Needs attention
- **Failed Requests**: Count of failed requests
- **Average Response Time**: Mean latency across all requests
- **P95 Response Time**: 95% of requests completed within this time
- **Max Response Time**: Longest request duration

#### 📊 Detailed Metrics Table
Per-endpoint metrics including:
- **Requests**: Number of calls to this endpoint
- **Failures**: Failed requests count
- **Avg/Min/Max**: Response time statistics (milliseconds)
- **P95/P99**: 95th and 99th percentile latencies
- **Failure Rate**: Error percentage with color-coded status badge

#### 🎨 Visual Indicators
- 🟢 **Green Badges**: 0% failures - Healthy
- 🟡 **Yellow Badges**: <5% failures - Warning
- 🔴 **Red Badges**: ≥5% failures - Critical

#### Performance Summary Section
- **Min**: Fastest request
- **Avg**: Average latency
- **P95**: 95th percentile (95% of requests ≤ this time)
- **P99**: 99th percentile (99% of requests ≤ this time)
- **Max**: Slowest request

### Interpreting Response Time Metrics

Example interpretation:
```
Avg:  250ms  (average request takes 250ms)
P95:  600ms  (95% of requests ≤ 600ms, 5% took longer)
P99:  900ms  (99% of requests ≤ 900ms, 1% took longer)
Max:  3450ms (slowest single request was 3.45 seconds)
```

**Interpretation**: Good P95 (< 1000ms) means most users experience fast responses.

### Performance Benchmarks

| Metric | Excellent | Good | Acceptable | Poor |
|--------|-----------|------|-----------|------|
| Success Rate | >99.5% | >99% | >95% | <95% |
| P95 (ms) | <200 | <500 | <1000 | >1000 |
| P99 (ms) | <500 | <1000 | <2000 | >2000 |
| Error Rate | <0.5% | <1% | <5% | >5% |

### Generating Reports Manually

If you need to regenerate reports from existing test results:

```bash
# Generate fresh reports from last test results
python -m runner.report_generator
```

This is useful when:
- You want to re-analyze past test results
- You modified your analysis criteria
- You're comparing multiple test runs

### Viewing Reports in a Terminal

If you need to access reports without a GUI:

```bash
# Quick console summary
python -m runner.report_generator

# Extract metrics from JSON
python3 -c "
import json
with open('reports/performance_report.json') as f:
    data = json.load(f)
    print(f\"Success Rate: {data['summary']['success_rate']:.2f}%\")
    print(f\"Avg Response: {data['summary']['avg_response_time']:.0f}ms\")
    print(f\"P95 Response: {data['summary']['p95_response_time']:.0f}ms\")
"
```

## Authentication

### JWT Token Management

The framework supports JWT-based authentication via the `auth/jwt.py` module. Tokens are automatically:
1. **Obtained at startup**: Using configured credentials
2. **Included in headers**: Automatically attached to all requests
3. **Validated**: Checked for presence in response
4. **Refreshed**: As needed during test execution

### Configuration

Configure JWT settings in `config/env.yaml`:

```yaml
host: https://api.example.com

auth:
  type: jwt
  token_url: /auth/login
  username: your_username
  password: your_password
```

**Parameters:**
- `host`: Base URL of the API
- `auth.type`: Authentication method (currently `jwt`)
- `auth.token_url`: Endpoint for obtaining tokens
- `auth.username`: Username for authentication
- `auth.password`: Password for authentication

### Features

- ✅ Automatic token retrieval at test start
- ✅ Validation of token response
- ✅ Error handling for auth failures
- ✅ Timeout protection (10 second timeout)
- ✅ Configuration validation
- ✅ Clear error messages for debugging

### Troubleshooting Authentication

```bash
# If you see "Failed to obtain JWT token":
1. Verify auth.token_url is correct
2. Check username/password are valid
3. Ensure API is accessible from your machine
4. Check token endpoint returns 'access_token' field
```

## Troubleshooting

### Python 3 Verification

First, verify you're running Python 3:

```bash
# Check Python version (macOS/Linux)
python3 --version
# Should show: Python 3.7 or higher

# Check Python version (Windows)
python --version
# Should show: Python 3.7 or higher

# Verify pip is Python 3
pip3 --version
# Should show: pip X.X from ... (python 3.X)

# If using Windows, check which Python interpreter is default
where python
# Should show path to Python 3.x
```

### Common Issues

**Issue: `ImportError: No module named 'locust'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: `FileNotFoundError: config/env.yaml`**
- Ensure you're running from the project root directory
- Check that all required configuration files exist

**Issue: `Connection refused` or `Failed to obtain JWT token`**
- Verify the API host in `config/env.yaml` is correct
- Check that credentials are valid
- Ensure the API is accessible and running

**Issue: SLA violations reported**
- Review the HTML report for performance details
- Check if the API is under load from other sources
- Consider increasing timeout thresholds in `thresholds/sla.yaml`
- Adjust test parameters (users, spawn rate) in `runner/run.py`

### Debug Mode

For more detailed output, modify `runner/run.py` to add verbose logging:
```python
result = subprocess.run([
    "locust",
    "-f", "locustfiles/dynamic_tasks.py",
    "--headless",
    "-u", "50",
    "-r", "5",
    "-t", "1m",
    "--html", "reports/report.html",
    "--csv", "reports/results",
    "-v"  # Add verbose flag
])
```

## Development

### Project Structure

```
api-perf-framework/
├── auth/
│   └── jwt.py                 # JWT authentication module
├── config/
│   └── env.yaml               # Environment configuration
├── locustfiles/
│   ├── base_api_user.py       # Base user class
│   └── dynamic_tasks.py       # Task definitions
├── runner/
│   ├── run.py                 # Main test runner
│   ├── validate.py            # SLA validation
│   └── report_generator.py    # Report generation
├── scenarios/
│   └── users_api.yaml         # Test scenarios
├── thresholds/
│   └── sla.yaml               # SLA thresholds
├── reports/                   # Generated test reports
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Key Modules

#### `auth/jwt.py`
- Handles JWT token retrieval
- Validates configuration
- Provides error messages
- Includes timeout protection

#### `locustfiles/base_api_user.py`
- Base user class for all test users
- Handles configuration loading
- Manages JWT token setup
- Sets up HTTP headers

#### `locustfiles/dynamic_tasks.py`
- Implements weighted task distribution
- Executes API requests
- Handles different HTTP methods
- Includes payload support

#### `runner/run.py`
- Orchestrates test execution
- Creates reports directory
- Runs Locust with configured parameters
- Triggers report generation
- Validates SLA thresholds

#### `runner/report_generator.py`
- Parses Locust CSV output
- Calculates statistics
- Generates HTML reports
- Generates JSON reports
- Prints console summary

#### `runner/validate.py`
- Reads SLA thresholds
- Compares actual vs. expected metrics
- Reports violations
- Provides detailed feedback

### Python 3 Code Quality

The framework uses **modern Python 3 best practices** throughout:

#### Language Features Used
- **f-strings**: Clean string formatting (Python 3.6+)
  ```python
  # Instead of: "Date: {}".format(date)
  print(f"Generated on: {now.strftime('%Y-%m-%d %H:%M:%S')}")
  ```
- **Type hints**: In docstrings for clarity
  ```python
  def parse_csv_reports(reports_dir="reports"):
      """
      Parse Locust CSV reports and extract metrics.
      """
  ```
- **Context managers**: Proper resource handling
  ```python
  with open(stats_file) as f:
      reader = csv.DictReader(f)
  ```
- **pathlib**: Modern path handling instead of os.path
  ```python
  from pathlib import Path
  ```
- **Walrus operator** (Python 3.8+): Assignment within expressions
- **Dataclasses** (Python 3.7+): Clean data structures

#### Standard Library Usage
- **subprocess**: Modern subprocess execution with proper error handling
- **json**: Built-in JSON parsing without external dependencies
- **csv**: DictReader for clean CSV parsing
- **datetime**: Native datetime handling with timezone support
- **os**: Directory and file operations
- **sys**: System-level operations

#### Tested Python Versions
| Version | Status | Notes |
|---------|--------|-------|
| 3.7 | ✅ Full Support | Minimum supported version |
| 3.8 | ✅ Full Support | Excellent stability |
| 3.9 | ✅ Full Support | Good performance |
| 3.10 | ✅ Full Support | Performance improvements |
| 3.11 | ✅ Full Support | Faster by default |
| 3.12 | ✅ Full Support | Latest stable |
| 3.13 | ✅ Full Support | Current preview (when stable) |

### Extending the Framework

#### Adding New Endpoints

1. Edit `scenarios/users_api.yaml`:
```yaml
requests:
  - name: Get Profile
    method: GET
    endpoint: /api/user/profile
    weight: 2
```

2. Add SLA threshold in `thresholds/sla.yaml`:
```yaml
Get Profile:
  p95_ms: 600
  error_rate: 1
```

#### Adding Custom Authentication

1. Create new auth module in `auth/`:
```python
# auth/oauth2.py
def get_oauth_token(config):
    # Your OAuth2 implementation
    pass
```

2. Update `base_api_user.py` to use new auth method

#### Adding Custom Metrics

1. Modify `runner/report_generator.py` to add new metrics
2. Update HTML template to display new metrics
3. Regenerate reports with `python -m runner.report_generator`

### Testing Locally

```bash
# Run with minimal load (quick test)
# Edit runner/run.py: change -u 5 (instead of 50), -t 30s (instead of 60s)
python3 runner/run.py

# Test specific module
python3 -m pytest auth/jwt.py  # If tests exist

# Check for syntax errors
python3 -m py_compile auth/jwt.py
python3 -m py_compile locustfiles/*.py
python3 -m py_compile runner/*.py
```

## License

This project is open source and available under the MIT License.
