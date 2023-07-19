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
from deepdiff.diff import DiffLevel  # type: ignore
from rich.columns import Columns
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
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
        was_value_added: bool,
    ) -> str | Any:
        # TODO: handle more cases for clearer render
        if isinstance(value, dict):
            return Panel.fit(
                Syntax(yaml.dump(value), "yaml"),
                title=Text("+ Added", "green") if was_value_added else Text("- Removed", "red"),
                border_style=("green" if was_value_added else "red"),
            )
        if _as_pydantic_:
            if isinstance(value, BaseModel):
                return Panel.fit(
                    Syntax(yaml.dump(value.model_dump()), "yaml"),
                    title=Text("+ Added", "green") if was_value_added else Text("- Removed", "red"),
                    border_style=("green" if was_value_added else "red"),
                )
        if isinstance(value, datetime):
            return Text(
                f"'{value}'", "yellow" if type == DiffType.MODIFIED else ("green" if was_value_added else "red")
            )
        if isinstance(value, str):
            return Text(
                f"'{value}'", "yellow" if type == DiffType.MODIFIED else ("green" if was_value_added else "red")
            )
        return Pretty(value)

    @staticmethod
    def _render_diff_level(node: TreeNode, diff_level: DiffLevel) -> str | Any:
        # Special case for text diff
        if diff_level.additional and "diff" in diff_level.additional:
            return Panel(
                Syntax(diff_level.additional["diff"], "diff"),
                title=RichViewer._render_node_name(node),
                expand=False,
            )
        # Special case for the set to make the diff more redable
        if diff_level.report_type == "set_item_added":
            return Columns(
                [
                    RichViewer._render_type(DiffType.ADDITION),
                    RichViewer._render_value(diff_level.t2, DiffType.ADDITION, True),
                ]
            )
        if diff_level.report_type == "set_item_removed":
            return Columns(
                [
                    RichViewer._render_type(DiffType.DELETION),
                    RichViewer._render_value(diff_level.t1, DiffType.DELETION, False),
                ]
            )

        renderables: List = [
            Text.assemble(RichViewer._render_type(node.diff_type), node.name, " = "),
        ]

        if str(diff_level.report_type).startswith("iterable_item"):
            renderables = [
                Text.assemble(RichViewer._render_type(node.diff_type), "at [", node.name, "]: "),
            ]

        if node.diff_type == DiffType.DELETION or node.diff_type == DiffType.MODIFIED:
            renderables.append(RichViewer._render_value(diff_level.t1, node.diff_type, False))

        if node.diff_type == DiffType.MODIFIED:
            renderables.append(Text(" -> "))

        if node.diff_type == DiffType.ADDITION or node.diff_type == DiffType.MODIFIED:
            renderables.append(RichViewer._render_value(diff_level.t2, node.diff_type, True))

        col = Columns(renderables)
        return col

    @staticmethod
    def _render_node_name(node) -> str | Any:
        return Text.assemble(RichViewer._render_type(node.diff_type), node.name)

    @staticmethod
    def _render_tree(node: TreeNode) -> str | Any:
        if len(node.children) != 0:
            out = Tree(RichViewer._render_node_name(node))

            for _, child in node.children.items():
                out.add(RichViewer._render_tree(child))

            return out

        if node.diff_type == DiffType.UNCHANGED:
            return Text("# unchanged", "grey31")

        if len(node.diff_levels) == 0:
            return RichViewer._render_node_name(node)

        if len(node.diff_levels) == 1:
            return RichViewer._render_diff_level(node, node.diff_levels[0])

        table = Table(box=None, show_header=False)
        for diff_level in node.diff_levels:
            table.add_row(RichViewer._render_diff_level(node, diff_level))

        return table

    def render(self) -> str | Any:
        return self._render_tree(self.root)
