# Constants used in the Python CLI application

# Importing the package to access the version and repository URL
import pkg_resources

# Command name for the CLI
command_name = 'micro-agent'

# Project name
project_name = 'Micro Agent'

# Repository URL extracted from the package information
repo_url = pkg_resources.require("micro-agent")[0].project_url
