from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand


class BaseResourceCommand(GeneratorCommand):
    name = "djing:base-resource"
    description = "Create a new resource class"
    type = "Resource"
    hidden = True

    def handle(self):
        return super().handle()

    def get_stub(self):
        return self.resolve_stub_path(
            "/stubs/base-resource.stub", Path(__file__).parent
        )

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing"
