import unittest, mock
from nose_parameterized import parameterized

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os

import reg
import main

# new test for self.adjust in ImgGraph class
# new test for switching tabs

valid_points = [str(x)+','+str(x)+','+str(x) for x in range(0,8)]
invalid_points = [str(x)+','+str(x) for x in range(0,8)] 
class ShapeSubmit(unittest.TestCase):
    # test if it is loading properly
    # test if it is saving properly
    @classmethod
    def setUpClass(self):
        """ points in this format = [ '1,1,1','0.2,123,1' ]
        """
        qApp=QtGui.QApplication(sys.argv)
        self.form = main.ApplicationWindow()
        self.name = 'test'
        self.db =main.sqldb(self.name)
    def setUp(self):
        self.ShapeTab = main.ShapeTab(self.form.ui, self.db)
        self.submit = self.form.ui.ShapeSubmit
        self.fields = self.ShapeTab.fields
    def setText(self, fields,points):
        for field, point in zip(fields,points):
            field.setText(point)
    @parameterized.expand([
        ("checkpass",valid_points,True),
        ("checkfail",invalid_points, False) ])
    def test_check(self,name, points, expected):
        # fill the fields with valid data, 
        self.setText(self.fields,points)
        # check function should accept them
        dummy_function = mock.MagicMock(return_value=None)
        self.ShapeTab.check(self.fields, dummy_function)
        self.assertEqual(dummy_function.called,expected)
    def test_textToTuple(self):
        string_points = ['1,1,1','0.1,.1,2.0','.1,.2,.3', '1.2,1.2,3.4']
        expected_points = [(1,1,1),(0.1,.1,2.0),( .1,.2,.3 ), ( 1.2,1.2,3.4 )]
        processed_points = [
                self.ShapeTab.text_to_tuple(string) 
                for string in string_points]
        self.assertListEqual( expected_points, processed_points)
    def test_submitTrue(self):
        dummy_compute_figure = mock.MagicMock(return_value=None)
        points = [str(x)+','+str(x)+','+str(x) for x in range(0,8)]
        expected = [ (x,x,x) for x in range(0,8)]
        # test that the fields accepts valid data
        self.setText(self.fields,points)
        #overide self.graph.compute_figure
        self.ShapeTab.connect(dummy_compute_figure)
        # click submit
        QTest.mouseClick(self.submit, Qt.LeftButton)
        # make sure that the submit button triggers self.graph.compute_figure
        dummy_compute_figure.assert_called_with(expected)
    @unittest.skip('to be tested')
    def test_validator(self):
        # make sure each lineedit has a validator
        pass
    @unittest.skip('spin out this test into different file')
    def test_fieldorder(self):
        # refactor into a seperator testcase for all tabs? this way you only hav
        # to run this every time you run pyuic4 ( make changes to your ui)
        self.geometry_fields = [ #order by order of apperance visually
                self.form.ui.t1,self.form.ui.t2,self.form.ui.t3,self.form.ui.t4,
                self.form.ui.b1,self.form.ui.b2,self.form.ui.b3,self.form.ui.b4
                    ]
        # render the form, neccessary for this test otherwise all coords return 0
        self.form.show()
        # ensure the visual order of the fields is maintained
        points = [field.y() for field in self.geometry_fields]
        self.form.hide()
        assert(sum(points)!=0)
        self.assertListEqual(points,sorted(points))
    @unittest.skip('')
    def test_submitFail( self ):
        pass
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(cls.name)


values={"mine":'hello',"orebody":'eating',
"level":'arste', "stopename":"tasrt"}
values2={"mine":'hello2',"orebody":'eating',
"level":'arste', "stopename":"tasrt2"}
partial = {'mine':'hello', 'orebody':None, 'level':None, 'stopename':None}
class SqlTest(unittest.TestCase):
    # Tests for SQLDB
    # Save a row with an existing name(renaming)/ renaming (how to handle this case?)
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        cls.db =main.sqldb(cls.name)
    def setUp(self):
        self.db.insert_header(values)
    def test_tables(self):
        results = [self.db.db.tables().contains(name) for name in  ["header","shape"]]
        self.assertTrue( all(results))
    @parameterized.expand([
        ("InsertPass",values2,True),
        # all of this data is exists in the db already and should return false
        ("InsertFail",values,False) ])
    def test_insert(self,name, values,expected):
        success=self.db.insert_header(values)
        self.assertEqual(success,expected)
    @unittest.skip("test not completed yet")
    def test_shapeTable(self):
        # test that you can't insert into child table without a proper key
        query = self.db.new_query()
        sql= "INSERT INTO SHAPE VALUES('1000','','','','','','','','')"
        #sql= "INSERT INTO SHAPE (1,'','','','','','','')"
        query.exec_(sql)
        print query.lastError().text()
        #self.assertFalse()
    def test_update(self):
        # these unique constraints exist already and they should update the other values
        success=self.db.insert_header(values, update=True)
        self.assertTrue(success)
    @parameterized.expand([
        ("select from header",values,values),
        ("header_select_partial_values",partial,values)])
    def test_select(self,name,values,expected):
        # select from db
        results= self.db.select_header(values)
        self.assertDictEqual(expected,results[-1])
    @unittest.skip("Not implemented")
    def test_delete(self):
        # assert what? 
        pass
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(cls.name)

class TabSql(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        cls.db =main.sqldb(cls.name)
    def setUp(self):
        pass
    def test_ShapeInsert(self):
        pass
    def test_ShapeUpdate(self):
        pass
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(cls.name)

class ImportExportSqlTest(unittest.TestCase):
    # Test for Import sql data into new database
    # Test for Export sql data into old database
    @classmethod
    def setUpClass(cls):
        cls.name1='test1'
        cls.name2='test2'
        cls.db1 = main.sqldb(cls.name1,connectionName="first")
        cls.db2 = main.sqldb(cls.name2,connectionName="second")
        # insert dummy data here
    def test_exportimport(self):
        # first it exports db1
        # then it imports into db2
        # we check that both of them work well
        pass
    @classmethod
    def tearDownClass(cls):
        cls.db1.close()
        cls.db2.close()
        os.remove(cls.name1)
        os.remove(cls.name2)


if __name__=="__main__":
    unittest.main()
