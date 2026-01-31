---
description: Migrate from SDD 1.0 to SDD 2.0 (preserves custom commands)
---

Upgrade this project from SDD 1.0 to SDD 2.0.

**Important**: Do NOT use `git auto` on existing SDD projects - it overwrites files. Use this command instead.

## Stock SDD Commands (safe to update)

```
catch-drift, check-coverage, code-review, design-component,
design-tokens, document-code, fix-bug, formalize, prototype,
refactor, spec-first, spec-init, start-feature, update-test-docs,
verify-test-counts
```

Any other commands are considered CUSTOM and will be preserved.

## Migration Steps

1. **Inventory commands**: Identify stock vs custom
2. **Create learnings folder**: `.specs/learnings/` with 7 category files
3. **Add frontmatter to specs**: Only if missing, don't change content
4. **Update stock commands**: Replace with 2.0 versions
5. **Preserve custom commands**: Don't touch them
6. **Add new commands**: compound.md, sdd-migrate.md
7. **Update stock rules**: Add compound.mdc
8. **Add hooks**: If not already present
9. **Add scripts**: Automation scripts
10. **Backup & regenerate mapping.md**
11. **Update CLAUDE.md**: Ask if customized
12. **Create version file**: .specs/.sdd-version = 2.0

## Frontmatter Format

Add to specs that don't have it:

```yaml
---
feature: {from # header}
domain: {from path}
source: {from Source File line}
tests: []
components: []
status: implemented
created: {today}
updated: {today}
---
```

Do NOT add ASCII mockups to existing specs - they work without them.

## Custom Command Detection

If a command exists that's not in the stock list, it's custom → preserve it.

If a stock command has been modified (differs from stock 1.0), ask before replacing.

## Output

Show inventory, migration plan, ask for confirmation, then execute preserving all custom work.
