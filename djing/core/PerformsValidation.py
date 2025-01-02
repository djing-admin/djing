from typing import TYPE_CHECKING
from Illuminate.Collections.helpers import collect
from Illuminate.Support.Facades.Validator import Validator
from Illuminate.Validation.ValidationResponse import ValidationResponse
from djing.core.Http.Requests.DjingRequest import DjingRequest

if TYPE_CHECKING:
    from djing.core.Resource import Resource


class PerformsValidation:
    @classmethod
    def validate_for_creation(cls, request: DjingRequest) -> ValidationResponse:
        validator = cls.validator_for_creation(request)

        response: ValidationResponse = validator.validate()

        return response

    @classmethod
    def validator_for_creation(cls, request: DjingRequest) -> Validator:
        data = request.all()

        rules = cls.rules_for_creation(request)

        validator = Validator.make(data, rules)

        return validator

    @classmethod
    def rules_for_creation(cls, request: DjingRequest):
        resource: Resource = cls.new_resource()

        return cls.format_rules(
            request,
            (
                resource.creation_fields(request)
                .without_readonly(request)
                .without_unfillable()
                .map_with_keys(lambda field: field.get_creation_rules(request))
                .all()
            ),
        )

    @classmethod
    def validate_for_update(cls, request: DjingRequest, resource: "Resource"):
        return cls.validator_for_update(request, resource).validate()

    @classmethod
    def validator_for_update(
        cls, request: DjingRequest, resource: "Resource"
    ) -> Validator:
        validator = Validator.make(
            request.all(), cls.rules_for_update(request, resource)
        )

        return validator

    @classmethod
    def rules_for_update(cls, request: DjingRequest, resource: "Resource"):
        return cls.format_rules(
            request,
            (
                resource.update_fields(request)
                .without_readonly(request)
                .without_unfillable()
                .map_with_keys(lambda field: field.get_update_rules(request))
                .all()
            ),
        )

    @classmethod
    def format_rules(cls, request: DjingRequest, rules={}):
        try:
            rules = collect(rules)

            parsed_rules = {}

            def get_rule(item):
                if isinstance(item, str) and "|" in item:
                    return item.split("|")
                else:
                    return [item]

            for key, items in rules:
                parsed_rules[key] = (
                    collect([get_rule(item) for item in items])
                    .flatten()
                    .json_serialize()
                )

            return parsed_rules
        except Exception as e:
            print(e)
