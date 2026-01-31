---
description: Create or update design tokens
---

Manage design tokens: $ARGUMENTS

## Actions

### `init` - Create default tokens
Create `.specs/design-system/tokens.md` with sensible defaults (colors, typography, spacing, radii, shadows).

### `update {token} to {value}` - Update specific token
Update token value and list changes.

### `import from {file}` - Import from existing config
Extract tokens from:
- `tailwind.config.js` - Custom theme values
- CSS variables file - Convert to documented tokens

### `add category {name}` - Add new token category
Add new category with specified tokens.

## Output

After changes, show:
- Changes made (old → new values)
- Files updated
- Token summary (count by category)

## Token Naming

Follow patterns:
- `color-{name}` / `color-{name}-{variant}`
- `text-{size}` / `font-{weight}`
- `spacing-{scale}` / `radius-{size}`
- `shadow-{size}` / `z-{layer}`
