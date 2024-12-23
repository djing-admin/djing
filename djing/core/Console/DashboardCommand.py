from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand


class DashboardCommand(GeneratorCommand):
    name = "djing:dashboard"
    description = "Create a new dashboard class"
    type = "Dashboard"

    def get_stub(self):
        console_path = Path(__file__).parent

        if self.get_name_input() == "Main":
            return self.resolve_stub_path("/stubs/main-dashboard.stub", console_path)
        else:
            return self.resolve_stub_path("/stubs/dashboard.stub", console_path)

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing/Dashboards"
