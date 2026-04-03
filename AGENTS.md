# AGENTS Memory

## Project Scope
- This is a learning project focused on a small static-site/markdown pipeline.
- Prefer clarity and correctness over framework-heavy patterns.
- Keep changes incremental and easy to review.

## Non-Goals
- Do not expand markdown support beyond the assignment scope unless explicitly requested.
- Do not introduce broad architecture changes when a focused fix is enough.
- Do not add large integration-style test suites when targeted unit tests cover behavior.

## Parser And Converter Expectations
- Validate core in-scope behavior strictly (node types, delimiter handling, conversion output, and known edge cases).
- Raise clear errors for malformed input only where behavior is in scope.
- When delimiter handling is in scope, include representative malformed unmatched-delimiter examples (for example `**bold*` and `*italics**`) to probe boundary behavior.
- Treat overlapping or nested delimiter parsing as out of required scope unless project requirements change.
- Treat unsupported markdown features as out of scope unless requirements change.

## Workflow Preferences
- Make small, focused edits.
- When parser/converter behavior changes, add or update tests first (or in the same change) for that behavior.
- Prefer parameterized tests for input/output variants.

## Testing Rule Intent
- When a task involves planning, writing, or refining tests, load and follow `.cursor/rules/pytest.mdc`.

## Chat Log Requirement
- Append a concise entry for each user/assistant interaction to `CHATLOG.md` in the project root.
