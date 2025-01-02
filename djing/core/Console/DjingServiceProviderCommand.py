from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand


class DjingServiceProviderCommand(GeneratorCommand):
    name = "djing:service-provider"
    description = "Create a new service provider class"
    type = "ServiceProvider"
    hidden = True

    def get_stub(self):
        return self.resolve_stub_path(
            "/stubs/DjingServiceProvider.stub", Path(__file__).parent
        )

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
            "base_directory": str(self.application.base_path()),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Providers"
