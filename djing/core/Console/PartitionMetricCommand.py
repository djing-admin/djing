from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand


class PartitionMetricCommand(GeneratorCommand):
    name = "djing:partition"
    description = "Create a new metric (partition) class"
    type = "Metric"

    def get_stub(self):
        return self.resolve_stub_path(f"/stubs/partition.stub", Path(__file__).parent)

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing/Metrics"
