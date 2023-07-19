from dataclasses import dataclass
from typing import Dict, List, Set

import pytest
from deepdiff import DeepDiff  # type: ignore

from deepdiff_viewer.base import DeepDiffTreeViewer, DiffType


class TestViewer(DeepDiffTreeViewer):
    """The DeepDiffTreeViewer is abstract but we need to test the compute tree function.
    We use this test class to do it."""

    __test__ = False

    def render(self) -> str:
        raise NotImplementedError("Class only used to test the tree building")


def test_diff():
    """Compare the two configurations"""

    t1: Dict = {"a": 1}
    t2: Dict = {"a": 3}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert "root" in viewer.index

    root_a_key = "['a']"
    assert root_a_key in viewer.index

    assert viewer.root.key == "root"
    assert len(viewer.root.children) == 1

    root_a = viewer.root.children[root_a_key]

    assert root_a.key == root_a_key
    assert len(root_a.children) == 0

    assert viewer.root.diff_type == DiffType.MODIFIED
    assert root_a.diff_type == DiffType.MODIFIED
