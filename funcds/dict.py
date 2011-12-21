from .lookuptree import LookupTree

def hashfunc(key):
	h = 2166136261
	for c in key:
		h = ( h * 16777619 ) ^ ord(c)
	return h 
	

class ImmutableDict:

	def __init__(self, initdict=None, **kwargs):
		if initdict == None: initdict = {}
		initdict.update(kwargs)
		hashlist = [(hashfunc(key), initdict[key]) for key in initdict]
		self.tree = LookupTree(dict(hashlist))
		self._length = len(initdict)

	def assoc(self, key, value):
		copydict = ImmutableDict()
		copydict.tree = self.tree.assoc(hashfunc(key), value)
		copydict._length = self._length + 1
		return copydict

	def get(self, key):
		try:
			return self[key]
		except KeyError: return None

	def __len__(self):
		return self._length

	def __getitem__(self, key):
		try:
			return self.tree[hashfunc(key)]
		except KeyError: raise KeyError(key)
