"""
API test report fixtures
Configure pytest for detailed reporting
"""

import pytest
import json
import os
from datetime import datetime


def pytest_configure(config):
    """
    Configure pytest hooks and add custom options
    """
    config.addinivalue_line("markers", "smoke: smoke tests for quick validation")
    config.addinivalue_line("markers", "validation: data validation tests")
    config.addinivalue_line("markers", "slow: slow tests that require more time")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for reporting
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        # Store test result on the item
        setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def test_report_dir(request):
    """
    Create a directory for test reports
    """
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"test_reports/{test_name}_{timestamp}"

    os.makedirs(report_dir, exist_ok=True)
    yield report_dir


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Generate summary at end of test run
    """
    print("\n" + "=" * 70)
    print("API TEST SUMMARY")
    print("=" * 70)

    reports = terminalreporter.getreports("")
    for report in reports:
        if report.when == "call":
            status = "✓ PASS" if report.passed else "✗ FAIL"
            print(f"{status}: {report.nodeid}")

    print("=" * 70)


class TestReporting:
    """Tests demonstrating reporting capabilities"""

    @pytest.mark.smoke
    def test_smoke_test(self, api_client):
        """Quick smoke test"""
        posts = api_client.get_posts(limit=1)
        assert len(posts) > 0

    def test_detailed_report(self, api_client, test_report_dir):
        """
        Test with report directory access
        Can write detailed reports here
        """
        posts = api_client.get_posts(limit=5)

        report_file = os.path.join(test_report_dir, "posts.json")
        with open(report_file, "w") as f:
            json.dump(posts, f, indent=2)

        assert len(posts) == 5
