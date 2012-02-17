class ImmutableList(object):
    
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            self._head = args[0][0]
            if len(args[0]) > 1:
                self._tail = ImmutableList(args[0][1:])
            else: self._tail = None

        elif len(args) == 2 and isinstance(args[1], ImmutableList):
            self._head = args[0]
            self._tail = args[1]

    def conj(self, itm):
        return ImmutableList(itm, self)

    def first(self):
        return self._head

    def rest(self):
        return self._tail

    def second(self):
        if self._tail == None:
            return None
        return self._tail._head

    def __contains__(self, itm):
        if self._head == itm:
            return True
        return itm in self._tail

    def __iter__(self):
        node = self
        while node != None:
            yield node._head
            node = node._tail

    def __eq__(self, other):
        node = self
        
        for itm in other:
            if node is None:
                return False
            if node._head != itm:
                return False
            node = node._tail
        
        return True

    def __len__(self):
        if self._tail is None:
            return 1
        else:
            return 1 + len(self._tail)
        
