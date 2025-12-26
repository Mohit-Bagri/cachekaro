"""
Windows platform implementation for CacheKaro.

Provides Windows-specific cache paths, system operations, and utilities.
"""

import ctypes
import getpass
import os
import platform
import shutil
import socket
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from cachekaro.platforms.base import (
    CachePath,
    Category,
    DiskUsage,
    PlatformBase,
    PlatformInfo,
    RiskLevel,
)


class WindowsPlatform(PlatformBase):
    """Windows-specific platform implementation."""

    @property
    def name(self) -> str:
        return "Windows"

    def get_platform_info(self) -> PlatformInfo:
        """Get detailed Windows platform information."""
        if self._platform_info is not None:
            return self._platform_info

        self._platform_info = PlatformInfo(
            name="Windows",
            version=platform.version(),
            architecture=platform.machine(),
            hostname=socket.gethostname(),
            username=getpass.getuser(),
            home_dir=self.get_home_dir(),
            temp_dir=self.get_temp_dir(),
        )
        return self._platform_info

    def get_home_dir(self) -> Path:
        """Get user home directory."""
        return Path.home()

    def get_temp_dir(self) -> Path:
        """Get system temp directory."""
        return Path(tempfile.gettempdir())

    def _get_appdata(self) -> Path:
        """Get APPDATA directory (Roaming)."""
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata)
        return self.get_home_dir() / "AppData" / "Roaming"

    def _get_localappdata(self) -> Path:
        """Get LOCALAPPDATA directory."""
        localappdata = os.environ.get("LOCALAPPDATA")
        if localappdata:
            return Path(localappdata)
        return self.get_home_dir() / "AppData" / "Local"

    def _get_programdata(self) -> Path:
        """Get ProgramData directory."""
        programdata = os.environ.get("PROGRAMDATA")
        if programdata:
            return Path(programdata)
        return Path("C:/ProgramData")

    def get_trash_path(self) -> Optional[Path]:
        """
        Get Windows Recycle Bin path.

        Note: Windows Recycle Bin is complex and per-drive.
        We can't easily clean it programmatically without special APIs.
        """
        # Windows Recycle Bin is special - return None and handle separately
        return None

    def get_config_dir(self) -> Path:
        """Get configuration directory for CacheKaro."""
        config_dir = self._get_appdata() / "cachekaro"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def get_disk_usage(self, path: str = "C:/") -> DiskUsage:
        """Get disk usage for the specified path."""
        usage = shutil.disk_usage(path)
        return DiskUsage(
            total_bytes=usage.total,
            used_bytes=usage.used,
            free_bytes=usage.free,
            mount_point=path,
        )

    def flush_dns_cache(self) -> tuple[bool, str]:
        """
        Flush Windows DNS cache.

        Uses ipconfig /flushdns command.
        """
        try:
            result = subprocess.run(
                ["ipconfig", "/flushdns"],
                capture_output=True,
                text=True,
                check=True,
            )
            return True, "DNS cache flushed successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to flush DNS cache: {e}"
        except FileNotFoundError:
            return False, "ipconfig command not found"

    def is_admin(self) -> bool:
        """Check if running as Administrator."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except (AttributeError, OSError):
            return False

    def empty_recycle_bin(self) -> tuple[bool, str]:
        """
        Empty the Windows Recycle Bin.

        Uses PowerShell to clear the recycle bin.
        """
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
                ],
                capture_output=True,
                text=True,
            )
            return True, "Recycle Bin emptied successfully"
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return False, f"Failed to empty Recycle Bin: {e}"

    def get_cache_paths(self) -> list[CachePath]:
        """Get all Windows cache paths."""
        if self._cache_paths:
            return self._cache_paths

        home = self.get_home_dir()
        appdata = self._get_appdata()
        localappdata = self._get_localappdata()
        temp = self.get_temp_dir()

        paths = []

        # ============================================================
        # TEMP DIRECTORIES - Safe
        # ============================================================
        paths.extend([
            CachePath(
                path=temp,
                name="User Temp",
                category=Category.SYSTEM_CACHE,
                description="User temporary files",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=Path("C:/Windows/Temp"),
                name="System Temp",
                category=Category.SYSTEM_CACHE,
                description="System temporary files (requires admin)",
                risk_level=RiskLevel.SAFE,
                requires_admin=True,
            ),
        ])

        # ============================================================
        # BROWSER CACHES (LocalAppData)
        # ============================================================
        paths.extend([
            CachePath(
                path=localappdata / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
                name="Chrome Cache",
                category=Category.BROWSER,
                description="Google Chrome browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Chrome",
            ),
            CachePath(
                path=localappdata / "Google" / "Chrome" / "User Data" / "Default" / "Code Cache",
                name="Chrome Code Cache",
                category=Category.BROWSER,
                description="Chrome JavaScript code cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Chrome",
            ),
            CachePath(
                path=localappdata / "Google" / "Chrome" / "User Data" / "Default" / "Service Worker",
                name="Chrome Service Workers",
                category=Category.BROWSER,
                description="Chrome web app service workers",
                risk_level=RiskLevel.SAFE,
                clean_contents_only=False,
                app_specific=True,
                app_name="Chrome",
            ),
            CachePath(
                path=localappdata / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
                name="Edge Cache",
                category=Category.BROWSER,
                description="Microsoft Edge browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Edge",
            ),
            CachePath(
                path=localappdata / "Microsoft" / "Edge" / "User Data" / "Default" / "Code Cache",
                name="Edge Code Cache",
                category=Category.BROWSER,
                description="Edge JavaScript code cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Edge",
            ),
            CachePath(
                path=localappdata / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "Cache",
                name="Brave Cache",
                category=Category.BROWSER,
                description="Brave browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Brave",
            ),
            CachePath(
                path=localappdata / "Mozilla" / "Firefox" / "Profiles",
                name="Firefox Cache",
                category=Category.BROWSER,
                description="Firefox browser profiles (contains cache)",
                risk_level=RiskLevel.MODERATE,
                app_specific=True,
                app_name="Firefox",
            ),
        ])

        # ============================================================
        # DEVELOPMENT CACHES
        # ============================================================

        # NPM (in AppData\Roaming)
        paths.append(
            CachePath(
                path=appdata / "npm-cache",
                name="NPM Cache",
                category=Category.DEVELOPMENT,
                description="NPM package manager cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # pip cache
        paths.append(
            CachePath(
                path=localappdata / "pip" / "Cache",
                name="pip Cache",
                category=Category.DEVELOPMENT,
                description="Python pip package cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # Yarn
        paths.append(
            CachePath(
                path=localappdata / "Yarn" / "Cache",
                name="Yarn Cache",
                category=Category.DEVELOPMENT,
                description="Yarn package manager cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # pnpm
        paths.append(
            CachePath(
                path=localappdata / "pnpm-cache",
                name="pnpm Cache",
                category=Category.DEVELOPMENT,
                description="pnpm package manager cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # NuGet
        paths.append(
            CachePath(
                path=localappdata / "NuGet" / "v3-cache",
                name="NuGet Cache",
                category=Category.DEVELOPMENT,
                description=".NET NuGet package cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # VS Code
        paths.extend([
            CachePath(
                path=appdata / "Code" / "Cache",
                name="VS Code Cache",
                category=Category.DEVELOPMENT,
                description="Visual Studio Code cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=appdata / "Code" / "CachedData",
                name="VS Code CachedData",
                category=Category.DEVELOPMENT,
                description="VS Code cached compiled data",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=appdata / "Code" / "CachedExtensionVSIXs",
                name="VS Code Extension Cache",
                category=Category.DEVELOPMENT,
                description="VS Code old extension downloads",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
        ])

        # JetBrains
        paths.extend([
            CachePath(
                path=localappdata / "JetBrains",
                name="JetBrains Cache",
                category=Category.DEVELOPMENT,
                description="JetBrains IDE caches",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="JetBrains",
            ),
        ])

        # Gradle
        paths.append(
            CachePath(
                path=home / ".gradle" / "caches",
                name="Gradle Cache",
                category=Category.DEVELOPMENT,
                description="Gradle build system cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # Maven
        paths.append(
            CachePath(
                path=home / ".m2" / "repository",
                name="Maven Repository",
                category=Category.DEVELOPMENT,
                description="Maven dependency cache",
                risk_level=RiskLevel.MODERATE,
            )
        )

        # Cargo (Rust)
        paths.append(
            CachePath(
                path=home / ".cargo" / "registry" / "cache",
                name="Cargo Registry Cache",
                category=Category.DEVELOPMENT,
                description="Rust Cargo package cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # Go
        paths.append(
            CachePath(
                path=home / "go" / "pkg" / "mod" / "cache",
                name="Go Module Cache",
                category=Category.DEVELOPMENT,
                description="Go module download cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # Docker
        paths.extend([
            CachePath(
                path=home / ".docker" / "buildx",
                name="Docker Buildx Cache",
                category=Category.DEVELOPMENT,
                description="Docker buildx builder cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=localappdata / "Docker" / "wsl",
                name="Docker WSL Data",
                category=Category.DEVELOPMENT,
                description="Docker Desktop WSL backend data",
                risk_level=RiskLevel.CAUTION,
            ),
        ])

        # HuggingFace
        paths.append(
            CachePath(
                path=home / ".cache" / "huggingface",
                name="HuggingFace Models",
                category=Category.DEVELOPMENT,
                description="HuggingFace AI models cache (can be large!)",
                risk_level=RiskLevel.MODERATE,
            )
        )

        # ============================================================
        # APPLICATION CACHES
        # ============================================================
        paths.extend([
            CachePath(
                path=appdata / "Spotify" / "Storage",
                name="Spotify Cache",
                category=Category.APPLICATION,
                description="Spotify streaming cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Spotify",
            ),
            CachePath(
                path=appdata / "discord" / "Cache",
                name="Discord Cache",
                category=Category.APPLICATION,
                description="Discord app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Discord",
            ),
            CachePath(
                path=appdata / "discord" / "Code Cache",
                name="Discord Code Cache",
                category=Category.APPLICATION,
                description="Discord JavaScript cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Discord",
            ),
            CachePath(
                path=appdata / "Slack" / "Cache",
                name="Slack Cache",
                category=Category.APPLICATION,
                description="Slack messaging app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Slack",
            ),
            CachePath(
                path=appdata / "Zoom" / "data",
                name="Zoom Cache",
                category=Category.APPLICATION,
                description="Zoom video conferencing cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Zoom",
            ),
            CachePath(
                path=localappdata / "Microsoft" / "Teams" / "Cache",
                name="Teams Cache",
                category=Category.APPLICATION,
                description="Microsoft Teams cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Teams",
            ),
        ])

        # ============================================================
        # WINDOWS SYSTEM CACHES
        # ============================================================
        paths.extend([
            CachePath(
                path=localappdata / "Microsoft" / "Windows" / "INetCache",
                name="Internet Cache",
                category=Category.SYSTEM_CACHE,
                description="Windows Internet Explorer/Edge cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=localappdata / "Microsoft" / "Windows" / "Explorer",
                name="Explorer Cache",
                category=Category.SYSTEM_CACHE,
                description="Windows Explorer thumbnail cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=localappdata / "CrashDumps",
                name="Crash Dumps",
                category=Category.LOGS,
                description="Application crash dump files",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=localappdata / "Microsoft" / "Windows" / "WER",
                name="Windows Error Reports",
                category=Category.LOGS,
                description="Windows Error Reporting files",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # WINDOWS UPDATE CACHE (requires admin)
        # ============================================================
        paths.append(
            CachePath(
                path=Path("C:/Windows/SoftwareDistribution/Download"),
                name="Windows Update Cache",
                category=Category.SYSTEM_CACHE,
                description="Windows Update downloaded files (requires admin)",
                risk_level=RiskLevel.MODERATE,
                requires_admin=True,
            )
        )

        # ============================================================
        # DOWNLOADS
        # ============================================================
        downloads_path = home / "Downloads"
        paths.append(
            CachePath(
                path=downloads_path,
                name="Downloads",
                category=Category.DOWNLOADS,
                description="Downloaded files (review before deleting!)",
                risk_level=RiskLevel.CAUTION,
            )
        )

        # ============================================================
        # PREFETCH (requires admin)
        # ============================================================
        paths.append(
            CachePath(
                path=Path("C:/Windows/Prefetch"),
                name="Prefetch",
                category=Category.SYSTEM_CACHE,
                description="Windows Prefetch files (requires admin)",
                risk_level=RiskLevel.MODERATE,
                requires_admin=True,
            )
        )

        self._cache_paths = paths
        return self._cache_paths
