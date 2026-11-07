import os
import json
import time

from google import genai
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")


client = genai.Client(api_key=api_key)


def generate_with_retry(prompt: str):
    """
    Send the prompt to Gemini.
    Retry temporary server errors before failing.
    """

    model = "gemini-3.5-flash"

    for attempt in range(3):
        try:
            print(
                f"Calling Gemini "
                f"(attempt {attempt + 1}/3)..."
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response

        except Exception as error:

            print(
                f"Gemini request failed: {error}"
            )

            if attempt < 2:
                print(
                    "Gemini may be temporarily busy. "
                    "Retrying in 5 seconds..."
                )

                time.sleep(2)

            else:
                raise


def create_test_plan(test_case: str):

    prompt = f"""
You are an AI web test planner.

Convert the following plain-English test case
into a simple JSON browser automation plan.

Test case:
{test_case}

Return ONLY valid JSON.

Supported actions:

1. navigate

Example:
{{
    "action": "navigate",
    "url": "https://example.com"
}}

2. click

Example:
{{
    "action": "click",
    "target": "Login"
}}

3. fill

Example:
{{
    "action": "fill",
    "target": "Email",
    "value": "test@example.com"
}}

4. verify_text

Example:
{{
    "action": "verify_text",
    "text": "Dashboard"
}}

5. verify_url

Example:
{{
    "action": "verify_url",
    "text": "dashboard"
}}

Return this format:

{{
    "actions": [
        {{
            "action": "...",
            "target": "...",
            "value": "..."
        }}
    ]
}}

Rules:

- Return ONLY JSON.
- Do not generate Python code.
- Do not generate Playwright code.
- Do not use CSS selectors.
- Do not use XPath.
- Do not hard-code a specific website.
- Use semantic descriptions such as "Login",
  "Email", "Dashboard", etc.
"""

    response = generate_with_retry(prompt)

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)