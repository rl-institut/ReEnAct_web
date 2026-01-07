"""Generate (virtual) API documentation for digiplan."""
from pathlib import Path

import mkdocs_gen_files


docs_dir = Path("docs/api")

PACKAGE_DIR = Path("reenact/reenact")
RESULTS_DIR = PACKAGE_DIR / "results"
SKIP_MODULES = ["__init__", "__pycache__", "admin", "migrations"]

for path in (PACKAGE_DIR, RESULTS_DIR):
    for module in path.iterdir():
        if module.is_dir():
            continue
        if module.stem in SKIP_MODULES:
            continue
        rel_path = Path("api", module.stem)  # e.g. api/mypackage/module.py
        file_path = rel_path.with_suffix(".md")

        module_path = f"{str(path).replace('/', '.')}.{module.stem}"
        with mkdocs_gen_files.open(file_path, "w") as f:
            f.write(f"# `{module_path}`\n\n")
            f.write(f"::: {module_path}\n")
            f.write(f"    handler: python\n")
            f.write(f"    options:\n")
            f.write(f"      show_submodules: true\n")
            f.write(f"      show_root_toc_entry: true\n")
            f.write(f"      show_root_full_path: true\n")

        mkdocs_gen_files.set_edit_path(file_path, path / module.stem)
