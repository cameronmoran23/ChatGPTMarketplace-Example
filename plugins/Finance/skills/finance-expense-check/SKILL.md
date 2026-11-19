---
name: finance-expense-check
description: "Check expense claims against a supplied policy and flag exceptions."
---

# Expense Policy Check

Compare submitted expense claims with the policy and records the user provides.

- Identify missing receipts or fields and apparent policy exceptions, with the relevant rule.
- Separate clear matches from items needing human review; do not infer approval authority or accuse a claimant.
- Summarize each exception with evidence and the next question.
- Format the result using the template in `assets/exception-report-template.md`. Keep its headings and table columns, and leave any section with nothing to report marked "None".

