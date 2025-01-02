from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand


class PublishCommand(GeneratorCommand):
    signature = "djing:publish {name}"
    description = "Publish assets"
    type = "Asset"
    hidden = True

    def get_stub(self):
        console_path = Path(__file__).parent

        name = self.get_name_input()

        return self.resolve_stub_path(f"/stubs/config/{name}.stub", console_path)

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
        }

    def get_default_namespace(self, root_namespace: Path):
        return self.application.base_path() / "config"
