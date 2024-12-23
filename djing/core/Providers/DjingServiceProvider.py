from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.ServiceProvider import ServiceProvider
from djing.core.Console.ActionCommand import ActionCommand
from djing.core.Console.BaseResourceCommand import BaseResourceCommand
from djing.core.Console.CardCommand import CardCommand
from djing.core.Console.DashboardCommand import DashboardCommand
from djing.core.Console.DjingServiceProviderCommand import DjingServiceProviderCommand
from djing.core.Console.FieldCommand import FieldCommand
from djing.core.Console.FilterCommand import FilterCommand
from djing.core.Console.InstallCommand import InstallCommand
from djing.core.Console.LensCommand import LensCommand
from djing.core.Console.PartitionMetricCommand import PartitionMetricCommand
from djing.core.Console.ProgressMetricCommand import ProgressMetricCommand
from djing.core.Console.PublishCommand import PublishCommand
from djing.core.Console.ResourceCommand import ResourceCommand
from djing.core.Console.TableMetricCommand import TableMetricCommand
from djing.core.Console.ValueMetricCommand import ValueMetricCommand


class DjingServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.app = app

    def register(self):
        self.commands(
            [
                InstallCommand,
                PublishCommand,
                DjingServiceProviderCommand,
                BaseResourceCommand,
                ResourceCommand,
                DashboardCommand,
                ActionCommand,
                FilterCommand,
                LensCommand,
                ValueMetricCommand,
                ProgressMetricCommand,
                PartitionMetricCommand,
                TableMetricCommand,
                FieldCommand,
                CardCommand,
            ]
        )

    def boot(self):
        pass
