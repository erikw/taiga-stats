import importlib.metadata

# Read version from pyproject.toml. Might not be correct in dev enviorment, but will be when distributed.
# Reference: https://stackoverflow.com/a/67097076/265508
__version__ = importlib.metadata.version("taiga-stats")
