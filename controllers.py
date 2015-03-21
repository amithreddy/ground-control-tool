from PyQt4 import QtGui, QtCore, QtSql
import sqlqueries
import main,reg

rowheaders= [
            'back',
            'north',
            'south',
            'east',
            'west']

class NumDelegate(QtGui.QStyledItemDelegate):
    def __init__(self,parent=None):
        super(NumDelegate,self).__init__(parent)
    def createEditor(self,parent,option,index):
        lineEdit= QtGui.QLineEdit(parent)
        lineEdit.setFrame(False)
        regExp =reg.match_one_num
        validator = QtGui.QRegExpValidator(regExp)
        lineEdit.setValidator(validator)
        return lineEdit
    def setEditorData(self,editor,index):
        value = index.model().data(index,QtCore.Qt.UserRole)
        if editor is not None:
            editor.setText(value)
    def setModelData(self, editor, model,index):
        if not editor.isModified():
            return
        text = editor.text()
        validator = editor.validator()
        if validator is not None:
            state,text =validator.validate(text,0)

        if state == QtGui.QValidator.Acceptable:
            color = '#ffffff' #white
            model.setData(index, editor.text())
        else:
            color = '#f6989d' #red
        editor.setStyleSheet('QLineEdit { background-color: %s }'%color)

class Model(QtCore.QAbstractTableModel):
    def __init__(self,db, parent=None, data=None,select_query=None,insert_query=None,
                pull_keys=None,rowheaders=[],colheaders=[]):
        QtCore.QAbstractTableModel.__init__(self)
        self.db=db
        self.select_query=select_query
        self.insert_query=insert_query
        self.column_headers= colheaders
        self.row_headers = rowheaders
        if data is None:
            self.modeldata= {key:'' for key in pull_keys}
        else:
            self.modeldata=data
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
            value = self.modeldata[key]
            return value
        if role == QtCore.Qt.UserRole:
            row=index.row()
            column =index.column()
            key=self.layout[row][column]
            value = self.modeldata[key]
            return value
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
    def updateData(self,newdata):
        self.layoutAboutToBeChanged.emit()
        self.modeldata=newdata
        self.layoutChanged.emit()
    def chunks(self, l, n):
        """Yield the list in n sized chunks"""
        for i in xrange(0, len(l),n):
            yield l[i:i+n]
    def flags(self,index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
    def load(self):
        values = self.db.query_db(self.select_query,bindings={"id":self.db.id},
                                                    pull_keys=self.pull_keys)
        self.updateData(values[0])
    def save(self):
        values =self.modeldata  
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

class generictableView(QtGui.QTableView):
    def __init__(self, model,delegate, parent=None):
        QtGui.QTableView.__init__(self)
        QtGui.QTableView.setSizePolicy(self,
                                       QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        self.model=model
        self.setModel(model)
        self.setItemDelegate(delegate)
        self.setParent(parent)
        self.adjustTableSize()
    def adjustTableSize(self):
        columns=self.model.columnCount(None)
        rows=self.model.rowCount(None)

class generictableView(QtGui.QTableView):
    def __init__(self, model,delegate, parent=None):
        QtGui.QTableView.__init__(self)
        QtGui.QTableView.setSizePolicy(self,
                                       QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        self.model=model
        self.setModel(model)
        self.setItemDelegate(delegate)
        self.setParent(parent)
        self.adjustTableSize()
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
