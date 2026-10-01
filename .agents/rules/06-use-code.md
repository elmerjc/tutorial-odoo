---
trigger: model_decision
---

# Reuse Existing Odoo Code

Before creating a new implementation:

1. Search the current addon.
2. Search sibling custom addons.
3. Search the Odoo addons available in the project.
4. Identify an existing model, method, mixin, utility or view that solves part of the problem.

Prefer:

existing Odoo mechanism
    >
existing project abstraction
    >
small extension
    >
new abstraction

Do not create a helper/service/util class unless reuse or separation is actually justified.