import unittest, mock
from nose_parameterized import parameterized
import projectmocks

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os

import reg
import main, sqlqueries,sql_testdata

qApp=None
main.mkQApp()
# new test for self.adjust in ImgGraph class
# new test for switching tabs


values={"mine":'hello',"orebody":'eating',
"level":'arste', "stopename":"tasrt"}
values2={"mine":'hello2',"orebody":'eating',
"level":'arste', "stopename":"tasrt2"}

partial = {'mine':'hello', 'orebody':None, 'level':None, 'stopename':None}
class SqlTest(unittest.TestCase):
    # Save a row with an existing name(updating) or renaming (how to handle this case?)
    @classmethod
    def setUpClass(cls):
        # Tests for SQLDB
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
    @parameterized.expand(sql_testdata.test_pull_data)
    def test_pull(self,sqlstr,keys,expected,bindings=None):
        val= self.db.pull_query(sqlstr,keys,bindings=bindings)
        self.assertListEqual(expected,val)
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
