import unittest, mock
from nose_parameterized import parameterized

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os

import reg
import main
import projectmocks

qApp=None
main.mkQApp()
# new test for self.adjust in ImgGraph class
# new test for switching tabs

valid_points = [str(x)+','+str(x)+','+str(x) for x in range(0,8)]
invalid_points = [str(x)+','+str(x) for x in range(0,8)] 
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
        self.fields = self.ShapeTab.fields
    @unittest.skip("don't need")
    def test_check(self,name, points, expected):
        # fill the fields with valid data, 
        self.ShapeTab.set_text(self.fields,points)
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
    @parameterized.expand([
        ("pass",valid_points,True),
        ("fail",invalid_points, False) ])
    def test_submit(self,name,points,expected):
        # this implicitly tests shape check
        #overide self.graph.compute_figure
        dummy_compute_figure = mock.MagicMock(return_value=None)
        self.ShapeTab.connect(dummy_compute_figure)
        self.ShapeTab.set_text(self.fields,points)
        # click submit
        QTest.mouseClick(self.submit, Qt.LeftButton)
        # make sure that the submit button triggers self.graph.compute_figure
        self.assertEqual(dummy_compute_figure.called, expected)
    @unittest.skip('to be tested')
    def test_validator(self):
        # make sure each lineedit has a validator
        pass
    @classmethod
    def tearDownClass(cls):
        pass

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
        cls.db =main.sqldb(name=cls.name)
        cls.db.insert_header(values)
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

@unittest.skip("not implemented")
class ImportExportSqlTest(unittest.TestCase):
    # Test for Import sql data into new database
    # Test for Export sql data into old database
    @classmethod
    def setUpClass(cls):
        cls.name1='test1'
        cls.name2='test2'
        cls.db1 = main.sqldb(name =cls.name1,connectionName="first")
        cls.db2 = main.sqldb(name =cls.name2,connectionName="second")
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
