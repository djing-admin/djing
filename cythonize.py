import os

from typing import List
from setuptools import Extension
from setuptools import setup
from Cython.Build import cythonize


def get_ext(package: str, package_path: str, file: str) -> Extension:
    name = f"{package}.{file}".replace(".py", "")

    file_path = os.path.join(package_path, file)

    return Extension(name=name, sources=[file_path], language="c++")


def find_extensions(
    base_package: str,
    base_path: str,
    included_directories: List[str] = [],
    excluded_directories: List[str] = [],
) -> List[Extension]:
    ext_modules: List[Extension] = []

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [
            d
            for d in dirs
            if os.path.join(root, d) not in excluded_directories
            and not d.startswith(".")
        ]

        if all(
            os.path.commonpath([os.path.join(root), included_path]) != included_path
            for included_path in included_directories
        ):
            continue

        rel_path = os.path.relpath(root, base_path)

        if rel_path == ".":
            package = base_package
        else:
            package = f"{base_package}.{rel_path.replace(os.path.sep, '.')}"

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                ext_modules.append(get_ext(package, root, file))

    return ext_modules


base_package = "djing"

base_path = os.path.join(os.path.dirname(__file__), base_package)

included_directories: list = [
    os.path.join(base_path, "core", "Foundation"),
]

excluded_directories: list = []

ext_modules = find_extensions(
    base_package, base_path, included_directories, excluded_directories
)

setup(
    name=base_package,
    ext_modules=cythonize(ext_modules, language_level=3),
)
