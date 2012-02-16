from .lookuptree import LookupTree
from itertools import islice

class ImmutableVector(object):
    '''An immutable vector class. Access, appending, and removal are
    guaranteed to have O(log(n)) performance. The constructor takes the same
    arguments as the builtin list class.'''

    def __init__(self, initvalues=None):
        if initvalues is None: initvalues = []
        self.tree = LookupTree(initvalues)
        self._length = len(initvalues)

    def assoc(self, index, value):
        '''Return a new vector with value associated at index. The implicit
        parameter is not modified.'''
        newvec = ImmutableVector()
        newvec.tree = self.tree.assoc(index, value)
        if index >= self._length:
            newvec._length = index+1
        else:
            newvec._length = self._length
        return newvec

    def concat(self, tailvec):
        '''Returns the result of concatenating tailvec to the implicit
        parameter'''
        newvec = ImmutableVector()
        vallist = [(i + self._length, tailvec[i]) \
                for i in range(0, tailvec._length)]
        newvec.tree = self.tree.multi_assoc(vallist)
        newvec._length = self._length + tailvec._length
        return newvec

    def pop(self):
        '''Return a new ImmutableVector with the last item removed.'''
        if self._length == 0:
            raise IndexError()
        newvec = ImmutableVector()
        newvec.tree = self.tree.remove(self._length-1)
        newvec._length = self._length-1
        return newvec

    def conj(self, value):
        '''Return a new ImmutableVector with value appended to the
        end of the vector'''
        return self.assoc(self._length, value)

    def _get(self, index):
        if index >= self._length:
            raise IndexError
        return self.tree[index]

    def _slice(self, slc):
        lst = [val for val in islice(self, slc.start, slc.stop, slc.step)]
        return ImmutableVector(lst)

    def __add__(self, other):
        return self.concat(other)

    def __iter__(self):
        for i in range(0, self._length):
            yield self[i]

    def __len__(self):
        return self._length

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._slice(index)
        return self._get(index)

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return 'ImmutableVector('+str(self)+')'

    def __contains__(self, item):
        for thing in self:
            if thing == item:
                return True
        return False

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self[i] != other[i]:
                return False

        return True

