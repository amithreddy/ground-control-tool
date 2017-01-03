import unittest, mock
import main, sqlqueries
from PyQt4.QtCore import Qt
from PyQt4.QtTest import QTest
from PyQt4 import QtGui, QtCore
import sys, os
import pdb, atexit
import projectmocks

qApp =main.mkQApp()
class SaveDialogTest(unittest.TestCase):
    # check if submit works
    @classmethod
    def setUpClass(self):
        self.name= "test"
        self.db = projectmocks.mocksqldb() 
    def setUp(self):
        self.dialog = main.NewRecord(self.db)
        self.dummy_true = mock.Mock()
        self.dummy_true.Yes = True
        self.dummy_true.No = False
        self.dummy_true.question.return_value=True
        self.dialog.db.query_db = mock.MagicMock(return_value=None)
    def test_save(self):
        # test the save function
        ui =[self.dialog.Mine, self.dialog.OreBody, self.dialog.Level, self.dialog.StopeName]
        QtGui.QMessageBox= self.dummy_true()
        for thing in ui:
            thing.setText('hello')
        self.dialog.save()
        self.assertTrue(self.dialog.db.query_db.called)
    def test_dialog(self):
        # test if clicking mouse button triggers dialog's save function
        self.dialog.save = mock.MagicMock(return_value=None)
        self.dialog.saveButton.clicked.connect(self.dialog.save)
        QTest.mouseClick(self.dialog.saveButton, Qt.LeftButton)
        self.assertTrue(self.dialog.save.called)
    @classmethod
    def tearDownClass(cls):
        pass

class OpenWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # this feels like a integration test?
        self.name ="test"
        self.db= main.sqldb(name=self.name)
        # fill in some random data
        for x in xrange(1,10):
            x = str(x)
            values ={'mine':x+'mine', 'orebody':x+'ore',
                            'level':x+'level','stopename':x+'stope'}
            self.db.query_db(sqlqueries.header_insert,bindings=values)
        self.dialog = main.OpenDialog(self.db)
    def test_populated(self):
        # check that on startup the rows have been filled from the database
        x = 1
        self.dialog.table.selectRow(x)
        self.assertListEqual(self.dialog.model.data_list[x-1],
                        self.dialog.model.data_list[self.dialog.table.currentIndex().row()-1])
    def test_search(self):
        values={'mine':'2mine','orebody':'2ore','level':'2level','stopename':'2stope'}
        result= self.db.query_db(sqlqueries.header_select, bindings=values, pull_keys=values)
        result = [val for key,val in result[0].iteritems()]
        self.dialog.ui['mine'].setText('2mine')
        QTest.mouseClick(self.dialog.searchButton, Qt.LeftButton)
        self.assertListEqual(sorted(self.dialog.model.data_list[0]),sorted(result))
    @unittest.skip("did not implement")
    def test_open(self):
        pass
    @unittest.skip("don't know how to test")
    def test_selection(self):
        #test that  only rows can be selected
        self.dialog.table.selectionModel().hasSelection()
    @unittest.skip("don't know to do this")
    def test_limit(self):
        # test how many records I can display without slowing down
        pass
    @classmethod
    def tearDownClass(self):
        self.db.close()
        os.remove(self.name)

class ApplicationSave(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db =projectmocks.mocksqldb()
        cls.window = main.ApplicationWindow(cls.db)
    def test_save(self):
        self.window.ShapeTab.save = mock.MagicMock(return_value=None)
        self.window.save()
        self.assertTrue(self.window.ShapeTab.save.called)
    @classmethod
    def tearDownClass(cls):
        pass
