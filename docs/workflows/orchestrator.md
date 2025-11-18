# Orchestrator Workflow

## Overview

The **Orchestrator** workflow simplifies the entire spec-driven development process by managing all phases automatically. Instead of manually invoking each command (constitution → specify → clarify → plan → tasks → analyze → implement), you can run the entire workflow with a single command.

## Why Use the Orchestrator?

**Manual Workflow:** 7 separate commands, manual state tracking, context loss at chat limits.

**Orchestrator Workflow:** `/speckitsmart.orchestrate <feature-description>` - 1 command, automatic state management, seamless resumption.

## Key Features

### 1. Single Entry Point

Run the entire workflow from feature description to implementation with one command.

### 2. State Persistence

The orchestrator saves progress to `.speckitsmart-state.json`, enabling:

- Resumption after chat token limits
- Cross-session continuity
- Progress tracking

### 3. Flexible Execution Modes

```mermaid
graph LR
    subgraph Interactive["Interactive Mode"]
        direction LR
        I1[Constitution] --> |Ask| I2[Specify] --> |Ask| I3[Clarify] --> |Ask| I4[Plan] --> |Ask| I5[Tasks] --> |Ask| I6[Analyze] --> |Ask| I7[Implement]
    end

    subgraph AutoSpec["Auto-Spec Mode"]
        direction LR
        A1[Constitution] --> A2[Specify] --> A3[Plan] --> A4[Tasks] --> |PAUSE| A5[Implement]
    end

    subgraph FullAuto["Full Auto Mode"]
        direction LR
        F1[Constitution] --> F2[Specify] --> F3[Plan] --> F4[Tasks] --> F5[Implement] --> F6[Done]
    end

    style Interactive fill:#e3f2fd,stroke:#333,stroke-width:2px
    style AutoSpec fill:#fff9c4,stroke:#333,stroke-width:2px
    style FullAuto fill:#e8f5e9,stroke:#333,stroke-width:2px
```

**Interactive Mode** (recommended):

- Asks permission before each major phase
- Allows review and adjustment between phases
- User maintains full control

**Auto-Spec Mode**:

- Runs constitution → specify → plan → tasks automatically
- Pauses before implementation for review

**Full Auto Mode**:

- Runs entire workflow to completion
- Minimal user interaction required

### 4. Context Restoration with `/speckitsmart.resume`

Restores context after chat limit: loads all artifacts, identifies stopping point, and continues with zero duplicate work.

## Usage Examples

**Interactive Mode:**

```bash
/speckitsmart.orchestrate Build a user authentication system with OAuth2 and JWT
```

Prompts at each phase for user confirmation and review.

**Auto-Spec Mode:**

```bash
/speckitsmart.orchestrate --mode=auto-spec Create an analytics dashboard
```

Runs constitution → specify → plan → tasks automatically, pauses before implementation for review.

**Resume After Chat Limit:**

```bash
/speckitsmart.resume
```

```mermaid
flowchart LR
    NewChat[New Chat] --> Resume[/resume]
    Resume --> LoadState[Load State]
    LoadState --> LoadArtifacts[Load Artifacts]
    LoadArtifacts --> Identify[Identify<br/>Resume Point]
    Identify --> Summary[Show Summary]
    Summary --> Confirm{Resume?}
    Confirm -->|Yes| Continue[Continue]
    Confirm -->|No| Cancel[Cancel]
    Continue --> Done[Complete]

    style NewChat fill:#e8eaf6,stroke:#333,stroke-width:2px
    style Resume fill:#e1f5e1,stroke:#333,stroke-width:2px
    style LoadState fill:#fff9c4,stroke:#333,stroke-width:2px
    style LoadArtifacts fill:#e3f2fd,stroke:#333,stroke-width:2px
    style Identify fill:#fff4e6,stroke:#333,stroke-width:2px
    style Summary fill:#e8f5e9,stroke:#333,stroke-width:2px
    style Continue fill:#c8e6c9,stroke:#333,stroke-width:2px
    style Done fill:#a5d6a7,stroke:#333,stroke-width:2px
```

Loads state, shows progress (e.g., 28/47 tasks), identifies next task, and continues from exact stopping point.

## State Management

The orchestrator creates `.speckitsmart-state.json` in your repository root:

```json
{
  "version": "1.0",
  "feature_number": "001",
  "feature_name": "user-auth",
  "feature_dir": "specs/001-user-auth",
  "current_phase": "implement",
  "completed_phases": ["constitution", "specify", "plan", "tasks"],
  "workflow_mode": "interactive",
  "started_at": "2025-11-02T10:30:00Z",
  "last_updated": "2025-11-02T11:15:00Z",
  "checkpoints": {
    "implement": {
      "status": "in_progress",
      "tasks_completed": 28,
      "tasks_total": 47,
      "current_task": "[T029] Implement webhook verification"
    }
  }
}
```

**Should you commit `.speckitsmart-state.json`?**

- ✅ **Yes** if you want cross-machine resumption or team collaboration
- ❌ **Add to .gitignore** if you prefer local-only state

## When to Use Orchestrator vs Individual Commands

- **New features:** Use `/speckitsmart.orchestrate`
- **Multi-day workflows:** Use orchestrator + `/speckitsmart.resume`
- **Learning:** Use individual commands
- **Re-running phases:** Use individual commands (e.g., `/speckitsmart.plan`)
- **Token limits:** Use `/speckitsmart.resume`

## Best Practices

- **Commit frequently** during long workflows
- **Review before implementation** using interactive or auto-spec mode
- **Commit `.speckitsmart-state.json`** for cross-machine work
- **Use `/speckitsmart.resume`** after token limits or errors

## Progress Visualization

**Task-Level Progress:**

```mermaid
graph LR
    subgraph US3["User Story 3: In Progress"]
        direction LR
        T015["T015: Auth<br/>middleware ✓"] --> T016["T016: JWT<br/>validation ⚙"]
        T016 -.-> T017["T017: Token<br/>refresh ⏳"]
        T017 -.-> T018["T018: Logout<br/>handler ⏳"]
        T018 -.-> T019["T019: Rate<br/>limiting ⏳"]
        T019 -.-> T020["T020:<br/>Tests ⏳"]
    end

    style T015 fill:#c8e6c9,stroke:#4caf50,stroke-width:2px
    style T016 fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style T017 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
    style T018 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
    style T019 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
    style T020 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
```

**Legend:**

- ✓ = Completed
- ⚙ = In Progress (current task)
- ⏳ = Pending
- ⏭ = Skipped

## Error Handling

If any phase fails:

```text
❌ Error in phase: implement

Error details: Module 'stripe' not found

Your progress has been saved.

To resume after fixing the issue:
  /speckitsmart.resume

To start over:
  rm .speckitsmart-state.json
  /speckitsmart.orchestrate <feature-description>
```

Simply fix the issue (e.g., `npm install stripe`) and run `/speckitsmart.resume` to continue.

## Workflow Diagram (Orchestrator)

```mermaid
flowchart LR
    Start([/orchestrate]) --> Constitution[Constitution]
    Constitution --> Specify[Specify]
    Specify --> Clarify[Clarify]
    Clarify --> Plan[Plan]
    Plan --> Tasks[Tasks]
    Tasks --> Analyze[Analyze]
    Analyze --> Implement[Implement]
    Implement --> Done([Done])

    State[.speckitsmart-state.json]
    Constitution -.-> State
    Specify -.-> State
    Clarify -.-> State
    Plan -.-> State
    Tasks -.-> State
    Analyze -.-> State
    Implement -.-> State

    State -.-> Resume[/resume]
    Resume -.-> |Restore| Constitution

    style Start fill:#e1f5e1,stroke:#333,stroke-width:2px
    style Done fill:#e1f5e1,stroke:#333,stroke-width:2px
    style Constitution fill:#fff4e6,stroke:#333,stroke-width:2px
    style Specify fill:#e3f2fd,stroke:#333,stroke-width:2px
    style Clarify fill:#f3e5f5,stroke:#333,stroke-width:2px
    style Plan fill:#e8f5e9,stroke:#333,stroke-width:2px
    style Tasks fill:#fff9c4,stroke:#333,stroke-width:2px
    style Analyze fill:#fce4ec,stroke:#333,stroke-width:2px
    style Implement fill:#e0f2f1,stroke:#333,stroke-width:2px
    style State fill:#fff3e0,stroke:#333,stroke-width:2px
    style Resume fill:#e8eaf6,stroke:#333,stroke-width:2px
```

## Summary

One-command execution, automatic state management, zero context loss, flexible modes, cross-session continuity, error recovery, and progress transparency.

```bash
/speckitsmart.orchestrate <your-feature-description>
```

## Related Documentation

- [Getting Started Guide](../getting-started.md)
- [Standard Workflow](../README.md#workflow-diagram-spec-driven-development)
- [Troubleshooting](../reference/troubleshooting.md)
