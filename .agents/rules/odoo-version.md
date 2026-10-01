---
trigger: always_on
---

# Odoo Version Policy

This project runs **Odoo 19** (Community + Enterprise) with Python 3.12 and PostgreSQL 16.

## Rules

- Always target Odoo 19 APIs. Do not use deprecated APIs from earlier versions.
- Do not assume APIs from Odoo 17 or 18 are identical — verify in the repository first.
- Before using any version-dependent API:
  1. Search the installed addons (`addons/`, `odoo/`) for existing usage patterns.
  2. Prefer patterns already used in `custom-addons/`.
  3. Consult external documentation only when the repository gives insufficient signal.

## OWL version

Odoo 19 ships with **OWL 2**. Use OWL 2 hooks and lifecycle methods:

- `onWillStart`, `onMounted`, `onWillUnmount`, `onWillUpdateProps`
- `useState`, `useRef`, `useService`, `useEnv`
- Do **not** use OWL 1 patterns (`willStart`, `mounted`, `willUnmount`).

## Key Odoo 19 changes to respect

- `ir.actions.act_window` `view_type` → use `view_mode`.
- Chatter uses `mail.chatter` component (OWL).
- `_sql_constraints` still supported.
- `fields.Html` uses Odoo's sanitizer by default; set `sanitize=False` only with justification.
- `website` module uses QWeb + OWL for interactive components.

When the project is upgraded, update this rule.