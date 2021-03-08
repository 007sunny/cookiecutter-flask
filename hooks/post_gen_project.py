"""Post gen hook to ensure that the generated project
has only one package management, either pipenv or pip."""
import logging
import os
import shutil
import sys

_logger = logging.getLogger()


def clean_extra_package_management_files():
    """Removes either requirements files and folder or the Pipfile."""
    try:
        shutil.copy(".env.example", ".env")
    except OSError as e:
        _logger.warning("While attempting to remove file(s) an error occurred")
        _logger.warning(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    clean_extra_package_management_files()
