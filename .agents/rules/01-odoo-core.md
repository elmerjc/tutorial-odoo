---
trigger: always_on
---

# Odoo Core Development Rules

Apply these rules to all Odoo development.

## Architecture

- Never modify Odoo core unless explicitly requested.
- Extend existing models using inheritance.
- Extend views using XML inheritance.
- Reuse existing Odoo mechanisms before creating custom ones.
- Search the repository before creating a new model, method, field, view, wizard or utility.

## ORM

- Prefer ORM over SQL.
- Work with recordsets.
- Prefer batch operations.
- Avoid N+1 queries.
- Do not browse records repeatedly inside loops when the recordset can be prefetched.
- Use `sudo()` only when technically necessary and document why.

## Changes

Before changing code:

1. Locate the existing implementation.
2. Read only the relevant files.
3. Identify dependencies.
4. Make the smallest correct change.

Do not refactor unrelated code.

## Existing code

When modifying existing files:

- Preserve the existing style.
- Minimize the diff.
- Do not reformat unrelated sections.
- Do not rename unrelated variables.
- Do not reorder imports unless necessary.

## Verification

After modifications:

- Inspect the git diff.
- Run the smallest relevant verification.
- If a test fails, diagnose the actual cause before changing more code.