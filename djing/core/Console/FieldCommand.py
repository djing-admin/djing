import os

from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Foundation.Console.Input.InputArgument import InputArgument
from Illuminate.Support.Str import Str


class FieldCommand(GeneratorCommand):
    name = "djing:field"
    description = "Create a new custom field"
    type = "Field"
    component_directory = Path(os.getcwd()) / "djing_components"

    def handle(self):
        name = self.argument("name")

        pascal_name = Str.pascal(name)

        kebab_name = Str.kebab(name)

        field_dir = self.component_directory / pascal_name

        os.makedirs(field_dir / "src/js/components", exist_ok=True)

        os.makedirs(field_dir / "src/css", exist_ok=True)

        self.install_field_service_provider(field_dir, kebab_name, pascal_name)

        self.install_field_python(field_dir, kebab_name, pascal_name)

        self.install_package(field_dir, kebab_name, pascal_name)

        self.install_vite_config(field_dir, kebab_name, pascal_name)

        self.install_field_js(field_dir, kebab_name, pascal_name)

        self.install_field_css(field_dir, kebab_name, pascal_name)

        self.install_components(field_dir, kebab_name, pascal_name)

        self.response(field_dir, kebab_name, pascal_name)

    def response(self, field_dir, kebab_name, pascal_name):
        if not self.silent:
            self.success(
                f"{self.type} [{field_dir/pascal_name}.py] created successfully."
            )

            self.info(
                f"make sure to add FieldServiceProvider to your config.app.providers list."
            )

            self.info(
                f"you can now cd into: {field_dir} and run npm install && npm run dev"
            )

    def install_field_service_provider(
        self, field_dir: Path, kebab_name: str, pascal_name: str
    ):
        field_stub_path = self.resolve_stub_path(
            "/stubs/field/FieldServiceProvider.stub", Path(__file__).parent
        )

        field_path = field_dir / "FieldServiceProvider.py"

        field_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            field_stub_path,
            field_path,
            field_stub_var,
        )

    def install_field_python(self, field_dir: Path, kebab_name: str, pascal_name: str):
        field_stub_path = self.resolve_stub_path(
            "/stubs/field/Field.stub", Path(__file__).parent
        )

        field_path = field_dir / f"{pascal_name}.py"

        field_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            field_stub_path,
            field_path,
            field_stub_var,
        )

    def install_package(self, field_dir: Path, kebab_name: str, pascal_name: str):
        field_stub_path = self.resolve_stub_path(
            "/stubs/field/package.stub", Path(__file__).parent
        )

        field_path = field_dir / "package.json"

        field_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            field_stub_path,
            field_path,
            field_stub_var,
        )

    def install_vite_config(self, field_dir: Path, kebab_name: str, pascal_name: str):
        field_stub_path = self.resolve_stub_path(
            "/stubs/field/vite.config.stub", Path(__file__).parent
        )

        field_path = field_dir / "vite.config.ts"

        field_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            field_stub_path,
            field_path,
            field_stub_var,
        )

    def install_field_js(self, field_dir: Path, kebab_name: str, pascal_name: str):
        field_stub_path = self.resolve_stub_path(
            "/stubs/field/src/js/field.stub", Path(__file__).parent
        )

        field_path = field_dir / "src/js/field.js"

        field_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            field_stub_path,
            field_path,
            field_stub_var,
        )

    def install_field_css(self, field_dir: Path, kebab_name: str, pascal_name: str):
        field_stub_path = self.resolve_stub_path(
            "/stubs/field/src/css/field.stub", Path(__file__).parent
        )

        field_path = field_dir / "src/css/field.css"

        field_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            field_stub_path,
            field_path,
            field_stub_var,
        )

    def install_components(self, field_dir: Path, kebab_name: str, pascal_name: str):
        for field in ["IndexField", "DetailField", "FormField"]:
            field_stub_path = self.resolve_stub_path(
                f"/stubs/field/src/js/components/{field}.stub", Path(__file__).parent
            )

            field_path = field_dir / f"src/js/components/{field}.vue"

            field_stub_var = {
                "kebab_name": kebab_name,
                "pascal_name": pascal_name,
            }

            self.generate_file_from_stub(
                field_stub_path,
                field_path,
                field_stub_var,
            )

    def get_arguments(self):
        return [
            ["name", InputArgument.REQUIRED, f"The name of the {self.type}", None],
        ]
