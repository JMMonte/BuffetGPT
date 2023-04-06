import os
import re

def generate_mermaid_diagram(root_dir):
    mermaid_diagram = "graph TD\n"
    ignore_dirs = ["venv", "__pycache__", ".vscode", ".git"]
    subgraphs = {}
    edges = set()
    for subdir, dirs, files in os.walk(root_dir):
        if any(ignore_dir in subdir for ignore_dir in ignore_dirs):
            continue
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                file_name = os.path.splitext(file)[0]
                subgraphs[file_name] = {"classes": set(), "methods": {}, "attributes": {}}
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    class_name = None
                    for line in lines:
                        if line.startswith("class "):
                            class_name = line.split(" ")[1].split("(")[0]
                            subgraphs[file_name]["classes"].add(class_name)
                            subgraphs[file_name]["methods"][class_name] = set()
                            subgraphs[file_name]["attributes"][class_name] = set()
                        elif class_name:
                            if line.startswith("    def "):
                                method_name = line.split(" ")[2].split("(")[0]
                                subgraphs[file_name]["methods"][class_name].add(method_name)
                            elif re.match(r"\s+self\.\w+\s*=", line):
                                attribute_name = re.search(r"\s+self\.(\w+)\s*=", line).group(1)
                                subgraphs[file_name]["attributes"][class_name].add(attribute_name)
                            elif re.search(r"\b[A-Z]\w+\(", line):
                                dependency_name = re.search(r"\b([A-Z]\w+)\(", line).group(1)
                                edges.add((class_name, dependency_name))

    for file_name, file_info in subgraphs.items():
        mermaid_diagram += f"    subgraph {file_name}\n"
        for class_name in file_info["classes"]:
            mermaid_diagram += f"        {class_name}\n"
            for method in file_info["methods"][class_name]:
                method_node_id = f"{class_name}_{method}"
                mermaid_diagram += f"        {method_node_id}({method})\n"
                mermaid_diagram += f"        {class_name} --> {method_node_id}\n"
            for attribute in file_info["attributes"][class_name]:
                attribute_node_id = f"{class_name}_{attribute}"
                mermaid_diagram += f"        {attribute_node_id}[{attribute}]\n"
                mermaid_diagram += f"        {class_name} --> {attribute_node_id}\n"
        mermaid_diagram += "    end\n"

    for edge in edges:
        mermaid_diagram += f"    {edge[0]} --> {edge[1]}\n"

    return mermaid_diagram

root_dir = os.getcwd()
mermaid_diagram = generate_mermaid_diagram(root_dir)

with open(os.path.join(root_dir, "mermaid_diagram.mmd"), "w") as f:
    f.write(mermaid_diagram)

print("Mermaid diagram saved to 'mermaid_diagram.mmd'")