# Contributing to n8n-to-Python

First off, thank you for considering contributing to this project! Your help is greatly appreciated. This document provides guidelines for adding new node handlers to the transpiler.

## How to Add a New Node Handler

Adding support for a new n8n node type involves implementing a handler function and registering it with the dispatcher. This ensures that the transpiler can correctly convert the node's JSON representation into executable Python code.

### 1. Create the Handler Function

A node handler is a Python function that takes a single argument: the node's JSON object from the n8n workflow. The function should return a string containing the Python code that replicates the node's functionality.

**Function Signature:**

```python
def handle_new_node(node: dict) -> str:
    """
    Generates Python code for a 'NewNode' n8n node.

    Args:
        node: A dictionary representing the n8n node's JSON data.

    Returns:
        A string of Python code.
    """
    # Extract parameters from the node object
    parameters = node.get("parameters", {})
    example_param = parameters.get("example_param", "default_value")

    # Generate the Python code
    python_code = f"print('This is a new node with param: {example_param}')"

    return python_code
```

### 2. Place the Handler in the Correct Module

To keep the codebase organized, group related handlers together. For example:
-   Data manipulation nodes go in `n8n_to_python/data_nodes.py`.
-   Database nodes go in `n8n_to_python/db_nodes.py`.
-   AI-related nodes go in `n8n_to_python/ai_nodes.py`.

If a suitable module doesn't exist, you can create a new one.

### 3. Register the Handler

After creating the handler function, you must register it in the `node_dispatcher` dictionary located in `n8n_to_python/utils.py`. The key should be the n8n node's `type` name, and the value should be the handler function.

**Example `n8n_to_python/utils.py`:**

```python
# utils.py

# ... other imports
from .my_new_nodes import handle_new_node # Import your new handler

node_dispatcher = {
    # ... existing handlers
    "NewNode": handle_new_node, # Add your new handler here
}
```

### 4. Testing Your Handler

While not yet enforced, it is highly recommended to add a test case for your new handler. You can do this by:

1.  Creating a minimal n8n workflow JSON file that uses the new node type.
2.  Adding a test function in a relevant test file that runs the transpiler on your new workflow.
3.  Asserting that the generated Python code is correct and executes without errors.

By following these steps, you can help expand the capabilities of the n8n-to-Python transpiler and make it more useful for everyone. Thank you for your contribution!