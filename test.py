import unittest
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore

import sys

import reg
import main

# new test for self.adjust in ImgGraph class

# new test for switching tabs
class ShapeSumbitFunctions(unittest.TestCase):
    def setUp(self):
        """ points in this format = [ '1,1,1','0.2,123' ]
        """
        qApp=QtGui.QApplication(sys.argv)
        self.form = main.ApplicationWindow()
        self.submit = self.form.ui.ShapeSubmit
        self.fields =[
            self.form.ui.b1,self.form.ui.b2,self.form.ui.b3,self.form.ui.b4,
            self.form.ui.t1,self.form.ui.t2,self.form.ui.t3,self.form.ui.t4
                    ]
    def atest_submitTrue( self):
        # this test is retired for now
        # this is not a unit test! this is more like a bad integration test
        # I don't this test can actually fail
        for points in self.points_set_true:
            for field, point in zip(self.fields,points):
                # QTest.keyClick(mywidget,str key)
                field.setText(point)
        # click submit
        QTest.mouseClick( self.submit, Qt.LeftButton )

class RegExTest(unittest.TestCase):
    def setUp(self):
        self.points_set_true= [
                    ['1,1,1','2,2,2','3,3,3','4,4,4','5,5,5','6,6,6',
                     '7,7,7','8,8,8'],
                    ['0.1,0.3,3.23']
                    ]
        self.points_set_false= [
                ['0.1','a','1.123.113'],
                ["0.1,1.2323.32,123"]
                ]
        self.regexpr= reg.match_nums
    def iter_string(self,points_set):
        data=[]
        for points in points_set:
            data.append(
                all(self.regexpr.exactMatch(point) for point in points))
        return data
    def test_true(self):
        self.assertTrue(all(self.iter_string(self.points_set_true)))
    def test_false(self):
        self.assertFalse(any(self.iter_string(self.points_set_false)))

unittest.main()
