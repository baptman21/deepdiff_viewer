from deepdiff import DeepDiff  # type: ignore
from pydantic import BaseModel
from rich import print

from deepdiff_viewer.rich import RichViewer


class Example(BaseModel):
    a: str
    b: int


t1 = {"modified": Example(a="hello", b=21), "removed": Example(a="hello", b=21)}
t2 = {"modified": Example(a="there", b=42), "added": Example(a="world", b=42)}


ddiff = DeepDiff(t1, t2, view="tree")
viewer = RichViewer(ddiff)
print(viewer.render())
