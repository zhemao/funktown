from .lookuptree import LookupTree
from collections import defaultdict

class ImmutableDict(object):
    '''An immutable dictionary class. Access, insertion, and removal
    are guaranteed to have O(log(n)) performance. Constructor takes same
    arguments as builtin dict'''

    def __init__(self, initdict=None, **kwargs):
        if initdict is None: initdict = {}
        initdict.update(kwargs)
        hashlist = [(hash(key), [(key, initdict[key])]) for key in initdict]
        self.tree = LookupTree(dict(hashlist))
        self._length = len(initdict)

    def _add_to_list(self, lst, key, val):
        found = False
            
        for i, item in enumerate(lst):
            k,v = item
            if key == k:
                lst[i] = (key, value)
                found = True
                break
        
        if not found:
            lst.append((key, value))
        
    def assoc(self, key, value):
        '''Returns a new ImmutableDict instance with value associated with key.
        The implicit parameter is not modified.'''
        
        oldlst = self.tree.get(hash(key))
        if not oldlst:
            oldlst = []
            newlst = [(key, value)]
        else:
            newlst = list(oldlst)
            self._add_to_list(newlst, key, value)

        copydict = ImmutableDict()
        copydict.tree = self.tree.assoc(hash(key), newlst)
        copydict._length = self._length + len(newlst) - len(oldlst)

        return copydict

    def update(self, other=None, **kwargs):
        '''Takes the same arguments as the update method in the builtin dict
        class. However, this version returns a new ImmutableDict instead of
        modifying in-place.'''
        copydict = ImmutableDict()
        fulldict = {}
        
        if other:
            fulldict.update(other)
        if kwargs:
            fulldict.update(kwargs)

        valdict = {}

        for key in fulldict:
            h = hash(key)
            if h in valdict:
                self._add_to_list(valdict[h], key, fulldict[key])
            else:
                oldlst = self.tree.get(h)
                if oldlst:
                    newlst = list(oldlst)
                    self._add_to_list(newlst, key, fulldict[key])
                    valdict[h] = newlst
                else:
                    valdict[h] = [(key, fulldict[key])]

        copydict.tree = self.tree.multi_assoc(valdict)
        copydict._length = iter_length(copydict.tree)
        return copydict

    def remove(self, key):
        '''Returns a new ImmutableDict with the given key removed.'''
        oldlst = self.tree.get(hash(key))
        if not oldlst:
            return self

        copydict = ImmutableDict()

        newlst = [(k, v) for (k, v) in oldlst if key != k]

        if len(newlst) == 0:
            copydict.tree = self.tree.remove(hash(key))
            copydict._length = self._length - 1
        else:
            copydict.tree = self.tree.assoc(hash(key), newlst)
            copydict._length = self._length + len(newlst) - len(oldlst)

        return copydict

    def get(self, key):
        '''Same as get method in builtin dict.'''
        try:
            return self[key]
        except KeyError: return None

    def __len__(self):
        return self._length

    def __getitem__(self, key):
        try:
            lst = self.tree[hash(key)]    
        except KeyError: raise KeyError(key)
        
        for k,v in lst:
            if key == k:
                return v
        raise KeyError(key)

    def __iter__(self):
        for lst in self.tree:
            for key, val in lst:
                yield key

    def keys(self):
        '''Same as keys method in dict builtin.'''

        return [key for (key,val) in self.items()]

    def values(self):
        '''Same as values method in dict builtin.'''
        return [val for (key,val) in self.items()]

    def items(self):
        '''Same as items method in dict builtin.'''
        itmlst = []

        for lst in self.tree:
            itmlst.extend(itm for itm in lst)
        
        return itmlst

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return 'ImmutableDict('+str(self)+')'

    def __contains__(self, key):
        try:
            self.tree[hash(key)]
            return True
        except KeyError: return False

    def __eq__(self, other):
        if other is None:
            return False

        if not hasattr(other, '__getitem__'):
            return False

        if len(self) != len(other):
            return False

        for key in self:
            if self[key] != other[key]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

def iter_length(iterable):
    try:
        return len(iterable)
    except:
        i = 0
        for x in iterable:
            i+=1
        return i
