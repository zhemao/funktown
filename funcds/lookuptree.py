class LookupTreeNode:
	def __init__(self, index=-1, value=None):
		self.children = [None]*32
		self.index = index
		self.value = value

class LookupTree:
	def __init__(self, initvalues=None):
		self.root = LookupTreeNode()
		if initvalues == None: pass
		elif isinstance(initvalues, dict):
			for key,val in initvalues.items():
				self.insert(key, val)
		else:
			for i,val in enumerate(initvalues):
				self.insert(i, val)


	def get(self, index):
		try:
			return self[index]
		except KeyError: return None

	def __getitem__(self, index):
		'''Find the value of the node with the given index'''
		node = self.root
		level = 0
		while node and node.index == -1:
			i = (index >> level * 5) & 31
			node = node.children[i]
			level+=1
		if node == None:
			raise KeyError(index)
		if node.index == index:
			return node.value
		raise KeyError(index)

	def assoc(self, index, value):
		newnode = LookupTreeNode(index, value)
		newtree = LookupTree()
		newtree.root = self._assoc_down(self.root, newnode, 0)
		return newtree

	def remove(self, index):
		newtree = LookupTree()
		newtree.root = self._remove_down(self.root, index, 0)
		return newtree

	def _assoc_down(self, node, newnode, level):
		ind = (newnode.index >> level * 5) & 31
		copynode = LookupTreeNode()
		for i,child in enumerate(node.children):
			if i != ind:
				copynode.children[i] = child
		child = node.children[ind]
		if child == None:
			copynode.children[ind] = newnode
		elif child.index == -1:
			copynode.children[ind] = self._assoc_down(child, newnode, level+1)
		else:
			branch = LookupTreeNode()
			copynode.children[ind] = branch
			level+=1
			cind = (child.index >> level * 5) & 31
			nind = (newnode.index >> level * 5) & 31
			branch.children[cind] = child
			branch.children[nind] = newnode
		return copynode

	def _remove_down(self, node, index, level):
		ind = (index >> level * 5) & 31
		
		if node.children[ind] == None:
			return node
		
		copynode = LookupTreeNode()

		for i,child in enumerate(node.children):
			if i != ind:
				copynode.children[i] = child
		
		child = node.children[ind]

		if child.index == index:
			copynode.children[ind] = None
		elif child.index == -1:
			copynode.children[ind] = self._remove_down(child, index, level+1)
		else:
			return node

		return copynode
		
	def insert(self, index, value):
		'''Insert a node in-place. It is highly suggested that you do not
		use this method. Use assoc instead'''
		newnode = LookupTreeNode(index, value)
		level = 0
		node = self.root
		while True:
			ind = (newnode.index >> level * 5) & 31 
			level+=1
			if node.children[ind] == None:
				node.children[ind] = newnode
				break
			elif node.children[ind].index == -1:
				node = node.children[ind]
			else:
				branch = LookupTreeNode()
				child = node.children[ind]
				nind = (newnode.index >> level * 5) & 31
				cind = (child.index >> level * 5) & 31
				node.children[ind] = branch
				branch.children[nind] = newnode
				branch.children[cind] = child
				break
				

