#!/usr/bin/env bash
# Devcontainer postCreateCommand.
# Install dependencies for running this project in GitHub Codespaces.

set -eux

# For project.
#pip install poetry # NOPE no longer needed as of adding poetry via devcontainer extra feature image.
poetry install --with docs
