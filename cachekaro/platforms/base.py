"""
Base platform class defining the interface for platform-specific implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class RiskLevel(Enum):
    """Risk level for cleaning a cache path."""
    SAFE = "safe"           # 100% safe to clean, no data loss
    MODERATE = "moderate"   # Generally safe, may require re-login
    CAUTION = "caution"     # May affect app behavior, use with care


class Category(Enum):
    """Categories for cache paths."""
    USER_CACHE = "user_cache"
    SYSTEM_CACHE = "system_cache"
    BROWSER = "browser"
    DEVELOPMENT = "development"
    LOGS = "logs"
    TRASH = "trash"
    DOWNLOADS = "downloads"
    APPLICATION = "application"
    CONTAINER = "container"
    CUSTOM = "custom"


@dataclass
class CachePath:
    """Represents a cache path to scan/clean."""
    path: Path
    name: str
    category: Category
    description: str
    risk_level: RiskLevel = RiskLevel.SAFE
    clean_contents_only: bool = True  # If True, clean contents but keep directory
    requires_admin: bool = False
    app_specific: bool = False
    app_name: str | None = None

    def exists(self) -> bool:
        """Check if the path exists."""
        return self.path.exists()

    def is_accessible(self) -> bool:
        """Check if the path is readable."""
        try:
            if self.path.is_dir():
                list(self.path.iterdir())
            return True
        except (PermissionError, OSError):
            return False


@dataclass
class DiskUsage:
    """Disk usage information."""
    total_bytes: int
    used_bytes: int
    free_bytes: int
    mount_point: str = "/"

    @property
    def used_percent(self) -> float:
        """Calculate percentage of disk used."""
        if self.total_bytes == 0:
            return 0.0
        return (self.used_bytes / self.total_bytes) * 100

    @property
    def free_percent(self) -> float:
        """Calculate percentage of disk free."""
        return 100.0 - self.used_percent


@dataclass
class PlatformInfo:
    """Information about the current platform."""
    name: str
    version: str
    architecture: str
    hostname: str
    username: str
    home_dir: Path
    temp_dir: Path


class PlatformBase(ABC):
    """
    Abstract base class for platform-specific implementations.

    Each platform (macOS, Linux, Windows) must implement this interface
    to provide cache paths and system operations specific to that OS.
    """

    def __init__(self) -> None:
        self._cache_paths: list[CachePath] = []
        self._platform_info: PlatformInfo | None = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the platform name (e.g., 'macOS', 'Linux', 'Windows')."""
        pass

    @abstractmethod
    def get_platform_info(self) -> PlatformInfo:
        """Get detailed platform information."""
        pass

    @abstractmethod
    def get_home_dir(self) -> Path:
        """Get the user's home directory."""
        pass

    @abstractmethod
    def get_temp_dir(self) -> Path:
        """Get the system temporary directory."""
        pass

    @abstractmethod
    def get_cache_paths(self) -> list[CachePath]:
        """
        Get all cache paths for this platform.

        Returns:
            List of CachePath objects representing scannable locations.
        """
        pass

    @abstractmethod
    def get_trash_path(self) -> Path | None:
        """Get the path to the user's trash/recycle bin."""
        pass

    @abstractmethod
    def get_disk_usage(self, path: str = "/") -> DiskUsage:
        """
        Get disk usage for the specified mount point.

        Args:
            path: Path to check (default: root)

        Returns:
            DiskUsage object with space information.
        """
        pass

    @abstractmethod
    def flush_dns_cache(self) -> tuple[bool, str]:
        """
        Flush the DNS cache.

        Returns:
            Tuple of (success, message)
        """
        pass

    @abstractmethod
    def is_admin(self) -> bool:
        """Check if running with administrator/root privileges."""
        pass

    @abstractmethod
    def get_config_dir(self) -> Path:
        """Get the directory for storing configuration files."""
        pass

    def get_paths_by_category(self, category: Category) -> list[CachePath]:
        """Get cache paths filtered by category."""
        return [p for p in self.get_cache_paths() if p.category == category]

    def get_paths_by_risk(self, max_risk: RiskLevel) -> list[CachePath]:
        """Get cache paths filtered by maximum risk level."""
        risk_order = [RiskLevel.SAFE, RiskLevel.MODERATE, RiskLevel.CAUTION]
        max_index = risk_order.index(max_risk)
        return [
            p for p in self.get_cache_paths()
            if risk_order.index(p.risk_level) <= max_index
        ]

    def get_existing_paths(self) -> list[CachePath]:
        """Get only cache paths that exist on this system."""
        return [p for p in self.get_cache_paths() if p.exists()]
