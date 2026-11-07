# CloudQA Task 2 - AI Test Agent

An AI-powered browser test automation tool that converts plain-English test cases into structured browser actions and executes them using Playwright.

## Features

- Accepts plain-English test cases
- Uses Google Gemini to generate a structured test plan
- Executes browser actions using Playwright
- Supports navigation, clicking, form filling, text verification, and URL verification
- Reports PASS or FAIL
- Uses semantic browser locators instead of fixed CSS/XPath selectors
- Designed to work with different websites and test cases

## Architecture

```text
Plain-English Test Case
          |
          v
       Gemini AI
          |
          v
   Structured JSON Plan
          |
          v
      Playwright
          |
          v
       Browser
          |
          v
      PASS / FAIL
```

## Technologies

- Python
- Google Gemini API
- Playwright
- python-dotenv

## Project Structure

```text
cloudqa-task2-ai-test-agent/
│
├── agent/
│   ├── ai_planner.py
│   └── executor.py
│
├── screenshots/
│
├── main.py
├── test_browser.py
├── test_gemini.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd cloudqa-task2-ai-test-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Chromium

```bash
playwright install chromium
```

### 6. Configure Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is ignored by Git and should never be committed.

## Run

```bash
python main.py
```

The program asks for:

1. Website URL
2. Plain-English test case

Example:

```text
Website URL:
https://example.com

Test case:
Verify that the page contains the text Example Domain
```

The AI generates a test plan and Playwright executes it in a browser.

## Example Result

```text
[1/2] navigate
      Opening: https://example.com
      PASS

[2/2] verify_text
      Checking: Example Domain
      PASS

==================================================
TEST RESULT: PASS
==================================================
```

## PHPTravels Test

The agent was also tested with the PHPTravels demo website.

Example test:

```text
Website URL:
https://phptravels.com/demo

Test case:
Verify that the PHPTravels demo website loads successfully
```

The generated test successfully navigated to the website and verified the URL.

## Limitations

The agent uses AI-generated plans and semantic browser locators. Because web pages can have different structures and ambiguous labels, some complex interactions may require additional locator strategies or AI planning improvements.

The solution intentionally avoids hard-coded selectors for a specific website so that it can be tested on unseen websites.

## Security

The Gemini API key is stored in `.env` and is excluded from Git using `.gitignore`.

Never commit the `.env` file or expose the API key publicly.