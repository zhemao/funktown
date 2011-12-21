import funcds

def treetest():
	t1 = funcds.LookupTree({0:0, 32:32, 4:4})
	assert t1.get(0) == 0
	t2 = t1.assoc(36, 36)
	assert t1.get(36) == None
	assert t2.get(36) == 36

def vectortest():
	v1 = funcds.ImmutableVector([0,1,2])
	v2 = v1.conj(3)
	assert len(v1) == 3
	assert len(v2) == 4
	assert v2[3] == 3

def dicttest():
	d1 = funcds.ImmutableDict(hello="world")
	d2 = d1.assoc("goodbye", "moon")
	assert d1["hello"] == "world"
	assert d2["goodbye"] == "moon"
	assert d1.get("goodbye") == None

if __name__ == "__main__":
	treetest()
	vectortest()
	dicttest()

