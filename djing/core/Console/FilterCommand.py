from pathlib import Path
from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from Illuminate.Foundation.Console.Input.InputOption import InputOption


class FilterCommand(GeneratorCommand):
    name = "djing:filter"
    description = "Create a new filter class"
    type = "Filter"

    def get_options(self):
        return [
            [
                "boolean",
                None,
                InputOption.VALUE_OPTIONAL,
                "Indicates if the generated filter should be a boolean filter",
                None,
            ],
            [
                "date",
                None,
                InputOption.VALUE_OPTIONAL,
                "Indicates if the generated filter should be a date filter",
                None,
            ],
        ]

    def get_stub(self):
        if self.option("boolean"):
            return self.resolve_stub_path(
                "/stubs/boolean-filter.stub", Path(__file__).parent
            )

        if self.option("date"):
            return self.resolve_stub_path(
                "/stubs/date-filter.stub", Path(__file__).parent
            )

        return self.resolve_stub_path("/stubs/filter.stub", Path(__file__).parent)

    def get_stub_vars(self):
        return {
            "name": self.argument("name"),
        }

    def get_default_namespace(self, root_namespace: Path):
        return root_namespace / "Djing/Filters"
