---
stage: test_stage_2
requires: test-stage-1.json
outputs: test_state_2
---

# Test Stage 2: State Loading and Update

## Purpose

Test if AI can load state from previous stage, modify it, and save updated state.

## Previous State

Load state from: `.analysis/.state/test-stage-1.json`

## Task

1. Load state from Stage 1
2. Verify state contains expected data
3. Modify state (increment counter, update stage)
4. Save updated state
5. Output completion marker

## Steps

### Step 1: Load Previous State

Use the Bash tool to load state:

```bash
cd /home/user/spec-kit-smart
./scripts/bash/chain-state.sh load test-stage-1
```

### Step 2: Verify State

The loaded state should contain:

- `chain_id`: "test1234"
- `test_data`: "Hello from Stage 1"
- `counter`: 1

Output: "✓ State loaded successfully"

### Step 3: Create Updated State

Generate updated JSON by:

- Adding "test_stage_2" to `stages_complete` array
- Changing `stage` to "test_stage_2"
- Incrementing `counter` to 2
- Adding new field `test_data_2`: "Hello from Stage 2"
- Updating `timestamp`

Result:

```json
{
  "chain_id": "test1234",
  "stage": "test_stage_2",
  "timestamp": "2025-11-14T12:05:00Z",
  "stages_complete": ["test_stage_1", "test_stage_2"],
  "test_data": "Hello from Stage 1",
  "test_data_2": "Hello from Stage 2",
  "counter": 2
}
```

### Step 4: Save Updated State

Use the Bash tool to save:

```bash
cd /home/user/spec-kit-smart
./scripts/bash/chain-state.sh save test-stage-2 '{
  "chain_id": "test1234",
  "stage": "test_stage_2",
  "timestamp": "2025-11-14T12:05:00Z",
  "stages_complete": ["test_stage_1", "test_stage_2"],
  "test_data": "Hello from Stage 1",
  "test_data_2": "Hello from Stage 2",
  "counter": 2
}'
```

### Step 5: Verify State Persistence

Load both states to verify:

```bash
cd /home/user/spec-kit-smart
echo "=== Stage 1 State ==="
./scripts/bash/chain-state.sh load test-stage-1
echo ""
echo "=== Stage 2 State ==="
./scripts/bash/chain-state.sh load test-stage-2
```

### Step 6: Output Completion Marker

Output:

```
STAGE_COMPLETE:TEST_STAGE_2
STATE_PATH: .analysis/.state/test-stage-2.json
CHAIN_TEST_SUCCESS: Both stages completed successfully
```

## Success Criteria

- Stage 1 state loaded successfully
- State modifications applied correctly
- Updated state saved to .analysis/.state/test-stage-2.json
- Both state files can be loaded independently
- Counter incremented from 1 to 2
- Completion marker output
