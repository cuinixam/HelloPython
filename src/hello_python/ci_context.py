from dataclasses import dataclass
from typing import Optional


@dataclass
class CIContext:
    #: CI system where the build is running
    name: str
    #: Whether the build is for a pull request
    is_pull_request: bool
    #: The branch to merge into
    target_branch: Optional[str]
    #: Branch being built
    current_branch: Optional[str]


def detect_ci_context() -> CIContext:
    pass
