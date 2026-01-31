# /sdd-migrate - Migrate from SDD 1.0 to 2.0

Upgrade an existing SDD 1.0 project to SDD 2.0 with compound learning and automation.

**Important**: This command is for projects that already have SDD installed. Do NOT use `git auto` on existing SDD projects - it would overwrite files.

## Detection

```
1. If .specs/.sdd-version exists → read version
2. If no version file but .specs/ exists → SDD 1.0
3. If no .specs/ → not an SDD project (suggest git auto)
```

## Stock SDD Commands

These are the "official" SDD commands that can be safely updated:

**SDD 1.0 Commands** (will be updated):
- catch-drift.md
- check-coverage.md
- code-review.md
- design-component.md
- design-tokens.md
- document-code.md
- fix-bug.md
- formalize.md
- prototype.md
- refactor.md
- spec-first.md
- spec-init.md
- start-feature.md
- update-test-docs.md
- verify-test-counts.md

**SDD 2.0 Adds** (new files):
- compound.md
- sdd-migrate.md

**Custom commands** (any other .md files) will be PRESERVED.

## Migration Steps (1.0 → 2.0)

### Step 1: Inventory Existing Commands

```
Scanning .cursor/commands/...

Stock SDD commands found (will update):
  ✓ spec-first.md
  ✓ spec-init.md
  ✓ catch-drift.md
  ... (list all found)

Custom commands found (will preserve):
  • my-deploy.md
  • team-standup.md
  ... (list any non-stock)

New commands to add:
  + compound.md
  + sdd-migrate.md
```

### Step 2: Create Learnings Folder

```bash
mkdir -p .specs/learnings
```

Create these files (only if they don't exist):
- `.specs/learnings/index.md`
- `.specs/learnings/testing.md`
- `.specs/learnings/performance.md`
- `.specs/learnings/security.md`
- `.specs/learnings/api.md`
- `.specs/learnings/design.md`
- `.specs/learnings/general.md`

### Step 3: Add YAML Frontmatter to Existing Specs

For each `.specs/features/**/*.feature.md` that does NOT already have frontmatter:

1. Read the file
2. Check if it starts with `---` (already has frontmatter) → skip
3. Extract feature name from `# Feature Name` header
4. Extract domain from file path
5. Look for `**Source File**:` line to get source
6. Prepend YAML frontmatter:

```yaml
---
feature: {extracted name}
domain: {from path}
source: {from Source File line or empty}
tests: []
components: []
design_refs: []
status: implemented
created: {today}
updated: {today}
---
```

**Do NOT**:
- Add ASCII mockups to existing specs (they work without them)
- Remove any existing content
- Change the spec format beyond adding frontmatter

### Step 4: Update Stock Commands Only

For each stock SDD command found in Step 1:
- Replace with SDD 2.0 version
- Show diff summary (lines added/removed)

For custom commands:
- Leave completely untouched
- Log that they were preserved

### Step 5: Update Stock Rules Only

**Stock SDD rules** (will update):
- design-tokens.mdc
- specs-workflow.mdc

**SDD 2.0 Adds**:
- compound.mdc

Custom rules (any other .mdc files) will be PRESERVED.

### Step 6: Add Hooks (if not exist)

Only create if they don't already exist:
- `.cursor/hooks.json`
- `.cursor/hooks/regenerate-mapping.sh`
- `.cursor/hooks/check-conflicts.sh`
- `.cursor/hooks/session-end.sh`

If hooks already exist, show warning and skip.

### Step 7: Add Automation Scripts

Create `scripts/` directory (if not exists) with:
- `generate-mapping.sh`
- `nightly-review.sh`
- `overnight-autonomous.sh`
- `setup-overnight.sh`
- `uninstall-overnight.sh`
- `launchd/` (plist files)

If any script already exists with same name, show diff and ask whether to overwrite.

### Step 8: Regenerate mapping.md

Backup old mapping.md:
```bash
cp .specs/mapping.md .specs/mapping.md.backup
```

Then regenerate:
```bash
./scripts/generate-mapping.sh
```

Tell user: "Old mapping backed up to mapping.md.backup"

### Step 9: Update CLAUDE.md

Compare existing CLAUDE.md with SDD 2.0 version:
- If identical to SDD 1.0 stock → replace
- If customized → show diff, ask whether to replace or merge

### Step 10: Create Version File

```bash
echo "2.0" > .specs/.sdd-version
```

---

## Output

```
═══════════════════════════════════════════════════════════════════
                    SDD MIGRATION: 1.0 → 2.0
═══════════════════════════════════════════════════════════════════

Detected: SDD 1.0 (no version file, .specs/ exists)

Command Inventory:
├── Stock commands to update: 15
├── Custom commands to preserve: 2
│   • my-deploy.md
│   • team-standup.md
└── New commands to add: 2

Feature Specs:
├── Total specs found: 8
├── Already have frontmatter: 2
└── Need frontmatter added: 6

Migration Plan:
├── Create .specs/learnings/ folder (7 files)
├── Add frontmatter to 6 feature specs
├── Update 15 stock commands
├── Preserve 2 custom commands
├── Add 2 new commands
├── Update 2 stock rules, add 1 new
├── Add hooks system
├── Add automation scripts
├── Backup and regenerate mapping.md
└── Create version file

Proceed? [y/n]
```

After confirmation:

```
═══════════════════════════════════════════════════════════════════
                    MIGRATION COMPLETE
═══════════════════════════════════════════════════════════════════

✓ Created .specs/learnings/ (7 files)
✓ Added frontmatter to 6 feature specs
✓ Updated 15 stock commands
✓ Preserved 2 custom commands (untouched)
✓ Added compound.md, sdd-migrate.md
✓ Updated 2 stock rules, added compound.mdc
✓ Added hooks system
✓ Added automation scripts
✓ Backed up mapping.md → mapping.md.backup
✓ Regenerated mapping.md
✓ Version: 2.0

Custom commands preserved:
  • .cursor/commands/my-deploy.md
  • .cursor/commands/team-standup.md

New capabilities:
• /compound - Extract learnings from sessions
• Overnight automation (run ./scripts/setup-overnight.sh)
• Auto-generated mapping (no more merge conflicts)
• Category-based learnings

Note: Existing feature specs were NOT modified beyond adding
frontmatter. They don't need ASCII mockups to work - new specs
created with /spec-first will have them.
```

---

## Edge Cases

### Custom command has same name as stock command

If user has customized a stock command (e.g., modified `spec-first.md`):
- Show diff between their version and stock 1.0 version
- If different from stock 1.0, ask: "spec-first.md appears customized. Update anyway? [y/n/diff]"

### CLAUDE.md is customized

- Show diff
- Offer options: [r]eplace, [m]erge (add new sections), [s]kip

### hooks.json already exists

- Show existing config
- Ask whether to merge or replace

---

## Rollback

If something goes wrong, user can restore from backup:

```bash
# Restore mapping
mv .specs/mapping.md.backup .specs/mapping.md

# Remove version file to re-run migration
rm .specs/.sdd-version
```
