import os

from djing.core.Http.Middlewares.Authenticate import Authenticate
from djing.core.Http.Middlewares.Authorize import Authorize
from djing.core.Http.Middlewares.BootTools import BootTools
from djing.core.Http.Middlewares.DispatchServingDjingEvent import (
    DispatchServingDjingEvent,
)
from djing.core.Http.Middlewares.HandleInertiaRequests import HandleInertiaRequests

djing = {
    # The license key required to activate the Djing Admin application.
    # Pulled from the environment variable DJING_LICENSE_KEY.
    # Example: export DJING_LICENSE_KEY="your-license-key"
    #
    "license_key": os.getenv("DJING_LICENSE_KEY"),
    #
    # The display name of your Djing Admin application.
    # Used in branding and display areas. Defaults to "Djing Admin".
    # Pulled from the environment variable DJING_APP_NAME, if set.
    #
    "app_name": os.getenv("DJING_APP_NAME", "Djing Admin"),
    #
    # The default name of your Django Project.
    # Used in calling command line apps. Defaults to "myproject".
    # Pulled from os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings').
    #
    "project_name": os.getenv("DJANGO_PROJECT_NAME", "myproject"),
    #
    # The application path or slug for the Djing Admin platform.
    # Defaults to "Djing Admin". Can be overridden by setting the DJING_APP_NAME env variable.
    #
    "path": os.getenv("DJING_PATH", "/djing-admin"),
    #
    # The default currency used throughout the application. Default is "USD".
    #
    "currency": os.getenv("DJING_CURRENCY", "USD"),
    #
    # You can choose between simple, load-more and links.
    #
    "pagination": os.getenv("DJING_PAGINATION", "simple"),
    #
    # The 'brand' section defines the visual identity and styling for the Djing Admin platform.
    # It contains assets like the logo and a set of color definitions to ensure consistent branding
    # across the user interface.
    #
    # The path or URL to the logo asset for branding within the Djing Admin platform.
    "brand_logo": "logo.png",
    #
    # This is background and text color styling for your brand.
    #
    "brand_colors": {
        # The branding color with 50% opacity, used for lighter UI elements.
        "400": "24, 182, 155, 0.5",
        # The primary branding color, used for major UI elements.
        "500": "24, 182, 155",
        # A darker shade of the primary branding color with 75% opacity.
        "600": "24, 182, 155, 0.75",
    },
    #
    # This tells djing to authenticate using given username field.
    # change it to 'email' if you are using email and password to authenticate.
    #
    "auth": {
        "username_field": "username",
    },
    #
    # This is a base middleware that will run on each request.
    #
    "middleware": [
        HandleInertiaRequests,
        DispatchServingDjingEvent,
        BootTools,
    ],
    #
    # This is a api middleware that will run on each request.
    #
    "api_middleware": [
        "djing",
        Authenticate,
        Authorize,
    ],
}
