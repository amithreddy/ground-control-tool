import unittest,mock
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from nose_parameterized import parameterized
import projectmocks

import main,sqlqueries

keys = [ 'b1','b2','b3','b4','t1','t2','t3','t4' ]
valid_data = [str(x)+','+str(x)+','+str(x) for x in range(0,8)]
invalid_data = [str(x)+','+str(x) for x in range(0,8)] 

valid_data = { key:point for key,point in zip(keys,valid_data)}
invalid_data = { key:point for key,point in zip(keys,invalid_data)}

class ShapeTab(unittest.TestCase):
    # test if it is loading properly
    # test if it is saving properly
    @classmethod
    def setUpClass(self):
        self.db = projectmocks.mocksqldb()
        self.form = main.ApplicationWindow(self.db)
    def setUp(self):
        self.ShapeTab = main.ShapeTab(self.form.ui, self.db)
        self.submit = self.form.ui.ShapeSubmit
    def test_textToTuple(self):
        string_points = ['1,1,1','0.1,.1,2.0','.1,.2,.3', '1.2,1.2,3.4']
        expected_points = [(1,1,1),(0.1,.1,2.0),( .1,.2,.3 ), ( 1.2,1.2,3.4 )]
        processed_points = [
                self.ShapeTab.text_to_tuple(string) 
                for string in string_points]
        self.assertListEqual( expected_points, processed_points)
    @parameterized.expand([
        ("pass",valid_data,True),
        ("fail",invalid_data, False)])
    def test_submit(self,name,points,expected):
        # this tests that is being verified and sent to proper functions
        # tests that submit button is properly mapped
            # tests, implicitly, ShapeTab.check
        # overide self.graph.compute_figure and connect it to submit
        dummy_compute_figure = mock.MagicMock(return_value=None)
        self.ShapeTab.connect(dummy_compute_figure)
        self.ShapeTab.set_data(self.ShapeTab.uielements,points)
        QTest.mouseClick(self.submit, Qt.LeftButton)
        self.assertEqual(dummy_compute_figure.called, expected)
    @unittest.skip('implement this test')
    def test_validator(self):
        # make sure each lineedit has a validator
        pass
    @classmethod
    def tearDownClass(cls):
        pass
