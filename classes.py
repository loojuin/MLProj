#!~/anaconda/bin/python
#
# This module contains the declarations of all the classes that will be used in this program.


# Superclass for all x, y, START and STOP nodes (corresponds to the diagram shown in class).
class StateNode:
    def __init__(self):
        pass


# Superclass for the START and STOP node. Used mainly to recognise them easily.
class SpecialNode(StateNode):
    def __init__(self):
        pass


# Represents the START node.
class Start(SpecialNode):
    # Params:
    # next_y - The Y object representing the node that was generated by this node.
    def __init__(self, next_tag):
        self.next_tag = next_tag
        self.name = "START"

    def __str__(self):
        return "START"

    def __repr__(self):
        return str(self)

    # Recursively turns a reference-linked node sequence into a list of nodes.
    def to_list(self):
        retval = [self]
        return self.next_tag.to_list(retval)


# Represents the STOP node.
class Stop(SpecialNode):
    def __init__(self):
        self.name = "STOP"

    def __str__(self):
        return "STOP"

    def __repr__(self):
        return str(self)

    # Method used in the recursive process of turning a reference-linked node sequence into a list of nodes.
    # Do not call this method directly. Call it only from the START object.
    def to_list(self, ls):
        ls.append(self)
        return ls


# Represents a Tag node.
class Tag(StateNode):
    # Params:
    # label - A string representing the label (e.g., "B-NP" or "I-NP")
    # word - The Word object being generated by this tag.
    # next_tag - The Tag object being generated by this tag.
    def __init__(self, label, word, next_tag = Stop()):
        self.name = label
        self.word = word
        self.next_tag = next_tag

    def __str__(self):
        return "%s => %s" % (self.name, self.word)

    def __repr__(self):
        return str(self)

    # Method used in the recursive process of turning a reference-linked node sequence into a list of nodes.
    # Do not call this method directly. Call it only from the START object.
    def to_list(self, ls):
        ls.append(self)
        return self.next_tag.to_list(ls)

    # Renders this object as "[word] [tag]", as would appear in the original text files provided.
    def to_text(self):
        return "%s %s" % (self.word.value, self.name)


# Represents a Word node.
class Word:
    # Params:
    # value - The literal word.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)
