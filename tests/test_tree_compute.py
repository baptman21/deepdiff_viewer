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


def test_compute():
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


def test_compute_deep():
    """Compare the two configurations"""

    t1: Dict = {"a": {"b": {"c": 4}}, "b": {"b": {}}}
    t2: Dict = {"a": {"b": {"c": 2}}, "b": {"b": {"b": 4}}}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert "root" in viewer.index

    for key in ["['a']", "['a', 'b']", "['a', 'b', 'c']"]:
        assert key in viewer.index
        assert viewer.index[key].diff_type == DiffType.MODIFIED

    for key in ["['b']", "['b', 'b']", "['b', 'b', 'b']"]:
        assert key in viewer.index
        assert viewer.index[key].diff_type == DiffType.ADDITION

    assert viewer.root.diff_type == DiffType.MODIFIED


def test_compute_with_list():
    """Compare the two list"""

    t1: List = [1, 2, 3]
    t2: List = [1, 2]

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.DELETION


def test_compute_with_same():
    """Compare the two list"""

    t1: Dict = {"a": 3, "b": "2", "c": {"x": "general", "z": "kenobi"}}
    t2: Dict = dict(t1)

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.UNCHANGED


def test_compute_remove_from_dict():
    """Compare the two list"""

    t1: Dict = {"a": {"x": 1, "y": [1, 2]}}
    t2: Dict = {}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.DELETION


def test_compute_change_type():
    """Compare the two list"""

    t1: Dict = {"a": "1"}
    t2: Dict = {"a": 1}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.MODIFIED


def test_compute_list_to_dict():
    """Compare the two list"""

    t1: Dict = {"a": {"x": 1, "y": [1, 2]}}
    t2: Dict = {"a": [1, 1, 2]}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.MODIFIED


def test_compute_with_sets():
    """Compare the two list"""

    t1: Set = {1, 2, 3}
    t2: Set = {1, 2}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.DELETION


def test_compute_with_objects():
    """Compare the two list"""

    @dataclass()
    class ExampleA:
        a: int
        b: str

    t1: ExampleA = ExampleA(42, "hello there")
    t2: ExampleA = ExampleA(44, "general kenobi")

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = TestViewer(ddiff)

    assert viewer.root.key == "root"
    assert viewer.root.diff_type == DiffType.MODIFIED
    assert viewer.index["['a']"].diff_type == DiffType.MODIFIED
    assert viewer.index["['b']"].diff_type == DiffType.MODIFIED


def test_compute_not_tree_view():
    with pytest.raises(AttributeError, match="`tree` view"):
        ddiff = DeepDiff(None, None)
        TestViewer(ddiff)
