import json
import py_compile
import sys
import black
from utils import node_dispatcher


def load_n8n_workflow(path):
    with open(path) as f:
        return json.load(f)


def transpile_workflow(n8n_json):
    python_lines = ["# Auto-generated from n8n workflow\n"]
    for node in n8n_json.get("nodes", []):
        handler = node_dispatcher.get(node["type"])
        if handler:
            code = handler(node)
            python_lines.append(code)
        else:
            python_lines.append(f"# Skipping unsupported node: {node['type']}")
    return "\n\n".join(python_lines)


if __name__ == "__main__":
    output_filename = "generated_workflow.py"
    workflow = load_n8n_workflow("n8n_to_python/example_workflow.json")
    python_code = transpile_workflow(workflow)

    try:
        python_code = black.format_str(python_code, mode=black.FileMode())
    except black.NothingChanged:
        pass

    with open(output_filename, "w") as f:
        f.write(python_code)

    try:
        py_compile.compile(output_filename, doraise=True)
        print(f"✅ Python workflow generated, formatted, and validated as {output_filename}")
    except py_compile.PyCompileError as e:
        print(f"❌ Error: Generated Python code in {output_filename} is invalid.", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
