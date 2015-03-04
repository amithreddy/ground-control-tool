from PyQt4 import QtGui, QtCore, QtSql
import sqlqueries
import main


class FactorADelegate():
    pass

class Model(QtCore.QAbstractTableModel):
    def __init__(self,db, parent=None, data=None,select_query=None,insert_query=None,
                pull_keys=None,rowheaders=[],colheaders=[]):
        QtCore.QAbstractTableModel.__init__(self)
        self.select_query=select_query
        self.insert_query=insert_query
        self.column_headers= colheaders
        self.row_headers = rowheaders
        self.db=db
        self.data=data
        self.pull_keys=pull_keys
        num_col = len(colheaders) 
        self.layout=[i for i in self.chunks(self.pull_keys,num_col)]
    def rowCount(self,parent):
        return len(self.layout)
    def columnCount(self,parent):
        return len(self.layout[0])
    def data(self,index,role):
        if role== QtCore.Qt.DisplayRole:
            row=index.row()
            column =index.column()
            key=self.layout[row][column]
            value = self.data[key]
            return value
    def updateData(self,newdata):
        self.layoutAboutToBeChanged.emit()
        self.data=newdata
        self.layoutChanged.emit()
    def chunks(self, l, n):
        """Yield the list in n sized chunks"""
        for i in xrange(0, len(l),n):
            yield l[i:i+n]
    def flags(self,index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def load(self):
        values=self.db.query_db(self.select_query,bindings={"id":self.db.id},
                                                    pull_keys=self.pull_keys)
        self.updateData(values[0])
    def save(self):
        values =self.data  
        values['id'] = self.db.id
        success = self.db.query_db(self.insert_query,bindings=values)
        return success
    def headerData(self,section,orientation,role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.column_headers):
                    return self.column_headers[section]

            if orientation == QtCore.Qt.Vertical:
                if section < len(self.row_headers):
                    return self.row_headers[section]


