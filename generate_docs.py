#!/usr/bin/env python3
"""
Generate HTML documentation for every module inside given package folders.

This script will:
- walk the listed package directories (by default: `src` and `tests`)
- compute dotted module names (e.g. `src.farm_data_analyzer`)
- add the project root to sys.path so imports succeed
- call pydoc.writedoc for each module and put the resulting HTML files into `docs/`

It handles ImportError gracefully and prints a short summary at the end.
"""
import os
import sys
import pydoc
import traceback
from typing import Set, List, Dict, Tuple
import ast
import importlib.util


def find_modules(packages: List[str], project_root: str) -> Dict[str, str]:
    """Return a set of dotted module names found under the given package folders.

    - packages: list of top-level folder names relative to project_root
    - project_root: absolute path to the project root (contains the packages)
    """
    modules: Dict[str, str] = {}
    for pkg in packages:
        pkg_path = os.path.join(project_root, pkg)
        if not os.path.isdir(pkg_path):
            print(f"Skipping missing package path: {pkg_path}")
            continue

        for root, dirs, files in os.walk(pkg_path):
            # Skip __pycache__ and hidden folders
            dirs[:] = [d for d in dirs if not (d == '__pycache__' or d.startswith('.'))]

            rel_root = os.path.relpath(root, project_root)
            # Convert path to dotted prefix, e.g. 'src' or 'src.subpkg'
            if rel_root == '.':
                prefix = ''
            else:
                prefix = rel_root.replace(os.sep, '.')

            for f in files:
                if not f.endswith('.py'):
                    continue
                if f.startswith('.'):
                    continue

                if f == '__init__.py':
                    # document the package itself
                    module_name = prefix or pkg
                else:
                    base = f[:-3]
                    if prefix:
                        module_name = f"{prefix}.{base}"
                    else:
                        module_name = f"{pkg}.{base}"

                modules[module_name] = os.path.join(root, f)

    return modules


def generate_docs(packages: List[str] = None) -> None:
    """Generate HTML documentation for all modules under the listed packages."""
    if packages is None:
        packages = ['src', 'tests']

    script_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = script_dir

    # Ensure project root is on sys.path so imports like `src.foo` work
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    modules_map = find_modules(packages, project_root)
    modules = sorted(modules_map.keys())
    if not modules:
        print("No modules found to document.")
        return

    docs_dir = os.path.join(project_root, 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    orig_cwd = os.getcwd()
    try:
        os.chdir(docs_dir)
        successes = []
        failures = []
        # top-level names that are part of this project and should be treated as available
        local_tops = set(packages) | {m.split('.')[0] for m in modules_map.keys()}

        for mod in modules:
            file_path = modules_map.get(mod)

            # Quick pre-check: parse imports and ensure third-party imports are available
            missing: List[str] = []
            try:
                with open(file_path, 'r', encoding='utf-8') as fh:
                    node = ast.parse(fh.read(), filename=file_path)
                for n in ast.walk(node):
                    if isinstance(n, ast.Import):
                        for alias in n.names:
                            top = alias.name.split('.')[0]
                            # skip standard library and project-local packages
                            if top in local_tops:
                                continue
                            if importlib.util.find_spec(top) is None:
                                missing.append(top)
                    elif isinstance(n, ast.ImportFrom):
                        # If this is a relative import (level > 0) it's local to the package
                        if getattr(n, 'level', 0) and n.level > 0:
                            continue
                        if n.module is None:
                            continue
                        top = n.module.split('.')[0]
                        if top in local_tops:
                            continue
                        if importlib.util.find_spec(top) is None:
                            missing.append(top)
            except Exception:
                # If parsing fails, just attempt to document and let pydoc report issues
                missing = []

            if missing:
                missing_unique = sorted(set(missing))
                msg = f"Skipping {mod} because the following imports are missing: {', '.join(missing_unique)}"
                print(msg)
                failures.append((mod, 'missing imports: ' + ','.join(missing_unique)))
                continue

            try:
                pydoc.writedoc(mod)
                print(f"Generated documentation for {mod}")
                successes.append(mod)
            except Exception as exc:  # import error or other failures
                print(f"Failed to document {mod}: {exc}")
                traceback.print_exc()
                failures.append((mod, str(exc)))

    finally:
        os.chdir(orig_cwd)

    print('\nSummary:')
    print(f'  Documented modules: {len(successes)}')
    if failures:
        print(f'  Failed modules: {len(failures)}')
        for mod, err in failures:
            print(f'    - {mod}: {err}')

    # Build an index.html in docs/ linking to generated module pages
    try:
        index_path = os.path.join(docs_dir, 'index.html')
        grouped: Dict[str, List[Tuple[str, bool]]] = {}
        # successes: modules successfully documented
        success_set = set(successes)
        failure_set = {f[0] for f in failures}

        for mod in modules:
            top = mod.split('.')[0]
            grouped.setdefault(top, []).append((mod, mod in success_set))

        lines = [
            '<!doctype html>',
            '<html lang="en">',
            '<head>',
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            f'  <title>Project documentation index</title>',
            '  <style> body{font-family:Segoe UI,Arial,Helvetica,sans-serif;padding:20px} h1{font-size:1.5rem} ul{line-height:1.6} .skipped{color:#c00} </style>',
            '</head>',
            '<body>',
            '  <h1>Documentation index</h1>',
            f'  <p>Generated modules: {len(successes)} — Skipped/failed: {len(failures)}</p>',
        ]

        for top in sorted(grouped.keys()):
            lines.append(f'  <h2>{top}</h2>')
            lines.append('  <ul>')
            for mod, ok in sorted(grouped[top]):
                # pydoc creates filenames like module.name.html (dots become dots)
                filename = f"{mod}.html"
                if ok:
                    lines.append(f'    <li><a href="{filename}">{mod}</a></li>')
                else:
                    lines.append(f'    <li class="skipped">{mod} (skipped)</li>')
            lines.append('  </ul>')

        lines.extend(['</body>', '</html>'])

        with open(index_path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))

        print(f"Wrote index to {index_path}")
    except Exception:
        print("Failed to write index.html")
        traceback.print_exc()


if __name__ == '__main__':
    generate_docs()