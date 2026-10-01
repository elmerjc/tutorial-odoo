---
description: Upgrade an existing Odoo module after model or view changes.
---

# Upgrade Odoo Module

Apply pending changes to an installed Odoo 19 module.

## When to use

Run an upgrade (`-u`) when you have changed:

- Python models (fields, methods, constraints)
- XML views, actions, or menus
- Security files (`ir.model.access.csv`, record rules)
- Data files

A module **reinstall** (`-i`) is only needed when the module is not yet installed.

## Process

### 1. Verify the change is saved

```bash
git diff --name-only
```

Confirm the modified files are saved.

### 2. Upgrade

```bash
docker compose exec web odoo -d <database> -u <module_name> --stop-after-init
```

For multiple modules:

```bash
docker compose exec web odoo -d <database> -u module_a,module_b --stop-after-init
```

### 3. Check logs

```bash
docker compose logs --tail=100 web
```

Look for:

- `ERROR` — fix before proceeding.
- `WARNING` about views — usually an XPath mismatch.
- Migration errors — model/field changes may need a migration script.

### 4. Verify behavior

- Open the Odoo UI and navigate to the affected area.
- Confirm the feature works as specified.
- Check that existing features are not broken.

### 5. Inspect diff

```bash
git diff
```

No unintended changes.

## Common upgrade issues

| Symptom | Likely cause |
|---|---|
| `Field ... does not exist` | Column not created — check model `_name` and `_inherit` |
| `View ... not found` | XML ID mismatch or missing `inherit_id` |
| `ir.model.access` error | Missing access rule for a model |
| Stale computed field | `depends` missing or inaccurate — force recompute via shell |

### Force recompute a stored computed field

```bash
docker compose exec web odoo shell -d <database>
# then in the shell:
env['my.model'].search([]).sudo()._compute_my_field()
env.cr.commit()
```
