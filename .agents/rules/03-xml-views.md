---
trigger: glob
globs: **/*.xml
---

# Odoo XML Rules

Apply when modifying XML files.

## Views

- Prefer inherited views.
- Use XPath whenever possible.
- Never copy an entire Odoo view just to modify one element.
- Use stable XPath expressions.
- Avoid brittle positional XPath selectors.
- Preserve existing attributes unless intentionally changing them.

## Buttons

Before creating or replacing a button:

1. Search for the existing button.
2. Identify its XML ID.
3. Determine its current action/method.
4. Determine visibility and security conditions.
5. Modify only the required attribute or element.

## Fields

Before adding a field to a view:

- Verify the field exists.
- Verify the model.
- Check visibility conditions.
- Check readonly conditions.
- Check groups/security.

## XML quality

- Keep XML readable.
- Avoid unnecessary nesting.
- Do not change unrelated views.