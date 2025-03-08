from unittest.mock import MagicMock, patch

import pytest

from hello_python.ci_context import detect_ci_context


@pytest.fixture
def mock_on_getenv():
    with patch("os.getenv") as mock_os_getenv:
        yield mock_os_getenv


def test_jenkins_branch_push(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {
        "JENKINS_HOME": "/jenkins/home",
        "BRANCH_NAME": "main",
    }.get(var, default)
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context.name == "JENKINS"
    assert ci_context.is_pull_request is False
    assert ci_context.target_branch == "main"
    assert ci_context.current_branch == "main"
