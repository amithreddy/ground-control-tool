import unittest, mock

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os
import main
qApp=QtGui.QApplication(sys.argv)

class TabsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        cls.db =main.sqldb(name=cls.name)
        cls.form = main.ApplicationWindow(cls.db)
    #@unittest.skip('')
    def test_shapefieldorder(self):
        # refactor into a seperator testcase for all tabs? this way you only hav
        # to run this every time you run pyuic4 ( make changes to your ui)
        self.geometry_fields = [ #ordered by apperance visually, top to bottom
                self.form.ui.t1,self.form.ui.t2,self.form.ui.t3,self.form.ui.t4,
                self.form.ui.b1,self.form.ui.b2,self.form.ui.b3,self.form.ui.b4
                    ]
        # render the form, neccessary for this test otherwise all coords return 0
        self.form.show()
        # ensure the visual order of the fields is maintained
        points = [field.y() for field in self.geometry_fields]
        assert(sum(points)!=0)
        self.assertListEqual(points,sorted(points))
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(cls.name)
