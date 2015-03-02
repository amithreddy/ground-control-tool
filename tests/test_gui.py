import unittest, mock
from nose.plugins.attrib import attr

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os
import main

# run this every time you run pyuic4 ( make changes to your ui)
qApp=None
main.mkQApp()
@attr('gui')
class TabsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        cls.db =main.sqldb(name=cls.name)
        cls.form = main.ApplicationWindow(cls.db)
    def test_shapefieldorder(self):
        # ensure the visual order of the fields is maintained
        self.geometry_fields = [ #ordered by apperance visually, top to bottom
                self.form.ui.t1,self.form.ui.t2,self.form.ui.t3,self.form.ui.t4,
                self.form.ui.b1,self.form.ui.b2,self.form.ui.b3,self.form.ui.b4
                    ]
        # render the form, neccessary for this test otherwise all coords return 0
        self.form.show()
        self.form.ui.tabWidget.setCurrentWidget(self.form.ui.Shape)
        points = [field.y() for field in self.geometry_fields]
        assert(sum(points)!=0)
        self.assertListEqual(points,sorted(points))
    @classmethod
    def tearDownClass(cls):
        cls.form.close()
        cls.db.close()
        os.remove(cls.name)
