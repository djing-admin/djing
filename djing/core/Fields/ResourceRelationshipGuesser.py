import importlib
from Illuminate.Support.Str import Str


class ResourceRelationshipGuesser:
    @classmethod
    def guess_resource(cls, name: str):
        try:
            singular = Str.singular(name)

            model_module = importlib.import_module(f"djing_admin.app.Djing.{singular}")

            resource = getattr(model_module, singular)

            return resource
        except (ModuleNotFoundError, ImportError):
            raise Exception("Invalid Django Model", name)
