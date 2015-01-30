from __future__ import unicode_literals
import sys
import os
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

def text_to_tuple(string): 
    """take a string which containts three numbers '1,1,1'
        and return a tuple (1,1,1)"""
    return tuple( (int(x) for x in string.split(',') ) )

def check(fields, callback):
    error=False
    for field in fields:
        validator =field.validator()
        state= validator.validate(field.text(),0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#ffffff' #yellow
        else:
            error=True
            color = '#f6989d' #red
        field.setStyleSheet('QLineEdit { background-color: %s }'%color)
    if error==False:
        callback([text_to_tuple(field.text())
            for field in fields])

regNumber =reg.match_nums
class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui= mining_ui.Ui_window()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtGui.QWidget(self)
        self.ui_elements()
        self.shape_tab()
        self.FactorA()
        #self.ui.Shape.clicked.connect(self.tabWidget.setCurrentWidget(self.ui.Shape) )
    def ui_elements(self):
        self.fields=[self.ui.b1, self.ui.b2, self.ui.b3, self.ui.b4,
                    self.ui.t1, self.ui.t2, self.ui.t3, self.ui.t4]
    def setValidator(self, fields,validator):
        [field.setValidator(validator) for field in self.fields]
    def shape_tab(self):
        grid= QtGui.QGridLayout()
        grid.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        l = MplCanvas(self.main_widget,width=4,height=4,dpi=100)
        l.compute_figure([])
        grid.addWidget(l,0,0)
        horizontal= self.ui.horizontalLayout
        horizontal.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        horizontal.addLayout(grid)
        validator= QtGui.QRegExpValidator(regNumber)
        self.setValidator(self.fields,validator)
        self.ui.ShapeSubmit.clicked.connect(
                    lambda: check(self.fields, l.compute_figure))
    def FactorA(self):
        al = ImgGraph(self.main_widget,imagename="test.png")
        al.setParent(self.ui.FactorA)
        adic={'back':(0,0), 'south':(10,10),
              'east':(20,20), 'north':(30,30),'west':(40,40)}
        al.plot(adic)

class sql:
    def __init__(self,name):
        self.connect(name)
        self.create_table()
    def connect(self, name):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(name)
        ok =self.db.open()
        if not ok:
            QtGui.QMessageBox.warning(None, "DB",
               QtCore.QString("database error: %1").arg(
                                            self.db.lastError().text()))
    def create_table(self):
        self.query= QtSql.QSqlQuery(self.db)
        a=self.query.exec_("""
                            CREATE TABLE IF NOT EXISTS STOPES(
                                            id INTEGER PRIMARY KEY,
                                            mine CHAR NOT NULL,
                                            orebody CHAR NOT NULL,
                                            level CHAR NOT NULL,
                                            stopename CHAR NOT NULL UNIQUE
                                            )
                            """
                        )
    def insert(self,values,update=False):
        if update:
            self.query.prepare(
                "REPLACE INTO STOPES (mine, orebody, level, stopename) \
                            VALUES(:mine, :orebody, :level, :stopename)"
                )
        else:
            self.query.prepare(
                "INSERT INTO STOPES (mine, orebody, level, stopename) \
                            VALUES(:mine, :orebody, :level, :stopename)"
                    )
        for key,val in values.iteritems():
            self.query.bindValue(":%s"%key, val)
        success=self.query.exec_()
        return success
    def select_row(self, values):
        self.query.prepare("""
                        SELECT * FROM STOPES 
                        WHERE orebody=:orebody 
                        AND stopename=:stopename AND level=:level
                        """
                        )
        for key,val in values.iteritems():
            self.query.bindValue(":%s"%key, val)
        success = self.query.exec_()
        if success == True:
            result={ key: None for key in values }
            self.query.next()
            for key in result:
                result[key]= str(self.query.record().value(key).toString())
            return result
        else:
            return False
    def record(self):
        pass
    def delete(self):
        pass

class NewRecord(QtGui.QDialog):
    def __init__(self,parent=None):
        super(NewRecord, self).__init__(parent)
        self.sql = sql(name='bob')
        mineLabel = QtGui.QLabel("&Mine:")
        self.Mine= QtGui.QLineEdit()
        mineLabel.setBuddy(self.Mine)

        levelLabel = QtGui.QLabel("&Level:")
        self.Level= QtGui.QLineEdit()
        levelLabel.setBuddy(self.Level)
        
        orebodyLabel = QtGui.QLabel("&OreBody:")
        self.OreBody = QtGui.QLineEdit()
        orebodyLabel.setBuddy(self.OreBody)

        stopeLabel = QtGui.QLabel("&Stope:")
        self.StopeName = QtGui.QLineEdit()
        stopeLabel.setBuddy(self.StopeName)

        today = QtCore.QDate.currentDate()
        self.Date = QtGui.QDateEdit()
        self.Date.setDate(today)

        self.saveButton = QtGui.QPushButton("Save")
        # signal submit click slot -> save function
        self.saveButton.clicked.connect(self.save)
        #create layout and add it to the qdialog
        horizontal = QtGui.QHBoxLayout()
        horizontal2 = QtGui.QHBoxLayout()
        [horizontal.addWidget(x) for x  in [mineLabel, self.Mine, levelLabel, self.Level]]
        [horizontal2.addWidget(x) for x in [orebodyLabel, self.OreBody, stopeLabel,
                                        self.StopeName, self.Date]]
        vertical = QtGui.QVBoxLayout()
        [vertical.addLayout(x) for x in [horizontal, horizontal2]]
        vertical.addWidget(self.saveButton)
        self.setLayout(vertical)
    def save(self):
        self.Date.date()
        values ={ "mine": self.Mine.text(), "orebody":self.OreBody.text(),
                  "level": self.Level.text(), "stopename": self.StopeName.text() }
        success= self.sql.insert(values)
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
                self.sql.insert(values, update=True)
                self.close()
            else:
                # wait for fruther action by the user
                pass

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

if __name__ == "__main__":
    qApp = QtGui.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())
