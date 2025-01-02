from Illuminate.Foundation.Console.Command import Command


class InstallCommand(Command):
    name = "djing:install"
    description = "Install assets"

    def handle(self):
        self.install_djing_service_provider()

        self.publish_config()

        self.publish_dashboard()

        self.publish_resource()

        self.response()

    def response(self):
        self.info("All set.")
        self.new_line()
        self.success("Djing scaffolding installed successfully.")
        self.new_line()

    def install_djing_service_provider(self):
        self.info("publishing service provider.")
        self.commander.call_silent(
            "djing:service-provider", {"name": "DjingServiceProvider"}
        )
        self.new_line()

    def publish_config(self):
        self.info("publishing app.")
        self.commander.call_silent("djing:publish", {"name": "app"})
        self.new_line()

        self.info("publishing djing.")
        self.commander.call_silent("djing:publish", {"name": "djing"})
        self.new_line()

    def publish_dashboard(self):
        self.info("publishing dashboard.")
        self.commander.call_silent("djing:dashboard", {"name": "Main"})
        self.new_line()

    def publish_resource(self):
        self.info("publishing resource.")
        self.commander.call_silent(
            "djing:resource", {"name": "User", "--model": "User"}
        )
        self.new_line()
