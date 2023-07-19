try:
    import rich
except ImportError:
    raise ImportError("To use `deepdiff_viewer.rich` you must install rich, or use deepdiff_viewer[rich]")

from typing import Any, List

from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

from .base import DeepDiffTreeViewer, DiffType, TreeNode


class RichViewer(DeepDiffTreeViewer):
    @staticmethod
    def _render_type(type: DiffType) -> str | Text:
        if type == DiffType.UNCHANGED:
            return ""
        if type == DiffType.ADDITION:
            return Text("+ ", "green")
        if type == DiffType.DELETION:
            return Text("- ", "red")
        if type == DiffType.MODIFIED:
            return Text("~ ", "yellow")
        raise NotImplementedError("unknown value")

    @staticmethod
    def _render_tree(node: TreeNode) -> str | Any:
        if len(node.children) != 0:
            out = Tree(node.name)

            for _, child in node.children.items():
                out.add(RichViewer._render_tree(child))

            return out

        if node.diff_type == DiffType.UNCHANGED:
            return Text("# unchanged", "grey31")

        renderables: List = [
            Text.assemble(RichViewer._render_type(node.diff_type), node.name, " = "),
        ]
        if node.diff_type == DiffType.DELETION or node.diff_type == DiffType.MODIFIED:
            renderables.append("old")
        if node.diff_type == DiffType.MODIFIED:
            renderables.append(Text(" -> "))
        if node.diff_type == DiffType.ADDITION or node.diff_type == DiffType.MODIFIED:
            renderables.append("new")

        col = Columns(renderables)
        return col

    def render(self) -> str | Any:
        return self._render_tree(self.root)
