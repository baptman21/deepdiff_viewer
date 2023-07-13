from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from deepdiff import DeepDiff  # type: ignore
from deepdiff.diff import DiffLevel  # type: ignore


class DiffType(Enum):
    UNCHANGED = 0
    ADDITION = 1
    DELETION = 2
    # Additions and deletions at the same time or value changed
    MODIFIED = 3

    @staticmethod
    def combine(left: "DiffType", right: "DiffType") -> "DiffType":
        if left == DiffType.UNCHANGED:
            return right
        if right == DiffType.UNCHANGED:
            return left
        if left == DiffType.MODIFIED or right == DiffType.MODIFIED:
            return DiffType.MODIFIED
        if left == right:
            return left
        return DiffType.MODIFIED


@dataclass
class TreeNode:
    key: str
    path: List[str]

    diff_levels: List[DiffLevel] = field(default_factory=list)

    diff_type: DiffType = DiffType.UNCHANGED

    children: List["TreeNode"] = field(default_factory=list)


class DeepDiffTreeViewer(ABC):
    """Object processing a DeepDiff object to render it in a specific format."""

    # Tree built from the ddiff and an index to access nodes in the tree quickly
    root: TreeNode
    index: Dict[str, TreeNode]

    def __init__(self, ddiff: DeepDiff):
        # TODO: process the ddiff
        pass

    @abstractmethod
    def render(self) -> str | Any:
        """Render the tree in a viewable format. The Any type is used for rich outputs to give typing"""
        raise NotImplementedError()
