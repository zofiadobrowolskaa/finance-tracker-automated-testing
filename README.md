# Finance Tracker

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![Code Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://coverage.readthedocs.io/)
[![Testing](https://img.shields.io/badge/testing-pytest%20%7C%20behave-orange.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A comprehensive REST API application for personal finance management, demonstrating industry-standard automated testing practices including unit, integration, performance, and BDD tests with full CI/CD automation.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Code Coverage](#code-coverage)

## Overview

Finance Tracker is a production-ready REST API built with Flask that enables users to manage their personal finances effectively. The application supports transaction tracking (income and expenses), balance calculations, multi-currency conversions via external API integration (NBP), and user account management with tiered features (Standard/Premium).

**Primary Goal:** This project serves as a comprehensive demonstration of automated testing methodologies, showcasing:
- Unit tests with dependency mocking
- Integration (API) tests
- Behavioral tests (BDD) using Gherkin syntax
- Performance testing for API endpoints
- 100% code coverage requirement
- Full CI/CD automation with GitHub Actions

## Key Features

### Transaction Management
- **CRUD Operations**: Create, read, update, and delete financial transactions
- **Transaction Categorization**: Automatic classification as Income or Expense
- **Historical Data**: Comprehensive transaction history with filtering capabilities
- **Data Validation**: Robust input validation (amounts, dates, categories)

### Financial Intelligence
- **Balance Calculation**: Real-time balance tracking (income minus expenses)
- **Budget Management**: Monthly spending limits with threshold monitoring
- **Multi-Currency Support**: Convert balances to USD, EUR, GBP using live exchange rates
- **Saving Goals**: User-based goal management (Standard: 1 goal, Premium: unlimited)

### User Management
- **User Profiles**: Complete user management with email validation
- **Age Verification**: Minimum age requirement (13+ years)
- **Account Tiers**: Standard and Premium account types with different feature sets
- **Email Validation**: RFC-compliant email format verification

### External Integrations
- **Currency Exchange API**: Integration with NBP API for real-time currency rates
- **Service Mocking**: Comprehensive mocking strategy for external dependencies

## Technology Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **Web Framework** | Flask |
| **Testing Frameworks** | Pytest, Behave (BDD), unittest.mock |
| **HTTP Client** | Flask Test Client, Requests |
| **Code Coverage** | Coverage.py (100% requirement) |
| **Code Quality** | Flake8 (PEP 8 compliance) |
| **CI/CD** | GitHub Actions |
| **API Integration** | NBP API (Polish National Bank) |

## Project Structure

```
finance-tracker-automated-testing/
├── .github/
│   └── workflows/          # CI/CD pipeline definitions
│       ├── unit-tests.yml
│       ├── api-tests.yml
│       ├── perf-tests.yml
│       └── bdd-tests.yml
├── src/
│   ├── __init__.py
│   ├── finance_manager.py  # Core business logic
│   ├── transaction.py      # Transaction model
│   ├── user.py            # User model and validation
│   ├── app/
│   │   ├── api.py         # REST API endpoints
│   │   └── __init__.py
│   └── utils/
│       ├── currency_service.py  # External API integration
│       ├── id_generator.py      # Unique ID generation
│       └── __init__.py
├── tests/
│   ├── unit/              # Unit tests with mocking
│   │   ├── test_finance_manager.py
│   │   ├── test_transaction.py
│   │   ├── test_user.py
│   │   └── test_currency_service.py
│   ├── api/               # Integration/API tests
│   │   └── test_finance_api.py
│   └── perf/              # Performance tests
│       └── test_performance.py
├── features/              # BDD scenarios (Gherkin)
│   ├── transaction_registry.feature
│   └── steps/
│       └── transaction_registry.py
├── htmlcov/              # Coverage reports (generated)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.10 or higher**
- **pip** - Python package installer (included with Python)
- **Git** - For cloning the repository

To verify your Python installation:
```bash
python --version  # Should show Python 3.10 or higher
```

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd finance-tracker-automated-testing
```

### Step 2: Create Virtual Environment

It is strongly recommended to use a virtual environment to avoid dependency conflicts:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/MacOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages from the requirements file:
```bash
pip install -r requirements.txt
```

**Required packages include:**
- `flask` - Web framework
- `requests` - HTTP library
- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin
- `behave` - BDD testing
- `flake8` - Code linter
- `coverage` - Code coverage measurement

## Running the Application

### Start the Development Server

**Windows (PowerShell):**
```powershell
$env:FLASK_APP = "src/app/api.py"
flask run
```

**Windows (Command Prompt):**
```cmd
set FLASK_APP=src/app/api.py
flask run
```

**Linux/MacOS:**
```bash
export FLASK_APP=src/app/api.py
flask run
```

The application will be available at: **http://127.0.0.1:5000**

### Verify Installation

Test if the API is running:
```bash
curl http://127.0.0.1:5000/api/summary
```

Expected response:
```json
{
  "user": "Alice",
  "balance": 0.0,
  "budget_status": "No limit set"
}
```

## API Documentation

### Base URL
```
http://127.0.0.1:5000/api
```

### Endpoints

#### 1. Add Transaction
Create a new financial transaction (income or expense).

**Endpoint:** `POST /api/transactions`

**Request Body:**
```json
{
  "amount": 100.50,
  "category": "Food",
  "date": "2026-02-11"  // Optional, defaults to today
}
```

**Response:** `201 Created`
```json
{
  "message": "Transaction added"
}
```

**Error Response:** `400 Bad Request` or `422 Unprocessable Entity`
```json
{
  "message": "Invalid transaction data"
}
```

**Income Categories:**
- Salary, Bonus, Gift, Interest

**Expense Categories:**
- All other categories (Food, Transport, Shopping, etc.)

---

#### 2. Get Transaction History
Retrieve all transactions for the current user.

**Endpoint:** `GET /api/transactions`

**Response:** `200 OK`
```json
[
  {
    "transaction_id": "TXN-123456",
    "amount": 2000,
    "category": "Salary",
    "type": "Income",
    "date": "2026-02-01"
  },
  {
    "transaction_id": "TXN-123457",
    "amount": 150.50,
    "category": "Food",
    "type": "Expense",
    "date": "2026-02-05"
  }
]
```

---

#### 3. Get Account Summary
Retrieve user's current balance and budget status.

**Endpoint:** `GET /api/summary`

**Response:** `200 OK`
```json
{
  "user": "Alice",
  "balance": 1849.50,
  "budget_status": "Within limit"
}
```

---

#### 4. Filter Transactions by Type
Get filtered transaction history (Income or Expense).

**Endpoint:** `GET /api/transactions/filter?type={Income|Expense}`

**Response:** `200 OK`
```json
[
  {
    "transaction_id": "TXN-123456",
    "amount": 2000,
    "category": "Salary",
    "type": "Income",
    "date": "2026-02-01"
  }
]
```

---

#### 5. Set Monthly Budget Limit
Define a monthly spending limit.

**Endpoint:** `POST /api/limit`

**Request Body:**
```json
{
  "limit": 5000
}
```

**Response:** `200 OK`
```json
{
  "message": "Limit set successfully"
}
```

---

#### 6. Convert Balance to Currency
Get current balance converted to specified currency.

**Endpoint:** `GET /api/balance/{currency_code}`

**Supported currencies:** `USD`, `EUR`, `GBP`

**Response:** `200 OK`
```json
{
  "balance_pln": 1849.50,
  "balance_usd": 462.38,
  "currency": "USD"
}
```

### Example Usage with cURL

```bash
# Add a transaction
curl -X POST http://127.0.0.1:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 500, "category": "Salary"}'

# Get transaction history
curl http://127.0.0.1:5000/api/transactions

# Get account summary
curl http://127.0.0.1:5000/api/summary

# Set monthly limit
curl -X POST http://127.0.0.1:5000/api/limit \
  -H "Content-Type: application/json" \
  -d '{"limit": 3000}'

# Get balance in USD
curl http://127.0.0.1:5000/api/balance/USD
```

## Testing

This project maintains **100% code coverage** and implements multiple testing strategies to ensure code quality and reliability.

### Testing Strategy Overview

| Test Type | Purpose | Framework | Coverage |
|-----------|---------|-----------|----------|
| **Unit Tests** | Test isolated business logic with mocked dependencies | Pytest + unittest.mock | Core logic |
| **API Tests** | Integration testing of REST endpoints (Black Box) | Pytest + Requests | API layer |
| **Performance Tests** | Verify API response times and stability under load | Pytest | API endpoints |
| **BDD Tests** | Behavior verification using user-centric scenarios | Behave (Gherkin) | User flows |

### Running All Tests

To run the complete test suite with coverage:
```bash
python -m pytest --cov=src --cov-report=html --cov-report=term tests/
```

### Unit Tests

Unit tests focus on individual components with external dependencies mocked (e.g., NBP API, ID generators).

**Run unit tests:**
```bash
python -m pytest tests/unit -v
```

**Run specific test file:**
```bash
python -m pytest tests/unit/test_finance_manager.py -v
```

**Example test coverage:**
- `test_finance_manager.py` - Balance calculations, budget limits, currency conversion
- `test_transaction.py` - Transaction creation, validation, categorization
- `test_user.py` - User validation, saving goals, account tiers
- `test_currency_service.py` - External API mocking and error handling

---

### API Tests (Integration Tests)

Integration tests verify the complete request-response cycle of REST endpoints using actual HTTP requests.

**Run API tests:**
```bash
python -m pytest tests/api -v
```

**What's tested:**
- HTTP status codes (200, 201, 400, 404, 422)
- Request/response payload validation
- Content-Type headers
- Error handling and edge cases
- End-to-end transaction flows

---

### Performance Tests

Performance tests ensure the API can handle expected load with acceptable response times.

**Run performance tests:**
```bash
python -m pytest tests/perf -v
```

**Performance benchmarks:**
- Individual endpoint response time: < 100ms
- Concurrent requests: Handle 50+ simultaneous transactions
- Memory stability: No leaks during extended operation

---

### BDD Tests (Behavior-Driven Development)

BDD tests use Gherkin syntax to describe system behavior from a user's perspective.

**Run BDD tests:**
```bash
behave
```

**Example Gherkin scenario:**
```gherkin
Scenario: User creates and verifies transactions
  Given Transaction registry is empty
  When I create a transaction amount: "1000", category: "Salary"
  And I create a transaction amount: "200", category: "Food"
  Then The account balance should be "800.0"
  And Number of transactions in registry equals: "2"
```
---

### Code Quality & Linting

Ensure code follows PEP 8 standards:
```bash
flake8 src/ tests/
```

## Code Coverage

This project enforces **100% code coverage** as a quality gate in the CI/CD pipeline.

### Generate Coverage Report

**HTML Report (Recommended):**
```bash
python -m pytest --cov=src --cov-report=html tests/
```

Open the report:
```bash
# Windows
start htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# MacOS
open htmlcov/index.html
```

**Terminal Report:**
```bash
python -m pytest --cov=src --cov-report=term-missing tests/
```

### Coverage Requirements

- **Minimum threshold:** 100%
- **Branches:** All conditional paths tested
- **Edge cases:** Negative values, invalid inputs, error conditions
- **Mocked dependencies:** External APIs (NBP), ID generation

---

## CI/CD Pipeline

The project uses **GitHub Actions** for continuous integration and deployment. All workflows trigger automatically on:
- `push` to the `main` branch
- Pull requests targeting `main`

### Workflow Definitions

#### 1. Unit Tests Workflow (`unit-tests.yml`)
```yaml
Triggers: push, pull_request
Steps:
  - Checkout code
  - Set up Python 3.10
  - Install dependencies
  - Run flake8 linter
  - Run unit tests with pytest
  - Verify 100% code coverage
  - Upload coverage report
```

**Status:** View in GitHub Actions → Unit Tests

---

#### 2. API Tests Workflow (`api-tests.yml`)
```yaml
Triggers: push, pull_request
Steps:
  - Checkout code
  - Set up Python 3.10
  - Install dependencies
  - Start Flask application
  - Run API integration tests
  - Verify endpoint responses
```

**Status:** View in GitHub Actions → API Tests

---

#### 3. Performance Tests Workflow (`perf-tests.yml`)
```yaml
Triggers: push, pull_request
Steps:
  - Checkout code
  - Set up Python 3.10
  - Install dependencies
  - Start Flask application
  - Run performance benchmarks
  - Verify response time thresholds
```

**Status:** View in GitHub Actions → Performance Tests

---

#### 4. BDD Tests Workflow (`bdd-tests.yml`)
```yaml
Triggers: push, pull_request
Steps:
  - Checkout code
  - Set up Python 3.10
  - Install dependencies
  - Start Flask application
  - Run Behave scenarios
  - Verify all features pass
```

**Status:** View in GitHub Actions → BDD Tests

---
## Future Enhancements

Planned features and improvements:

- [ ] User authentication and authorization (JWT)
- [ ] PostgreSQL database integration
- [ ] Docker containerization
- [ ] Real-time notifications
- [ ] Advanced reporting and analytics
- [ ] Mobile app integration
- [ ] Multi-language support
