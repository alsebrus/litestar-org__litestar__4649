from __future__ import annotations

from datetime import datetime, timezone

from litestar.file_system import get_fsspec_mtime_equivalent


def _utc(y: int, m: int, d: int, h: int = 0, mi: int = 0, s: int = 0) -> float:
    """Build a UTC-anchored timestamp so comparisons are TZ-independent."""
    return datetime(y, m, d, h, mi, s, tzinfo=timezone.utc).timestamp()


def test_get_fsspec_mtime_equivalent_rfc_2822() -> None:
    """RFC 2822 formatted dates should be parsed correctly.

    On the base commit, get_fsspec_mtime_equivalent only handles ISO 8601
    format strings via datetime.fromisoformat(). RFC 2822 dates (e.g.
    'Thu, 01 Jan 2025 12:00:00 GMT') will raise ValueError.

    The fix adds a fallback parser that handles RFC 2822 date strings.
    """
    result = get_fsspec_mtime_equivalent({"mtime": "Thu, 01 Jan 2025 12:00:00 GMT"})
    assert result == _utc(2025, 1, 1, 12, 0, 0)


def test_get_fsspec_mtime_equivalent_rfc_2822_with_different_timezone() -> None:
    """RFC 2822 dates with different timezones should be parsed."""
    result = get_fsspec_mtime_equivalent({"mtime": "Sun, 15 Jun 2025 08:30:00 GMT"})
    assert result == _utc(2025, 6, 15, 8, 30, 0)


def test_get_fsspec_mtime_equivalent_iso_format_still_works() -> None:
    """ISO 8601 dates that previously worked must still work."""
    result = get_fsspec_mtime_equivalent({"mtime": "2025-01-01T12:00:00+00:00"})
    assert result == _utc(2025, 1, 1, 12, 0, 0)


def test_get_fsspec_mtime_equivalent_invalid_string_raises() -> None:
    """Completely invalid date strings should still raise ValueError."""
    import pytest

    with pytest.raises(ValueError):
        get_fsspec_mtime_equivalent({"mtime": "not a date at all"})
