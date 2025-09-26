# Contributing to n8n-to-Python Best Practices

This document outlines the best practices for contributing to the n8n-to-Python transpiler. Adhering to these guidelines will help maintain code quality, improve readability, and make the project more robust and extensible.

## 1. Error Handling for Unsupported Nodes

When encountering a node type that is not supported by the transpiler, the script should not crash. Instead, it should:

- **Log a warning:** Inform the user that an unsupported node type was found and that it will be skipped.
- **Continue processing:** The transpiler should proceed with the rest of the workflow, generating code for the supported nodes.
- **Placeholder comment:** In the generated Python script, a comment should be inserted to indicate where the unsupported node was in the original workflow.

Example:
```python
# Unsupported node type "ExampleNode" was skipped.
```

## 2. Python Code Validation

All generated Python code must be syntactically valid. To ensure this, a validation step should be part of the transpilation process.

- **Use `py_compile`:** The `py_compile` module can be used to check for syntax errors in the generated code without executing it.
- **Report errors:** If syntax errors are found, they should be reported to the user, and the script should exit with a non-zero status code.

## 3. Output Formatting

The generated Python code should be clean, readable, and follow standard Python conventions.

- **PEP 8 compliance:** All code should adhere to the PEP 8 style guide.
- **Use a code formatter:** A tool like `black` or `autopep8` should be used to automatically format the generated code.
- **Add comments and docstrings:** The generated code should include comments explaining complex logic and docstrings for all functions and modules.

## 4. Documentation for Extending Node Handlers

To make it easier for other developers to contribute, there must be clear documentation on how to add new node handlers. This documentation should be in a `CONTRIBUTING.md` file and include:

- **Handler function signature:** A clear definition of the arguments and return values for a node handler function.
- **Code examples:** A complete example of a new node handler, from implementation to registration.
- **Dispatcher registration:** Instructions on how to add the new handler to the `node_dispatcher` in `n8n_to_python/utils.py`.

## 5. Increasing Node Type Coverage

When adding a new node handler, follow these steps:

- **Create a new function:** The function should accept the node's parameters as arguments and return the corresponding Python code as a string.
- **Place the function in the appropriate module:** Group related node handlers together in the same file (e.g., `data_nodes.py`, `ai_nodes.py`).
- **Register the handler:** Add the new handler function to the `node_dispatcher` in `utils.py`.
- **Add a test case:** Create a test case that uses a sample n8n workflow with the new node type and verifies that the generated Python code is correct.