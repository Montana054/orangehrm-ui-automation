# OrangeHRM UI Automation Tests

![UI Tests](https://github.com/Montana054/orangehrm-ui-automation/actions/workflows/tests.yml/badge.svg)


This project demonstrates UI test automation using Python, Selenium, and Pytest for the [OrangeHRM Open Source Demo](https://opensource-demo.orangehrmlive.com/).  
It follows the Page Object Model (POM) and includes both functional and end-to-end scenarios.

## ✅ Features

- Python + Selenium + Pytest
- Page Object Model (POM)
- Allure for reporting
- Configurable browsers (Chrome, headless mode)
- Structured logging
- Parameterized data from CSV (for employee search)

## 📂 Project Structure

```
project-root/ 
├── pages/ # Page Object classes 
│ ├── base_page.py 
│ ├── login_page.py 
│ ├── main_page.py 
│ └── employee_page.py 
├── tests/ # Test files 
│ ├── conftest.py # Fixtures, browser setup 
│ ├── test_login.py # Login tests 
│ ├── test_main.py # Add/search employee, CSV check 
│ ├── test_employee.py # E2E scenarios 
│ └── test_logout.py 
├── utils/ # Helpers 
│ ├── config.py 
│ ├── data_helper.py 
│ └── logger.py ├── data/
│ └── users.csv # Saved employee info 
├── screenshots/ # Error screenshots on failure 
├── screenshots_allure/ # Screenshots for report preview 
├── requirements.txt └── README.md
```

## 🚀 How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run all tests (GUI mode):
```bash
pytest tests/
```

3. Run in headless mode:
```bash
pytest tests/ --headless
```

4. Generate Allure report:
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```
## 📈 Example Test Scenarios Covered

- Valid login (Admin, Employee)
- Invalid login (wrong credentials)
- Logout
- Add employee (UI form)
- CSV save and search validation
- Full E2E: Admin creates user → user logs in

## 🖼 Allure Report Preview
### ✅ Overview
![Overview](screenshots_allure/overview.png)

### ✅ Test Suites (Login, Employee, E2E)
![Test Suites](screenshots_allure/test_suite_list.png)

### ✅ Terminal & Report
![Terminal Success](screenshots_allure/terminal_run_success.png)

## 🔍 Tech Stack

- Python 3.x
- Selenium WebDriver
- Pytest
- Allure
- WebDriver Manager

## ✍ Author- 
Created by Anatolii Zakharov as part of QA Automation portfolio.