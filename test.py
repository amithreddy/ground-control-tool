import unittest, mock
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os

import reg
import main

# new test for self.adjust in ImgGraph class
# new test for switching tabs

class SaveDialogTest(unittest.TestCase):
    # learn how to use mocks here
    # check if submit works
    @classmethod
    def setUpClass(self):
        self.qApp=QtGui.QApplication(sys.argv)
    def setUp(self):
        self.dialog = main.NewRecord()
        self.dummy_true = mock.Mock()
        self.dummy_true.Yes = True
        self.dummy_true.No = False
        self.dummy_true.question.return_value=True
    def test_save(self):
        ui =[self.dialog.Mine, self.dialog.OreBody, self.dialog.Level, self.dialog.StopeName]
        self.dialog.sql.insert = mock.MagicMock(return_value=None)
        QtGui.QMessageBox= self.dummy_true()
        for thing in ui:
            thing.setText('hello')
        self.dialog.save()
        #assert that sql.insert has been called
        self.assertTrue(self.dialog.sql.insert.called)
    def test_dialog(self):
        # test if clicking mouse button triggers dialog's save function
        # mock out the save method
        self.dialog.save = mock.MagicMock(return_value=True)
        QTest.mouseClick(self.dialog.saveButton, Qt.LeftButton)
        self.assertTrue(self.dialog.save.callled)
    @classmethod
    def tearDownClass(self):
        self.qApp.quit()
        os.remove('bob')

class SqlTest(unittest.TestCase):
    # Tests for SQL
    # Save a row with an existing name(renaming)/ renaming (how to handle this case?)
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        cls.db =main.sql(cls.name)
        cls.values={"mine":'hello',"orebody":'eating',
                    "level":'arste', "stopename":"tasrt"}
    def test_table(self):
        self.assertTrue(self.db.db.tables().contains("STOPES"))
    def test_insert(self):
        success=self.db.insert(self.values)
        if success != True:
            print 'insert_error:', self.db.query.lastError().text()
        self.assertTrue(success)
    def test_insertFalse(self):
        # all of this data is exists in the db already and should return false
        success=self.db.insert(self.values)
        self.assertFalse(success)
    def test_update(self):
        # these unique constraints exist already and they should update the other values
        success=self.db.insert(self.values, update=True)
        self.assertTrue(success)
    def test_select(self):
        # read test
        results= self.db.select_row(self.values)
        self.assertDictEqual(self.values,results)
    @unittest.skip("Not implemented")
    def test_delete(self):
        # assert what? 
        pass
    @unittest.skip("Not implemented")
    def test_select_conditional(self):
        #if I add logic to my select statements, here I should write tests when I do
        pass
    @classmethod
    def tearDownClass(cls):
        cls.db.db.close()
        os.remove(cls.name)

class ImportExportSqlTest(unittest.TestCase):
    # Test for Import sql data into new database
    # Test for Export sql data into old database
    @classmethod
    def setUpClass(cls):
        cls.name1='test1'
        cls.name2='test2'
        cls.db1 = main.sql(cls.name1)
        cls.db2 = main.sql(cls.name2)
        # insert dummy data here
    def test_exportimport(self):
        # first it exports db1
        # then it imports into db2
        # we check that both of them work well
        pass
    @classmethod
    def tearDownClass(cls):
        cls.db1.db.close()
        cls.db2.db.close()
        os.remove(cls.name1)
        os.remove(cls.name2)

class RegExTest(unittest.TestCase):
    def setUp(self):
        self.points_set_true= [
                    ['1,1,1','2,2,2','3,3,3','4,4,4','5,5,5','6,6,6',
                     '7,7,7','8,8,8'],
                    ['0.1,0.3,3.23']
                    ]
        self.points_set_false= [
                [',1,2,3'],['3,2,1,'],
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

class ShapeSumbitFunctions(unittest.TestCase):
        # test if the form inputs have a validator 
        # and they all validate data properly
    def setUp(self):
        """ points in this format = [ '1,1,1','0.2,123,1' ]
        """
        qApp=QtGui.QApplication(sys.argv)
        self.form = main.ApplicationWindow()
        self.submit = self.form.ui.ShapeSubmit
        self.fields =[
            self.form.ui.b1,self.form.ui.b2,self.form.ui.b3,self.form.ui.b4,
            self.form.ui.t1,self.form.ui.t2,self.form.ui.t3,self.form.ui.t4
                    ]
    @unittest.skip("Don't know how to test")
    def test_submitTrue( self):
        # this test is retired for now
        # this is not a unit test! this is more like a bad integration test
        # I don't think this test can actually fail
        for points in self.points_set_true:
            for field, point in zip(self.fields,points):
                # QTest.keyClick(mywidget,str key)
                field.setText(point)
        # click submit
        QTest.mouseClick( self.submit, Qt.LeftButton )
unittest.main()
