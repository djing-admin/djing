import os
import sys

from pathlib import Path


class PackageManager:
    @staticmethod
    def remove_init(root_directory: Path) -> None:
        for dirpath, dirnames, filenames in os.walk(root_directory):
            if "__init__.py" in filenames:
                init_file_path = Path(dirpath) / "__init__.py"
                init_file_path.unlink()
                print(f"Removed: {init_file_path}")

    @staticmethod
    def add_init(root_directory: Path) -> None:
        for dirpath, dirnames, filenames in os.walk(root_directory):
            if any([file.endswith(".py") for file in filenames]):
                init_file_path = Path(dirpath) / "__init__.py"

                if not init_file_path.exists():
                    init_file_path.touch()
                    print(f"Added: {init_file_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python package.py {generate|clean} {directory_name}")
        sys.exit(1)

    action = sys.argv[1]

    directory_name = sys.argv[2]

    root_directory = Path(__file__).parent / directory_name

    if not root_directory.is_dir():
        print(f"Error: {root_directory} is not a valid directory.")
        sys.exit(1)

    if action == "generate":
        PackageManager.add_init(root_directory)
    elif action == "clean":
        PackageManager.remove_init(root_directory)
    else:
        print("Usage: python manage_stubs.py {generate|clean}")
        sys.exit(1)


if __name__ == "__main__":
    main()
