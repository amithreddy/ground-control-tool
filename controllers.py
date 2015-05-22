from PyQt4 import QtGui, QtCore, QtSql
import sqlqueries, main
import genericdelegates

rowheaders= ['back', 'north','south', 'east', 'west']

class Model(QtCore.QAbstractTableModel):
    def __init__(self,db, parent=None, data=None,select_query=None,insert_query=None,
                pull_keys=None,rowheaders=[],colheaders=[]):
        QtCore.QAbstractTableModel.__init__(self)
        self.db = db
        self.select_query = select_query
        self.insert_query = insert_query
        self.column_headers = colheaders
        self.row_headers = rowheaders
        self.pull_keys = pull_keys
        self.updateData(data)
    def rowCount(self,parent):
        return len(self.layout)
    def columnCount(self,parent):
        return len(self.layout[0])
    def data(self,index,role):
        if not index.isValid():
            return QtCore.QVariant()
        if role== QtCore.Qt.DisplayRole:
            row=index.row()
            column =index.column()
            key=self.layout[row][column]
            value = self.modeldata[key]
            return QtCore.QVariant(value)
        elif role == QtCore.Qt.UserRole:
            row=index.row()
            column =index.column()
            key=self.layout[row][column]
            value = self.modeldata[key]
            return value
        else:
            return QtCore.QVariant()
    def setData(self,index,value,role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                row=index.row()
                col=index.column()
                key=self.layout[row][col]
                self.modeldata[key]= value
                self.dataChanged.emit(index,index)
                return True
        return False
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable |QtCore.Qt.ItemIsUserCheckable
    def headerData(self,section,orientation,role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.column_headers[section]
            if orientation == QtCore.Qt.Vertical:
                    return self.row_headers[section]
        return None
    def load(self):
        values =self.db.query_db(self.select_query,bindings={"id":self.db.id},
                                                    pull_keys=self.pull_keys)
        self.updateData(values[0])
    def save(self):
        values =self.modeldata
        values['id'] = self.db.id
        success = self.db.query_db(self.insert_query,bindings=values)
        return success
    def updateData(self,newdata):
        self.layoutAboutToBeChanged.emit()
        if newdata is None:
            self.modeldata = {key:'' for key in self.pull_keys}
        else:
            assert ( type(newdata) is dict)
            self.modeldata = newdata
        num_col = len(self.column_headers)
        self.layout = [i for i in self.chunks(self.pull_keys,num_col)]
        self.layoutChanged.emit()
    def chunks(self, l, n):
        """Yield the list in n sized chunks"""
        for i in xrange(0, len(l),n):
            yield l[i:i+n]

class generictableView(QtGui.QTableView):
    def __init__(self, model, parent=None, delegates = []):
        QtGui.QTableView.__init__(self)
        QtGui.QTableView.setSizePolicy(self,QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setParent(parent)
        self.model=model
        self.setModel(self.model)
        self.adjustTableSize()
        self.setDelegates(delegates)
    def setDelegates(self, delegates):
        itemdel = genericdelegates.GenericDelegate()
        itemdel.setDelegates( delegates)
        self.setItemDelegate(itemdel)
    def adjustTableSize(self):
        columns=self.model.columnCount(None)
        rows=self.model.rowCount(None)
        tablewidth=0
        tablewidth+=self.verticalHeader().width()*2
        for i in range(columns):
            tablewidth += self.columnWidth(i)
        tableheight=0
        tableheight+= self.horizontalHeader().height()*2
        tablewidth=0
        tablewidth+=self.verticalHeader().width()+2
        for i in range(columns):
            self.setColumnWidth(i,self.sizeHintForColumn(i))
            tablewidth += self.columnWidth(i)
        tableheight=0
        tableheight+= self.horizontalHeader().height()+2
        for i in range(0,rows):
            tableheight+=self.rowHeight(i)
        self.setMaximumHeight(tableheight)
        self.setMaximumWidth(tablewidth)
    def sizeHintForColumn(self, column):
        fm = self.fontMetrics()
        max_width = fm.width('0123456789')
        return max_width
