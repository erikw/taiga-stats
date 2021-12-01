try:
    from importlib import metadata
except ImportError:  # for Python<3.8. Reference: https://stackoverflow.com/a/59734959/265508
    import importlib_metadata as metadata

# Read version from pyproject.toml. Might not be correct in dev enviorment, but will be when distributed.
# Reference: https://stackoverflow.com/a/67097076/265508
__version__ = metadata.version("taiga-stats")
