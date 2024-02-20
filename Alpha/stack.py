class StackLL:

    class _Node:
        __slot__ = "key", "_next"

        def __init__(self, key, next) -> None:
            self.key = key
            self.next = next

    def __init__(self) -> None:
        self._head = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def push(self, key):
        """Push an element into stack

        Args:
            key (Any): key

        Returns:
            Stack.Node: The added node
        """
        self._head = self._Node(key, self._head)
        self._size += 1
        return self._head

    def top(self):
        """Return the head node

        Returns:
            Stack.Node:
        """
        return self._head

    def pop(self):
        """Remove and return the key

        Raises:
            IndexError: Stack is empty

        Returns:
            key_type: The head node
        """
        if not self._head:
            raise IndexError("Stack is empty")

        old = self._head.key
        self._head = self._head.next

        self._size -= 1

        return old
