# cli_runner.py

import argparse
import json
import py_compile
import sys
import black
import inspect
import pkgutil
import importlib
import nodes as nds


def build_node_dispatcher():
    dispatcher = {}

    # Walk all submodules inside the nodes package
    for module_info in pkgutil.walk_packages(nds.__path__, nds.__name__ + "."):
        module = importlib.import_module(module_info.name)

        # Collect all functions named handle_*
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("handle_"):
                key = (
                    name.replace("handle_", "")
                    .replace("_", " ")
                    .title()
                )
                dispatcher[key] = func

    return dispatcher


def transpile_workflow(json_path, output_path="generated_workflow.py"):
    node_dispatcher = build_node_dispatcher()

    with open(json_path) as f:
        workflow = json.load(f)

    generated_code = []
    for node in workflow.get("nodes", []):
        node_type = node.get("type")
        handler = node_dispatcher.get(node_type)
        if handler:
            generated_code.append(f"# {node['name']}\n" + handler(node))
        else:
            generated_code.append(f"# {node['name']}\n# Unsupported node type: {node_type}")

    code_string = "\n\n".join(generated_code)

    try:
        code_string = black.format_str(code_string, mode=black.FileMode())
    except black.NothingChanged:
        pass

    with open(output_path, "w") as f:
        f.write(code_string)

    try:
        py_compile.compile(output_path, doraise=True)
        print(f"✅ Workflow transpiled, formatted, and validated to {output_path}")
    except py_compile.PyCompileError as e:
        print(f"❌ Error: Generated Python code in {output_path} is invalid.", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Transpile an n8n JSON workflow to Python script.")
    parser.add_argument("workflow", help="Path to n8n workflow JSON file")
    parser.add_argument("--output", default="generated_workflow.py", help="Output Python file path")
    args = parser.parse_args()

    transpile_workflow(args.workflow, args.output)


if __name__ == "__main__":
    main()
