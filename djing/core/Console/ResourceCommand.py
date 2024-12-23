from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Foundation.Console.Input.InputOption import InputOption


class ResourceCommand(GeneratorCommand):
    name = "djing:resource"
    description = "Create a new resource class"
    type = "Resource"

    def handle(self):
        self.commander.call_silent("djing:base-resource", {"name": "Resource"})

        return super().handle()

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

        if self.get_name_input() == "User":
            return self.resolve_stub_path("/stubs/user-resource.stub", console_path)
        else:
            return self.resolve_stub_path("/stubs/resource.stub", console_path)

    def get_stub_vars(self):
        name = self.argument("name")

        model = self.option("model")

        model_namespace = f"'{model}.models.{name}'"

        return {
            "name": name,
            "model_namespace": model_namespace,
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing"
