---
description: 
---

# Fix Odoo Bug

Follow this process:

1. Read the user's bug description.
2. Search for the relevant implementation.
3. Identify the smallest root cause.
4. Inspect only directly related files.
5. Implement the smallest fix.
6. Add or update a focused test if appropriate.
7. Run the smallest relevant test.
8. Inspect git diff.

Do not:

- refactor unrelated code
- rewrite complete files
- create unnecessary abstractions
- generate documentation
- explain every unchanged file

Final response:

- Root cause
- Files changed
- Verification performed
- Remaining uncertainty, if any