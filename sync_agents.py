#!/usr/bin/env python3
import ast
import os
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
AGENTS_MD = ROOT / "AGENTS.md"

def _scan_module_docstring(path: Path) -> str:
    """Extract the first line of the docstring from a Python file."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, (ast.Constant, ast.Str)):
            doc = getattr(tree.body[0].value, "value", None) or getattr(tree.body[0].value, "s", "")
            if isinstance(doc, str):
                return doc.strip().split("\n")[0].rstrip(".")[:80]
    except Exception:
        pass
    return ""

def build_file_tree() -> str:
    """Build a generalized file tree up to a few levels deep, excluding common dev folders."""
    lines = []
    ignores = {".git", "node_modules", ".venv", "venv", "__pycache__", ".idea", ".vscode", "build", "dist", ".pytest_cache", ".agents"}
    
    def describe(path: Path) -> str:
        if path.suffix == ".py":
            return _scan_module_docstring(path)
        return ""

    def walk_dir(directory: Path, prefix: str = "", child_prefix: str = "", depth: int = 0) -> None:
        if depth > 4:  # Stop going too deep to keep AGENTS.md clean
            return
            
        try:
            entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return
            
        entries = [e for e in entries if e.name not in ignores and not e.name.startswith(".")]
        
        for i, item in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            extension = "    " if is_last else "│   "
            desc = describe(item) if item.is_file() else ""
            
            name = item.name + ("/" if item.is_dir() else "")
            padding = max(1, 40 - len(child_prefix) - len(connector) - len(name))
            
            if desc:
                lines.append(f"{child_prefix}{connector}{name}{' ' * padding}# {desc}")
            else:
                lines.append(f"{child_prefix}{connector}{name}")
                
            if item.is_dir():
                walk_dir(item, connector, child_prefix + extension, depth + 1)

    walk_dir(ROOT)
    return "\n".join(lines)

def update_section(text: str, content: str) -> str:
    """Replace the code block under the '## Project Structure' heading."""
    pattern = re.compile(r"(## Project Structure\s*\n\s*```text\n).*?(\n```)", re.DOTALL)
    if pattern.search(text):
        return pattern.sub(rf"\g<1>{content}\g<2>", text)
        
    # fallback to adding it if heading exists
    if "## Project Structure" in text:
        return text.replace("## Project Structure", f"## Project Structure\n\n```text\n{content}\n```\n")
        
    # Append to end if not found
    return text + f"\n\n## Project Structure\n\n```text\n{content}\n```\n"

def main():
    if not AGENTS_MD.is_file():
        AGENTS_MD.write_text("# Repository Guidelines\n\n## Project Structure\n\n```text\n```\n")
        
    original = AGENTS_MD.read_text(encoding="utf-8")
    tree = build_file_tree()
    updated = update_section(original, tree)
    
    if updated != original:
        AGENTS_MD.write_text(updated, encoding="utf-8")
        print("✓ AGENTS.md project structure updated")

if __name__ == "__main__":
    main()
