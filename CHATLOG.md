# Chat Log

## 2026-04-01

- User: "make a rules folder"
- Assistant: Created `rules/` with `rules/.gitkeep`.
- User: "I meant a cursor rules folder"
- Assistant: Created `.cursor/rules/` with `.cursor/rules/.gitkeep`.
- User: "add the cursor directory to git ignore"
- Assistant: Updated `.gitignore` to ignore `.cursor/`.
- User: "@.cursor/rules/pytest.mdc flesh out the current test suite"
- Assistant: Expanded `src/test/test_html_node.py` with additional behavior and error-path tests.
- User: "Split HTMLNode Test And Improve Suite"
- Assistant: Split constructor assertions into focused tests, parameterized `props_to_html` cases, improved `TextNode` test names/coverage, and validated lint status.
