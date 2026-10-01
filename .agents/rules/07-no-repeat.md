---
trigger: always_on
---

# Efficiency Rules

Do not repeat work.

Before executing a command:

- Check whether its result is already available.
- Reuse previous command results when still valid.

Before reading a file:

- Check whether it was already read in the current task.

Before searching:

- Search the repository first.
- Do not search the internet unless repository information is insufficient.

Before changing code:

- Identify the exact files involved.

After changing code:

- Do not reread the entire file unless necessary.
- Inspect the relevant diff instead.

Do not:

- run the same test twice without a reason
- repeatedly inspect the same file
- repeatedly explain the same requirement
- regenerate unchanged code
- search for information already established
- perform broad repository scans for narrow tasks

Prefer:

search → targeted read → edit → focused test → diff