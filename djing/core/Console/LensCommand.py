from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Support.Str import Str


class LensCommand(GeneratorCommand):
    name = "djing:lens"
    description = "Create a new lens class"
    type = "Lens"

    def get_stub(self):
        console_path = Path(__file__).parent

        return self.resolve_stub_path("/stubs/lens.stub", console_path)

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
            "uri_key": Str.kebab(self.argument("name")),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing/Lenses"
