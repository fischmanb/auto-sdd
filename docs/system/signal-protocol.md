# Signal Protocol

> How build agents communicate results to the orchestration loop.
> Signals are grep-parseable flat strings — no JSON, no eval on agent output.

---

## Design rationale

Agents communicate via flat strings that the build loop extracts with `grep`. This is an architectural choice (L-00028): grep is reliable, available everywhere, and fails visibly. JSON parsing introduces fragility — malformed output from an agent silently breaks downstream logic instead of failing at the grep step.

---

## Build agent signals

Each signal must appear on its own line in the agent's output.

| Signal | Meaning | Required? |
|--------|---------|-----------|
| `FEATURE_BUILT: {name}` | Feature implemented successfully | Yes (on success) |
| `SPEC_FILE: {path}` | Path to the .feature.md file | Yes (with FEATURE_BUILT) |
| `SOURCE_FILES: {paths}` | Comma-separated paths to created/modified source files | Yes (with FEATURE_BUILT) |
| `BUILD_FAILED: {reason}` | Build attempt failed | Yes (on failure) |
| `NO_FEATURES_READY` | No pending features found in roadmap | Emitted by agent |

## Drift agent signals

| Signal | Meaning |
|--------|---------|
| `NO_DRIFT` | Spec and implementation are aligned |
| `DRIFT_FIXED` | Drift detected and reconciled |
| `DRIFT_UNRESOLVABLE` | Drift detected, could not fix |

## Review agent signals

| Signal | Meaning |
|--------|---------|
| `REVIEW_CLEAN` | Code review found no issues |
| `REVIEW_FIXED` | Issues found and fixed |
| `REVIEW_FAILED` | Issues found, could not fix |

---

## Parsing rules

The build loop uses `_parse_signal(signal_name, output)` to extract the value after the colon:

```python
# Example: extracts "Rent Potential" from "FEATURE_BUILT: Rent Potential"
feature_name = _parse_signal("FEATURE_BUILT", build_result)
```

**Signal fallback detection**: If the agent doesn't emit `FEATURE_BUILT` but the build loop detects `NO_DRIFT` or `DRIFT_FIXED` plus HEAD advanced + clean tree + build passes + tests pass, it infers success. This handles agents that do the work but forget the signal.

---

## Prompt placement

Signals must be the agent's final output. The build prompt places signal instructions in two locations:
1. After the implementation instructions (first mention)
2. Inside a `═══` bordered CRITICAL block as the absolute last content in the prompt

This dual placement was hardened in Round 31.1 after agents consistently buried signals mid-output where grep couldn't reliably extract them.
