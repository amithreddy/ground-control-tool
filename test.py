import unittest, mock
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import sys, os

import reg
import main

# new test for self.adjust in ImgGraph class
# new test for switching tabs

class ShapeSumbitFunctions(unittest.TestCase):
    # test if the form inputs have a validator 
    # and they all validate data properly
    # test if it is loading properly
    # test if it is saving properly
    # mock out the sql I don't have to worry? if i included sql is it considered cheating?
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
    def test_(self):
            pass
    @unittest.skip("spin out the shape tab method into another class and test it")
    def test_submitTrue( self):
        # test that the fields accepts valid data
        for points in self.points_set_true:
            for field, point in zip(self.fields,points):
                # QTest.keyClick(mywidget,str key)
                field.setText(point)
        # click submit
        QTest.mouseClick( self.submit, Qt.LeftButton )
    @unittest.skip('')
    def test_submitFail( self ):
        pass

class OpenWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.qApp=QtGui.QApplication(sys.argv)
        self.db= main.sql()
        # fill in some random data
        for x in xrange(1,10):
            x = str(x)
            values ={'mine':x+'mine', 'orebody':x+'ore',
                            'level':x+'level','stopename':x+'stope'}
            self.db.insert_header(values)
        self.dialog = main.OpenDialog()
    def test_populated(self):
        # check that on startup the rows have been filled from the database
        x = 1
        self.dialog.table.selectRow(x)
        self.assertListEqual(self.dialog.model.data_list[x-1],
                        self.dialog.model.data_list[self.dialog.table.currentIndex().row()-1])
    def test_search(self):
        result= self.db.select_header({'mine':'2mine','orebody':'2ore','level':'2level','stopename':'2stope'})
        result = [val for key,val in result[0].iteritems()]
        self.dialog.ui['mine'].setText('2mine')
        QTest.mouseClick(self.dialog.searchButton, Qt.LeftButton)
        self.assertListEqual(sorted(self.dialog.model.data_list[0]),sorted(result))
    @unittest.skip("don't know play this")
    def test_open(self):
        pass
    @unittest.skip("don't know play this")
    def test_limit(self):
        # test how many records I can display without slowing down
        pass
    @unittest.skip("don't know how to test")
    def test_selection(self):
        #test that  only rows can be selected
        self.dialog.table.selectionModel().hasSelection()
    @classmethod
    def tearDownClass(self):
        self.db.db.close()
        self.qApp.quit()
        os.remove('MiningStopes')

class SaveDialogTest(unittest.TestCase):
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
        self.dialog.sql.insert_header = mock.MagicMock(return_value=None)
    def test_save(self):
        # test the save function
        ui =[self.dialog.Mine, self.dialog.OreBody, self.dialog.Level, self.dialog.StopeName]
        QtGui.QMessageBox= self.dummy_true()
        for thing in ui:
            thing.setText('hello')
        self.dialog.save()
        #assert that sql.insert has been called
        self.assertTrue(self.dialog.sql.insert_header.called)
    def test_dialog(self):
        # test if clicking mouse button triggers dialog's save function
        # mock out the save method
        self.dialog.save = mock.MagicMock(return_value=True)
        self.dialog.saveButton.clicked.connect(self.dialog.save)
        QTest.mouseClick(self.dialog.saveButton, Qt.LeftButton)
        self.assertTrue(self.dialog.save.called)
    @classmethod
    def tearDownClass(self):
        self.qApp.quit()
        os.remove('MiningStopes')

class SqlTest(unittest.TestCase):
    # Tests for SQL
    # Save a row with an existing name(renaming)/ renaming (how to handle this case?)
    @classmethod
    def setUpClass(cls):
        cls.name = 'test'
        cls.db =main.sql(cls.name)
        cls.values={"mine":'hello',"orebody":'eating',
                    "level":'arste', "stopename":"tasrt"}
        cls.values2={"mine":'hello2',"orebody":'eating',
                    "level":'arste', "stopename":"tasrt2"}
    def setUp(self):
        self.db.insert_header(self.values)
    def test_tables(self):
        results = [self.db.db.tables().contains(name) for name in  ["header","shape"]]
        self.assertTrue( all(results))
    def test_insert(self):
        success=self.db.insert_header(self.values2)
        self.assertTrue(success)
    def test_insertFalse(self):
        # all of this data is exists in the db already and should return false
        success=self.db.insert_header(self.values)
        self.assertFalse(success)
    def test_relations(self):
        pass
        # test that you can't insert into child table without a proper key
    def test_update(self):
        # these unique constraints exist already and they should update the other values
        success=self.db.insert_header(self.values, update=True)
        self.assertTrue(success)
    def test_select(self):
        # select from db
        results= self.db.select_header(self.values)
        self.assertDictEqual(self.values,results[-1])
    def test_selectpartial(self):
        # select values only partialy filled
        results = self.db.select_header({'mine':'hello', 'orebody':None, 'level':None, 'stopename':None})
        self.assertDictEqual(self.values,results[-1])
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

class TabSql(unittest.TestCase):
    def setUp(self):
        pass
    def test_ShapeInsert(self):
        pass
    def test_ShapeUpdate(self):
        pass

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

if __name__=="__main__":
    unittest.main()
