---
description: Create a new Odoo 19 custom addon from scratch.
---

# Create Odoo Module

Create a new Odoo 19 addon in `custom-addons/`.

## Process

### 1. Clarify requirements

Before writing any code:

- Confirm the technical name (snake_case, no spaces).
- Confirm the business purpose.
- Identify which Odoo modules it extends (`sale`, `account`, `stock`, etc.).
- If requirements are ambiguous, ask before implementing architecture.

### 2. Search for existing solutions

- Search `custom-addons/` for similar functionality.
- Search `addons/` and `odoo/` for reusable models, mixins, and views.
- Do not create what already exists.

### 3. Plan the structure

Determine the minimum required files:

```
custom-addons/<module_name>/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── <model>.py
├── views/
│   └── <model>_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security_groups.xml        # only if new groups are needed
├── data/                           # only if needed
├── wizard/                         # only if needed
├── static/src/                     # only if JS/CSS needed
└── i18n/                           # only if shipping translations
```

Do not create empty directories or placeholder files.

### 4. Create the manifest

```python
{
    "name": "Module Name",
    "version": "19.0.1.0.0",
    "summary": "One-line description",
    "category": "Category",
    "author": "Takana Cloud",
    "license": "LGPL-3",
    "depends": ["base"],           # minimal accurate list
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/<model>_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
```

### 5. Implement models

For each model:

1. Search for an existing model to extend (`_inherit`) before creating a new one (`_name`).
2. Define only the fields required by the specification.
3. Add `_description` to every model.
4. Add `company_id` if the model must be multi-company aware.
5. Add `active` field only if archiving is a real requirement.

### 6. Implement security

For every model:

1. Create `security/ir.model.access.csv`:

   ```csv
   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
   access_my_model_user,access.my.model.user,model_my_model,base.group_user,1,1,1,0
   access_my_model_manager,access.my.model.manager,model_my_model,base.group_system,1,1,1,1
   ```

2. Add record rules if row-level access is needed.
3. Do not grant more access than required.

### 7. Implement views and actions

- Prefer inherited views when extending existing forms.
- Create a minimal form view, list view, and action per model.
- Add menu items with correct parent and sequence.

### 8. Validate

- [ ] Manifest `depends` is accurate.
- [ ] Manifest `data` load order: security → data → views.
- [ ] All XML IDs are unique and follow `<module>.<meaningful_name>`.
- [ ] `ir.model.access.csv` covers all new models.
- [ ] No unused models, fields, or views.

### 9. Install and verify

```bash
docker compose exec web odoo -d <database> -i <module_name> --stop-after-init
```

Check the log for errors. Fix before continuing.

### 10. Inspect git diff

```bash
git diff --stat
git diff
```

Confirm only intended files are modified.

## Rules

- Do not generate demo data unless requested.
- Do not generate README files unless requested.
- Do not create unused models, fields, views, or wizard files.
- Do not create unnecessary utilities or services.
- Reuse existing Odoo functionality whenever possible.