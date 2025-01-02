from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from djing.djing_application import djing_application


def handle_command():
    try:
        application = djing_application()

        application.handle_command(ArgvInput(), False)
    except Exception as e:
        exit(e)
