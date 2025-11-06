# Markdown Style Guide

This document describes the markdown style conventions used in this project.

## Markdownlint Configuration

We use a `.markdownlintrc` configuration that balances strictness with practicality for documentation.

### Enabled Rules

**MD003**: Header style - ATX style (`#` prefix)

- ✅ Correct: `## Heading`
- ❌ Incorrect: `Heading\n-------`

**MD004**: Unordered list style - Dash style

- ✅ Correct: `- List item`
- ❌ Incorrect: `* List item`

**MD024**: Multiple headers with same content (siblings_only)

- Same headers allowed if not siblings (different sections)
- Helps with FAQ sections and repeated patterns

**MD046**: Code block style - Fenced (```)

- ✅ Correct: ` ```language\ncode\n``` `
- ❌ Incorrect: Indented code blocks

### Disabled Rules (With Rationale)

**MD013**: Line length

- **Why disabled**: Documentation often requires long lines for:
  - Example commands
  - URLs
  - Code snippets
  - Table content
- **Best practice**: Still try to keep prose under 100 characters when possible

**MD026**: Trailing punctuation in headers

- **Why disabled**: Allows headers like:
  - `## What's Good ✅`
  - `## What's Bad ❌`
  - `## Prerequisites?`
- Emojis and question marks can improve readability

**MD033**: Inline HTML

- **Why disabled (but limited)**: Allows specific HTML elements:
  - `<div align="center">` for centering content
  - `<img>` for logo/images with specific attributes
  - `<h1>`, `<h3>`, `<p>`, `<strong>`, `<a>` for README styling
- Still discouraged outside README and landing pages

**MD040**: Fenced code blocks should have language

- **Why disabled**: Many examples use plain text or output:
  - Command outputs
  - Generic text examples
  - Multi-language snippets
- **Best practice**: Add language when known (bash, python, json, etc.)

**MD041**: First line should be top-level header

- **Why disabled**: Allows YAML front matter in templates:

```yaml
---
description: Command description
---
```

## Best Practices

### 1. Headers

Use ATX style with blank lines before and after:

```markdown
Paragraph text.

## New Section

More text here.
```

### 2. Lists

Use dashes for unordered lists, blank lines before/after:

```markdown
Paragraph.

- Item 1
- Item 2
- Item 3

Next paragraph.
```

### 3. Code Blocks

Use fenced style with language when possible:

````markdown
Command example:

```bash
npm install
```

Output:

```text
✓ Installation complete
```
````

### 4. Links

Use reference-style for repeated links:

```markdown
See [GitHub Issues][issues] for details.
Check [GitHub Issues][issues] again.

[issues]: https://github.com/user/repo/issues
```

### 5. Tables

Align pipes for readability:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

### 6. Emphasis

- **Bold**: `**important**` for important terms
- *Italic*: `*emphasis*` for emphasis
- `Code`: `` `code` `` for inline code, commands, file names

### 7. Line Breaks

- Use single blank line between paragraphs
- Use two blank lines before major sections (optional)
- No trailing whitespace

## File-Specific Guidelines

### README.md

- Keep concise (link to detailed docs)
- Use HTML sparingly for styling
- Include badges at top
- Table of contents for long docs

### Documentation (docs/*)

- Comprehensive is okay
- Use examples liberally
- Include troubleshooting sections
- Cross-reference related docs

### Templates (templates/*)

- Include YAML front matter
- Clear section markers
- Placeholder syntax: `[PLACEHOLDER]`
- Comments for AI agents

## Validation

To check markdown (if markdownlint-cli installed):

```bash
npx markdownlint-cli2 "**/*.md" "#node_modules"
```

To fix auto-fixable issues:

```bash
npx markdownlint-cli2-fix "**/*.md" "#node_modules"
```

## When to Break Rules

Rules can be broken when:

1. **Readability improves**: Tables with long lines
2. **Examples require it**: Long command outputs
3. **External constraints**: Generated content
4. **Accessibility**: Screen reader-friendly formatting

Always prioritize:

1. Clarity
2. Consistency
3. Maintainability
4. Strict compliance

## References

- [Markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [CommonMark Spec](https://commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
