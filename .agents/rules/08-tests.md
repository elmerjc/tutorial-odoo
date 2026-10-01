---
trigger: manual
globs: "**/tests/*.py"
---

# Odoo Test Rules

Apply when writing or modifying test files.

## Test base classes

| Use case | Class |
|---|---|
| Business logic, ORM | `odoo.tests.common.TransactionCase` |
| HTTP endpoints, controllers | `odoo.tests.common.HttpCase` |
| UI tours (browser) | `odoo.tests.common.HttpCase` + `self.start_tour()` |

## Structure

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError, AccessError


class TestMyFeature(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create shared fixtures here — runs once per class
        cls.partner = cls.env["res.partner"].create({"name": "Test"})

    def test_something_meaningful(self):
        # Arrange
        record = self.env["my.model"].create({...})
        # Act
        record.action_confirm()
        # Assert
        self.assertEqual(record.state, "confirmed")
```

## Rules

- Tests must be **deterministic** — no dependency on existing DB data.
- Use `setUpClass` for shared fixtures; `setUp` for per-test mutable state.
- Test **behavior**, not implementation details.
- Do not test Odoo core behavior — only custom logic.
- Use `with self.assertRaises(ValidationError):` to test constraints.
- Use `with self.assertRaises(AccessError):` to test access control.
- Do not create tests for trivial field assignments.
- Each test method must test one logical behavior.

## Running tests

```bash
# Run all tests for a module
docker compose exec web odoo -d <db> --test-enable -u <module> --stop-after-init

# Run a specific test class
docker compose exec web odoo -d <db> --test-enable -u <module> \
  --test-tags <module>.TestMyFeature --stop-after-init

# Run a specific test method
docker compose exec web odoo -d <db> --test-enable -u <module> \
  --test-tags <module>.TestMyFeature.test_something_meaningful --stop-after-init
```