---
description: Write or improve automated tests for an Odoo module.
---

# Write Odoo Tests

Write automated tests for Odoo 19 custom modules.

## Test types

| Type | Base class | When to use |
|---|---|---|
| Unit / integration | `TransactionCase` | Business logic, model methods, ORM |
| HTTP / controller | `HttpCase` | Controllers, JSON-RPC endpoints, website pages |
| Tours | `HttpCase` + `start_tour` | UI / browser interaction flows |

## Process

### 1. Identify what to test

- New model methods or overrides with non-trivial logic.
- Computed fields with complex dependencies.
- Constrains (`@api.constrains`).
- Onchange side effects that affect other records.
- Security: records that should/should not be accessible.
- Workflows: state transitions, button actions.

Do not write tests for trivial getters or Odoo-standard CRUD.

### 2. File location

```
custom-addons/<module>/
└── tests/
    ├── __init__.py
    ├── test_<feature>.py
    └── ...
```

Enable tests in the manifest:

```python
# __manifest__.py
"installable": True,
# no extra key needed — Odoo discovers tests/ automatically
```

### 3. Write the test

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError


class TestMyModel(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Test Partner",
        })

    def test_field_computed_correctly(self):
        record = self.env["my.model"].create({
            "partner_id": self.partner.id,
            "amount": 100,
        })
        self.assertEqual(record.computed_field, expected_value)

    def test_constraint_raises_on_invalid_value(self):
        with self.assertRaises(ValidationError):
            self.env["my.model"].create({"amount": -1})

    def test_user_cannot_access_other_company_record(self):
        # Test multi-company isolation
        other_company = self.env["res.company"].create({"name": "Other"})
        record = self.env["my.model"].sudo().create({
            "company_id": other_company.id,
        })
        # Switch to a user in the main company
        user = self.env.ref("base.user_demo")
        with self.assertRaises(Exception):
            self.env["my.model"].with_user(user).browse(record.id).name
```

### 4. Run tests

```bash
docker compose exec web odoo \
  -d <database> \
  --test-enable \
  -u <module_name> \
  --stop-after-init \
  --log-level=test
```

Run a specific test class or method:

```bash
docker compose exec web odoo \
  -d <database> \
  --test-enable \
  -u <module_name> \
  --test-tags <module_name>.TestMyModel \
  --stop-after-init
```

### 5. Verify

- All tests pass (no `ERROR` or `FAIL` in output).
- No test depends on external state or DB data not created in `setUpClass`.
- `git diff` shows only test files plus any production code changes.

## Rules

- Tests must be deterministic — no dependency on pre-existing DB records.
- Use `setUpClass` for shared fixtures; use `setUp` for per-test state.
- Test the behavior, not the implementation.
- Do not test Odoo core behavior — only custom logic.
- Do not create tests for trivial attribute assignments.
