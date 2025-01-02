from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing
from djing.core.Menu.MenuGroup import MenuGroup
from djing.core.Menu.MenuItem import MenuItem
from djing.core.Menu.MenuSection import MenuSection
from djing.core.Tool import Tool


class ResourceManager(Tool):
    def menu(self, request: DjingRequest):
        grouped_resources = Djing.grouped_resources_for_navigation(request)

        if grouped_resources.count() > 1:
            resources = self.grouped_menu(grouped_resources, request)
        else:
            resources = self.ungrouped_menu(grouped_resources, request)

        menu_section = MenuSection.make("Resources", resources)

        if resources.count() > 1:
            menu_section.collapsable()

        return menu_section

    def grouped_menu(self, grouped_resources, request: DjingRequest):
        return grouped_resources.map(
            lambda group, key: MenuGroup.make(
                key,
                group.map(
                    lambda resource_class: self.__resolve_resource(
                        resource_class, request
                    )
                ),
            ).collapsable()
        )

    def ungrouped_menu(self, grouped_resources: Collection, request: DjingRequest):
        return grouped_resources.flatten().map(
            lambda resource_class: self.__resolve_resource(resource_class, request)
        )

    def __resolve_resource(self, resource_class, request: DjingRequest):
        if hasattr(resource_class, "menu"):
            resource = resource_class()
            return resource.menu(request)

        return MenuItem.resource(resource_class)
