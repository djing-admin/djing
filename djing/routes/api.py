from Illuminate.Support.Facades.Route import Route
from djing.core.Http.Controllers.ActionController import ActionController
from djing.core.Http.Controllers.CardController import CardController
from djing.core.Http.Controllers.CreationFieldController import CreationFieldController
from djing.core.Http.Controllers.DashboardController import DashboardController
from djing.core.Http.Controllers.DashboardMetricController import (
    DashboardMetricController,
)
from djing.core.Http.Controllers.DetailMetricController import DetailMetricController
from djing.core.Http.Controllers.FieldDestroyController import FieldDestroyController
from djing.core.Http.Controllers.FieldDownloadController import FieldDownloadController
from djing.core.Http.Controllers.FilterController import FilterController
from djing.core.Http.Controllers.LensController import LensController
from djing.core.Http.Controllers.MetricController import MetricController
from djing.core.Http.Controllers.ResourceDestroyController import (
    ResourceDestroyController,
)
from djing.core.Http.Controllers.ResourceIndexController import ResourceIndexController
from djing.core.Http.Controllers.ResourceShowController import ResourceShowController
from djing.core.Http.Controllers.ResourceStoreController import ResourceStoreController
from djing.core.Http.Controllers.UpdateFieldController import UpdateFieldController
from djing.core.Http.Controllers.ResourceUpdateController import (
    ResourceUpdateController,
)

# Dashboards
Route.get("dashboards/:name", DashboardController)

# Actions
Route.get(":resource/actions", [ActionController, "index"])
Route.post(":resource/actions", [ActionController, "store"])

# Filters
Route.get(":resource/filters", FilterController)

# Lenses
Route.get(":resource/lenses", [LensController, "index"])

# Cards / Metrics
Route.get("metrics/:metric", DashboardMetricController)
Route.get(":resource/metrics/:metric", [MetricController, "show"])
Route.get(":resource/:resource_id/metrics/:metric", DetailMetricController)
Route.get(":resource/cards", CardController)

# Resources
Route.get(":resource", ResourceIndexController)
Route.get(":resource/creation-fields", CreationFieldController)
Route.get(":resource/:resource_id/update-fields", UpdateFieldController)
Route.get(":resource/:resource_id/download/:field", FieldDownloadController)
Route.delete(":resource/:resource_id/delete/:field", FieldDestroyController)
Route.put(":resource/:resource_id", ResourceUpdateController)
Route.get(":resource/:resource_id", ResourceShowController)
Route.post(":resource", ResourceStoreController)
Route.delete(":resource", ResourceDestroyController)
