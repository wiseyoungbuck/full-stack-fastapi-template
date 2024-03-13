#!/usr/bin/env bash

set -e  # Exit immediately if a command exits with a non-zero status.
set -x  # Print commands and their arguments as they are executed.

coverage run --source=app -m pytest  # Run pytest under coverage tracking, targeting the 'app' directory.
coverage report --show-missing  # Generate a coverage report, showing lines that are missing coverage.
coverage html --title "${@-coverage}"  # Generate an HTML coverage report with a custom title, defaulting to 'coverage' if no arguments are provided.
