from deepdiff_viewer.base import DiffType


def test_diff_type_combine_same():
    assert DiffType.combine(DiffType.UNCHANGED, DiffType.UNCHANGED) == DiffType.UNCHANGED
    assert DiffType.combine(DiffType.ADDITION, DiffType.ADDITION) == DiffType.ADDITION
    assert DiffType.combine(DiffType.DELETION, DiffType.DELETION) == DiffType.DELETION


def test_diff_type_combine_opposite():
    assert DiffType.combine(DiffType.DELETION, DiffType.ADDITION) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.DELETION, DiffType.ADDITION) == DiffType.MODIFIED


def test_diff_type_combine_modified_wins():
    assert DiffType.combine(DiffType.MODIFIED, DiffType.UNCHANGED) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.MODIFIED, DiffType.ADDITION) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.MODIFIED, DiffType.DELETION) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.MODIFIED, DiffType.MODIFIED) == DiffType.MODIFIED

    assert DiffType.combine(DiffType.UNCHANGED, DiffType.MODIFIED) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.ADDITION, DiffType.MODIFIED) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.DELETION, DiffType.MODIFIED) == DiffType.MODIFIED
    assert DiffType.combine(DiffType.MODIFIED, DiffType.MODIFIED) == DiffType.MODIFIED
