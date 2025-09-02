# Webform Automation with Playwright and MySQL

This project automates filling the [DemoQA Automation Practice Form](https://demoqa.com/automation-practice-form) using Python, Playwright, and data stored in a MySQL database.

---

## Features

- Fetches user data from a MySQL database (`users_v2` table).
- Fills all form fields:
  - First Name, Last Name, Email
  - Gender
  - Mobile
  - Date of Birth
  - Subjects (handles autocomplete properly)
  - Hobbies
  - Profile Picture
  - Current Address
  - State and City (handles City, State order from database)
- Submits the form automatically.
- Waits for the confirmation modal and closes it before continuing to the next user.

---

## Requirements

- Python 3.10 or higher
- [Playwright](https://playwright.dev/python/)
- MySQL database with a table named `users_v2`
- VSCode or any Python IDE

---

## Installation

1. **Clone the repository**:

```bash
git clone git clone https://github.com/Carlosnp23/Webform-Automation-Playwright_V2.git
cd Webform-Automation-Playwright
