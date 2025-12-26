"""
Pytest fixtures for CacheKaro tests.
"""

import gc
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from cachekaro.models.cache_item import CacheItem
from cachekaro.models.scan_result import ScanMetadata, ScanResult
from cachekaro.platforms.base import CachePath, Category, RiskLevel


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
        # Force garbage collection to release file handles on Windows
        gc.collect()


@pytest.fixture
def sample_cache_path(temp_dir):
    """Create a sample cache path with test files."""
    cache_dir = temp_dir / "test_cache"
    cache_dir.mkdir()

    # Create some test files
    (cache_dir / "file1.txt").write_text("test content 1")
    (cache_dir / "file2.log").write_text("test log content")
    (cache_dir / "file3.cache").write_bytes(b"x" * 1024)  # 1KB file

    # Create a subdirectory
    sub_dir = cache_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "nested.txt").write_text("nested content")

    return CachePath(
        path=cache_dir,
        name="Test Cache",
        category=Category.USER_CACHE,
        description="Test cache for unit tests",
        risk_level=RiskLevel.SAFE,
    )


@pytest.fixture
def sample_cache_item():
    """Create a sample CacheItem for testing."""
    return CacheItem(
        path=Path("/test/cache"),
        name="Test Cache",
        category=Category.USER_CACHE,
        description="Test cache item",
        size_bytes=1024 * 1024,  # 1 MB
        file_count=10,
        dir_count=2,
        last_accessed=datetime.now() - timedelta(days=5),
        last_modified=datetime.now() - timedelta(days=10),
        risk_level=RiskLevel.SAFE,
        is_cleanable=True,
    )


@pytest.fixture
def sample_scan_result(sample_cache_item):
    """Create a sample ScanResult for testing."""
    items = [
        sample_cache_item,
        CacheItem(
            path=Path("/test/browser_cache"),
            name="Browser Cache",
            category=Category.BROWSER,
            description="Browser cache",
            size_bytes=500 * 1024 * 1024,  # 500 MB
            file_count=1000,
            dir_count=50,
            risk_level=RiskLevel.SAFE,
        ),
        CacheItem(
            path=Path("/test/dev_cache"),
            name="Dev Cache",
            category=Category.DEVELOPMENT,
            description="Development cache",
            size_bytes=2 * 1024 * 1024 * 1024,  # 2 GB
            file_count=5000,
            dir_count=100,
            last_accessed=datetime.now() - timedelta(days=60),  # Stale
            risk_level=RiskLevel.SAFE,
            stale_threshold_days=30,
        ),
    ]
    # Make the third item stale
    items[2].stale_threshold_days = 30

    metadata = ScanMetadata(
        scan_time=datetime.now(),
        duration_seconds=5.5,
        platform="Test",
        platform_version="1.0",
        hostname="testhost",
        username="testuser",
        scan_paths_total=10,
        scan_paths_found=3,
        scan_paths_accessible=3,
    )

    return ScanResult(
        items=items,
        metadata=metadata,
        disk_total=500 * 1024 * 1024 * 1024,  # 500 GB
        disk_used=250 * 1024 * 1024 * 1024,   # 250 GB
        disk_free=250 * 1024 * 1024 * 1024,   # 250 GB
    )
