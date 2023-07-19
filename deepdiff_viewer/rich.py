try:
    import rich
except ImportError:
    raise ImportError("To use `deepdiff_viewer.rich` you must install rich, or use deepdiff_viewer[rich]")

try:
    from pydantic import BaseModel

    _as_pydantic_ = True
except ImportError:
    _as_pydantic_ = False

from datetime import datetime
from typing import Any, List

import yaml
from rich.columns import Columns
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
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
    def _render_value(
        value: Any,
        type: DiffType,
        is_right: bool,
    ) -> str | Any:
        # TODO: handle more cases for clearer render
        if isinstance(value, dict):
            return Panel.fit(
                Syntax(yaml.dump(value), "yaml"),
                title=Text("+ Added", "green") if is_right else Text("Removed", "red"),
                border_style=("green" if is_right else "red"),
            )
        if _as_pydantic_:
            if isinstance(value, BaseModel):
                return Panel.fit(
                    Syntax(yaml.dump(value.model_dump()), "yaml"),
                    title=Text("+ Added", "green") if is_right else Text("Removed", "red"),
                    border_style=("green" if is_right else "red"),
                )
        if isinstance(value, datetime):
            return Text(f"'{value}'", "yellow" if type == DiffType.MODIFIED else ("green" if is_right else "red"))
        if isinstance(value, str):
            return Text(f"'{value}'", "yellow" if type == DiffType.MODIFIED else ("green" if is_right else "red"))
        return Pretty(value)

    @staticmethod
    def _render_tree(node: TreeNode) -> str | Any:
        if len(node.children) != 0:
            out = Tree(Text.assemble(RichViewer._render_type(node.diff_type), node.name))

            for _, child in node.children.items():
                out.add(RichViewer._render_tree(child))

            return out

        if node.diff_type == DiffType.UNCHANGED:
            return Text("# unchanged", "grey31")

        if len(node.diff_levels) == 0:
            return Text.assemble(RichViewer._render_type(node.diff_type), node.name)

        renderables: List = [
            Text.assemble(RichViewer._render_type(node.diff_type), node.name, " = "),
        ]
        if node.diff_type == DiffType.DELETION or node.diff_type == DiffType.MODIFIED:
            renderables.append(RichViewer._render_value(node.diff_levels[0].t1, node.diff_type, False))
        if node.diff_type == DiffType.MODIFIED:
            renderables.append(Text(" -> "))
        if node.diff_type == DiffType.ADDITION or node.diff_type == DiffType.MODIFIED:
            renderables.append(RichViewer._render_value(node.diff_levels[0].t2, node.diff_type, True))

        col = Columns(renderables)
        return col

    def render(self) -> str | Any:
        return self._render_tree(self.root)
