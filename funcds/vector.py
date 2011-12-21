from .lookuptree import LookupTree 

class ImmutableVector:
	def __init__(self, initvalues=None, *args):
		if not initvalues: initvalues = []
		self.tree = LookupTree(initvalues + args)
		self._length = len(initvalues) + len(args)

	def assoc(self, index, value):
		newvec = ImmutableVector()
		newvec.tree = self.tree.assoc(index, value)
		if index >= self._length:
			newvec._length = index+1
		else:
			newvec._length = self._length
		return newvec

	def conj(self, value):
		return self.assoc(self._length, value)

	def __len__(self):
		return self._length

	def __getitem__(self, index):
		return self.tree.get(index)

