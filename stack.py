"""A list-backed stack ADT. Author: Emory Bruington."""


class Stack:
    """A Last-In, First-Out collection with a private list implementation."""

    def __init__(self):
        """Create an empty stack. No preconditions."""
        self._items = []

    def push(self, item):
        """Add item to the top. Amortized O(1); returns None."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top in O(1); raise IndexError when empty."""
        if self.is_empty():
            raise IndexError('Cannot pop an empty stack.')
        return self._items.pop()

    def peek(self):
        """Return the top without mutation; raise IndexError when empty."""
        if self.is_empty():
            raise IndexError('Cannot peek at an empty stack.')
        return self._items[-1]

    def is_empty(self):
        """Return True exactly when there are no items. O(1)."""
        return not self._items

    def size(self):
        """Return the number of items. O(1)."""
        return len(self._items)


def _run_tests():
    """Run the module's assertion tests; importing this module runs no tests."""
    stack = Stack()
    assert stack.is_empty() and stack.size() == 0
    stack.push(10)
    assert not stack.is_empty() and stack.size() == 1
    assert stack.peek() == 10 and stack.size() == 1
    stack.push(20)
    stack.push(30)
    assert stack.size() == 3
    assert [stack.pop(), stack.pop(), stack.pop()] == [30, 20, 10]
    assert stack.is_empty() and stack.size() == 0
    for method, message in [(stack.pop, 'Cannot pop'), (stack.peek, 'Cannot peek')]:
        try:
            method()
        except IndexError as error:
            assert message in str(error)
        else:
            raise AssertionError('Empty stack operation did not raise IndexError.')
        assert stack.is_empty() and stack.size() == 0
    token = object()
    stack.push(token)
    assert stack.peek() is token and stack.pop() is token
    other = Stack()
    stack.push(None)
    assert stack.size() == 1 and other.is_empty()
    print('Stack: all 10 test cases passed.')


if __name__ == '__main__':
    _run_tests()
