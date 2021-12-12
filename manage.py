#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import configparser
import os
import sys


def process_env_line(env_line):
    part = env_line.partition("=")
    key = part[0].strip()
    value = part[2].strip()
    # Replace environment variables in value. for instance:
    # TEST_DIR={USER}/repo_test_dir.
    value = value.format(**os.environ)
    # use D: as a way to designate a default value
    # that will only override env variables if they
    # do not exist already
    dkey = key.split("D:")
    default_val = False
    if len(dkey) == 2:
        key = dkey[1]
        default_val = True
    if not default_val or key not in os.environ:
        os.environ[key] = value


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "litreview.settings")
    try:
        index = sys.argv.index("test")
    except ValueError:
        pass
    else:
        # Load pytest env variables if running tests
        if sys.argv[index - 1].endswith("manage.py"):
            config = configparser.ConfigParser()
            with open("pytest.ini", "r") as pytest_file:
                config.read(["pytest.ini"])
            env_lines = [item for item in config["pytest"]["env"].split("\n") if item]
            for env_line in env_lines:
                process_env_line(env_line)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
