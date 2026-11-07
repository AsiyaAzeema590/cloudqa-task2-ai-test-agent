from agent.ai_planner import create_test_plan


test_case = """
Open https://example.com and verify that the page
contains the text Example Domain.
"""


print("Sending test case to Gemini...")
print()

plan = create_test_plan(test_case)

print("AI generated test plan:")
print()

print(plan)