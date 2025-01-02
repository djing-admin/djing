from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Foundation.Console.Input.InputOption import InputOption
from djing.core.Util import Util


class PolicyCommand(GeneratorCommand):
    name = "djing:policy"
    description = "Create a new authorization policy"
    type = "Policy"

    def get_options(self):
        return [
            [
                "model",
                "m",
                InputOption.VALUE_REQUIRED,
                "The model class being represented.",
                None,
            ],
        ]

    def get_stub(self):
        console_path = Path(__file__).parent

        return self.resolve_stub_path("/stubs/policy.stub", console_path)

    def get_stub_vars(self):
        name = self.argument("name")

        model = self.option("model")

        model_path, model_name = Util.validate_model_path(model)

        return {
            "name": name,
            "model_path": model_path,
            "model_name": model_name,
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Policies"
