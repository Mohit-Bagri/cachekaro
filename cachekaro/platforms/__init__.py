"""
Platform-specific implementations for CacheKaro.

Provides abstraction layer for different operating systems.
"""

from cachekaro.platforms.detector import get_platform, get_platform_name
from cachekaro.platforms.base import PlatformBase, CachePath, DiskUsage

__all__ = [
    "get_platform",
    "get_platform_name",
    "PlatformBase",
    "CachePath",
    "DiskUsage",
]
