import subprocess


def get_project_name():
    result = subprocess.run(
        ["python", "manage.py", "get_project_name"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()
