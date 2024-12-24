# Djing: A Laravel Nova Inspired Django Admin Panel

Djing is a powerful and elegant Django admin panel inspired by Laravel Nova. It brings the flexibility, functionality, and modern aesthetics of Laravel Nova to Django developers, making it a breeze to manage your Django projects. With support for actions, filters, metrics, lenses, and custom components, Djing aims to simplify and enhance your administrative workflows.

## Features

- **Actions**: Perform bulk operations on resources with ease.
- **Filters**: Customize the data displayed in your views using advanced filters.
- **Metrics & Cards**: Gain insights into your data with dynamic, customizable metrics and cards.
- **Lenses**: Create focused views to analyze specific subsets of your data.
- **Resources**: Manage your models and resources effortlessly.
- **Custom Fields**: Add personalized fields to meet your application's unique needs.
- **Custom Cards**: Extend the interface with custom-designed cards.
- **Custom Tools**: Extend the interface with custom-designed tools.
- **Beautiful UI**: Enjoy a clean, modern, and responsive user interface.

## Screenshots

Below is an example of the Djing admin panel interface:

<table>
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/djing-admin/djing/refs/heads/main/screenshots/login.png" alt="Djing Admin - Login" width="300"/>
      <p align="center">Login</p>
    </td>
    <td>
      <img src="https://raw.githubusercontent.com/djing-admin/djing/refs/heads/main/screenshots/resources.png" alt="Djing Admin - Resources" width="300"/>
      <p align="center">Resources</p>
    </td>
    <td>
      <img src="https://raw.githubusercontent.com/djing-admin/djing/refs/heads/main/screenshots/resource-detail.png" alt="Djing Admin - Resource Detail" width="300"/>
      <p align="center">Resource Detail</p>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/djing-admin/djing/refs/heads/main/screenshots/create-resource.png" alt="Djing Admin - Create Resource" width="300"/>
      <p align="center">Create Resource</p>
    </td>
    <td>
      <img src="https://raw.githubusercontent.com/djing-admin/djing/refs/heads/main/screenshots/update-resource.png" alt="Djing Admin - Update Resource" width="300"/>
      <p align="center">Update Resource</p>
    </td>
    <td></td>
  </tr>
</table>

_The above screenshot showcases the clean and modern UI of the Djing admin panel._

## Installation

To install Djing, use pip:

```bash
pip install djing
```

Add `djing` to your `INSTALLED_APPS` in your Django project:

```python
INSTALLED_APPS = [
    ...,
    'djing',
]
```

Make sure to set the `STATIC_ROOT` & `STATIC_URL` in your `settings.py` file before collecting static files:

```python
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"
```

Also you need to add `STORAGES`, `MEDIA_ROOT` & `MEDIA_URL` in your `settings.py`.

```python
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": BASE_DIR / "media",  # Replace with your media directory path
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"
```

Run the following command to collect static files:

```bash
python manage.py collectstatic
```

Run the Djing installation command:

```bash
python manage.py djing:install
```

Ensure that the `django_project_name` is set in the `.env` file. If not specified, it defaults to `myproject`:

```env
DJANGO_PROJECT_NAME=<your-project-name>
DJING_LICENSE_KEY=<your-license-key>
```

### Commands

Djing provides a set of commands to help you work efficiently:

```bash
commander list
```

```plaintext
PyJinx Framework 0.2.3

Usage:
    Commands [options] [arguments]

Options:
    -h, --help                 Display help for the given command. When no command is given display help for the list command
    -q, --quiet                Do not output any message
    -v, --version              Display this application version

Available Commands:
        list                       List all commands
    djing
        djing:install              Install assets
        djing:resource             Create a new resource class
        djing:dashboard            Create a new dashboard class
        djing:action               Create a new action class
        djing:filter               Create a new filter class
        djing:lens                 Create a new lens class
        djing:value                Create a new metric (single value) class
        djing:progress             Create a new metric (progress) class
        djing:partition            Create a new metric (partition) class
        djing:table                Create a new metric (table) class
        djing:field                Create a new custom field
        djing:card                 Create a new custom card
        djing:tool                 Create a new custom tool
        djing:resource-tool        Create a new custom resource tool
```

## Customization

Djing is highly extensible. You can create your own cards, fields, and components to match your project's specific requirements. Refer to the documentation for details on creating custom components.

## Documentation

Comprehensive documentation is available at [Djing Documentation](https://djing.vercel.app/docs) to help you get started and explore advanced features.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements. For major changes, open an issue to discuss your ideas first.

## License

Djing is open-source software licensed under the [MIT license](LICENSE) **only for development purposes**.

For production use, a valid license key is required. To obtain a production license, visit the [Djing Licensing Page](https://djing.vercel.app/licenses).

## Support

For questions, issues, or feature requests, please create an issue on the [GitHub repository](https://github.com/djing-admin/djing).

## Author

- **Krunal Dodiya**
- Email: [kunal.dodiya1@gmail.com](mailto:kunal.dodiya1@gmail.com)
