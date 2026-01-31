# /compound - Extract Session Learnings

Extract and persist learnings from the current coding session.

## Instructions

1. **Reflect** on what was accomplished this session
2. **Identify** patterns, gotchas, decisions, and bug fixes
3. **Categorize** each learning:
   - Feature-specific → add to that spec's `## Learnings` section
   - Cross-cutting → add to `.specs/learnings.md`
   - Critical rules → add to `CLAUDE.md` `## Learned Patterns` section
4. **Update** the `updated:` date in any modified spec frontmatter
5. **Commit** changes with message `compound: learnings from [brief description]`
6. **Summarize** what was captured and where

## Learning Format

```markdown
### YYYY-MM-DD
- **Pattern**: [What worked well]
- **Gotcha**: [Edge case or pitfall]
- **Decision**: [Choice made and rationale]
```

## When to Promote to CLAUDE.md

Only promote learnings that:
- Are security-related
- Prevent common/costly mistakes
- Apply to ALL future work in this codebase
- Are architectural decisions

Most learnings should stay in feature specs or learnings.md.
