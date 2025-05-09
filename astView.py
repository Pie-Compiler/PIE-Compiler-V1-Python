import json
from parser import Parser, print_ast  # Ensure Parser is imported

def ast_to_json(node):
    """Convert the AST into a JSON-compatible structure."""
    if isinstance(node, tuple):
        return [node[0]] + [ast_to_json(child) for child in node[1:]]
    elif isinstance(node, list):
        return [ast_to_json(item) for item in node]
    else:
        return node

def export_ast_to_json(ast, output_file="ast.json"):
    """Export the AST to a JSON file."""
    with open(output_file, "w") as file:
        json.dump(ast_to_json(ast), file, indent=2)

def format_tree(node, prefix="", is_last=True):
    lines = []

    if isinstance(node, list):
        if not node:
            return lines

        label = str(node[0])  # Node type
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + label)

        new_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(node[1:]):
            last = (i == len(node[1:]) - 1)
            child_lines = format_tree(child, new_prefix, last)
            lines.extend(child_lines)

        if prefix == "":  # Add blank line between top-level nodes
            lines.append("")

    else:
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + str(node))

    return lines


def export_ast_to_txt(ast, output_file="ast.txt"):
    """Export the AST to a human-readable tree structure in a text file."""
    lines = format_tree(ast)
    with open(output_file, "w") as f:
        f.write("\n".join(lines))

def main():
    parser = Parser()
    input_file = "test2.pie"

    try:
        with open(input_file, "r") as file:
            input_program = file.read()

        ast = parser.parse(input_program)
        print("Parsing successful!")

        export_ast_to_json(ast, "ast.json")
        print("AST exported to 'ast.json'")

        export_ast_to_txt(ast_to_json(ast), "ast.txt")
        print("AST exported visually to 'ast.txt'")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Parsing error: {e}")

if __name__ == "__main__":
    main()