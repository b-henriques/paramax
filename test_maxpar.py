from maxpar import Task, TaskSystem
import unittest

X = None
Y = None
Z = None


def runT1():
    global X
    X = 1


def runT2():
    global Y
    X = 2


def runTsomme():
    global X, Y, Z
    Z = X+Y


class test_maxpar(unittest.TestCase):

    #TODO test exemple
    def test_makeprec(self):
        t1 = Task("T1", [], ["X"], runT1)
        t2 = Task("T2", [], ["Y"], runT2)
        tsomme = Task("Tsomme", ["Y","X"], ["Z"], runTsomme)
        tasksystem = TaskSystem([t1, t2, tsomme], {"T1": [], "T2": ["T1"], "Tsomme": ["T1", "T2"]})

    #TODO : test run

    #TODO : test exo td