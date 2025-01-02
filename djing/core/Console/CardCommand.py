import os

from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Foundation.Console.Input.InputArgument import InputArgument
from Illuminate.Support.Str import Str


class CardCommand(GeneratorCommand):
    name = "djing:card"
    description = "Create a new custom card"
    type = "Card"
    component_directory = Path(os.getcwd()) / "djing_components"

    def handle(self):
        name = self.argument("name")

        pascal_name = Str.pascal(name)

        kebab_name = Str.kebab(name)

        asset_dir = self.component_directory / pascal_name

        os.makedirs(asset_dir / "src/js/components", exist_ok=True)

        os.makedirs(asset_dir / "src/css", exist_ok=True)

        self.install_asset_service_provider(asset_dir, kebab_name, pascal_name)

        self.install_asset_python(asset_dir, kebab_name, pascal_name)

        self.install_asset_package(asset_dir, kebab_name, pascal_name)

        self.install_vite_config(asset_dir, kebab_name, pascal_name)

        self.install_asset_js(asset_dir, kebab_name, pascal_name)

        self.install_asset_css(asset_dir, kebab_name, pascal_name)

        self.install_components(asset_dir, kebab_name, pascal_name)

        self.response(asset_dir, kebab_name, pascal_name)

    def response(self, asset_dir, kebab_name, pascal_name):
        if not self.silent:
            self.success(
                f"{self.type} [{asset_dir/pascal_name}.py] created successfully."
            )

            self.info(
                f"make sure to add CardServiceProvider to your config.app.providers list."
            )

            self.info(
                f"you can now cd into: {asset_dir} and run npm install && npm run dev"
            )

    def install_asset_service_provider(
        self, asset_dir: Path, kebab_name: str, pascal_name: str
    ):
        asset_stub_path = self.resolve_stub_path(
            "/stubs/card/CardServiceProvider.stub", Path(__file__).parent
        )

        asset_path = asset_dir / "CardServiceProvider.py"

        asset_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            asset_stub_path,
            asset_path,
            asset_stub_var,
        )

    def install_asset_python(self, asset_dir: Path, kebab_name: str, pascal_name: str):
        asset_stub_path = self.resolve_stub_path(
            "/stubs/card/Card.stub", Path(__file__).parent
        )

        asset_path = asset_dir / f"{pascal_name}.py"

        asset_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            asset_stub_path,
            asset_path,
            asset_stub_var,
        )

    def install_asset_package(self, asset_dir: Path, kebab_name: str, pascal_name: str):
        asset_stub_path = self.resolve_stub_path(
            "/stubs/card/package.stub", Path(__file__).parent
        )

        asset_path = asset_dir / "package.json"

        asset_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            asset_stub_path,
            asset_path,
            asset_stub_var,
        )

    def install_vite_config(self, asset_dir: Path, kebab_name: str, pascal_name: str):
        asset_stub_path = self.resolve_stub_path(
            "/stubs/card/vite.config.stub", Path(__file__).parent
        )

        asset_path = asset_dir / "vite.config.ts"

        asset_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            asset_stub_path,
            asset_path,
            asset_stub_var,
        )

    def install_asset_js(self, asset_dir: Path, kebab_name: str, pascal_name: str):
        asset_stub_path = self.resolve_stub_path(
            "/stubs/card/src/js/card.stub", Path(__file__).parent
        )

        asset_path = asset_dir / "src/js/card.js"

        asset_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            asset_stub_path,
            asset_path,
            asset_stub_var,
        )

    def install_asset_css(self, asset_dir: Path, kebab_name: str, pascal_name: str):
        asset_stub_path = self.resolve_stub_path(
            "/stubs/card/src/css/card.stub", Path(__file__).parent
        )

        asset_path = asset_dir / "src/css/card.css"

        asset_stub_var = {
            "kebab_name": kebab_name,
            "pascal_name": pascal_name,
        }

        self.generate_file_from_stub(
            asset_stub_path,
            asset_path,
            asset_stub_var,
        )

    def install_components(self, asset_dir: Path, kebab_name: str, pascal_name: str):
        for asset in ["Card"]:
            asset_stub_path = self.resolve_stub_path(
                f"/stubs/card/src/js/components/{asset}.stub", Path(__file__).parent
            )

            asset_path = asset_dir / f"src/js/components/{asset}.vue"

            asset_stub_var = {
                "kebab_name": kebab_name,
                "pascal_name": pascal_name,
            }

            self.generate_file_from_stub(
                asset_stub_path,
                asset_path,
                asset_stub_var,
            )

    def get_arguments(self):
        return [
            ["name", InputArgument.REQUIRED, f"The name of the {self.type}", None],
        ]
