# Local LLM Pipeline (Archived)

This directory contains a self-contained local LLM pipeline that
predates the current Claude-CLI-based build system.

## Contents

- `lib/common.sh` — shared utilities: check_model_health, call_model,
  extract_content, parse_files_from_output, validate_json,
  has_pending_features, update_spec_status
- `lib/models.sh` — model health checks: check_all_models
- `stages/` — build pipeline stages: 01-plan.sh through 04-fix.sh
- `framework/ai-dev` — AI development framework
- `demo.sh` — demonstration script

## Status

Archived — not connected to the active build system
(`scripts/build-loop-local.sh`, `scripts/overnight-autonomous.sh`).
Preserved for reference when implementing local model support in the
active pipeline. The utilities in `lib/common.sh` may be reusable
for LM Studio integration.
