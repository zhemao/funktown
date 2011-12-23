# FuncDS: Functional Data Structures for Python

This library implements an efficient ImmutableDict and ImmutableVector class 
inspired by the implementation of Vectors and Maps in the Clojure programming
language.

## API

### ImmutableVector

The constructor takes a list of initial values. Supports item access in the
same way as builtin python lists

assoc(index, value)

Returns a new vector with the value assigned to the given index

conj(value)

Returns a new vector with the value appended to the back. Roughly equivalent 
to vec.assoc(len(vec), value)

pop()

Returns a new vector with the final item removed.

### ImmutableDict

The constructor can take a dict and/or keyword arguments. Item access follows
the same behavior as builtin python dicts.

assoc(key, value)

Returns a new immutable dict with the value associated with the given key.

get(key)

Like in Python's builtin dict, this will act like item access, except 
returning None instead of raising a KeyError.

remove(key)

Return a new ImmutableDict with the item at that key removed

## Coming Soon
 * Vector concatenation
 * Dict extension

