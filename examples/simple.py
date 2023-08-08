from deepdiff import DeepDiff
from rich import print

from deepdiff_viewer.rich import RichViewer

t1 = {"a": 1}
t2 = {"a": 3}

ddiff = DeepDiff(t1, t2, view="tree")
viewer = RichViewer(ddiff)
print(viewer.render())
