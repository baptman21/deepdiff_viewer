from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from deepdiff import DeepDiff  # type: ignore
from deepdiff.diff import TREE_VIEW, DiffLevel  # type: ignore


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
    # Key in the index, str of the full path
    key: str
    # Name of the current node, not the key
    name: str
    # Path computed by DeepDiff, can be used to find the parent
    path: List[str]

    # Diffs for this node, leaf node
    diff_levels: List[DiffLevel] = field(default_factory=list)

    # Type of the node. If it has children it will represent the combination of all its children diff type.
    diff_type: DiffType = DiffType.UNCHANGED

    # Children of the node, the key of the dict is the name, not the full key.
    children: Dict[str, "TreeNode"] = field(default_factory=dict)

    def add_level(self, type: DiffType, level: DiffLevel):
        """Add a diff level to the current node, this means that this node contains a direct change (value change)."""
        self.update_type(type)
        self.diff_levels.append(level)

    def update_type(self, type: DiffType):
        """Update the type of a node by combine it with the current type."""
        self.diff_type = DiffType.combine(self.diff_type, type)


_ROOT_KEY: str = "[]"


class DeepDiffTreeViewer(ABC):
    """Object processing a DeepDiff object to render it in a specific format."""

    # Tree built from the ddiff and an index to access nodes in the tree quickly
    root: TreeNode
    index: Dict[str, TreeNode]

    def __init__(self, ddiff: DeepDiff):
        # TODO: process the ddiff
        self.index = {}
        self.index[_ROOT_KEY] = TreeNode(_ROOT_KEY, "root", [])
        self.root = self.index[_ROOT_KEY]

        self._compute_tree(ddiff)

    def _add_missing_nodes(self, path: List[str]):
        """Add missing nodes to the tree."""
        current: List[str] = []
        key = _ROOT_KEY
        for elem in path:
            parent: str = key
            current.append(elem)
            key = str(current)
            if key not in self.index:
                self.index[key] = TreeNode(key=key, name=elem, path=list(current))
                self.index[parent].children[elem] = self.index[key]

    def _update_parents(self, path: List[str], type: DiffType):
        """Update the status of parents of a node"""
        current = self.root
        for elem in path:
            current = current.children[elem]
            current.update_type(type)

    def _compute_tree(self, ddiff: DeepDiff):
        if ddiff.view != TREE_VIEW:
            raise AttributeError("DeepDiff object must use `tree` view to use the TreeViewer")
        dtype: str
        dvalues: List[DiffLevel]
        for dtype, dvalues in ddiff.items():
            diff_type = DiffType.UNCHANGED
            if "change" in dtype:
                diff_type = DiffType.MODIFIED
            elif "added" in dtype:
                diff_type = DiffType.ADDITION
            elif "removed" in dtype:
                diff_type = DiffType.DELETION

            # If there are changes, the root node is affected as it is the main parent
            self.root.diff_type = DiffType.combine(self.root.diff_type, diff_type)

            for diff_level in dvalues:
                path: List[str] = [str(e) for e in diff_level.path(output_format="list")]  # type: ignore
                self._add_missing_nodes(path)
                key = str(path)

                self.index[key].add_level(diff_type, diff_level)
                self._update_parents(path, diff_type)

    @abstractmethod
    def render(self) -> str | Any:
        """Render the tree in a viewable format. The Any type is used for rich outputs to give typing"""
        raise NotImplementedError()
