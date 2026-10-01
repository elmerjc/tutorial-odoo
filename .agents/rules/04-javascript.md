---
trigger: glob
globs: **/*.js, **/*.xml
---

# Odoo JavaScript / OWL Rules (Odoo 19 / OWL 2)

Apply these rules when modifying JavaScript, OWL components, frontend behavior,
webclient code or assets.

## General principles

- Search `custom-addons/`, `addons/`, and `odoo/` for an existing implementation first.
- Prefer extending or reusing existing Odoo components, services, hooks, and registries.
- Do not create a new OWL component if an existing component can be extended or patched.
- Do not introduce JavaScript when the requirement can be solved cleanly with XML/Python.
- Keep JavaScript changes as small as possible.
- Do not refactor unrelated JavaScript.

## OWL 2 components

Odoo 19 uses **OWL 2**. Always use OWL 2 lifecycle and APIs:

```javascript
import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";

class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static props = { record: Object };

    setup() {
        this.state = useState({ loading: false });
        onMounted(() => { /* ... */ });
        onWillUnmount(() => { /* cleanup */ });
    }
}
```

**Do NOT use OWL 1 patterns:**
- ~~`willStart()`~~ → use `onWillStart()`
- ~~`mounted()`~~ → use `onMounted()`
- ~~`willUnmount()`~~ → use `onWillUnmount()`
- ~~`patched()`~~ → use `onPatched()`

## Services

Before creating a service, search for an existing one:

- `orm` — model CRUD operations
- `rpc` — raw RPC calls
- `notification` — toast messages
- `dialog` — modal dialogs
- `action` — execute actions
- `user` — current user info
- `company` — multi-company info
- `router` — URL / hash navigation

Do not use low-level `fetch` or raw XHR when an Odoo service handles the operation.

## OWL hooks

Prefer existing OWL/Odoo hooks:

- `useService(name)` — inject a service
- `useEnv()` — access OWL env
- `useModel(resModel, fields)` — in list/form views

Create a custom hook only when:
- Behavior is reused across multiple components.
- The abstraction materially reduces duplication.
- The hook has a single clear responsibility.

## Registries

When integrating with the Odoo web client:

- Search existing registry usage first.
- Use the appropriate registry category (`fields`, `views`, `actions`, `services`, etc.).
- Follow the registration pattern already used in the project.

```javascript
import { registry } from "@web/core/registry";
registry.category("fields").add("my_field_widget", MyFieldWidget);
```

## Patching

Before using `patch()`:

1. Search for an existing extension mechanism (registry, inheritance).
2. Use `patch()` only when it is the correct Odoo extension mechanism.

```javascript
import { patch } from "@web/core/utils/patch";
import { SomeComponent } from "@web/...";

patch(SomeComponent.prototype, {
    // only the minimal override
});
```

- Patch the smallest possible surface.
- Avoid multiple patches for the same target when one is sufficient.
- Never modify Odoo core files directly.

## Templates (QWeb / XML)

- Prefer XML templates over generating HTML strings in JavaScript.
- Use `t-inherit` / `t-inherit-mode` for template inheritance.
- Do not copy complete templates to change a small section.
- JavaScript handles behavior; XML handles presentation.

## Events

Prefer OWL's standard event mechanisms (`t-on-click`, `t-on-change`, etc.).

Avoid:
- Manually attaching DOM listeners when OWL is sufficient.
- Global `document` or `window` listeners.
- jQuery event handling.

If a native DOM listener is necessary, clean it up in `onWillUnmount`.

## DOM manipulation

Prefer declarative OWL rendering.

Avoid:
- `document.querySelector()`, `document.getElementById()`
- `innerHTML`, manual element creation

Unless the Odoo architecture or browser API specifically requires it.

## RPC / ORM

```javascript
// Preferred: use orm service
const result = await this.orm.read("res.partner", [id], ["name", "email"]);
const ids = await this.orm.search("res.partner", [["active", "=", true]]);
await this.orm.write("res.partner", [id], { name: "New" });
```

Do not duplicate server-side business logic in JavaScript.
Business rules must be enforced on the server.

## Security

Never rely on JavaScript for security.

- A hidden button, disabled field, or frontend condition is not access control.
- Server-side permissions, access rights, and record rules enforce security.

## Assets

Before modifying assets:

1. Inspect the module `__manifest__.py` `assets` key.
2. Identify the relevant asset bundle (`web.assets_backend`, `web.assets_frontend`, etc.).
3. Search how similar assets are declared in the project.
4. Modify only the required bundle entry.

Do not add JavaScript to multiple bundles unless required.
Do not create duplicate asset declarations.

## Performance

Avoid:
- Unnecessary renders or state updates.
- Repeated RPC calls — batch them.
- RPC calls inside loops.
- Repeated DOM queries.
- Large client-side datasets when server-side filtering is possible.

Prefer:
- `onWillStart` for async data loading before first render.
- Server-side filtering and pagination.
- Existing Odoo services.
- Minimal reactive state.

## Error handling

Do not silently swallow errors:

```javascript
// BAD
try {
    await this.orm.write(...);
} catch {
    // empty
}

// GOOD
try {
    await this.orm.write(...);
} catch (error) {
    this.notification.add(error.message, { type: "danger" });
    throw error; // or handle meaningfully
}
```