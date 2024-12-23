from typing import Self
from Illuminate.Collections.Collection import Collection
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from djing.core.Http.Requests.DjingRequest import DjingRequest


class MenuCollection(Collection):
    def authorize(self, request: DjingRequest) -> Self:
        return self.reject(
            lambda menu: hasattr(menu, "authorized_to_see")
            and not menu.authorized_to_see(request)
        ).values()

    def without_empty_items(self):
        def transform_menu_collection(menu):
            if isinstance(menu, JsonSerializable):
                payload = menu.json_serialize()

                from djing.core.Menu.MenuGroup import MenuGroup
                from djing.core.Menu.MenuList import MenuList

                if isinstance(menu, (MenuGroup, MenuList)) and len(menu._items) == 0:
                    return None

                return payload

            return menu

        return self.transform(transform_menu_collection).filter().values()
