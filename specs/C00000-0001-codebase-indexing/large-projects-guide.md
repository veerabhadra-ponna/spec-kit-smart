# Large Project Indexing Guide

Guidelines for indexing codebases with 50,000+ files.

## Overview

Large codebases present unique challenges:
- **Time**: Full index may take 10+ minutes
- **Memory**: Processing requires careful memory management
- **Relevance**: Not all files need indexing
- **Maintenance**: More frequent updates needed

This guide covers strategies for efficient large-scale indexing.

## Recommended Approach: Subdirectory Indexing

Instead of indexing the entire repository, index critical directories separately.

### Step 1: Identify Core Directories

```bash
# Find directories with most code files
find . -name "*.ts" -o -name "*.js" -o -name "*.py" |
  sed 's|/[^/]*$||' |
  sort |
  uniq -c |
  sort -rn |
  head -20
```

### Step 2: Create Targeted Indexes

```bash
# Index core business logic
/speckitsmart.index --path src/services --verbose

# Index API layer
/speckitsmart.index --path src/api --verbose

# Index data models
/speckitsmart.index --path src/models --verbose
```

### Step 3: Merge Results (Optional)

Combine multiple indexes for comprehensive querying:

```bash
# Merge structure files
jq -s '.[0].classes + .[1].classes | {classes: .}' \
  services/.analysis/index/structure.json \
  api/.analysis/index/structure.json > combined-structure.json
```

## Time Estimates by Project Size

| Files | Full Build | Incremental | Memory |
|-------|-----------|-------------|--------|
| 10K | 1-2 min | <10 sec | ~200MB |
| 25K | 3-5 min | <15 sec | ~350MB |
| 50K | 5-10 min | <30 sec | ~500MB |
| 100K | 15-30 min | <1 min | ~1GB |
| 200K+ | 30-60 min | 1-2 min | ~2GB |

## Optimization Strategies

### 1. Language Filtering

Only index relevant languages:

```bash
# TypeScript/JavaScript only
/speckitsmart.index --languages ts,tsx,js,jsx

# Backend only
/speckitsmart.index --languages py,java,go
```

### 2. Directory Exclusion

Skip non-essential directories:

```bash
# Add to .indexignore
node_modules/
vendor/
dist/
build/
coverage/
.git/
*.min.js
*.bundle.js
```

### 3. Batch Processing

For very large projects, process in batches:

```bash
#!/bin/bash
# batch-index.sh

BATCH_SIZE=5000
TOTAL_FILES=$(find src -name "*.ts" | wc -l)
BATCHES=$((TOTAL_FILES / BATCH_SIZE + 1))

for i in $(seq 1 $BATCHES); do
    echo "Processing batch $i of $BATCHES..."

    # Get files for this batch
    find src -name "*.ts" |
      sed -n "$((($i-1)*BATCH_SIZE+1)),$((i*BATCH_SIZE))p" > batch_files.txt

    # Index batch (custom implementation needed)
    /speckitsmart.index --files-from batch_files.txt --append

    # Progress
    echo "Batch $i complete"
done
```

### 4. Scheduled Full Rebuilds

Run full rebuilds during low-activity periods:

```cron
# Crontab entry: Full rebuild at 3 AM Sunday
0 3 * * 0 cd /path/to/repo && /speckitsmart.index --full > /var/log/index-rebuild.log 2>&1
```

### 5. Incremental-First Workflow

```bash
# Daily development
/speckitsmart.index --incremental

# After major merges
/speckitsmart.index --full

# After branch switch
git checkout main && /speckitsmart.index --incremental
```

## Memory Management

### Monitor Memory Usage

```bash
# Watch memory during indexing
/speckitsmart.index --verbose 2>&1 | tee index.log &
watch -n 1 'ps aux | grep build-codebase-index | grep -v grep'
```

### Reduce Memory Footprint

1. **Stream Processing**: Don't load entire files into memory
2. **Clear Caches**: Release parsed data after extraction
3. **Incremental Writes**: Write to index files as you go
4. **Limit Parallelism**: Single-threaded for memory control

### Memory Limits

Set memory limits to prevent system impact:

```bash
# Linux: Limit to 2GB
ulimit -v 2097152
/speckitsmart.index --full

# Or use cgroups
cgexec -g memory:indexing /speckitsmart.index --full
```

## Monorepo Strategies

### Per-Package Indexing

```
monorepo/
├── packages/
│   ├── frontend/
│   │   └── .analysis/index/  # Frontend index
│   ├── backend/
│   │   └── .analysis/index/  # Backend index
│   └── shared/
│       └── .analysis/index/  # Shared index
└── .analysis/index/          # Root summary index
```

```bash
# Index each package
for pkg in packages/*; do
    echo "Indexing $pkg..."
    /speckitsmart.index --path "$pkg" --verbose
done
```

### Cross-Package Queries

```bash
# Query across all packages
for index in packages/*/.analysis/index; do
    echo "=== $(dirname $index) ==="
    bash search-knowledge-base.sh --index "$index" --query "$QUERY"
done
```

## Distributed Indexing (Advanced)

For extremely large codebases, distribute indexing across machines:

### Architecture

```
┌─────────────────┐
│  Coordinator    │
│  (orchestrates) │
└────────┬────────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
┌─────┐┌─────┐┌─────┐
│Node1││Node2││Node3│
│src/a││src/b││src/c│
└──┬──┘└──┬──┘└──┬──┘
   │      │      │
   └──────┼──────┘
          ▼
    ┌───────────┐
    │  Merger   │
    │(combines) │
    └───────────┘
```

### Implementation Steps

1. **Partition**: Divide codebase by directory
2. **Distribute**: Send partitions to worker nodes
3. **Index**: Each node indexes its partition
4. **Collect**: Gather partial indexes
5. **Merge**: Combine into unified index

## Performance Monitoring

### Track Indexing Metrics

```bash
# Create metrics file
echo "timestamp,files,duration_ms,memory_mb" > metrics.csv

# Log each run
START_MS=$(date +%s%3N)
/speckitsmart.index --full 2>&1
END_MS=$(date +%s%3N)
DURATION=$((END_MS - START_MS))
FILES=$(jq '.statistics.indexed_files' .analysis/index/metadata.json)
MEMORY=$(ps aux | grep build-codebase-index | awk '{print $6}' | head -1)

echo "$(date -Iseconds),$FILES,$DURATION,$MEMORY" >> metrics.csv
```

### Alert on Performance Regression

```bash
# Check if build time exceeded threshold
DURATION=$(calculate_duration)
THRESHOLD=600000  # 10 minutes

if [[ $DURATION -gt $THRESHOLD ]]; then
    echo "WARNING: Index build took $((DURATION/1000)) seconds"
    echo "Consider running subdirectory indexing"
fi
```

## Best Practices Summary

1. **Start Incremental**: Use incremental updates for daily work
2. **Schedule Full Builds**: Run full rebuilds weekly or after major changes
3. **Filter Aggressively**: Only index relevant languages and directories
4. **Monitor Resources**: Watch memory and time during indexing
5. **Document Configuration**: Keep indexing configuration in repo
6. **Test Regularly**: Validate index quality periodically

## Troubleshooting

### Index Build Timeout

```
Error: Index build exceeded 30 minute timeout
```

**Solutions**:
1. Increase timeout: `--timeout 3600`
2. Index subdirectories separately
3. Filter by language

### Out of Memory

```
Error: JavaScript heap out of memory
```

**Solutions**:
1. Increase memory: `NODE_OPTIONS=--max-old-space-size=4096`
2. Process in batches
3. Use streaming parser

### Stale Results

```
Warning: Index may be stale (detected file changes)
```

**Solutions**:
1. Run `--incremental` more frequently
2. Set up git hooks for auto-update
3. Use CI/CD for scheduled rebuilds

---

*For projects exceeding 500K files, consider a dedicated search infrastructure like Elasticsearch or Sourcegraph.*
