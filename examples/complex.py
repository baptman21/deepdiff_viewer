from datetime import datetime

from deepdiff import DeepDiff
from rich import print

from deepdiff_viewer.rich import RichViewer

t1 = {
    "int": 1,
    "change type": 42,
    "set": {
        "hello",
        "there",
    },
    "list": [1, 2, 3, 4],
    "multiline": """hello
there
!
""",
    "dict": {
        "a": 42,
        "b": 51,
        "c": {"x": 1, "y": 2},
    },
    "removed_dict": {
        "a": 21,
        "b": {"x": 1},
    },
    "date": datetime(2005, 12, 15, 9, 55, 0),
}
t2 = {
    "int": 2,
    "change type": "42",
    "set": {
        "world",
    },
    "list": [2, 3, 4, 5],
    "multiline": """hello

world
""",
    "dict": {
        "a": 21,
        "c": {"x": 1},
    },
    "new_dict": {
        "a": 21,
        "b": {"x": 1},
    },
    "date": datetime(2000, 12, 12, 14, 55, 0),
}

ddiff = DeepDiff(t1, t2, view="tree")
viewer = RichViewer(ddiff)
print(viewer.render())
