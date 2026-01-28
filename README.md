# Finance Tracker

- **Author:** Zofia Dobrowolska
- **Group:** 1

## Project Description

Finance Tracker is a REST API application built with Python (Flask) designed for personal finance management. The system allows users to register transactions (incomes and expenses), calculate balances, convert currencies based on external API data (NBP), and manage saving goals depending on the user status (Standard/Premium).

The primary goal of this project is to demonstrate a comprehensive approach to automated testing, including unit tests, integration (API) tests, behavioral tests (BDD), and performance tests, along with full CI/CD automation.

## Scope of Functionality

1. **Transaction Management (CRUD):** Adding, retrieving history, updating categories, and deleting transactions.
2. **Business Logic:**
   - Balance calculation (incomes minus expenses).
   - Budget limit verification.
   - Input data validation (e.g., negative amounts, missing fields).
3. **User Logic:**
   - Age validation (user must be at least 13 years old).
   - Account status handling (Standard vs. Premium) affecting saving goal limits.
4. **External Integration:**
   - Balance conversion to other currencies (USD, EUR, GBP) using simulated connections to the NBP API (mocking).

## Technologies

- **Language:** Python 3.10+
- **Application Framework:** Flask
- **Testing:** Pytest, Behave, Unittest.mock
- **HTTP Client (Testing):** Flask Test Client
- **Code Coverage:** Coverage.py
- **CI/CD:** GitHub Actions

## Project Structure

- `src/` - Application source code (API, finance manager, user logic).
- `tests/unit/` - Unit tests with dependency mocking.
- `tests/api/` - Integration tests for REST API endpoints.
- `tests/perf/` - API performance tests.
- `features/` - BDD test scenarios (Gherkin).
- `.github/workflows/` - CI/CD pipeline configuration.

## Setup Instructions

### 1. Environment Preparation

It is recommended to create a virtual environment:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate

# Linux/MacOS:
source venv/bin/activate
```

### 2. Install Dependencies

Install all required packages from the requirements file:
```bash
pip install -r requirements.txt
```

### 3. Running the Application
To start the Flask development server:

```bash
# Windows (PowerShell):
$env:FLASK_APP = "src/app/api.py"
flask run

# Linux/MacOS:
export FLASK_APP=src/app/api.py
flask run
```
The application will be available at: http://127.0.0.1:5000

### 4. Running Tests
The project is configured to maintain 100% code coverage.

**Unit Tests**
- Test isolated business logic using mocks (e.g., for the NBP API).

```bash
python -m pytest tests/unit
```

**API Tests (Integration Tests)**
- Test HTTP endpoint functionality using `requests` (Black Box testing).

```bash
python -m pytest tests/api
```

**Performance Tests**
- Verify API speed and stability under higher operation loads.

```bash
python -m pytest tests/perf
```

**BDD Tests (Behavior-Driven Development)**
- Execute scenarios written in Gherkin, describing system behavior from a user's perspective.

```bash
behave
```

**Code Coverage Report**
- To generate an HTML report checking code coverage (requirement: 100%):

```bash
python -m pytest --cov=src --cov-report=html tests
```

The report will be generated in the htmlcov/index.html directory.


**CI/CD (GitHub Actions)**
- The repository has configured GitHub Actions workflows that trigger automatically on every Push and Pull Request to the main branch.

**Defined pipelines:**

1. Unit tests: Runs unit tests, linter (flake8), and verifies that code coverage is 100%.

2. API tests: Runs integration tests for endpoints.

3. API Performance: Runs performance tests.

4. BDD Tests: Runs behavioral scenarios using Behave against the running application.

The execution status of tests is visible in the "Actions" tab on GitHub.