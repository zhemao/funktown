from .lookuptree import LookupTree

class ImmutableDict:

	def __init__(self, initdict=None, **kwargs):
		if initdict == None: initdict = {}
		initdict.update(kwargs)
		hashlist = [(hash(key), (key, initdict[key])) for key in initdict]
		self.tree = LookupTree(dict(hashlist))
		self._length = len(initdict)

	def assoc(self, key, value):
		copydict = ImmutableDict()
		copydict.tree = self.tree.assoc(hash(key), (key, value))
		copydict._length = self._length + 1
		return copydict

	def update(self, other):
		copydict = ImmutableDict()
		vallist = [(hash(key), (key, other[key])) for key in other]
		copydict.tree = self.tree.multi_assoc(vallist)
		copydict._length = iter_length(copydict.tree)
		return copydict

	def remove(self, key):
		copydict = ImmutableDict()
		copydict.tree = self.tree.remove(hash(key))
		copydict._length = self._length - 1
		return copydict

	def get(self, key):
		try:
			return self[key]
		except KeyError: return None
	
	def __len__(self):
		return self._length

	def __getitem__(self, key):
		try:
			return self.tree[hash(key)][1]
		except KeyError: raise KeyError(key)

	def __iter__(self):
		for key,val in self.tree:
			yield key
	
	def keys(self):
		return [key for (key,val) in self.tree]

	def values(self):
		return [val for (key,val) in self.tree]

	def items(self):
		return [item for item in self.tree]

def iter_length(iterable):
	try:
		return len(iterable)
	except:
		i = 0
		for x in iterable: 
			i+=1
		return i
