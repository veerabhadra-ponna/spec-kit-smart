---
stage: test_stage_1
requires: nothing
outputs: test_state_1
---

# Test Stage 1: Basic State Creation

## Purpose

Test if AI can create and save state in first stage.

## Task

1. Generate a chain ID (any 8-character hex string)
2. Create initial state JSON
3. Save state using chain-state.sh
4. Output completion marker

## Steps

### Step 1: Generate Chain ID

Create a simple chain ID (for testing, use: `test1234`)

### Step 2: Create Initial State

Generate this JSON:

```json
{
  "chain_id": "test1234",
  "stage": "test_stage_1",
  "timestamp": "2025-11-14T12:00:00Z",
  "stages_complete": ["test_stage_1"],
  "test_data": "Hello from Stage 1",
  "counter": 1
}
```text

### Step 3: Save State

Use the Bash tool to save state:

```bash
cd /home/user/spec-kit-smart
./scripts/bash/chain-state.sh save test-stage-1 '{
  "chain_id": "test1234",
  "stage": "test_stage_1",
  "timestamp": "2025-11-14T12:00:00Z",
  "stages_complete": ["test_stage_1"],
  "test_data": "Hello from Stage 1",
  "counter": 1
}'
```text

### Step 4: Verify State Saved

Load the state back to verify:

```bash
cd /home/user/spec-kit-smart
./scripts/bash/chain-state.sh load test-stage-1
```text

### Step 5: Output Completion Marker

Output:

```text
STAGE_COMPLETE:TEST_STAGE_1
STATE_PATH: .analysis/.state/test-stage-1.json
```text

## Success Criteria

- State JSON created with all required fields
- State saved successfully to .analysis/.state/test-stage-1.json
- State can be loaded back
- Completion marker output
