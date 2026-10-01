---
trigger: glob
globs: **/*.py
---

# Odoo Python Rules

Apply when modifying Python files.

- Follow Odoo coding conventions.
- Prefer ORM APIs.
- Prefer recordset operations.
- Avoid unnecessary searches inside loops.
- Avoid raw SQL unless ORM cannot reasonably solve the problem.
- Do not add defensive code for impossible states without evidence.
- Do not add type annotations unless the project already uses them.
- Do not add docstrings to trivial Odoo methods.
- Keep methods small and focused.
- Preserve existing method structure when extending stable code.

When overriding an Odoo method:

1. Understand the parent implementation.
2. Call `super()` unless there is a specific reason not to.
3. Preserve the expected return contract.
4. Preserve context and company behavior.
5. Consider batch operations.

Before adding a field:

- Search for an existing field with equivalent semantics.
- Check dependencies.
- Check whether a related field can solve the requirement.