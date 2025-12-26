"""
Configuration system for CacheKaro.
"""

from cachekaro.config.default import Config, load_config, save_config, get_config_path

__all__ = [
    "Config",
    "load_config",
    "save_config",
    "get_config_path",
]
