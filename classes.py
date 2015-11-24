#!~/anaconda/bin/python
#


class StateNode:
    def __init__(self):
        pass


class SpecialNode(StateNode):
    def __init__(self):
        pass


class Start(SpecialNode):
    def __init__(self, next_y):
        self.next_y = next_y
        self.label = None

    def __str__(self):
        return "START"

    def __repr__(self):
        return str(self)

    def to_list(self):
        retval = [self]
        return self.next_y.to_list(retval)


class Stop(SpecialNode):
    def __init__(self):
        self.label = None

    def __str__(self):
        return "STOP"

    def __repr__(self):
        return str(self)

    def to_list(self, ls):
        ls.append(self)
        return ls


class Y(StateNode):
    def __init__(self, label, x, next_y = Stop()):
        self.label = label
        self.x = x
        self.next_y = next_y

    def __str__(self):
        return "%s => %s" % (self.label, self.x)

    def __repr__(self):
        return str(self)

    def to_list(self, ls):
        ls.append(self)
        return self.next_y.to_list(ls)


class X:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)
