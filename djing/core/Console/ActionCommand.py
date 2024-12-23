from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Foundation.Console.Input.InputOption import InputOption


class ActionCommand(GeneratorCommand):
    name = "djing:action"
    description = "Create a new action class"
    type = "Action"

    def get_options(self):
        return [
            [
                "destructive",
                None,
                InputOption.VALUE_OPTIONAL,
                "Indicate that the action deletes / destroys resources",
                None,
            ],
        ]

    def get_stub(self):
        console_path = Path(__file__).parent

        return (
            self.resolve_stub_path("/stubs/destructive-action.stub", console_path)
            if self.option("destructive") == True
            else self.resolve_stub_path("/stubs/action.stub", console_path)
        )

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing/Actions"
