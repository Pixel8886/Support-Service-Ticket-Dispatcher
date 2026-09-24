from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class Request:
    id: int
    title: str
    priority: int

    def __repr__(self) -> str:
        return f"{self.id}({self.priority})"


@dataclass
class TreeNode:
    request: Request
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


REQUESTS: list[Request] = [
    Request(50, "Ошибка оплаты", 9),
    Request(30, "Сброс пароля", 4),
    Request(70, "Интеграция API", 13),
    Request(20, "Изменение профиля", 2),
    Request(40, "Ошибка отчёта", 7),
    Request(60, "Настройка уведомлений", 11),
    Request(80, "Сбой сервера", 15),
    Request(10, "Удаление аккаунта", 1),
    Request(25, "Проблема входа", 3),
    Request(35, "Экспорт данных", 5),
    Request(45, "Возврат платежа", 8),
    Request(55, "Подключение тарифа", 10),
    Request(65, "Ошибка синхронизации", 12),
    Request(75, "Недоступна база данных", 14),
    Request(90, "Обновление реквизитов", 6),
]


def insert(root: Optional[TreeNode], request: Request) -> TreeNode:
    if root is None:
        return TreeNode(request)
    if request.id < root.request.id:
        root.left = insert(root.left, request)
    elif request.id > root.request.id:
        root.right = insert(root.right, request)
    return root


def delete(root: Optional[TreeNode], request_id: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if request_id < root.request.id:
        root.left = delete(root.left, request_id)
    elif request_id > root.request.id:
        root.right = delete(root.right, request_id)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = root.right
        while successor.left is not None:
            successor = successor.left
        root.request = successor.request
        root.right = delete(root.right, successor.request.id)
    return root


def preorder(root: Optional[TreeNode]) -> list[Request]:
    if root is None:
        return []
    return [root.request] + preorder(root.left) + preorder(root.right)


def inorder(root: Optional[TreeNode]) -> list[Request]:
    if root is None:
        return []
    return inorder(root.left) + [root.request] + inorder(root.right)


def postorder(root: Optional[TreeNode]) -> list[Request]:
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.request]


def level_order(root: Optional[TreeNode]) -> list[Request]:
    if root is None:
        return []
    result: list[Request] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.request)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


def search(root: Optional[TreeNode], request_id: int) -> tuple[Optional[Request], list[int]]:
    path: list[int] = []
    node = root
    while node is not None:
        path.append(node.request.id)
        if request_id == node.request.id:
            return node.request, path
        node = node.left if request_id < node.request.id else node.right
    return None, path


def find_min(root: TreeNode) -> Request:
    while root.left is not None:
        root = root.left
    return root.request


def find_max(root: TreeNode) -> Request:
    while root.right is not None:
        root = root.right
    return root.request


def count_nodes(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaves(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)


def height(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def get_depth(root: Optional[TreeNode], request_id: int) -> int:
    depth = 0
    node = root
    while node is not None:
        if request_id == node.request.id:
            return depth
        node = node.left if request_id < node.request.id else node.right
        depth += 1
    return -1


def validate_bst(root: Optional[TreeNode]) -> bool:
    def check(node: Optional[TreeNode],
              low: Optional[int],
              high: Optional[int]) -> bool:
        if node is None:
            return True
        if low is not None and node.request.id <= low:
            return False
        if high is not None and node.request.id >= high:
            return False
        return (check(node.left, low, node.request.id)
                and check(node.right, node.request.id, high))
    return check(root, None, None)


def _key(req: Request) -> tuple[int, int]:
    return (req.priority, req.id)


def sift_down(data: list[Request], heap_size: int, index: int) -> None:
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2
    if left < heap_size and _key(data[left]) > _key(data[largest]):
        largest = left
    if right < heap_size and _key(data[right]) > _key(data[largest]):
        largest = right
    if largest != index:
        data[index], data[largest] = data[largest], data[index]
        sift_down(data, heap_size, largest)


def build_max_heap(data: list[Request]) -> None:
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(data, n, i)


def is_max_heap(data: list[Request]) -> bool:
    n = len(data)
    for i in range(n // 2):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and _key(data[left]) > _key(data[i]):
            return False
        if right < n and _key(data[right]) > _key(data[i]):
            return False
    return True


def heap_sort(data: list[Request]) -> None:
    build_max_heap(data)
    for end in range(len(data) - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        sift_down(data, end, 0)


def _fmt(requests: list[Request]) -> str:
    return ", ".join(repr(r) for r in requests)


def _ids(requests: list[Request]) -> str:
    return ", ".join(str(r.id) for r in requests)


def build_initial_tree() -> TreeNode:
    root: Optional[TreeNode] = None
    for req in REQUESTS:
        root = insert(root, req)
    assert root is not None
    return root


def stage_1() -> TreeNode:
    print("=" * 60)
    print("ЭТАП 1. Построение бинарного дерева поиска")
    print("=" * 60)
    root = build_initial_tree()
    print("Уровневый обход:", _fmt(level_order(root)))
    return root


def stage_2(root: TreeNode) -> None:
    print()
    print("=" * 60)
    print("ЭТАП 2. Обходы дерева")
    print("=" * 60)
    print("Прямой обход:       ", _ids(preorder(root)))
    print("Симметричный обход: ", _ids(inorder(root)))
    print("Обратный обход:     ", _ids(postorder(root)))
    print("Уровневый обход:    ", _ids(level_order(root)))


def stage_3(root: TreeNode) -> None:
    print()
    print("=" * 60)
    print("ЭТАП 3. Поиск и анализ дерева")
    print("=" * 60)

    found, path = search(root, 65)
    print(f"Поиск 65: найдено = {found}, путь = {path}")

    found, path = search(root, 99)
    print(f"Поиск 99: найдено = {found}, путь = {path}")

    print("Количество узлов:  ", count_nodes(root))
    print("Количество листьев:", count_leaves(root))
    print("Высота дерева:     ", height(root))
    print("Минимальный ID:    ", find_min(root).id)
    print("Максимальный ID:   ", find_max(root).id)
    print("Глубина узла 65:   ", get_depth(root, 65))
    print("validate_bst():    ", validate_bst(root))


def _print_state(root: Optional[TreeNode], name: str) -> None:
    print(f"--- {name} ---")
    if root is None:
        print("Симметричный обход: []")
        print("Количество узлов:  0")
        print("Высота дерева:     0")
        print("validate_bst():    True")
        return
    print("Симметричный обход:", _ids(inorder(root)))
    print("Количество узлов:  ", count_nodes(root))
    print("Высота дерева:     ", height(root))
    print("validate_bst():    ", validate_bst(root))


def stage_4(root: TreeNode) -> TreeNode:
    print()
    print("=" * 60)
    print("ЭТАП 4. Изменение дерева")
    print("=" * 60)

    root = insert(root, Request(37, "Утечка данных", 16))
    _print_state(root, "Добавлена заявка 37 (Утечка данных, 16)")

    root = insert(root, Request(50, "Ошибка оплаты", 9))
    _print_state(root, "Попытка повторно добавить 50 (дубликат)")

    root = delete(root, 10)
    _print_state(root, "Удалён узел 10 (лист)")

    root = delete(root, 35)
    _print_state(root, "Удалён узел 35 (один потомок)")

    root = delete(root, 70)
    _print_state(root, "Удалён узел 70 (два потомка)")

    root = delete(root, 999)
    _print_state(root, "Попытка удалить отсутствующий узел 999")

    return root


def stage_5(root: TreeNode) -> list[Request]:
    print()
    print("=" * 60)
    print("ЭТАП 5. Построение двоичной кучи")
    print("=" * 60)

    data: list[Request] = inorder(root)
    print("Исходный массив:        ", _fmt(data))

    build_max_heap(data)
    print("Массив после build_heap:", _fmt(data))
    print("Элементы по уровням:    ", _fmt(data))
    print("is_max_heap():          ", is_max_heap(data))

    return data


def stage_6(data: list[Request]) -> None:
    print()
    print("=" * 60)
    print("ЭТАП 6. Сортировка кучей")
    print("=" * 60)
    print("До сортировки: ", _fmt(data))
    heap_sort(data)
    print("После сортировки:", _fmt(data))


def main() -> None:
    root = stage_1()
    stage_2(root)
    stage_3(root)
    root = stage_4(root)
    data = stage_5(root)
    stage_6(data)


if __name__ == "__main__":
    main()