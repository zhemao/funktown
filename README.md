# FunkTown: Functional Data Structures for Python

This library implements an efficient ImmutableDict and ImmutableVector class 
inspired by the implementation of Vectors and Maps in the Clojure programming
language.

## Installation

If you are installing from the cloned repository, just use

	python setup.py install

Package is also available from PyPI. In that case, use

	pip install funktown

ArchLinux users can install from the AUR

	yaourt -S python2-funktown 
	yaourt -S python-funktown # python 3 version

## API

### ImmutableVector

The constructor takes a list of initial values. It supports standard list
operations such as item access, slicing, and concatenation.

#### assoc(index, value)

Returns a new vector with the value assigned to the given index

#### conj(value)

Returns a new vector with the value appended to the back. Roughly equivalent 
to vec.assoc(len(vec), value)

#### pop()

Returns a new vector with the final item removed.

### ImmutableDict

The constructor can take a dict and/or keyword arguments. Item access follows
the same behavior as builtin python dicts.

#### assoc(key, value)

Returns a new immutable dict with the value associated with the given key.

#### get(key)

Like in Python's builtin dict, this will act like item access, except 
returning None instead of raising a KeyError.

#### remove(key)

Return a new ImmutableDict with the item at that key removed

#### update(otherdict)

Return a new immutable dict updated with the records in otherdict.

## Compatiblity 

Funktown has been tested with Python 2.7.2 and 3.2.2 on a Linux system.
It should be compatible with all python versions greater than 2.6.
