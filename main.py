from __future__ import unicode_literals
import sys, os
import random
import itertools
import re

from PyQt4 import QtGui, QtCore, QtSql
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg 

import reg
import mining_ui
from geometry import *
import sqlqueries

progname = os.path.basename(sys.argv[0])
progversion = "0.1"
def unpack(points):
    """ takes[(x,y,z),(1,1,1),(2,2,2)] and returns
        [x,1,2],[y,1,2],[z,1,2] """
    if len(points[0])==3:
        x,y,z= ([point[0] for point in points],
            [point[1] for point in points],
            [point[2] for point in points]
            )
        return x,y,z
    else:
        x,y= ( 
                [point[0] for point in points],
                [point[1] for point in points]
                )
        return x,y

color ={
        'top': 'red', 'bottom':'blue',
        'left': 'black', 'right':'green'
        }
color_to_view= { val:key for key,val in color.iteritems()} 
class MplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100):
        self.fig = plt.figure(figsize=(width,height),dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
    def create_subplot(self,number,_3d=False):
        if _3d:
            axes= self.fig.add_subplot(number,projection='3d')
            axes.mouse_init()
            axes.set_axis_off()
        else:
            axes = self.fig.add_subplot(number) 
        axes.hold(True)
        return axes
    def draw_view(self,view=None):
        x,y,z=0,1,2
        if view=="plan":i,c=x,y
        elif view=="front":i,c=x,z
        elif view=="side":i,c=y,z
        else: 
            return "ERROR NO VIEW"
    
        p1,p2,p3,p4,p5,p6,p7,p8=[(point[i],point[c]) for point in self.points]
        views = {
            'top':[p5,p6,p7,p8],
            'bottom':[p1,p2,p3,p4],
            'left': [p1,p5,p6,p2],
            'right':[p7,p3, p8,p4]
            }
    
        def front_or_side(axes):
            self.draw_plot(view, views['top'],axes, color=color['top'])
            self.draw_plot(view, unpack(views['left'][:2]), axes, color=color['left'])
            self.draw_plot(view, unpack(views['left'][2:]), axes, color=color['left'])
            self.draw_plot(view, unpack(views['right'][:2]), axes, color=color['right'])
            self.draw_plot(view, unpack(views['right'][2:]), axes, color=color['right'])
            self.draw_plot(view, views['bottom'], axes, color=color['bottom'])
            
        if view=="plan":
            self.draw_plot(view, views['bottom'], self.plan, color=color['bottom'])
            self.draw_plot(view, views['top'], self.plan, color=color['top'])
            self.adjust_lim(self.plan)
        elif view=="front":
            front_or_side(self.front)
            self.adjust_lim(self.front)
        elif view=="side":
            front_or_side(self.side)
            self.adjust_lim(self.side)
    def draw_plot3d(self,axes):
        p1,p2,p3,p4,p5,p6,p7,p8 = self.points
        views = {
                'top':[p5,p6,p7,p8,p5],
                'bottom':[p1,p2,p3,p4,p1],
                'left': [p1,p5,p6,p2],
                'right':[p7,p3,p8,p4]
                }
        axes.plot3D(*unpack(views['top']), color=color['top'])
        axes.plot3D(*unpack(views['left'][:2]), color=color['left'])
        axes.plot3D(*unpack(views['left'][2:]), color=color['left'])
        axes.plot3D(*unpack(views['right'][2:]), color=color['right'])
        axes.plot3D(*unpack(views['right'][:2]), color=color['right'])
        axes.plot3D(*unpack(views['bottom']), color=color['bottom'])
    def draw_plot(self,view,_set,axes,color='black'):
        axes.set_title(view,fontsize=12)
        if len(_set)==4:
            x,y= self.line(_set)
        else:
            x,y= _set
        axes.grid()
        axes.axis('equal')
        axes.plot(x,y,color=color,label=color_to_view[color],linewidth=2.0)
    def adjust_lim(self,axes):        
        xticks= axes.get_xticks()
        #shift a half a step to the left
        # x0 - (x1- x0)/ 2 = (3*x0-x1)/2
        xmin = (3*xticks[0] - xticks[1])/2
        #shift a half a tick to the right
        xmax = (3*xticks[-1] - xticks[-2])/2
        axes.set_xlim(xmin,xmax)
        
        yticks= axes.get_yticks()
        #shift a half a step to the left
        # y0 - (y1- y0)/ 2 = (3*y0-y1)/2
        ymin = (3*yticks[0] - yticks[1])/2
        #shift a half a tick to the right
        ymax = (3*yticks[-1] - yticks[-2])/2
        axes.set_ylim(ymin,ymax)

        axes.set_xticks([min(xticks),max(xticks)/2,max(xticks)])
    def line(self,points):
        Path = mpath.Path
        p1,p2,p3,p4=points
        path_data =[
                    (Path.MOVETO, p1),
                    (Path.CURVE4, p2),
                    (Path.CURVE4, p3),
                    (Path.CURVE4, p4),
                    (Path.CLOSEPOLY,p1)
                    ]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        
        # plot control points and connecting lines
        x, y = zip(*path.vertices)
        return x,y
    def compute_figure(self,points):
        # points need in this order
        # [b1,b2,b3,b4, t1,t2,t3,t4]
        plt.clf() 
        self.front = self.create_subplot(221) 
        self.plan = self.create_subplot(222) 
        self.side = self.create_subplot(223)
        self.axes3d = self.create_subplot(224, _3d='True')
        if len(points) > 0:
            self.points= points
            self.draw_view(view='front')
            self.draw_view(view='side')
            self.draw_view(view='plan')
            self.draw_plot3d(self.axes3d)
            self.draw()
        """
        handles,labels = self.front.get_legend_handles_labels()
        handles=[handles[0],handles[1],handles[-2],handles[-1]]
        labels=set(labels)
        
        self.fig.legend(handles, labels, bbox_to_anchor=(1,0.5),
            loc='upper right', borderaxespad=0,fontsize=10,ncol=6)
        self.fig.tight_layout(h_pad=3)
        """
        self.fig.tight_layout()
    def sizeHint(self):
        w, h =self.get_width_height()
        return QtCore.QSize(w,h)

class ImgGraph(FigureCanvas):
    """ Fixed y and x axis. On running plots a line, and updates it with
    user data"""
    def __init__(self,parent=None, imagename=None,origin=(0,0),width=5,height=5,dpi=100):
        self.fig = plt.figure(figsize=(width,height),dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        FigureCanvas.updateGeometry(self)
        self.axes = self.fig.add_subplot(111)
        self.setParent(parent)
        self.img = mpimg.imread(imagename)
        self.origin = origin
    def clear(self):
        self.axes.clear()
        self.axes.imshow(self.img)
    def adjust_points(self,dic):
        new_dic={}
        for key, val in dic.iteritems():
            x,y = val
            x+=self.origin[0]; y+= self.origin[1]
            new_dic[key]=(x,y)
        return new_dic
    def plot(self,dic):
        self.clear()
        colors = { 'back':'green', 'south':'gray','east':'blue',
                'north':'black','west':'red'}
        # here we will plot a scatter plot
        # for each point we will assign a color
        for key, val in self.adjust_points(dic).iteritems():
            x,y= val
            plt.scatter( x,y, color=colors[key], label=key)
        plt.legend(bbox_to_anchor=(0.5,-0.05), loc='upper center',
                borderaxespad=0,scatterpoints=1,fontsize=10,ncol=5)

class TemplateTab(object):
    def __init__(self, db,insert_query=None, select_query=None):
        self.db = db
        self.insert_query =insert_query
        self.select_query = select_query
    def get_values(self,uielements=None):
        if uielements is None: uielements= self.uielements
        values ={}
        if uielements['fields']:
            for key,element in uielements['fields'].iteritems():
                values[key]= str(element.text())

        if uielements['checkboxes']:
            for key, element in uielements['checkboxes'].iteritems():
                values[key] = element.checkState()
        return values
    def clear_data(self,uielements=None):
        if uielements is None: uielements= self.uielements
        if uielements['fields']:
            for key, field in uielements['fields'].iteritems():
                field.setText('')
        if uielements['checkboxes']:
            for key, checkbox in uielements['checkboxes'].iteritems():
                chekbox.setChecked(False)
    def set_data(self,data,uielements=None):
        if uielements is None: uielements= self.uielements
        self.clear_data()
        if uielements['fields']:
            for key,field in uielements['fields'].iteritems():
                field.setText(data[key])
        elif uielements['checkboxes']:
            for key,checkbox in uielements['checkbox'].iteritems():
                if uielements['checkboxes'][key]:
                    checkbox.setChecked(True)
        else:
            pass
    def setValidator(self,fields):
        validator= QtGui.QRegExpValidator(reg.match_nums)
        [field.setValidator(validator) for field in fields]
    def load(self):
        # pulls data from sql table
        # and also places into appropriate fields
        values=self.db.query_db(self.select_query,
                bindings={"id":self.db.id},pull_keys=self.pull_keys)
        self.set_data(values[0])
    def save(self):
        #takes data from fields and pushes data to sql table
        values =self.get_values()
        values['id']=self.db.id
        success=self.db.query_db(self.insert_query,values)
        return success

class CriticalJSTab(TemplateTab):
    def __init__(self,ui,db):
        TemplateTab.__init__(self,db,insert_query= None,select_query= None)

        self.criticalJS_select =sqlqueries.criticalJS_select
        self.criticalJS_insert = sqlqueries.criticalJS_insert
        self.Q_insert= sqlqueries.Q_insert
        self.Q_select= sqlqueries.Q_select
        self.criticaljs_keys=sqlqueries.criticaljs_keys 
        self.Q_keys= sqlqueries.Q_keys
        self.ui= ui
        self.Critical_Joints={
            'fields':{  
                'backdip':self.ui.backdip,'backdirection':self.ui.backdirection,
                'northdip':self.ui.northdip,'northdirection':self.ui.northdirection,
                'southdip':self.ui.southdip,'southdirection':self.ui.southdirection,
                'eastdip':self.ui.eastdip,'eastdirection':self.ui.eastdirection,
                'westdip':self.ui.westdip,'westdirection':self.ui.westdirection},
            'checkboxes':{
                'backworstcase':self.ui.backworstcase,'backexamineface':self.ui.backexamineface, 
                'northworstcase':self.ui.northworstcase,'northexamineface':self.ui.northexamineface, 
                'southworstcase':self.ui.southworstcase,'southexamineface':self.ui.southexamineface, 
                'eastworstcase':self.ui.eastworstcase,'eastexamineface':self.ui.eastexamineface, 
                'westworstcase':self.ui.westworstcase,'westexamineface':self.ui.westexamineface
                    }
                }
        self.Rock_Face_Q ={ 
                'fields':{
                'rockback':self.ui.rockback,'rocknorth':self.ui.rocknorth,
                'rocksouth':self.ui.rocksouth,'rockeast':self.ui.rockeast,
                'rockwest':self.ui.rockwest, 'q_minimum':self.ui.q_minimum,
                'q_maximum':self.ui.q_maximum,'q_most_likely':self.ui.q_mostlikely
                    },
                'checkboxes':{}
            }
        self.fields={}
        self.fields.update(self.Critical_Joints['fields'])
        self.fields.update(self.Rock_Face_Q['fields'])
        self.checkboxes = {}
        self.checkboxes.update(self.Critical_Joints['checkboxes'])
        self.uielements= {"fields":self.fields, "checkboxes":None}
        self.Project_Q_Range = None
        self.setValidator(list(self.fields.itervalues()))
    def connect(self,function):
        pass
    def load(self):
        values ={}
        criticalJSvalues=self.db.query_db(self.criticalJS_select,
                    bindings= {"id":self.db.id},pull_keys=self.criticaljs_keys)
        Qvalues=self.db.query_db(self.Q_select,
                                bindings= {"id":self.db.id},pull_keys=self.Q_keys)
        values.update(criticalJSvalues[0])
        values.update(Qvalues[0])
        self.set_data(values)
    def save(self):
        critical_js_values =self.get_values(uielements=self.Critical_Joints)
        critical_js_values['id']=self.db.id

        Q_values =self.get_values(uielements=self.Rock_Face_Q)
        Q_values['id']=self.db.id
        successCJS=self.db.query_db(self.criticalJS_insert,critical_js_values)
        successQ=self.db.query_db(self.Q_insert,Q_values)
        return all([ successQ,successCJS ])

class ShapeTab(TemplateTab):
    def __init__(self,ui,db,insert_query=None,select_query=None):
        TemplateTab.__init__(self,db,insert_query= sqlqueries.shape_insert,
                            select_query= sqlqueries.shape_select )
        self.pull_keys =sqlqueries.shape_keys 
        self.ui= ui
        self.fields={
        'b1':self.ui.b1,'b2':self.ui.b2,'b3':self.ui.b3,'b4':self.ui.b4,
        't1':self.ui.t1,'t2':self.ui.t2,'t3':self.ui.t3,'t4':self.ui.t4 }
        self.uielements= { 'fields':self.fields, 'checkboxes':None}
        grid= QtGui.QGridLayout()
        grid.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.graph = MplCanvas(width=4,height=4,dpi=100)
        self.graph.compute_figure([])

        grid.addWidget(self.graph,0,0)
        horizontal= self.ui.horizontalLayout
        horizontal.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        horizontal.addLayout(grid)

        regNumber =reg.match_nums
        self.setValidator(list(self.fields.itervalues()))
        self.connect(self.graph.compute_figure)
    def text_to_tuple(self, string): 
        """take a string which containts three numbers '1,1,1'
            and return a tuple (1,1,1)"""
        return tuple( (float(x) for x in string.split(',') ) )
    def check(self, fields, callback):
        error=False
        for field in fields:
            validator =field.validator()
            state= validator.validate(field.text(),0)[0]
            if state == QtGui.QValidator.Acceptable:
                color = '#ffffff' #white
            else:
                error=True
                color = '#f6989d' #red
            field.setStyleSheet('QLineEdit { background-color: %s }'%color)
        if error is False:
            callback([self.text_to_tuple(field.text())
                                    for field in fields])
    def connect(self,function):
        self.ui.ShapeSubmit.clicked.connect(
                    lambda: self.check(list(self.fields.itervalues()),function)) 

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self,db ):
        QtGui.QMainWindow.__init__(self)
        self.ui= mining_ui.Ui_window()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtGui.QWidget(self)
        self.db = db 
        self.ShapeTab = ShapeTab( self.ui, self.db)
        self.FactorA()
    def save(self):
        self.ShapeTab.save()
    def FactorA(self):
        al = ImgGraph(self.main_widget,imagename="test.png")
        al.setParent(self.ui.FactorA)
        adic={'back':(0,0), 'south':(10,10),
              'east':(20,20), 'north':(30,30),'west':(40,40)}
        al.plot(adic)

class sqldb: 
    def __init__(self,name="MiningStopes",connectionName=None):
        self.connect(name,connectionName)
        self.create_tables()
    def connect(self, name,connectionName):
        self.name=name
        if connectionName == None:
            self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        else:
            self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE", connectionName)
        self.db.setDatabaseName(self.name)
        ok =self.db.open()
        if not ok:
            QtGui.QMessageBox.warning(None, "DB",
               QtCore.QString("database error: %1").arg(
                                            self.db.lastError().text()))
    def close(self):
        connection = self.db.connectionName()
        self.db.close()
        self.db= QtSql.QSqlDatabase()
        self.db.removeDatabase(connection)
    def create_tables(self):
        self.query_db(sqlqueries.header_schema)
        self.query_db(sqlqueries.shape_schema)
        self.query_db(sqlqueries.criticalJS_schema)
        self.query_db(sqlqueries.Q_schema)
        self.query_db(sqlqueries.FactorA_schema)
    def bind(self,query,bindings):
        for key,val in bindings.iteritems():
                if val ==None:
                    #create a Null value for sqlite
                    NULL = QtCore.QVariant(QtCore.QString).toString()
                    query.bindValue(":%s"%key,NULL)
                else:
                    query.bindValue(":%s"%key, val)
    def query_db(self, sqlstr, bindings =None, pull_keys=None):
        self.query=QtSql.QSqlQuery(self.db)
        self.query.prepare(sqlstr)
        if bindings is not None:
            self.bind(self.query,bindings)
        else: pass

        success=self.query.exec_()
        if  self.query.isSelect() is True:
            if success is True:
                result= []
                while self.query.next():
                    result.append(self.extract_values(self.query,pull_keys))
                return result
            else:
                print self.query.lastError().text(), sqlstr
                return False 
        else: #this is a insert query or a create table query
            if success is True:
                return True
            else:
                # this is a failed insert query
                print self.query.lastError().text(),sqlstr,bindings
                return False
    def extract_values(self, query, keys):
        row={key: None for key in keys }
        for key in row:
            row[key]= str(query.record().value(key).toString())
        return row

class SearchDBDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(SearchDBDialog, self).__init__(parent)
        self.mineLabel = QtGui.QLabel("&Mine:")
        self.Mine= QtGui.QLineEdit()
        self.mineLabel.setBuddy(self.Mine)

        self.levelLabel = QtGui.QLabel("&Level:")
        self.Level= QtGui.QLineEdit()
        self.levelLabel.setBuddy(self.Level)
        
        self.orebodyLabel = QtGui.QLabel("&OreBody:")
        self.OreBody = QtGui.QLineEdit()
        self.orebodyLabel.setBuddy(self.OreBody)

        self.stopeLabel = QtGui.QLabel("&Stope:")
        self.StopeName = QtGui.QLineEdit()
        self.stopeLabel.setBuddy(self.StopeName)
        
        self.ui = { 'mine':self.Mine, 'level':self.Level,
                'orebody':self.OreBody, 'stopename': self.StopeName}
    def get_values(self):
        values={}
        #repalces empty string with None
        no_empty_str= lambda x:str(x) if len(x)>0 else None
        for key, value in self.ui.iteritems():
            values[key] = no_empty_str(value.text())
        return values

class NewRecord(SearchDBDialog):
    # create a new record in the database
    def __init__(self,db, parent=None):
        super(NewRecord, self).__init__(parent)
        self.db=db
        today = QtCore.QDate.currentDate()
        self.Date = QtGui.QDateEdit()
        self.Date.setDate(today)

        self.saveButton = QtGui.QPushButton("Save")
        # signal submit click slot -> save function
        self.saveButton.clicked.connect(self.save)
        #create layout and add it to the qdialog
        horizontal = QtGui.QHBoxLayout()
        horizontal2 = QtGui.QHBoxLayout()
        [horizontal.addWidget(x) for x  in [self.mineLabel, self.Mine, 
                                            self.levelLabel, self.Level]]
        [horizontal2.addWidget(x) for x in [self.orebodyLabel, self.OreBody, self.stopeLabel,
                                            self.StopeName, self.Date]]
        vertical = QtGui.QVBoxLayout()
        [vertical.addLayout(x) for x in [horizontal, horizontal2]]
        vertical.addWidget(self.saveButton)
        self.setLayout(vertical)
        self.Date.date()
    def save(self):
        success= self.db.query_db(sqlqueries.header_insert,
                                    bindings=self.get_values())
        if success == False:
            # return a QMessageBox that  saying the data exists already
            # ask if they want to overwrite it
            message ="A record with that stope name already exists.\
                    Would you like to replace it?"
            reply = QtGui.QMessageBox.question(self,"Error", message,
                                QtGui.QMessageBox.Yes| QtGui.QMessageBox.No
                                            )
            # test empty values , or add a qvalidator not to allow blanks
            if reply == QtGui.QMessageBox.Yes:
                self.db.query_db(sqlqueries.header_insert_update,bindings=values)
                self.close()
            else:
                # wait for further action by the user
                pass

class SQLTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], headers=[], parent = None):
        super(SQLTableModel, self).__init__(parent)
        self.headers = headers
        self.data_list = data
    def rowCount(self, parent):
        return len(self.data_list) 
    def columnCount(self, parent):
        return len(self.headers)
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row= index.row()
            column= index.column()
            value = self.data_list[row][column]
            return value
    def updateData(self,raw):
        self.layoutAboutToBeChanged.emit()
        self.data_list = self.rawDataHandler(raw)
        self.layoutChanged.emit()
    def rawDataHandler(self,raw):
        keys = ['mine','orebody','level','stopename']
        data = []
        for row in raw:
            data.append([row[key] for key in keys]) 
        return data
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "not implemented"
            else:
                return "None"

class OpenDialog(SearchDBDialog):
    def __init__(self,db,parent=None):
        super(OpenDialog,self).__init__(parent)
        self.db=db
        #set up table view
        self.headers = sqlqueries.header_keys
        self.table = QtGui.QTableView()
        self.model = SQLTableModel(headers= self.headers)
        self.table.setModel(self.model)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        # signal submit click slot -> search function
        self.searchButton = QtGui.QPushButton("Search")
        self.searchButton.clicked.connect(self.search)

        # signal open click slot -> open_ function
        self.openButton = QtGui.QPushButton("open")
        self.openButton.clicked.connect(self.open_)

        horizontal = QtGui.QHBoxLayout()
        horizontal2 = QtGui.QHBoxLayout()
        [horizontal.addWidget(x) for x  in [self.mineLabel, self.Mine,
                                            self.levelLabel, self.Level]]
        [horizontal2.addWidget(x) for x in [self.orebodyLabel, self.OreBody,
                                            self.stopeLabel,self.StopeName]]
        vertical = QtGui.QVBoxLayout()
        [vertical.addLayout(x) for x in [horizontal, horizontal2]]
        vertical.addWidget(self.searchButton)
        vertical.addWidget(self.table)
        vertical.addWidget(self.openButton)
        self.setLayout(vertical)
        
        # on open the the tableview contains all the values of the databse
        self.fill_all()
    def fill_all(self):
        # fill the table view with the last 100 of the data from the db
        values={'mine':None,'orebody':None,'level':None,'stopename':None}
        rows=self.db.query_db(sqlqueries.header_select,
                        bindings=values,pull_keys=values)
        self.model.updateData(rows)
    def search(self):
        values = self.db.query_db(sqlqueries.header_select,
                                    bindings=self.get_values(),pull_keys=self.get_values())
        # update the model's data
        self.model.updateData(values)
    def open_(self):
        # this should set the sqldb's id to the selecteds' row
        # this should call fillout method of main application
        pass
# to add
# to be implemented
    # Export Import SQL
    # Import .DHR files
    # search sql from search field, and list
def export_sql(src,dst):
    pass
def import_sql(src,dst):
    #attach sqlite command
    #on conflict
    #if user wants to replace with the new db
        #insert_or_replace command
    #if the user want to ignore conflicts
        #insert ignore
    pass
def mkQApp():
    if QtGui.QApplication.instance() is None:
        global qApp
        qApp =QtGui.QApplication(sys.argv)

if __name__ == "__main__":
    qApp = None
    mkQApp()
    #aw = ApplicationWindow()
    #aw.setWindowTitle("%s" % progname)
    #aw.show()
    sys.exit(qApp.exec_())
