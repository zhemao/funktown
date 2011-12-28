class LookupTreeNode(object):
    def __init__(self, index=-1, value=None):
        self.children = [None] * 32
        self.index = index
        self.value = value

    def __iter__(self):
        if self.index == -1:
            for child in self.children:
                if child is None:
                    continue
                if child.index == -1:
                    for value in child:
                        yield value
                else: yield child.value


class LookupTree(object):
    '''A lookup tree with a branching factor of 32. The constructor
    takes an argument initvalues, which can either be a list of values
    or a dictionary mapping indices to values.'''
    def __init__(self, initvalues=None):
        self.root = LookupTreeNode()
        if initvalues is None:
            pass
        elif isinstance(initvalues, dict):
            for key,val in initvalues.items():
                self.insert(key, val)
        else:
            for i,val in enumerate(initvalues):
                self.insert(i, val)

    def get(self, index):
        '''Like tree[index], but returns None if index not found'''
        try:
            return self[index]
        except KeyError:
            return None

    def __getitem__(self, index):
        '''Find the value of the node with the given index'''
        node = self.root
        level = 0
        while node and node.index == -1:
            i = _getbits(index, level)
            node = node.children[i]
            level += 1

        if node is not None and node.index == index:
            return node.value
        else:
            raise KeyError(index)

    def assoc(self, index, value):
        '''Return a new tree with value associated at index.'''
        newnode = LookupTreeNode(index, value)
        newtree = LookupTree()
        newtree.root = _assoc_down(self.root, newnode, 0)
        return newtree

    def multi_assoc(self, values):
        '''Return a new tree with multiple values associated. The parameter
        values can either be a dictionary mapping indices to values, or a list
        of (index,value) tuples'''
        if isinstance(values, dict):
            nndict = dict([(i, LookupTreeNode(i, values[i])) for i in values])
        else:
            nndict = dict([(i, LookupTreeNode(i, val)) for (i,val) in values])
        newtree = LookupTree()
        newtree.root = _multi_assoc_down(self.root, nndict, 0)
        return newtree

    def remove(self, index):
        '''Return new tree with index removed.'''
        newtree = LookupTree()
        newtree.root = _remove_down(self.root, index, 0)
        return newtree

    def insert(self, index, value):
        '''Insert a node in-place. It is highly suggested that you do not
        use this method. Use assoc instead'''
        newnode = LookupTreeNode(index, value)
        level = 0
        node = self.root
        while True:
            ind = _getbits(newnode.index, level)
            level += 1
            child = node.children[ind]
            if child is None or child.index == newnode.index:
                node.children[ind] = newnode
                break
            elif child.index == -1:
                node = child
            else:
                branch = LookupTreeNode()
                nind = _getbits(newnode.index, level)
                cind = _getbits(child.index, level)
                node.children[ind] = branch
                branch.children[nind] = newnode
                branch.children[cind] = child
                break

    def __iter__(self):
        return iter(self.root)


def _assoc_down(node, newnode, level):
    ind = _getbits(newnode.index, level)
    copynode = LookupTreeNode()
    for i,child in enumerate(node.children):
        if i != ind:
            copynode.children[i] = child
    child = node.children[ind]
    if child is None or child.index == newnode.index:
        copynode.children[ind] = newnode
    elif child.index == -1:
        copynode.children[ind] = _assoc_down(child, newnode, level+1)
    else:
        branch = LookupTreeNode()
        copynode.children[ind] = branch
        level+=1
        cind = _getbits(child.index, level)
        nind = _getbits(newnode.index, level)
        branch.children[cind] = child
        branch.children[nind] = newnode
    return copynode

def _multi_assoc_down(node, nndict, level):
    indices = set([_getbits(index, level) for index in nndict])
    copynode = LookupTreeNode()
    for i,child in enumerate(node.children):
        if i not in indices:
            copynode.children[i] = child

    for ind in indices:
        subnndict = dict([(i,nndict[i]) for i in nndict \
                        if ind == (i >> level * 5) & 31])
        child = node.children[ind]
        if child is None or child.index in subnndict:
            if len(subnndict) == 1:
                values = [val for val in subnndict.values()]
                copynode.children[ind] = values[0]
            else:
                branch = LookupTreeNode()
                copynode.children[ind] = \
                    _multi_assoc_down(branch, subnndict, level+1)
        elif child.index == -1:
            copynode.children[ind] = \
                _multi_assoc_down(node, subnndict, level+1)
        else:
            branch = LookupTreeNode()
            copynode.children[ind] = \
                _multi_assoc_down(branch, subnndict, level+1)

    return copynode

def _remove_down(node, index, level):
    ind = _getbits(index, level)

    if node.children[ind] is None:
        return node

    copynode = LookupTreeNode()

    for i,child in enumerate(node.children):
        if i != ind:
            copynode.children[i] = child

    child = node.children[ind]

    if child.index == index:
        copynode.children[ind] = None
    elif child.index == -1:
        copynode.children[ind] = _remove_down(child, index, level+1)
    else:
        return node

    return copynode

def _getbits(num, level):
    return (num >> 5 * level) & 31
