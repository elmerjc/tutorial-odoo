---
trigger: glob
globs: "**/models/*.py, **/security/*.csv, **/security/*.xml, **/__manifest__.py"
---

# Odoo Security Rules

Apply when creating or modifying models, menus, actions, or business operations.

## Access control checklist

When adding a new model:

1. **`ir.model.access.csv`** — define read/write/create/unlink per group.
2. **Groups** — assign to the appropriate group (`base.group_user`, a custom group, etc.).
3. **Record rules** — define domain-based row-level access if users must be isolated.
4. **Multi-company** — add `company_id = fields.Many2one('res.company', ...)` and filter by `company_id`.
5. **`sudo()`** — use only when technically necessary; add a comment explaining the reason.

## Mandatory checks before approving code

- [ ] Every new model has at least one `ir.model.access.csv` entry.
- [ ] No model grants more access than required (principle of least privilege).
- [ ] Record rules don't accidentally expose cross-company records.
- [ ] `sudo()` usage is minimal and documented.
- [ ] Security files are loaded **before** views in the manifest `data` list.

## Multi-company

When a model stores company-specific data:

```python
company_id = fields.Many2one(
    "res.company",
    string="Company",
    required=True,
    default=lambda self: self.env.company,
)
```

Add a record rule to restrict access:

```xml
<record id="rule_my_model_company" model="ir.rule">
    <field name="name">My Model: company</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="global" eval="True"/>
    <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
</record>
```

## Never

- Use UI hiding as an access control mechanism.
  - Hidden buttons, disabled fields, and invisible conditions are **not** security.
- Use `sudo()` to bypass an access error without understanding why access is denied.
- Grant `perm_unlink=1` to regular users without explicit justification.
- Store sensitive data (passwords, tokens) in plain `Char` fields — use `password`-type or encrypted storage.