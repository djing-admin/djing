import shutil
import subprocess
import sys

from pathlib import Path


def generate_stubs(stub_directory: Path):
    core_directory = stub_directory.parent
    core_module = stub_directory.name

    print(f"Generating stubs for the {stub_directory} package in {core_directory}...")

    result = subprocess.run(
        ["stubgen", "-p", core_module, "-o", "."],
        cwd=core_directory,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error generating stubs:\n{result.stderr}")
        sys.exit(1)
    else:
        print(result.stdout)


def clean_generated_files(stub_directory: Path):
    print(f"Cleaning up generated files in {stub_directory}...")

    cpp_files = list(stub_directory.rglob("*.cpp"))
    so_files = list(stub_directory.rglob("*.so"))
    pyi_files = list(stub_directory.rglob("*.pyi"))
    pycache_dirs = list(stub_directory.rglob("__pycache__"))

    for file_list, ext in [(cpp_files, ".cpp"), (so_files, ".so"), (pyi_files, ".pyi")]:
        for file in file_list:
            print(f"Removing {ext} file: {file}")
            file.unlink()

    for pycache in pycache_dirs:
        print(f"Removing __pycache__ directory and its contents: {pycache}")
        shutil.rmtree(pycache)


def main(stub_directory: Path):
    if len(sys.argv) != 2:
        print("Usage: python manage_stubs.py {generate|clean}")
        sys.exit(1)

    action = sys.argv[1]

    if not stub_directory.is_dir():
        print(f"Error: {stub_directory} is not a valid directory.")
        sys.exit(1)

    if action == "generate":
        generate_stubs(stub_directory)
    elif action == "clean":
        clean_generated_files(stub_directory)
    else:
        print("Usage: python manage_stubs.py {generate|clean}")
        sys.exit(1)


if __name__ == "__main__":
    stub_directory = Path(__file__).parent / "djing" / "core" / "Foundation"
    main(stub_directory)
