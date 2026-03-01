from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("fast-pmtiles")
except PackageNotFoundError:
    __version__ = "uninstalled"
