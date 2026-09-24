from __future__ import annotations

import pytest

from main import (
    Request,
    TreeNode,
    REQUESTS,
    insert,
    delete,
    preorder,
    inorder,
    postorder,
    level_order,
    search,
    find_min,
    find_max,
    count_nodes,
    count_leaves,
    height,
    get_depth,
    validate_bst,
    sift_down,
    build_max_heap,
    is_max_heap,
    heap_sort,
    build_initial_tree,
    _key,
)


@pytest.fixture
def root():
    return build_initial_tree()


def test_initial_level_order(root):
    assert [r.id for r in level_order(root)] == [
        50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90
    ]


def test_preorder(root):
    assert [r.id for r in preorder(root)] == [
        50, 30, 20, 10, 25, 40, 35, 45, 70, 60, 55, 65, 80, 75, 90
    ]


def test_inorder(root):
    assert [r.id for r in inorder(root)] == [
        10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90
    ]


def test_postorder(root):
    assert [r.id for r in postorder(root)] == [
        10, 25, 20, 35, 45, 40, 30, 55, 65, 60, 75, 90, 80, 70, 50
    ]


def test_inorder_returns_sorted_ids(root):
    ids = [r.id for r in inorder(root)]
    assert ids == sorted(ids)


def test_count_nodes(root):
    assert count_nodes(root) == 15


def test_count_leaves(root):
    assert count_leaves(root) == 8


def test_height(root):
    assert height(root) == 4


def test_height_empty():
    assert height(None) == 0


def test_height_single():
    assert height(TreeNode(Request(1, "a", 1))) == 1


def test_find_min_max(root):
    assert find_min(root).id == 10
    assert find_max(root).id == 90


def test_search_existing(root):
    found, path = search(root, 65)
    assert found is not None
    assert found.id == 65
    assert path == [50, 70, 60, 65]


def test_search_missing(root):
    found, path = search(root, 99)
    assert found is None
    assert path == [50, 70, 80, 90]


def test_get_depth(root):
    assert get_depth(root, 65) == 3
    assert get_depth(root, 50) == 0
    assert get_depth(root, 99) == -1


def test_validate_bst_true(root):
    assert validate_bst(root) is True


def test_validate_bst_false():
    a = TreeNode(Request(10, "a", 1))
    b = TreeNode(Request(5, "b", 1))
    c = TreeNode(Request(20, "c", 1))
    a.left = b
    a.right = c
    b.right = TreeNode(Request(15, "d", 1))
    assert validate_bst(a) is False


def test_insert_duplicate_ignored(root):
    before = count_nodes(root)
    root = insert(root, Request(50, "Дубликат", 99))
    assert count_nodes(root) == before


def test_delete_leaf(root):
    root = delete(root, 10)
    assert search(root, 10)[0] is None
    assert validate_bst(root)


def test_delete_one_child(root):
    root = insert(root, Request(37, "Утечка данных", 16))
    root = delete(root, 35)
    assert search(root, 35)[0] is None
    assert validate_bst(root)


def test_delete_two_children(root):
    root = delete(root, 70)
    assert search(root, 70)[0] is None
    assert validate_bst(root)


def test_delete_root(root):
    root = delete(root, 50)
    assert search(root, 50)[0] is None
    assert validate_bst(root)


def test_delete_missing(root):
    before = [r.id for r in inorder(root)]
    root = delete(root, 999)
    assert [r.id for r in inorder(root)] == before


def test_final_state_after_all_deletions(root):
    root = insert(root, Request(37, "Утечка данных", 16))
    root = insert(root, Request(50, "Ошибка оплаты", 9))
    root = delete(root, 10)
    root = delete(root, 35)
    root = delete(root, 70)
    root = delete(root, 999)
    assert [r.id for r in inorder(root)] == [
        20, 25, 30, 37, 40, 45, 50, 55, 60, 65, 75, 80, 90
    ]
    assert count_nodes(root) == 13
    assert height(root) == 4


def test_heap_key_order():
    a = Request(1, "a", 5)
    b = Request(2, "b", 5)
    assert _key(b) > _key(a)


def test_build_max_heap_property():
    data = list(REQUESTS)
    build_max_heap(data)
    assert is_max_heap(data)


def test_build_max_heap_expected_array():
    data = inorder(build_initial_tree())
    build_max_heap(data)
    expected = [
        (37, 16), (75, 14), (80, 15), (60, 11), (65, 12),
        (45, 8), (50, 9), (55, 10), (25, 3), (20, 2),
        (40, 7), (30, 4), (90, 6),
    ]
    assert [_key(r) for r in data] == expected


def test_is_max_heap_false():
    data = [Request(1, "a", 1), Request(2, "b", 5)]
    assert is_max_heap(data) is False


def test_sift_down():
    data = [Request(1, "a", 1), Request(2, "b", 5), Request(3, "c", 3)]
    sift_down(data, len(data), 0)
    assert is_max_heap(data)


def test_heap_sort_ascending():
    data = list(REQUESTS)
    heap_sort(data)
    keys = [_key(r) for r in data]
    assert keys == sorted(keys)


def test_heap_sort_empty_and_single():
    empty: list[Request] = []
    heap_sort(empty)
    assert empty == []

    single = [Request(1, "a", 1)]
    heap_sort(single)
    assert len(single) == 1