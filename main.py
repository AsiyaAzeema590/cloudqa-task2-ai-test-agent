from playwright.sync_api import sync_playwright

from agent.ai_planner import create_test_plan
from agent.executor import execute_test_plan


def main():

    print("=" * 50)
    print("CloudQA Task 2 - AI Test Agent")
    print("=" * 50)

    print()
    website_url = input("Enter website URL: ").strip()

    print()
    test_case = input("Enter test case: ").strip()

    if not website_url:
        print("ERROR: Website URL is required.")
        return

    if not test_case:
        print("ERROR: Test case is required.")
        return

    # Add the URL to the test case if the user
    # did not include it.
    complete_test_case = f"""
Website URL:
{website_url}

Test case:
{test_case}
"""

    try:

        print()
        print("Planning test with Gemini...")

        plan = create_test_plan(
            complete_test_case
        )

        print()
        print("AI generated plan:")
        print(plan)

        print()
        print("Starting browser...")

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            try:

                print()
                print("Executing test...")

                execute_test_plan(
                    page,
                    plan
                )

                print()
                print("=" * 50)
                print("TEST RESULT: PASS")
                print("=" * 50)

            except Exception as error:

                print()
                print("=" * 50)
                print("TEST RESULT: FAIL")
                print("=" * 50)

                print()
                print("Reason:")
                print(error)

            finally:

                print()
                print("Closing browser...")

                browser.close()

    except Exception as error:

        print()
        print("=" * 50)
        print("TEST RESULT: FAIL")
        print("=" * 50)

        print()
        print("Error:")
        print(error)


if __name__ == "__main__":
    main()