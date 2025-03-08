import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, Type


@dataclass
class CIContext:
    #: CI system where the build is running
    ci_system: "CISystem"
    #: Whether the build is for a pull request
    is_pull_request: bool
    #: The branch being build or the branch from the PR to merge into (e.g. main)
    target_branch: Optional[str]
    #: Branch being built or the branch from the PR that needs to be merged (e.g. feature/branch)
    current_branch: Optional[str]

    @property
    def name(self) -> str:
        return str(self.ci_system)


class CIDetector(ABC):
    """Abstract base class for CI system detectors."""

    @abstractmethod
    def detect(self) -> Optional[CIContext]:
        """Detects the CI system and returns a CIContext, or None if not detected."""
        pass

    @staticmethod
    def get_env_variable(var_name: str, default: Optional[str] = None) -> Optional[str]:
        """Helper function to get environment variables."""
        return os.getenv(var_name, default)


class JenkinsDetector(CIDetector):
    """Detects Jenkins CI."""

    def detect(self) -> Optional[CIContext]:
        if self.get_env_variable("JENKINS_HOME") is not None:
            is_pull_request = self.get_env_variable("CHANGE_ID") is not None
            if is_pull_request:
                target_branch = self.get_env_variable("CHANGE_TARGET")
                current_branch = self.get_env_variable("CHANGE_BRANCH")
            else:
                target_branch = self.get_env_variable("BRANCH_NAME")
                current_branch = target_branch

            return CIContext(
                ci_system=CISystem.JENKINS,
                is_pull_request=is_pull_request,
                target_branch=target_branch,
                current_branch=current_branch,
            )
        return None


class CISystem(Enum):
    UNKNOWN = (auto(), None)  # Special case for unknown
    JENKINS = (auto(), JenkinsDetector)
    # Add new CI systems here:  MY_CI = (auto(), MyCIDetector)

    def __init__(self, _: Any, detector_class: Optional[Type[CIDetector]]):
        self._value_ = _  # Use auto() value, but ignore it in __init__
        self.detector_class = detector_class

    def get_detector(self) -> Optional[CIDetector]:
        return self.detector_class() if self.detector_class else None

    def __str__(self) -> str:
        """Return the name of the CI system in uppercase."""
        return self.name.upper()


def detect_ci_context() -> CIContext:
    ci_context: Optional[CIContext] = None
    for ci_system in CISystem:
        detector = ci_system.get_detector()
        if detector:
            ci_context = detector.detect()
            if ci_context:
                break  # Stop at the first detected CI
    # If no CI system was detected, return unknown CIContext
    else:
        ci_context = CIContext(
            ci_system=CISystem.UNKNOWN,
            is_pull_request=False,
            target_branch=None,
            current_branch=None,
        )
    return ci_context
