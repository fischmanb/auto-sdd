---
description: Create a feature spec with Gherkin scenarios and ASCII mockups (TDD step 1)
---

Create the feature specification for: $ARGUMENTS

## Instructions

1. **Check/Create Design System**
   - If no `.specs/design-system/tokens.md` exists, create default tokens
   - Inform user of created files

2. **Create Feature Spec with YAML Frontmatter**
   - Create `.specs/features/{domain}/{feature}.feature.md`
   - Include YAML frontmatter:
     ```yaml
     ---
     feature: Feature Name
     domain: domain-name
     source: path/to/feature.tsx
     tests: []
     components: []
     design_refs: []
     status: stub
     created: YYYY-MM-DD
     updated: YYYY-MM-DD
     ---
     ```
   - Write Gherkin scenarios: happy path, edge cases, error states, loading states
   - Include empty `## Learnings` section at the end

3. **Create ASCII Mockup**
   - Add `## UI Mockup` section with ASCII art
   - Show component layout, interactive elements, states
   - Reference design tokens

4. **Create Component Stubs**
   - If mockup references components not in `.specs/design-system/components/`, create stubs

5. **STOP for Approval**
   - Do NOT write implementation code
   - Do NOT write tests yet
   - Ask: "Does this look right? Ready to write tests?"

## After Approval

When user approves:
1. Write failing tests covering all scenarios
2. Update frontmatter: `status: tested`, add test files to `tests: []`
3. Ask: "Tests written (failing). Ready to implement?"

When implementation approved:
1. Implement until tests pass using design tokens
2. Update frontmatter: `status: implemented`, add components to `components: []`
3. Optionally run `/compound` to extract learnings
