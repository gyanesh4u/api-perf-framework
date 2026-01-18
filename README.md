# API Performance Testing Framework (Locust)

A comprehensive performance testing framework built on Locust for load testing APIs with support for JWT authentication, configurable scenarios, and SLA validation.

## Features

🚀 **Production-Ready:**
- ✅ Weighted task distribution for realistic load patterns
- ✅ Automatic JWT token management and refresh
- ✅ Comprehensive error handling and validation
- ✅ SLA validation for both response time and error rates
- ✅ HTML and CSV report generation
- ✅ YAML-based configuration for easy management

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Scenarios](#test-scenarios)
- [SLA Thresholds](#sla-thresholds)
- [Reports](#reports)
- [Authentication](#authentication)

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
- Python 3.7+
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- **locust**: Load testing framework
- **pyyaml**: YAML configuration parsing
- **requests**: HTTP client library

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

## Reports

Test reports are generated automatically in the `reports/` directory:
- `report.html`: Interactive HTML report with charts and statistics
- `results_stats.csv`: Summary statistics for all requests
- `results_failures.csv`: Failed requests details

## Authentication

The framework supports JWT-based authentication via the `auth/jwt.py` module. Tokens are automatically:
1. Obtained using configured credentials at test start
2. Included in request headers
3. Refreshed as needed during test execution

Configure JWT settings in `config/env.yaml` and the module handles the rest automatically.

## Troubleshooting

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

## License

This project is open source and available under the MIT License.
