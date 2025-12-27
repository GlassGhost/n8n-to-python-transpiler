#####
File: cli_runner.py
#####

```
# cli_runner.py

import argparse
import json
import py_compile
import sys
import black
from utils import node_dispatcher


def transpile_workflow(json_path, output_path="generated_workflow.py"):
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

```
#####
File: main.py
#####

```
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

```
#####
File: utils.py
#####

```
# utils.py

from data_nodes import handle_set, handle_if, handle_merge, handle_comment
from db_nodes import handle_mysql, handle_postgresql, handle_mongodb
from control_nodes import handle_cron, handle_delay
from auth_nodes import handle_http_basic_auth, handle_oauth2
from ai_nodes import handle_openai_completion, handle_huggingface_transformer
from file_nodes import handle_read_file, handle_write_file
from integration_nodes import handle_sendgrid_email, handle_slack_message
from webhook_nodes import handle_webhook_trigger

node_dispatcher = {
    "Set": handle_set,
    "If": handle_if,
    "Merge": handle_merge,
    "n8n-nodes-base.stickyNote": handle_comment,
    "MySQL": handle_mysql,
    "PostgreSQL": handle_postgresql,
    "MongoDB": handle_mongodb,
    "Cron": handle_cron,
    "Delay": handle_delay,
    "HTTP Basic Auth": handle_http_basic_auth,
    "OAuth2": handle_oauth2,
    "OpenAI": handle_openai_completion,
    "HuggingFace": handle_huggingface_transformer,
    "Read File": handle_read_file,
    "Write File": handle_write_file,
    "SendGrid": handle_sendgrid_email,
    "Slack": handle_slack_message,
    "Webhook": handle_webhook_trigger
}

```
