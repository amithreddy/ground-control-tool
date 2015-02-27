import unittest, mock
from nose_parameterized import parameterized
import projectmocks

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os, shutil

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
    # Tests for main.sqldb
    # Save a row with an existing name(updating) or renaming (how to handle this case?)
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        shutil.copyfile('generateddb','test')
        cls.db = main.sqldb(name=cls.name)
    def test_tables(self):
        results = [self.db.db.tables().contains(name) for name in ["header","shape"]]
        self.assertTrue( all(results))
    def test_insert(self,sqlstr,expected,bindings=None):
        success=self.db.query_db(sqlstr,bindings=bindings)
        self.assertEqual(success,expected)
    @parameterized.expand(sql_testdata.pull_data)
    def test_pull(self,sqlstr,expected,bindings=None,pull_keys=None):
        val= self.db.query_db(sqlstr,bindings=bindings,pull_keys=pull_keys)
        self.assertEqual(expected,val)
    @unittest.skip("test not completed yet")
    def test_shapeTable(self):
        # test that you can't insert into child table without a proper key
        query = self.db.new_query()
        sql= "INSERT INTO SHAPE VALUES('1000','','','','','','','','')"
        query.exec_(sql)
        print query.lastError().text()
        #self.assertFalse()
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(cls.name)

@unittest.skip("test not completed yet")
class TabSql(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        shutil.copyfile('generateddb','test')
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
