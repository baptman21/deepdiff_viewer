from dataclasses import dataclass
from typing import Dict, List, Set

from deepdiff import DeepDiff
from rich import print

from deepdiff_viewer.rich import RichViewer


def test_simple_diff():
    t1: Dict = {"a": 1}
    t2: Dict = {"a": 3}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_compute_deep():
    """Compare the two configurations"""

    t1: Dict = {"a": {"b": {"c": 4}}, "b": {"b": {}}}
    t2: Dict = {"a": {"b": {"c": 2}}, "b": {"b": {"b": 4}}}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_with_list():
    """Compare the two list"""

    t1: List = [1, 2, 3]
    t2: List = [1, 2]

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_with_same():
    """Compare the two list"""

    t1: Dict = {"a": 3, "b": "2", "c": {"x": "general", "z": "kenobi"}}
    t2: Dict = dict(t1)

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_remove_from_dict():
    """Compare the two list"""

    t1: Dict = {"a": {"x": 1, "y": [1, 2]}}
    t2: Dict = {}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_change_type():
    """Compare the two list"""

    t1: Dict = {"a": "1"}
    t2: Dict = {"a": 1}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_dict_to_list():
    """Compare the two list"""

    t1: Dict = {"a": {"x": 1, "y": [1, 2]}}
    t2: Dict = {"a": [1, 1, 2]}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_with_sets():
    """Compare the two list"""

    t1: Set = {1, 2, 3}
    t2: Set = {1, 2}

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())


def test_render_rich_with_objects():
    """Compare the two list"""

    @dataclass
    class ExampleA:
        a: int
        b: str

    t1: ExampleA = ExampleA(42, "hello there")
    t2: ExampleA = ExampleA(44, "general kenobi")

    ddiff = DeepDiff(t1, t2, view="tree")
    viewer = RichViewer(ddiff)
    print(viewer.render())
