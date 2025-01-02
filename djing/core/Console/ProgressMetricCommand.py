from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Support.Str import Str


class ProgressMetricCommand(GeneratorCommand):
    name = "djing:progress"
    description = "Create a new metric (progress) class"
    type = "Metric"

    def get_stub(self):
        return self.resolve_stub_path(f"/stubs/progress.stub", Path(__file__).parent)

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
            "uri_key": Str.kebab(self.argument("name")),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing/Metrics"
