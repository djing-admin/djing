from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Support.Str import Str


class RuleCommand(GeneratorCommand):
    name = "djing:rule"
    description = "Create a new validation rule"
    type = "Rule"

    def get_stub(self):
        console_path = Path(__file__).parent

        return self.resolve_stub_path("/stubs/rule.stub", console_path)

    def get_stub_vars(self):
        name = self.argument("name")

        pascal_name = Str.pascal(name)

        return {
            "name": pascal_name,
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Rules"
