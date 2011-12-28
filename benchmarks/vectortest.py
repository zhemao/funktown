import moka
import funktown
import cProfile as profile

def mokatest(fname):
    mlist = moka.List()
    with open(fname) as f:
        for line in f:
            mlist = mlist.append(line)

def funktowntest(fname):
    ftvec = funktown.ImmutableVector()
    with open(fname) as f:
        for line in f:
            ftvec = ftvec.conj(line)

def stdlibtest(fname):
    lst = []
    with open(fname) as f:
        for line in f:
            lst.append(line)

if __name__ == "__main__":
    fname = "studyinscarlet.txt"
    profile.run('mokatest(fname)')
    profile.run('funktowntest(fname)')
    profile.run('stdlibtest(fname)')

