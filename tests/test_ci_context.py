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


def test_jenkins_pull_request(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {
        "JENKINS_HOME": "/jenkins/home",
        "CHANGE_ID": "123",
        "CHANGE_TARGET": "main",
        "CHANGE_BRANCH": "feature-branch",
    }.get(var, default)
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context.name == "JENKINS"
    assert ci_context.is_pull_request
    assert ci_context.target_branch == "main"
    assert ci_context.current_branch == "feature-branch"


def test_non_jenkins_environment(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {}.get(var, default)
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context is not None
    assert ci_context.name == "UNKNOWN"
    assert not ci_context.is_pull_request
    assert ci_context.target_branch is None
    assert ci_context.current_branch is None
