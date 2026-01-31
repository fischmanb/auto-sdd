# Design Tokens

**Status**: 📋 Template (customize for your project)
**Last Updated**: [date]

This file defines the design tokens for your project. These tokens are referenced in feature specs and used during implementation to ensure visual consistency.

---

## Colors

### Brand Colors

| Token | Value | Usage |
|-------|-------|-------|
| `color-primary` | `#3B82F6` | Primary actions, links, focus states |
| `color-primary-hover` | `#2563EB` | Primary hover state |
| `color-primary-light` | `#DBEAFE` | Primary backgrounds, highlights |
| `color-secondary` | `#8B5CF6` | Secondary actions, accents |
| `color-secondary-hover` | `#7C3AED` | Secondary hover state |

### Neutral Colors

| Token | Value | Usage |
|-------|-------|-------|
| `color-background` | `#FFFFFF` | Page background |
| `color-surface` | `#F9FAFB` | Card/panel backgrounds |
| `color-surface-elevated` | `#FFFFFF` | Elevated surfaces (modals, dropdowns) |
| `color-border` | `#E5E7EB` | Default borders |
| `color-border-strong` | `#D1D5DB` | Emphasized borders |

### Text Colors

| Token | Value | Usage |
|-------|-------|-------|
| `color-text` | `#111827` | Primary text |
| `color-text-secondary` | `#6B7280` | Secondary/muted text |
| `color-text-tertiary` | `#9CA3AF` | Placeholder, disabled text |
| `color-text-inverse` | `#FFFFFF` | Text on dark backgrounds |

### Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| `color-success` | `#10B981` | Success states, positive feedback |
| `color-success-light` | `#D1FAE5` | Success backgrounds |
| `color-warning` | `#F59E0B` | Warning states, caution |
| `color-warning-light` | `#FEF3C7` | Warning backgrounds |
| `color-error` | `#EF4444` | Error states, destructive actions |
| `color-error-light` | `#FEE2E2` | Error backgrounds |
| `color-info` | `#3B82F6` | Informational states |
| `color-info-light` | `#DBEAFE` | Info backgrounds |

---

## Typography

### Font Families

| Token | Value | Usage |
|-------|-------|-------|
| `font-sans` | `'Inter', system-ui, sans-serif` | Body text, UI |
| `font-mono` | `'JetBrains Mono', monospace` | Code, technical content |
| `font-display` | `'Inter', system-ui, sans-serif` | Headings (customize) |

### Font Sizes

| Token | Value | Line Height | Usage |
|-------|-------|-------------|-------|
| `text-xs` | `0.75rem` (12px) | 1rem | Badges, captions |
| `text-sm` | `0.875rem` (14px) | 1.25rem | Secondary text, labels |
| `text-base` | `1rem` (16px) | 1.5rem | Body text |
| `text-lg` | `1.125rem` (18px) | 1.75rem | Large body, subtitles |
| `text-xl` | `1.25rem` (20px) | 1.75rem | H4, card titles |
| `text-2xl` | `1.5rem` (24px) | 2rem | H3 |
| `text-3xl` | `1.875rem` (30px) | 2.25rem | H2 |
| `text-4xl` | `2.25rem` (36px) | 2.5rem | H1 |
| `text-5xl` | `3rem` (48px) | 1 | Display, hero |

### Font Weights

| Token | Value | Usage |
|-------|-------|-------|
| `font-normal` | `400` | Body text |
| `font-medium` | `500` | Emphasis, labels |
| `font-semibold` | `600` | Subheadings, buttons |
| `font-bold` | `700` | Headings, strong emphasis |

---

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `spacing-0` | `0` | No spacing |
| `spacing-1` | `0.25rem` (4px) | Tight spacing |
| `spacing-2` | `0.5rem` (8px) | Small gaps |
| `spacing-3` | `0.75rem` (12px) | Compact padding |
| `spacing-4` | `1rem` (16px) | Default padding |
| `spacing-5` | `1.25rem` (20px) | Medium padding |
| `spacing-6` | `1.5rem` (24px) | Large padding |
| `spacing-8` | `2rem` (32px) | Section spacing |
| `spacing-10` | `2.5rem` (40px) | Large section spacing |
| `spacing-12` | `3rem` (48px) | Page section gaps |
| `spacing-16` | `4rem` (64px) | Major section gaps |

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `radius-none` | `0` | Sharp corners |
| `radius-sm` | `0.125rem` (2px) | Subtle rounding |
| `radius-md` | `0.375rem` (6px) | Default rounding |
| `radius-lg` | `0.5rem` (8px) | Cards, containers |
| `radius-xl` | `0.75rem` (12px) | Large cards, modals |
| `radius-2xl` | `1rem` (16px) | Feature cards |
| `radius-full` | `9999px` | Pills, avatars |

---

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| `shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, dropdowns |
| `shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |
| `shadow-xl` | `0 20px 25px rgba(0,0,0,0.1)` | Floating elements |

---

## Breakpoints

| Token | Value | Usage |
|-------|-------|-------|
| `screen-sm` | `640px` | Small tablets |
| `screen-md` | `768px` | Tablets |
| `screen-lg` | `1024px` | Laptops |
| `screen-xl` | `1280px` | Desktops |
| `screen-2xl` | `1536px` | Large desktops |

---

## Animation

| Token | Value | Usage |
|-------|-------|-------|
| `duration-fast` | `150ms` | Micro-interactions |
| `duration-normal` | `200ms` | Default transitions |
| `duration-slow` | `300ms` | Larger transitions |
| `easing-default` | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard easing |
| `easing-in` | `cubic-bezier(0.4, 0, 1, 1)` | Accelerate |
| `easing-out` | `cubic-bezier(0, 0, 0.2, 1)` | Decelerate |

---

## Z-Index Scale

| Token | Value | Usage |
|-------|-------|-------|
| `z-base` | `0` | Default layer |
| `z-dropdown` | `10` | Dropdowns, tooltips |
| `z-sticky` | `20` | Sticky headers |
| `z-modal` | `30` | Modals, dialogs |
| `z-toast` | `40` | Toast notifications |
| `z-max` | `50` | Maximum (debugging) |

---

## How to Use

### In ASCII Mockups (Feature Specs)

Reference tokens by name to indicate design intent:

```
┌─ Card (bg: surface, radius: lg, shadow: md) ────────────────┐
│                                                             │
│  Title (text: xl, weight: semibold, color: text)           │
│                                                             │
│  Description text (text: base, color: text-secondary)      │
│                                                             │
│  ┌─────────────────────────┐                                │
│  │  Button (primary)       │                                │
│  └─────────────────────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### In Implementation

**Tailwind CSS:**
```jsx
<div className="bg-surface rounded-lg shadow-md p-6">
  <h2 className="text-xl font-semibold text-gray-900">Title</h2>
  <p className="text-base text-gray-600">Description</p>
  <button className="bg-primary hover:bg-primary-hover text-white">
    Button
  </button>
</div>
```

**CSS Variables:**
```css
:root {
  --color-primary: #3B82F6;
  --spacing-4: 1rem;
  --radius-lg: 0.5rem;
}

.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
}
```

---

## Customization

This is a **starting template**. Customize these values to match your brand:

1. Update color palette to your brand colors
2. Change font families if using custom fonts
3. Adjust spacing scale if needed
4. Add project-specific tokens as needed

Keep this file updated as your design system evolves.
