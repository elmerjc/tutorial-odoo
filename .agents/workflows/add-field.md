---
description: Add a field to an existing Odoo model and its views.
---

# Add Field to Odoo Model

Add a new field to an existing model in a custom addon.

## Process

### 1. Check if the field already exists

```bash
grep -r "my_field_name" custom-addons/ addons/ odoo/
```

Do not add a field that already exists or can be addressed with a `related` field.

### 2. Determine field placement

- **Custom model** (`_name = 'my.module.model'`): add directly to the model file.
- **Inherited Odoo model** (`_inherit = 'res.partner'`): create or update the inheritance file in `custom-addons/<module>/models/`.

### 3. Choose the correct field type

| Requirement | Field type |
|---|---|
| Text (short) | `Char` |
| Text (long) | `Text` |
| Formatted text | `Html` |
| Integer | `Integer` |
| Decimal | `Float` or `Monetary` |
| Date | `Date` |
| Date + time | `Datetime` |
| Boolean | `Boolean` |
| Selection list | `Selection` |
| Many-to-one | `Many2one` |
| One-to-many | `One2many` |
| Many-to-many | `Many2many` |
| Derived value | `compute=` (stored or non-stored) |
| Mirror another field | `related=` |

### 4. Add the field

```python
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    my_field = fields.Char(
        string="My Field",
        help="Explain what this field represents.",
        copy=False,       # set if copying the record should not copy this value
        index=True,       # set only if searched frequently
    )
```

For computed fields:

```python
my_computed = fields.Float(
    string="Computed Value",
    compute="_compute_my_computed",
    store=True,           # store=True if needed for search/group
    depends=["related_field_id", "related_field_id.amount"],
)

def _compute_my_computed(self):
    for record in self:
        record.my_computed = sum(record.related_field_id.mapped("amount"))
```

### 5. Add to view

Use XML inheritance — do not rewrite the entire view:

```xml
<record id="view_res_partner_form_inherit_my_module" model="ir.ui.view">
    <field name="name">res.partner.form.inherit.my_module</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='phone']" position="after">
            <field name="my_field"/>
        </xpath>
    </field>
</record>
```

XPath guidelines:
- Use `[@name='...']` attribute selectors — not positional indices.
- `position="after"` | `"before"` | `"inside"` | `"replace"` | `"attributes"`.

### 6. Upgrade the module

```bash
docker compose exec web odoo -d <database> -u <module_name> --stop-after-init
```

### 7. Verify

- [ ] Field appears in the UI.
- [ ] Computed field value is correct.
- [ ] `store=True` fields are queryable from list view / filters.
- [ ] No unrelated views were changed.
- [ ] `git diff` shows only the intended changes.
