#!/bin/bash
# overnight-autonomous.sh
# Autonomous overnight feature implementation
# Scans Slack/Jira → creates specs → implements → opens draft PRs
#
# CONFIGURATION (set these in .env.local or export before running):
#   SLACK_CHANNEL      - Slack channel to scan (e.g., "feature-requests")
#   JIRA_PROJECT       - Jira project key (e.g., "PROJ")
#   JIRA_AUTO_LABEL    - Jira label marking items as auto-ok (default: "auto-ok")
#   MAX_FEATURES       - Max features to implement per night (default: 4)
#   PROJECT_DIR        - Project directory (default: current directory)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
success() { echo -e "${GREEN}[$(date '+%H:%M:%S')] ✓${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] ⚠${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] ✗${NC} $1"; }

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(dirname "$SCRIPT_DIR")}"

if [ -f "$PROJECT_DIR/.env.local" ]; then
    source "$PROJECT_DIR/.env.local"
fi

# Defaults
SLACK_CHANNEL="${SLACK_CHANNEL:-feature-requests}"
JIRA_PROJECT="${JIRA_PROJECT:-}"
JIRA_AUTO_LABEL="${JIRA_AUTO_LABEL:-auto-ok}"
MAX_FEATURES="${MAX_FEATURES:-4}"

log "Starting overnight autonomous run"
log "Project: $PROJECT_DIR"
log "Slack channel: #$SLACK_CHANNEL"
log "Jira project: ${JIRA_PROJECT:-not configured}"
log "Max features: $MAX_FEATURES"

cd "$PROJECT_DIR"

# ─────────────────────────────────────────────
# STEP 0: Ensure we're on main and up to date
# ─────────────────────────────────────────────

log "Syncing with main branch..."
git checkout main 2>/dev/null || git checkout master 2>/dev/null
git pull origin "$(git branch --show-current)"
success "Synced with remote"

# ─────────────────────────────────────────────
# STEP 1: Rebase any existing auto PRs
# ─────────────────────────────────────────────

if command -v gh &> /dev/null; then
    log "Checking for existing auto PRs to rebase..."
    
    for pr_branch in $(gh pr list --search "head:auto/" --json headRefName --jq '.[].headRefName' 2>/dev/null); do
        log "Rebasing $pr_branch..."
        git fetch origin "$pr_branch" 2>/dev/null || continue
        git checkout "$pr_branch" 2>/dev/null || continue
        
        if git rebase origin/main 2>/dev/null; then
            git push --force-with-lease origin "$pr_branch" 2>/dev/null && success "Rebased $pr_branch"
        else
            git rebase --abort 2>/dev/null
            warn "Could not rebase $pr_branch - may need manual intervention"
        fi
    done
    
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
fi

# ─────────────────────────────────────────────
# STEP 2: Scan for feature candidates
# ─────────────────────────────────────────────

log "Scanning for feature candidates..."

CANDIDATES_FILE=$(mktemp)
echo "[]" > "$CANDIDATES_FILE"

# Check if Cursor CLI (agent) is available
if ! command -v agent &> /dev/null; then
    error "Cursor CLI (agent) not found. Install from: https://cursor.com/cli"
    error "Run: curl https://cursor.com/install -fsS | bash"
    exit 1
fi

# Use Cursor agent to scan sources
agent -p --force --output-format text "
You have access to Slack and Jira MCPs.

TASK: Find feature candidates for overnight implementation.

1. SLACK (if configured):
   - Search channel #$SLACK_CHANNEL for feature requests from last 7 days
   - Look for messages that describe features, improvements, or bug fixes
   - Exclude messages that already have a ✅ reaction (already handled)
   - Extract: message ID, summary of the request

2. JIRA (if configured, project: $JIRA_PROJECT):
   - Search for issues with label '$JIRA_AUTO_LABEL' in 'To Do' status
   - Extract: issue key, summary

3. OUTPUT:
   Save to $CANDIDATES_FILE as JSON array:
   [
     {\"source\": \"slack\", \"id\": \"message-id\", \"summary\": \"Feature description\"},
     {\"source\": \"jira\", \"id\": \"PROJ-123\", \"summary\": \"Issue summary\"}
   ]

   Maximum $MAX_FEATURES candidates.
   If no candidates found, save empty array [].

4. Do NOT implement anything yet - just gather candidates.
"

# Read candidates
CANDIDATE_COUNT=$(jq length "$CANDIDATES_FILE" 2>/dev/null || echo "0")
log "Found $CANDIDATE_COUNT candidates"

if [ "$CANDIDATE_COUNT" -eq 0 ]; then
    success "No candidates to implement. Exiting."
    rm "$CANDIDATES_FILE"
    exit 0
fi

# ─────────────────────────────────────────────
# STEP 3: Implement each candidate
# ─────────────────────────────────────────────

CREATED_PRS=0

for i in $(seq 0 $((CANDIDATE_COUNT - 1))); do
    candidate=$(jq -r ".[$i]" "$CANDIDATES_FILE")
    source=$(echo "$candidate" | jq -r '.source')
    id=$(echo "$candidate" | jq -r '.id')
    summary=$(echo "$candidate" | jq -r '.summary')
    
    log "Processing [$((i+1))/$CANDIDATE_COUNT]: $summary"
    
    # Create branch name (sanitize for git)
    BRANCH_NAME="auto/${id}-$(date +%Y%m%d)"
    BRANCH_NAME=$(echo "$BRANCH_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9\-]/-/g' | sed 's/--*/-/g')
    
    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME" 2>/dev/null; then
        warn "Branch $BRANCH_NAME already exists, skipping"
        continue
    fi
    
    # Create feature branch
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
    git checkout -b "$BRANCH_NAME"
    
    # Run agent to implement
    log "Creating spec and implementing..."
    
    agent -p --force --output-format text "
    FEATURE REQUEST:
    Source: $source ($id)
    Summary: $summary
    
    INSTRUCTIONS:
    1. Create feature spec at .specs/features/auto/${id}.feature.md
       - Include YAML frontmatter (feature, domain, source, tests, components, status: stub)
       - Write Gherkin scenarios covering happy path, edge cases, errors
       - Include ASCII UI mockup if user-facing
       - Include empty ## Learnings section
    
    2. Update frontmatter to status: specced
    
    3. Write failing tests based on scenarios
       - Update frontmatter: status: tested, add test files to tests: []
    
    4. Implement until tests pass
       - Update frontmatter: status: implemented, add components to components: []
       - Use design tokens from .specs/design-system/tokens.md
    
    5. Commit all changes with message:
       'feat(auto): $summary'
    
    IMPORTANT:
    - Do NOT edit .specs/mapping.md directly (it auto-regenerates)
    - Follow existing code patterns in this codebase
    - If you get stuck or tests won't pass after 3 attempts, commit what you have and note the issue
    "
    
    # Check if there are changes to commit
    if [ -n "$(git status --porcelain)" ]; then
        git add -A
        git commit -m "feat(auto): $summary" 2>/dev/null || true
    fi
    
    # Push branch
    if git push -u origin "$BRANCH_NAME" 2>/dev/null; then
        success "Pushed branch $BRANCH_NAME"
        
        # Create draft PR
        if command -v gh &> /dev/null; then
            SPEC_FILE=".specs/features/auto/${id}.feature.md"
            SPEC_CONTENT=""
            if [ -f "$SPEC_FILE" ]; then
                SPEC_CONTENT=$(cat "$SPEC_FILE")
            fi
            
            PR_URL=$(gh pr create --draft \
                --title "Auto: $summary" \
                --body "$(cat <<EOF
## Source
**$source**: \`$id\`

## Generated Spec

<details>
<summary>Click to expand spec</summary>

\`\`\`markdown
$SPEC_CONTENT
\`\`\`

</details>

## Review Checklist

- [ ] Spec makes sense for the request
- [ ] Implementation matches spec
- [ ] Tests are adequate
- [ ] No security issues
- [ ] Code follows project patterns

---

_Generated automatically by overnight-autonomous.sh_
EOF
)" 2>/dev/null)
            
            if [ -n "$PR_URL" ]; then
                success "Created PR: $PR_URL"
                CREATED_PRS=$((CREATED_PRS + 1))
                
                # Mark source as handled
                agent -p --force --output-format text "
                Mark this item as handled:
                - Source: $source
                - ID: $id
                
                If Slack: Add ✅ reaction to the message
                If Jira: Transition issue to 'In Review' or add comment 'PR created: $PR_URL'
                "
            fi
        else
            warn "gh CLI not available - PR not created"
        fi
    else
        error "Failed to push branch $BRANCH_NAME"
    fi
    
    # Return to main for next iteration
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
done

# ─────────────────────────────────────────────
# STEP 4: Summary
# ─────────────────────────────────────────────

rm "$CANDIDATES_FILE"

echo ""
echo "═══════════════════════════════════════════════════════════"
success "Overnight run complete!"
echo "  Candidates found: $CANDIDATE_COUNT"
echo "  PRs created: $CREATED_PRS"
echo "═══════════════════════════════════════════════════════════"

# Optionally notify via Slack
if [ "$CREATED_PRS" -gt 0 ] && [ -n "$SLACK_NOTIFY_CHANNEL" ]; then
    agent -p --force --output-format text "
    Post to Slack channel #$SLACK_NOTIFY_CHANNEL:
    '🤖 Overnight run complete! Created $CREATED_PRS draft PRs. Check GitHub for review.'
    "
fi
