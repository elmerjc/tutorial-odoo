---
description: Review an Odoo addon for correctness, security, and quality.
---

# Review Odoo Module

Perform a structured review of a custom Odoo addon.

## Process

1. Read the module manifest (`__manifest__.py`).
2. Identify models, views, wizards, controllers, and assets.
3. Review each area below.

## Checklist

### ORM & Python

- [ ] No raw SQL where ORM can solve it.
- [ ] No N+1 queries (searches/browses inside loops).
- [ ] `super()` called in overridden methods unless documented reason not to.
- [ ] Return contracts of overridden methods preserved.
- [ ] Computed fields have `compute=` and appropriate `store=` / `depends=`.
- [ ] No unused imports, fields, or methods.
- [ ] `sudo()` usage is minimal and documented.

### Security

- [ ] Every model has an `ir.model.access.csv` entry.
- [ ] Record rules defined where row-level access is needed.
- [ ] Groups declared and assigned correctly.
- [ ] Multi-company: `company_id` present and filtered where required.
- [ ] No `sudo()` used to bypass access without justification.
- [ ] No security logic delegated to the UI.

### XML / Views

- [ ] All views use `inherit_id` where extending core views.
- [ ] XPath selectors are stable and specific (not positional).
- [ ] No entire view duplicated to modify one element.
- [ ] `string` attributes are translatable where needed.
- [ ] Buttons reference valid methods or actions.
- [ ] Fields in views exist on the model.

### Manifest

- [ ] `depends` list is minimal and accurate.
- [ ] `data` list includes all XML files in correct load order:
  - security files first
  - data/demo files
  - views and actions last
- [ ] `version` follows Odoo convention (`19.0.x.y.z`).
- [ ] `license` declared.

### Assets (JavaScript)

- [ ] Assets declared in the correct bundle.
- [ ] No duplicate asset declarations.
- [ ] OWL 2 patterns used (not OWL 1).
- [ ] No business logic in JavaScript.

### Translations

- [ ] User-facing strings wrapped with `_()` (Python) or translation tags (XML).
- [ ] `.pot` / `.po` files present if module ships translations.

### Performance

- [ ] No repeated ORM calls for the same record inside a loop.
- [ ] Computed fields with `store=True` have accurate `depends` to avoid stale values.
- [ ] No large recordset operations without pagination consideration.

### Tests

- [ ] Business logic has at least one test.
- [ ] Tests use `TransactionCase` or `HttpCase` as appropriate.
- [ ] Tests clean up after themselves (or rely on transaction rollback).

## Output format

For each issue found:

```
[SEVERITY] file:line — description
```

Severity: `CRITICAL` | `WARNING` | `INFO`

Finish with a summary count per severity.