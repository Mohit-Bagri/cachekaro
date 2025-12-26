"""
macOS platform implementation for CacheKaro.

Provides macOS-specific cache paths, system operations, and utilities.
"""

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


class MacOSPlatform(PlatformBase):
    """macOS-specific platform implementation."""

    @property
    def name(self) -> str:
        return "macOS"

    def get_platform_info(self) -> PlatformInfo:
        """Get detailed macOS platform information."""
        if self._platform_info is not None:
            return self._platform_info

        self._platform_info = PlatformInfo(
            name="macOS",
            version=platform.mac_ver()[0],
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

    def get_trash_path(self) -> Optional[Path]:
        """Get macOS Trash path."""
        trash = self.get_home_dir() / ".Trash"
        return trash if trash.exists() else None

    def get_config_dir(self) -> Path:
        """Get configuration directory (XDG-style on macOS)."""
        config_dir = self.get_home_dir() / ".config" / "cachekaro"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

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
        Flush macOS DNS cache.

        Requires sudo privileges.
        """
        try:
            subprocess.run(
                ["sudo", "dscacheutil", "-flushcache"],
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["sudo", "killall", "-HUP", "mDNSResponder"],
                capture_output=True,
                check=True,
            )
            return True, "DNS cache flushed successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to flush DNS cache: {e}"
        except FileNotFoundError:
            return False, "DNS flush commands not available"

    def is_admin(self) -> bool:
        """Check if running as root."""
        return os.geteuid() == 0

    def get_cache_paths(self) -> list[CachePath]:
        """Get all macOS cache paths."""
        if self._cache_paths:
            return self._cache_paths

        home = self.get_home_dir()
        library = home / "Library"

        paths = []

        # ============================================================
        # USER CACHES (~/Library/Caches) - 100% Safe
        # ============================================================
        caches = library / "Caches"

        # System caches
        paths.extend([
            CachePath(
                path=caches / "com.apple.textunderstandingd",
                name="Apple Text Understanding",
                category=Category.SYSTEM_CACHE,
                description="Apple text analysis cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "SiriTTS",
                name="Siri TTS",
                category=Category.SYSTEM_CACHE,
                description="Siri text-to-speech cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "GeoServices",
                name="GeoServices",
                category=Category.SYSTEM_CACHE,
                description="Apple location services cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "com.apple.Safari",
                name="Safari Cache",
                category=Category.BROWSER,
                description="Safari browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Safari",
            ),
        ])

        # Browser caches
        paths.extend([
            CachePath(
                path=caches / "Google",
                name="Google/Chrome Cache",
                category=Category.BROWSER,
                description="Google Chrome browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Chrome",
            ),
            CachePath(
                path=caches / "BraveSoftware",
                name="Brave Browser Cache",
                category=Category.BROWSER,
                description="Brave browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Brave",
            ),
            CachePath(
                path=caches / "Firefox",
                name="Firefox Cache",
                category=Category.BROWSER,
                description="Firefox browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Firefox",
            ),
            CachePath(
                path=caches / "com.microsoft.Edge",
                name="Microsoft Edge Cache",
                category=Category.BROWSER,
                description="Microsoft Edge browser cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Edge",
            ),
        ])

        # Application caches
        paths.extend([
            CachePath(
                path=caches / "com.spotify.client",
                name="Spotify Cache",
                category=Category.APPLICATION,
                description="Spotify streaming cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Spotify",
            ),
            CachePath(
                path=caches / "JetBrains",
                name="JetBrains IDE Cache",
                category=Category.DEVELOPMENT,
                description="JetBrains IDEs cache (IntelliJ, PyCharm, WebStorm, etc.)",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="JetBrains",
            ),
            CachePath(
                path=caches / "electron",
                name="Electron Apps Cache",
                category=Category.APPLICATION,
                description="Electron-based applications cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "com.lwouis.alt-tab-macos",
                name="Alt-Tab Cache",
                category=Category.APPLICATION,
                description="Alt-Tab window switcher cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Alt-Tab",
            ),
            CachePath(
                path=caches / "com.openai.chat",
                name="ChatGPT Cache",
                category=Category.APPLICATION,
                description="ChatGPT desktop app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="ChatGPT",
            ),
            CachePath(
                path=caches / "com.discord.Discord",
                name="Discord Cache",
                category=Category.APPLICATION,
                description="Discord app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Discord",
            ),
            CachePath(
                path=caches / "com.hnc.Discord",
                name="Discord (Alt) Cache",
                category=Category.APPLICATION,
                description="Discord alternative app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Discord",
            ),
            CachePath(
                path=caches / "Slack",
                name="Slack Cache",
                category=Category.APPLICATION,
                description="Slack messaging app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Slack",
            ),
            CachePath(
                path=caches / "com.tinyspeck.slackmacgap",
                name="Slack (Mac) Cache",
                category=Category.APPLICATION,
                description="Slack Mac app cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Slack",
            ),
            CachePath(
                path=caches / "us.zoom.xos",
                name="Zoom Cache",
                category=Category.APPLICATION,
                description="Zoom video conferencing cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Zoom",
            ),
        ])

        # Development tool caches
        paths.extend([
            CachePath(
                path=caches / "pnpm",
                name="pnpm Package Cache",
                category=Category.DEVELOPMENT,
                description="pnpm package manager cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "yarn",
                name="Yarn Cache",
                category=Category.DEVELOPMENT,
                description="Yarn package manager cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "pip",
                name="pip Cache",
                category=Category.DEVELOPMENT,
                description="Python pip package cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "Homebrew",
                name="Homebrew Cache",
                category=Category.DEVELOPMENT,
                description="Homebrew package downloads cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "node-gyp",
                name="node-gyp Cache",
                category=Category.DEVELOPMENT,
                description="Node.js native addon build cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "typescript",
                name="TypeScript Cache",
                category=Category.DEVELOPMENT,
                description="TypeScript compiler cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "ms-playwright-go",
                name="Playwright Cache",
                category=Category.DEVELOPMENT,
                description="Playwright browser automation cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "CocoaPods",
                name="CocoaPods Cache",
                category=Category.DEVELOPMENT,
                description="iOS/macOS dependency manager cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=caches / "org.carthage.CarthageKit",
                name="Carthage Cache",
                category=Category.DEVELOPMENT,
                description="iOS/macOS Carthage dependency cache",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # HIDDEN CACHES (~/.cache) - Safe
        # ============================================================
        hidden_cache = home / ".cache"

        paths.extend([
            CachePath(
                path=hidden_cache / "huggingface",
                name="HuggingFace Models",
                category=Category.DEVELOPMENT,
                description="HuggingFace AI models cache (can be large!)",
                risk_level=RiskLevel.MODERATE,
            ),
            CachePath(
                path=hidden_cache / "puppeteer",
                name="Puppeteer Browsers",
                category=Category.DEVELOPMENT,
                description="Puppeteer browser automation cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=hidden_cache / "pip",
                name="pip HTTP Cache",
                category=Category.DEVELOPMENT,
                description="pip HTTP cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=hidden_cache / "pre-commit",
                name="pre-commit Cache",
                category=Category.DEVELOPMENT,
                description="pre-commit hooks cache",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=hidden_cache / "uv",
                name="uv Cache",
                category=Category.DEVELOPMENT,
                description="uv Python package manager cache",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # NPM CACHE (~/.npm) - Safe
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
        # APPLICATION SUPPORT CACHES
        # ============================================================
        app_support = library / "Application Support"

        # Chrome Service Workers
        paths.append(
            CachePath(
                path=app_support / "Google" / "Chrome" / "Default" / "Service Worker",
                name="Chrome Service Workers",
                category=Category.BROWSER,
                description="Chrome web app service workers (PWA cache)",
                risk_level=RiskLevel.SAFE,
                clean_contents_only=False,
                app_specific=True,
                app_name="Chrome",
            )
        )

        # VS Code caches
        paths.extend([
            CachePath(
                path=app_support / "Code" / "Cache",
                name="VS Code Cache",
                category=Category.DEVELOPMENT,
                description="Visual Studio Code cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=app_support / "Code" / "CachedData",
                name="VS Code CachedData",
                category=Category.DEVELOPMENT,
                description="VS Code cached compiled data",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=app_support / "Code" / "CachedExtensionVSIXs",
                name="VS Code Extension Cache",
                category=Category.DEVELOPMENT,
                description="VS Code old extension downloads",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
            CachePath(
                path=app_support / "Code" / "CachedProfilesData",
                name="VS Code Profiles Cache",
                category=Category.DEVELOPMENT,
                description="VS Code profile data cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="VS Code",
            ),
        ])

        # Cursor (VS Code fork)
        paths.extend([
            CachePath(
                path=app_support / "Cursor" / "Cache",
                name="Cursor Cache",
                category=Category.DEVELOPMENT,
                description="Cursor editor cache",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Cursor",
            ),
            CachePath(
                path=app_support / "Cursor" / "CachedData",
                name="Cursor CachedData",
                category=Category.DEVELOPMENT,
                description="Cursor editor cached compiled data",
                risk_level=RiskLevel.SAFE,
                app_specific=True,
                app_name="Cursor",
            ),
        ])

        # ============================================================
        # LOGS
        # ============================================================
        logs = library / "Logs"

        paths.extend([
            CachePath(
                path=logs / "JetBrains",
                name="JetBrains Logs",
                category=Category.LOGS,
                description="JetBrains IDE log files",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=logs / "DiagnosticReports",
                name="Diagnostic Reports",
                category=Category.LOGS,
                description="macOS crash reports and diagnostics",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=logs / "Claude",
                name="Claude Logs",
                category=Category.LOGS,
                description="Claude AI app logs",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=logs / "Homebrew",
                name="Homebrew Logs",
                category=Category.LOGS,
                description="Homebrew installation logs",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=logs / "Spotify",
                name="Spotify Logs",
                category=Category.LOGS,
                description="Spotify application logs",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # DEVELOPER DIRECTORY (Xcode)
        # ============================================================
        developer = library / "Developer"

        paths.extend([
            CachePath(
                path=developer / "Xcode" / "DerivedData",
                name="Xcode DerivedData",
                category=Category.DEVELOPMENT,
                description="Xcode build artifacts (can be very large!)",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=developer / "Xcode" / "Archives",
                name="Xcode Archives",
                category=Category.DEVELOPMENT,
                description="Xcode archived builds (review before deleting)",
                risk_level=RiskLevel.MODERATE,
            ),
            CachePath(
                path=developer / "CoreSimulator" / "Caches",
                name="iOS Simulator Cache",
                category=Category.DEVELOPMENT,
                description="iOS Simulator cache",
                risk_level=RiskLevel.SAFE,
            ),
        ])

        # ============================================================
        # TRASH & DOWNLOADS
        # ============================================================
        paths.extend([
            CachePath(
                path=home / ".Trash",
                name="Trash",
                category=Category.TRASH,
                description="Files in Trash (permanently delete)",
                risk_level=RiskLevel.SAFE,
            ),
            CachePath(
                path=home / "Downloads",
                name="Downloads",
                category=Category.DOWNLOADS,
                description="Downloaded files (review before deleting!)",
                risk_level=RiskLevel.CAUTION,
            ),
        ])

        # ============================================================
        # CONTAINER APPS
        # ============================================================
        containers = library / "Containers"

        paths.append(
            CachePath(
                path=containers,
                name="Container Apps",
                category=Category.CONTAINER,
                description="Sandboxed app data (use with caution)",
                risk_level=RiskLevel.CAUTION,
            )
        )

        # ============================================================
        # ADDITIONAL DEVELOPMENT CACHES
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
                description="Maven dependency cache (review before deleting)",
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
        ])

        self._cache_paths = paths
        return self._cache_paths
