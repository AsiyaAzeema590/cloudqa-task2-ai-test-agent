
from playwright.sync_api import Page


def execute_test_plan(page: Page, plan: dict):

    actions = plan.get("actions", [])

    if not actions:
        raise ValueError("AI returned no actions.")

    for index, action in enumerate(actions, start=1):

        action_type = action.get("action")

        print()
        print(f"[{index}/{len(actions)}] {action_type}")

        # -------------------------------------------------
        # NAVIGATE
        # -------------------------------------------------
        if action_type == "navigate":

            url = action.get("url")

            if not url:
                raise ValueError(
                    "Navigate action is missing URL."
                )

            print(f"      Opening: {url}")

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            page.wait_for_timeout(1000)

            print("      PASS")

        # -------------------------------------------------
        # CLICK
        # -------------------------------------------------
        elif action_type == "click":

            target = action.get("target")

            if not target:
                raise ValueError(
                    "Click action is missing target."
                )

            print(f"      Looking for: {target}")

            try:

                page.get_by_role(
                    "button",
                    name=target,
                    exact=True
                ).first.click(timeout=5000)

            except Exception:

                try:

                    page.get_by_role(
                        "link",
                        name=target,
                        exact=True
                    ).first.click(timeout=5000)

                except Exception:

                    try:

                        page.get_by_text(
                            target,
                            exact=True
                        ).first.click(timeout=5000)

                    except Exception:

                        page.get_by_text(
                            target,
                            exact=False
                        ).first.click(timeout=5000)

            print("      PASS")

        # -------------------------------------------------
        # FILL
        # -------------------------------------------------
        elif action_type == "fill":

            target = action.get("target")
            value = action.get("value", "")

            if not target:
                raise ValueError(
                    "Fill action is missing target."
                )

            print(f"      Filling: {target}")

            try:

                page.get_by_label(
                    target,
                    exact=True
                ).first.fill(value)

            except Exception:

                page.get_by_placeholder(
                    target,
                    exact=True
                ).first.fill(value)

            print("      PASS")

        # -------------------------------------------------
        # VERIFY TEXT
        # -------------------------------------------------
        elif action_type == "verify_text":

            expected_text = action.get("text")

            if not expected_text:
                raise ValueError(
                    "Verify text action is missing text."
                )

            print(
                f"      Checking: {expected_text}"
            )

            page.wait_for_load_state(
                "domcontentloaded"
            )

            page.wait_for_timeout(1000)

            # Method 1: Playwright text locator
            try:

                text_locator = page.get_by_text(
                    expected_text,
                    exact=False
                ).first

                text_locator.wait_for(
                    state="visible",
                    timeout=5000
                )

                print("      PASS")
                continue

            except Exception:
                pass

            # Method 2: body text
            try:

                body_text = page.locator(
                    "body"
                ).inner_text()

                if expected_text.lower() in body_text.lower():

                    print("      PASS")
                    continue

            except Exception:
                pass

            # Method 3: complete HTML text
            try:

                page_text = page.locator(
                    "html"
                ).text_content() or ""

                if expected_text.lower() in page_text.lower():

                    print("      PASS")
                    continue

            except Exception:
                pass

            raise AssertionError(
                f"Expected text was not found: "
                f"{expected_text}\n"
                f"Current URL: {page.url}"
            )

        # -------------------------------------------------
        # VERIFY URL
        # -------------------------------------------------
        elif action_type == "verify_url":

            expected_url = action.get("text")

            if not expected_url:
                raise ValueError(
                    "Verify URL action is missing text."
                )

            print(
                f"      Checking URL contains: "
                f"{expected_url}"
            )

            current_url = page.url

            if expected_url.lower() not in current_url.lower():

                raise AssertionError(
                    f"URL verification failed.\n"
                    f"Expected URL to contain: "
                    f"{expected_url}\n"
                    f"Current URL: {current_url}"
                )

            print("      PASS")

        # -------------------------------------------------
        # UNKNOWN ACTION
        # -------------------------------------------------
        else:

            raise ValueError(
                f"Unsupported action: {action_type}"
            )
