# Chain Orchestration Test

## Purpose

Test if AI can self-orchestrate a 2-stage workflow with state management.

## Test Workflow

This test validates the core assumption of our chained prompt architecture: that an AI agent can read stage prompts from files, execute them sequentially, and manage state between stages.

## Prerequisites

1. State management scripts exist:
   - `scripts/bash/chain-state.sh`

2. State directory will be created:
   - `.analysis/.state/`

3. Test stage prompts exist:
   - `tests/chain-test-stage-1.md`
   - `tests/chain-test-stage-2.md`

## Test Execution

### Initialize Test Environment

First, ensure we're in the correct directory and initialize state management:

```bash
cd /home/user/spec-kit-smart
./scripts/bash/chain-state.sh init
```text

You should see: `✓ Initialized state directory: .analysis/.state`

---

### STAGE 1: Execute First Stage

**Your task**: Load and execute the first test stage.

1. Use the **Read** tool to load: `tests/chain-test-stage-1.md`

2. Read the ENTIRE file and follow ALL instructions in that file

3. Execute each step as documented

4. When complete, you should output: `STAGE_COMPLETE:TEST_STAGE_1`

**Expected outcome**:

- State file created at `.analysis/.state/analyze-project-test-stage-1.json`
- State contains: `{"chain_id":"test1234", "counter":1, ...}`

---

### STAGE 2: Execute Second Stage

**Your task**: Load and execute the second test stage.

1. Use the **Read** tool to load: `tests/chain-test-stage-2.md`

2. Read the ENTIRE file and follow ALL instructions in that file

3. Execute each step as documented (including loading Stage 1 state)

4. When complete, you should output: `STAGE_COMPLETE:TEST_STAGE_2`

**Expected outcome**:

- State file created at `.analysis/.state/analyze-project-test-stage-2.json`
- State contains: `{"chain_id":"test1234", "counter":2, ...}`
- Stage 2 successfully loaded and modified Stage 1 state

---

### Verification

After completing both stages, verify the test succeeded:

```bash
cd /home/user/spec-kit-smart

echo "=== Checking State Files ==="
ls -la .analysis/.state/analyze-project-test-stage-*.json

echo ""
echo "=== Stage 1 Final State ==="
./scripts/bash/chain-state.sh load test-stage-1

echo ""
echo "=== Stage 2 Final State ==="
./scripts/bash/chain-state.sh load test-stage-2

echo ""
echo "=== Verification ==="
# Check counter incremented
stage2_counter=$(./scripts/bash/chain-state.sh load test-stage-2 | jq -r '.counter')
if [[ "$stage2_counter" == "2" ]]; then
    echo "✅ TEST PASSED: Counter incremented correctly (1 → 2)"
else
    echo "❌ TEST FAILED: Counter not incremented (expected 2, got $stage2_counter)"
fi

# Check both stages in complete list
stages_complete=$(./scripts/bash/chain-state.sh load test-stage-2 | jq -r '.stages_complete | length')
if [[ "$stages_complete" == "2" ]]; then
    echo "✅ TEST PASSED: Both stages recorded in stages_complete"
else
    echo "❌ TEST FAILED: stages_complete count incorrect (expected 2, got $stages_complete)"
fi
```text

---

## Test Success Criteria

The test **PASSES** if:

- ✅ Both stage files can be read and executed
- ✅ State is saved after Stage 1
- ✅ Stage 2 can load Stage 1 state
- ✅ State is updated correctly (counter: 1 → 2)
- ✅ Both completion markers output
- ✅ Final verification shows correct state

The test **FAILS** if:

- ❌ Cannot read stage files
- ❌ State not saved correctly
- ❌ Stage 2 cannot load Stage 1 state
- ❌ State not updated
- ❌ Verification fails

---

## Cleanup

After test completes, clean up test files:

```bash
cd /home/user/spec-kit-smart
rm -f .analysis/.state/analyze-project-test-stage-*.json
```text

---

## What This Test Validates

1. **File Loading**: AI can use Read tool to load stage prompts
2. **Instruction Following**: AI executes all steps in each stage
3. **State Management**: AI can call chain-state.sh to save/load state
4. **State Persistence**: State survives between stages
5. **State Mutation**: AI can modify and update state correctly
6. **Sequential Execution**: Stages execute in correct order

If this test passes, it validates that the chained prompt architecture is viable for the full analyze-project workflow.

---

## Begin Test

**You should now**:

1. Initialize state directory (run init command above)
2. Execute Stage 1 (load and follow `chain-test-stage-1.md`)
3. Execute Stage 2 (load and follow `chain-test-stage-2.md`)
4. Run verification commands
5. Report test results

Proceed with the test execution.
