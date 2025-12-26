"""
Linux platform implementation for CacheKaro.

Provides Linux-specific cache paths, system operations, and utilities.
Follows XDG Base Directory Specification.
"""

from __future__ import annotations

import getpass
import os
import platform
import shutil
import socket
import subprocess
import tempfile
from pathlib import Path

from cachekaro.platforms.base import (
    CachePath,
    Category,
    DiskUsage,
    PlatformBase,
    PlatformInfo,
    RiskLevel,
)


class LinuxPlatform(PlatformBase):
    """Linux-specific platform implementation."""

    @property
    def name(self) -> str:
        return "Linux"

    def get_platform_info(self) -> PlatformInfo:
        """Get detailed Linux platform information."""
        if self._platform_info is not None:
            return self._platform_info

        # Try to get distribution info
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                distro = "Linux"
                version = ""
                for line in lines:
                    if line.startswith("PRETTY_NAME="):
                        distro = line.split("=")[1].strip().strip('"')
                    elif line.startswith("VERSION_ID="):
                        version = line.split("=")[1].strip().strip('"')
        except (FileNotFoundError, PermissionError):
            distro = "Linux"
            version = platform.release()

        self._platform_info = PlatformInfo(
            name=distro,
            version=version,
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

    def get_trash_path(self) -> Path | None:
        """Get Linux Trash path (FreeDesktop.org spec)."""
        # Check XDG_DATA_HOME first
        xdg_data = os.environ.get("XDG_DATA_HOME")
        if xdg_data:
            trash = Path(xdg_data) / "Trash"
        else:
            trash = self.get_home_dir() / ".local" / "share" / "Trash"

        if trash.exists():
            return trash

        # Fallback to ~/.Trash
        fallback = self.get_home_dir() / ".Trash"
        return fallback if fallback.exists() else None

    def get_config_dir(self) -> Path:
        """Get configuration directory (XDG spec)."""
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            config_dir = Path(xdg_config) / "cachekaro"
        else:
            config_dir = self.get_home_dir() / ".config" / "cachekaro"

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def _get_xdg_cache_home(self) -> Path:
        """Get XDG cache home directory."""
        xdg_cache = os.environ.get("XDG_CACHE_HOME")
        if xdg_cache:
            return Path(xdg_cache)
        return self.get_home_dir() / ".cache"

    def _get_xdg_config_home(self) -> Path:
        """Get XDG config home directory."""
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            return Path(xdg_config)
        return self.get_home_dir() / ".config"

    def _get_xdg_data_home(self) -> Path:
        """Get XDG data home directory."""
        xdg_data = os.environ.get("XDG_DATA_HOME")
        if xdg_data:
            return Path(xdg_data)
        return self.get_home_dir() / ".local" / "share"

    def get_disk_usage(self, path: str = "/") -> DiskUsage:
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
        Flush Linux DNS cache.

        Linux DNS caching varies by distribution and configuration.
        """
        commands_to_try = [
            # systemd-resolved (Ubuntu, Fedora, etc.)
            ["sudo", "systemd-resolve", "--flush-caches"],
            ["sudo", "resolvectl", "flush-caches"],
            # nscd
            ["sudo", "systemctl", "restart", "nscd"],
            # dnsmasq
            ["sudo", "systemctl", "restart", "dnsmasq"],
        ]

        for cmd in commands_to_try:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    return True, f"DNS cache flushed using {cmd[1]}"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        return False, "No DNS cache service found or flush failed"

    def is_admin(self) -> bool:
        """Check if running as root."""
        # os.geteuid() is Unix-only, use getattr for type safety
        geteuid = getattr(os, "geteuid", None)
        if geteuid is not None:
            return bool(geteuid() == 0)
        return False

    def get_cache_paths(self) -> list[CachePath]:
        """Get all Linux cache paths."""
        if self._cache_paths:
            return self._cache_paths

        home = self.get_home_dir()
        cache_home = self._get_xdg_cache_home()
        config_home = self._get_xdg_config_home()
        data_home = self._get_xdg_data_home()

        paths = []

        # ============================================================
        # XDG CACHE (~/.cache) - Safe
        # ============================================================

        # Browser caches
        paths.extend([
            CachePath(
                path=cache_home / "google-chrome",
                name="Google Chrome Cache",
                category=Category.BROWSER,
                description="Google Chrome browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Chrome",
            ),
            CachePath(
                path=cache_home / "chromium",
                name="Chromium Cache",
                category=Category.BROWSER,
                description="Chromium browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Chromium",
            ),
            CachePath(
                path=cache_home / "mozilla",
                name="Firefox Cache",
                category=Category.BROWSER,
                description="Mozilla Firefox browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Firefox",
            ),
            CachePath(
                path=cache_home / "BraveSoftware",
                name="Brave Browser Cache",
                category=Category.BROWSER,
                description="Brave browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Brave",
            ),
            CachePath(
                path=cache_home / "microsoft-edge",
                name="Microsoft Edge Cache",
                category=Category.BROWSER,
                description="Microsoft Edge browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Edge",
            ),
        ])

        # Development tool caches
        paths.extend([
            CachePath(
                path=cache_home / "pip",
                name="pip Cache",
                category=Category.DEVELOPMENT,
                description="Python pip package cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "yarn",
                name="Yarn Cache",
                category=Category.DEVELOPMENT,
                description="Yarn package manager cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "pnpm",
                name="pnpm Cache",
                category=Category.DEVELOPMENT,
                description="pnpm package manager cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "node-gyp",
                name="node-gyp Cache",
                category=Category.DEVELOPMENT,
                description="Node.js native addon build cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "typescript",
                name="TypeScript Cache",
                category=Category.DEVELOPMENT,
                description="TypeScript compiler cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "JetBrains",
                name="JetBrains Cache",
                category=Category.DEVELOPMENT,
                description="JetBrains IDE cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="JetBrains",
            ),
            CachePath(
                path=cache_home / "huggingface",
                name="HuggingFace Models",
                category=Category.DEVELOPMENT,
                description="HuggingFace AI models cache (can be large!)",
                risk_level=RiskLevel.MODERATE,
            ),
            CachePath(
                path=cache_home / "puppeteer",
                name="Puppeteer Browsers",
                category=Category.DEVELOPMENT,
                description="Puppeteer browser automation cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "pre-commit",
                name="pre-commit Cache",
                category=Category.DEVELOPMENT,
                description="pre-commit hooks cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "uv",
                name="uv Cache",
                category=Category.DEVELOPMENT,
                description="uv Python package manager cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "go-build",
                name="Go Build Cache",
                category=Category.DEVELOPMENT,
                description="Go compilation cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "bazel",
                name="Bazel Cache",
                category=Category.DEVELOPMENT,
                description="Bazel build system cache",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # Application caches
        paths.extend([
            CachePath(
                path=cache_home / "spotify",
                name="Spotify Cache",
                category=Category.APPLICATION,
                description="Spotify streaming cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Spotify",
            ),
            CachePath(
                path=cache_home / "discord",
                name="Discord Cache",
                category=Category.APPLICATION,
                description="Discord app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Discord",
            ),
            CachePath(
                path=cache_home / "Slack",
                name="Slack Cache",
                category=Category.APPLICATION,
                description="Slack messaging app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Slack",
            ),
            CachePath(
                path=cache_home / "zoom",
                name="Zoom Cache",
                category=Category.APPLICATION,
                description="Zoom video conferencing cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Zoom",
            ),
            CachePath(
                path=cache_home / "thumbnails",
                name="Thumbnails",
                category=Category.SYSTEM_CACHE,
                description="File manager thumbnail cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "fontconfig",
                name="Font Cache",
                category=Category.SYSTEM_CACHE,
                description="Font configuration cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=cache_home / "mesa_shader_cache",
                name="Mesa Shader Cache",
                category=Category.SYSTEM_CACHE,
                description="OpenGL shader compilation cache",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # NPM CACHE (~/.npm)
        # ============================================================
        paths.append(
            CachePath(
                path=home / ".npm" / "_cacache",
                name="NPM Cache",
                category=Category.DEVELOPMENT,
                description="NPM package manager cache",
                risk_level=RiskLevel.SAFE,
            )
        )

        # ============================================================
        # CONFIG-BASED APP DATA (~/.config)
        # ============================================================

        # VS Code
        paths.extend([
            CachePath(
                path=config_home / "Code" / "Cache",
                name="VS Code Cache",
                category=Category.DEVELOPMENT,
                description="Visual Studio Code cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=config_home / "Code" / "CachedData",
                name="VS Code CachedData",
                category=Category.DEVELOPMENT,
                description="VS Code cached compiled data",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=config_home / "Code" / "CachedExtensionVSIXs",
                name="VS Code Extension Cache",
                category=Category.DEVELOPMENT,
                description="VS Code old extension downloads",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
        ])

        # Chrome/Chromium user data (Service Workers)
        paths.extend([
            CachePath(
                path=config_home / "google-chrome" / "Default" / "Service Worker",
                name="Chrome Service Workers",
                category=Category.BROWSER,
                description="Chrome web app service workers",
                risk_level=RiskLevel.SAFE,
                clean_contents_only=False,
                app_specific=True,
                app_name="Chrome",
            ),
            CachePath(
                path=config_home / "chromium" / "Default" / "Service Worker",
                name="Chromium Service Workers",
                category=Category.BROWSER,
                description="Chromium web app service workers",
                risk_level=RiskLevel.SAFE,
                clean_contents_only=False,
                app_specific=True,
                app_name="Chromium",
            ),
        ])

        # ============================================================
        # DEVELOPMENT CACHES (Home directory)
        # ============================================================
        paths.extend([
            CachePath(
                path=home / ".gradle" / "caches",
                name="Gradle Cache",
                category=Category.DEVELOPMENT,
                description="Gradle build system cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=home / ".m2" / "repository",
                name="Maven Repository",
                category=Category.DEVELOPMENT,
                description="Maven dependency cache",
                risk_level=RiskLevel.MODERATE,
            ),
            CachePath(
                path=home / ".cargo" / "registry" / "cache",
                name="Cargo Registry Cache",
                category=Category.DEVELOPMENT,
                description="Rust Cargo package cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=home / "go" / "pkg" / "mod" / "cache",
                name="Go Module Cache",
                category=Category.DEVELOPMENT,
                description="Go module download cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=home / ".docker" / "buildx",
                name="Docker Buildx Cache",
                category=Category.DEVELOPMENT,
                description="Docker buildx builder cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=home / ".composer" / "cache",
                name="Composer Cache",
                category=Category.DEVELOPMENT,
                description="PHP Composer package cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=home / ".gem" / "cache",
                name="Ruby Gem Cache",
                category=Category.DEVELOPMENT,
                description="Ruby gem package cache",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # LOGS
        # ============================================================
        paths.extend([
            CachePath(
                path=data_home / "JetBrains",
                name="JetBrains Data",
                category=Category.LOGS,
                description="JetBrains IDE logs and data",
                risk_level=RiskLevel.MODERATE,
            ),
            CachePath(
                path=home / ".xsession-errors",
                name="X Session Errors",
                category=Category.LOGS,
                description="X Window session error log",
                risk_level=RiskLevel.SAFE,
                clean_contents_only=False,
            ),
        ])

        # ============================================================
        # TRASH
        # ============================================================
        trash_path = self.get_trash_path()
        if trash_path:
            paths.extend([
                CachePath(
                    path=trash_path / "files",
                    name="Trash Files",
                    category=Category.TRASH,
                    description="Files in Trash (permanently delete)",
                    risk_level=RiskLevel.SAFE,
                ),
                CachePath(
                    path=trash_path / "info",
                    name="Trash Info",
                    category=Category.TRASH,
                    description="Trash metadata",
                    risk_level=RiskLevel.SAFE,
                ),
            ])

        # ============================================================
        # DOWNLOADS
        # ============================================================
        # Check XDG user dirs
        downloads_path = home / "Downloads"
        xdg_downloads = os.environ.get("XDG_DOWNLOAD_DIR")
        if xdg_downloads:
            downloads_path = Path(xdg_downloads)

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
        # SNAP & FLATPAK CACHES
        # ============================================================
        paths.extend([
            CachePath(
                path=home / "snap",
                name="Snap Packages",
                category=Category.CONTAINER,
                description="Snap package data (use with caution)",
                risk_level=RiskLevel.CAUTION,
            ),
            CachePath(
                path=data_home / "flatpak",
                name="Flatpak Data",
                category=Category.CONTAINER,
                description="Flatpak application data",
                risk_level=RiskLevel.CAUTION,
            ),
        ])

        self._cache_paths = paths
        return self._cache_paths
