# Commands Reference

> Index of all `.claude/commands/` slash commands available to Claude Code agents.
> Invoke in Claude Code with `/command-name` or by saying the command name in chat.

---

## Session management

| Command | Purpose |
|---------|---------|
| `/checkpoint` | Update all context management files. Run before ending a session, before risky operations, or on demand. Executes the 8-step protocol. |
| `/wrap` | End-of-session protocol. Runs learnings extraction, full checkpoint, and handoff file creation in sequence. |
| `/extract-learnings` | Scan current session for uncaptured learnings, output in graph schema format. |
| `/review-signals` | Scan HOW-I-WORK methodology signals for patterns that should graduate to learnings. |

## Build workflow

| Command | Purpose |
|---------|---------|
| `/build-next` | Pick the next pending feature from the roadmap and build it through the full TDD cycle. |
| `/start-feature` | Sync with main branch and create a new feature branch. |
| `/fix-bug` | Fix a bug with proper regression testing. |
| `/prototype` | Rapid prototyping — skip specs and tests. |
| `/formalize` | Convert prototype to production code with specs and tests. |
| `/refactor` | Refactor code while ensuring tests still pass. |
| `/code-review` | Review code against senior engineering standards. |

## Spec-driven development

| Command | Purpose |
|---------|---------|
| `/vision` | Create or update the project's vision document (`.specs/vision.md`). |
| `/roadmap` | Create, update, or restructure the project's build roadmap (`.specs/roadmap.md`). |
| `/spec-first` | Create a feature spec with Gherkin scenarios and ASCII mockups (TDD step 1). |
| `/spec-init` | Bootstrap spec-driven workflow on an existing codebase (autonomous). |
| `/catch-drift` | Detect when specs and code have diverged, then reconcile. |
| `/check-coverage` | Compare specs against tests to find gaps. |
| `/clone-app` | Analyze an existing web app and create a build plan (vision + roadmap). |

## Documentation & design

| Command | Purpose |
|---------|---------|
| `/document-code` | Generate specs and tests from existing code (reverse TDD). |
| `/design-component` | Document a component pattern in the design system. |
| `/design-tokens` | Create or update design tokens. |
| `/update-test-docs` | Sync test documentation with actual tests. |

## Verification

| Command | Purpose |
|---------|---------|
| `/verify-test-counts` | Run tests and reconcile counts vs documentation. |
| `/verify-learnings-counts` | Count learnings entries and reconcile vs documentation claims. |
| `/verify-propagation` | Mechanical propagation check after writing learnings or protocol changes. |
| `/agent-prompt-checklist` | Validate that an agent prompt includes all required sections. |

## Project-specific (SitDeck)

| Command | Purpose |
|---------|---------|
| `/sitdeck-roadmap` | Create or update the SitDeck product roadmap. |
| `/sitdeck-scaffold-stubs` | Generate all SitDeck feature stub files from the roadmap. |

## Migration & infrastructure

| Command | Purpose |
|---------|---------|
| `/sdd-migrate` | Migrate from SDD 1.0 to SDD 2.0 (preserves custom commands). |
| `/compound` | Extract and persist learnings (legacy — prefer `/extract-learnings`). |
| `/roadmap-triage` | Scan Slack and Jira for feature requests and add to roadmap. |
