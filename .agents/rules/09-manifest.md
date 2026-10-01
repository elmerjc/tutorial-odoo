---
trigger: glob
globs: "**/__manifest__.py"
---

# Odoo Manifest Rules

Apply when creating or modifying a `__manifest__.py` file.

## Required fields

```python
{
    "name": "Human Readable Name",       # required
    "version": "19.0.1.0.0",            # required — major.minor.patch.fix
    "summary": "One-line description",   # required
    "category": "...",                   # use Odoo's standard categories
    "author": "Takana Cloud",            # required
    "license": "LGPL-3",                 # required — LGPL-3 or OPL-1
    "depends": [...],                    # required — minimal and accurate
    "data": [...],                       # required — load order matters
    "installable": True,
    "auto_install": False,               # True only for bridge modules
}
```

## Version convention

`19.0.<major>.<minor>.<patch>`

- `19.0` — Odoo major version prefix (never change this).
- `<major>` — increment on breaking changes (field renames, removed features).
- `<minor>` — increment on new features.
- `<patch>` — increment on bug fixes.

Start at `19.0.1.0.0` for new modules.

## `depends` rules

- Only list **direct** dependencies.
- Do not add a dependency that is already a dependency of another listed module.
- Do not add `base` if another listed module already depends on it (except for modules that only extend `base`).
- Verify each dependency is available in `addons/` or `odoo/`.

## `data` load order

Load files in this order:

1. Security groups (`security/security_groups.xml`)
2. Access rights (`security/ir.model.access.csv`)
3. Record rules (`security/record_rules.xml`)
4. Configuration data (`data/*.xml`)
5. Views, actions, menus (`views/*.xml`)
6. Email templates, reports (`templates/`, `report/`)
7. Demo data in `demo` key, not `data`

## Checks before saving

- [ ] `version` follows `19.0.x.y.z`.
- [ ] `license` declared.
- [ ] All files in `data` actually exist.
- [ ] No file listed twice.
- [ ] `depends` list does not include modules not available in this project.
- [ ] `auto_install` is `False` unless this is intentionally a bridge module.
