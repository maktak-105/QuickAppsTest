from quickappstest.backends.pywinauto_backend import title_matches

HTML_TITLE = "QuickDiskBench v2.1.1 - Storage Benchmark"
WIN32_TITLE = "QuickDiskBench v2.1.1 - Native Storage Benchmark (Cache Modes & Statistics)"


def test_win32_title_is_not_html_title() -> None:
    assert title_matches(WIN32_TITLE, "Native Storage Benchmark")
    assert not title_matches(HTML_TITLE, "Native Storage Benchmark")
    assert title_matches(WIN32_TITLE, "QuickDiskBench")
    assert title_matches(HTML_TITLE, "QuickDiskBench")


def test_empty_title_does_not_match() -> None:
    assert not title_matches(None, "QuickDiskBench")
    assert not title_matches("", "QuickDiskBench")
