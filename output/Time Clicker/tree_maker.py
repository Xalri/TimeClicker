import os

def generate_tree(directory, prefix=""):
    ignore_list = {"__pycache__", ".vscode", ".gitignore", ".git", ".prettierrc", "auto-py-to-exe.json", "build.json", "Dispo.pdf", "humans.py", "main_old.py", "template.jpeg", "tree_maker.py"}  # Folders and files to ignore
    entries = sorted(os.listdir(directory), key=lambda e: (os.path.isdir(os.path.join(directory, e)), e.lower()))
    entries = [e for e in entries if e not in ignore_list]  # Filter out ignored entries
    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            generate_tree(path, new_prefix)

if __name__ == "__main__":
    project_dir = os.path.abspath(".")  # Change this to your project's root directory if needed
    print(os.path.basename(project_dir) + "/")
    generate_tree(project_dir)