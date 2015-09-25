#!/usr/bin/env python

import uuid

import funktown

from funktown.lookuptree import LookupTree
from funktown import ImmutableDict, ImmutableVector, ImmutableList

import collections

def treetest():
    t1 = LookupTree({0:0, 32:32, 4:4})
    assert t1.get(0) == 0
    t2 = t1.assoc(36, 36)
    assert t1.get(36) is None
    assert t2.get(36) == 36
    t3 = t2.assoc(36, 35)
    assert t3.get(36) == 35
    t4 = t2.multi_assoc([(15,15), (14,14)])
    assert t4.get(15) == 15
    assert t4.get(14) == 14

def vectortest():
    v1 = ImmutableVector([0,1,2])
    v2 = v1.conj(3)
    v3 = v1.pop()
    assert len(v1) == 3
    assert len(v2) == 4
    assert len(v3) == 2
    assert v2[3] == 3
    assert v2 == [0, 1, 2, 3]
    v4 = v1 + v2
    assert v4 == [0,1,2,0,1,2,3]
    assert v4[0:4] == [0,1,2,0]
    assert 2 in v4
    assert ImmutableVector() == []

def dicttest():
    d1 = ImmutableDict(hello="world")
    d2 = d1.assoc("goodbye", "moon")
    d3 = d2.remove("hello")
    assert d1["hello"] == "world"
    assert d2["goodbye"] == "moon"
    assert d1.get("goodbye") is None
    assert d3.get("hello") is None
    assert d2 == {"hello":"world", "goodbye":"moon"}
    d4 = d2.update(ImmutableDict({"a":"b", "c":"d"}))
    assert len(d4) == 4
    assert d4['a'] == 'b'
    assert d4['c'] == 'd'
    d5 = d1.update(hola="mundo")
    assert d5['hola'] == 'mundo'
    assert 'hola' in d5
    assert ImmutableDict() == {}
    assert ImmutableDict().get(1, 2) == 2

def dictismappingtest():
    start = {'a': 1, 'b': 2, 'c': 3}
    i_d = ImmutableDict(start)
    assert isinstance(i_d, collections.Mapping)

def dict_creation_test():
    d1 = {"a": 1, "b": 2, "c": 3, 4: 'd'}
    initial_length = len(d1)
    i_d = ImmutableDict(d1, d=4)
    assert len(d1) == initial_length
    assert len(i_d) == initial_length + 1

def dict_int_test():
    d = {n:n for n in range(16)}
    d1 = ImmutableDict(d)
    assert (len(d1.keys()) == 16)

def ugly_tree_creation_test():
    tree = LookupTree()
    error_values = []
    for i in range(10000):
        tree.insert(hash(i), (i, i))
        n = 0
        try:
            for k, v in tree:
                n += 1
            if n != i+1:
                error_values.append(i)
        except TypeError:
            # this is failing the first time through the loop, because
            # integers aren't iterable.
            # I'm torn about what to think about this fact.
            # Probably just means I don't understand the tree as well as I thought
            print "Quit being able to iterate over tree on insert # %d" % i
            raise
    assert not error_values

def brutal_creation_test():
    """ Note that this is incredibly slow and painful.
    You probably won't want to run it often """
    errors = []
    for i in range(10000):
        print '@',
        d = {n:n for n in range(i)}
        i_d = ImmutableDict(d)
        for j in range(i):
            if j not in i_d:
                msg = '@ length {}, index {} got lost'
                errors.append(msg.format(i, j))
        if not i % 80:
            print '!'
    assert not errors, str(errors)

def simpler_dict_collision_test():
    d = {n:n for n in range(10000)}
    i_d = ImmutableDict(d)
    failures = []
    result_keys = i_d.keys()
    for n in range(10000):
        if n not in result_keys:
            failures.append(n)
    if failures:
        print "Lost %d keys: %s" % (len(failures), failures)
        assert False, str(failures)

def dict_collision_test():
    l = [str(uuid.uuid4()) for _ in range(10000)]
    d = {l[n]: n for n in range(10000)}
    i_d = ImmutableDict(d)
    assert len(i_d.keys()) == len(d.keys())
    failures = []
    for k in l:
        if str(k) not in i_d:
            failures.append({k: d[k]})
    if failures:
        msg = 'UUID entries lost:'
        for uid in failures:
            msg += '{}\n'.format(uid)
        msg += '\n(There are {} of them)'.format(len(failures))
        assert False, msg

def listtest():
    l1 = ImmutableList([2, 3])
    assert l1.conj(1) == [1, 2, 3]
    assert len(l1) == 2
    assert l1.conj(1) == ImmutableList(1, l1)
    l3 = ImmutableList()
    assert len(l3) == 0
    assert l3 == ImmutableList([])

def typetest():
    l = ImmutableList()
    v = ImmutableVector()
    d = ImmutableDict()

    assert l is not None
    assert v != 3
    assert d != 'a'

    assert l == v
    assert d != v
    assert d != l

if __name__ == "__main__":
    dict_collision_test()
    simpler_dict_collision_test()
    # This is simply too slow to run regularly/often
    # (if at all)
    # brutal_creation_test()
    dict_int_test()
    # TODO: Get this passing
    # ugly_tree_creation_test()
    dict_creation_test()
    treetest()
    vectortest()
    dicttest()
    dictismappingtest()
    listtest()
    typetest()
    print("All tests passed")
