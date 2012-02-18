class ImmutableList(object):
    
    def __init__(self, *args):
        if len(args) == 0:
            self._empty = True
            self._head = None
            self._tail = None

        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            self._head = args[0][0]
            if len(args[0]) > 1:
                self._tail = ImmutableList(args[0][1:])
            else: self._tail = ImmutableList()
            self._empty = False

        elif len(args) == 2 and isinstance(args[1], ImmutableList):
            self._head = args[0]
            self._tail = args[1]
            self._empty = False

    def conj(self, itm):
        return ImmutableList(itm, self)

    def first(self):
        return self._head

    def rest(self):
        if self._empty:
            return self
        return self._tail

    def second(self):
        if self._empty:
            return None
        return self._tail._head

    def __contains__(self, itm):
        if self._empty:
            return False
        if self._head == itm:
            return True
        return itm in self._tail

    def __iter__(self):
        node = self
        while not node._empty:
            yield node._head
            node = node._tail

    def __eq__(self, other):
        if other is None:
            return False

        if not hasattr(other, '__iter__'):
            return False

        node = self
        
        for itm in other:
            if node._empty:
                return False
            if node._head != itm:
                return False
            node = node._tail
        
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        if self._empty:
            return 0
        else:
            return 1 + len(self._tail)

    def __str__(self):
        return '[' + ', '.join([str(x) for x in self]) + ']'

    def __repr__(self):
        return 'ImmutableList(' + str(self) + ')'
        
