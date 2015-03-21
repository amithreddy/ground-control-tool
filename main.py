from __future__ import unicode_literals
import sys, os, shutil
import random
import itertools
import re

from PyQt4 import QtGui, QtCore, QtSql
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.path as mpath
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.image as mpimg 
import numpy as np
import controllers 
import reg
import mining_ui
from geometry import *
import sqlqueries
import scipy
from scipy import interpolate

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
class ShapeCanvas(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100):
        self.fig = Figure((width,height),dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        sizePolicy= QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                   QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHeightForWidth(True)
        FigureCanvas.setSizePolicy(self,sizePolicy)
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
    def draw_stope(self,axes):
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
    def convert_points(self,pointsdict,keys=None):
        # points need in this order
        points_keys= keys
        try:
            rawpoints= [pointsdict[key] for key in points_keys]
        except KeyError:
            #give the user gui feed back here 
            return []
        # here I combine seperate x,y,z values into one tuple
        points=[]
        for x in xrange(0,len(rawpoints),3):
            points.append(tuple(float(x) for x in rawpoints[x:x+3]))
        return points
    def compute_figure(self,pointsdict):
        self.fig.clear()
        self.front = self.create_subplot(221)
        self.plan = self.create_subplot(222)
        self.side = self.create_subplot(223)
        self.axes3d = self.create_subplot(224, _3d='True')
        self.points= self.convert_points(pointsdict, keys=sqlqueries.shape_keys)
        if len(self.points) > 0:
            self.draw_view(view='front')
            self.draw_view(view='side')
            self.draw_view(view='plan')
            self.draw_stope(self.axes3d)
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
    def heightForWidth(self, width):
        return width

class StopeVisualization(ShapeCanvas):
    def compute_figure(self,pointsdict):
        self.fig.clear()
        self.axes3d = self.create_subplot(111,_3d='True')
        self.points = self.convert_points(pointsdict,keys=sqlqueries.shape_keys)
        self.draw_stope(self.axes3d)
        self.draw_plane(self.axes3d,[(0,0,0.5), (0,1,0.5),(1,1,0.5),(1,0,0.5)])
        self.draw()
        self.fig.tight_layout()
    def draw_plane(self, axes,points):
        # points in this format
        # p1 p2 p3 p4
        # (x,y,z), (x2,y2,z2)...
        poly3d = Poly3DCollection([points])
        axes.add_collection3d(poly3d)

def factorA(x):
    """ returns values of factor a given x,
        where x is UCS/Oi (stress (MPa))
    """
    if x <=2: return 0.1
    
    if 2 <x and x<10: 
        return 0.1125*x -0.125
    if x>=10: 
        return 1.0

class BaseGraph(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100):
        self.fig = Figure((width,height),dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        sizePolicy= QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                   QtGui.QSizePolicy.MinimumExpanding)
        FigureCanvas.setSizePolicy(self,sizePolicy)
        self.setParent(parent)
        self.colors = { 
                    'back':'red',
                    'north':'yellow',
                    'south':'orange',
                    'east':'blue',
                    'west':'green'
                        }
        self.draw_all()
    def plot(self, axes, formula, x_range):
        x = np.array(x_range)
        y = [formula(xx) for xx in x]
        axes.plot(x,y,color='black',linewidth=2.0)
    def plot_scatter(self,axes,pointsdict):
        x= []
        y= []
        color_list= []
        for key,color in self.colors.iteritems():
            x.append(pointsdict[key][0])
            y.append(pointsdict[key][1])
            color_list.append(color)
        axes.scatter(x,y,c=color_list,s=30)

class FactorA(BaseGraph):
    def adjust_lim(self,axes):
        ymin =0
        ymax =1.1
        axes.set_ylim(ymin,ymax)
        axes.set_xlim(0)
    def draw_all(self):
        values= { 
                    'back':(1,0.5),
                    'north':(1,0.4),
                    'south':(1,0.3),
                    'east':(1,0.2),
                    'west':(1,0.1)
                        }
        self.fig.clear()
        self.axes= self.fig.add_subplot(111)
        self.plot(self.axes,factorA,xrange(15))
        self.plot_scatter(self.axes, values)
        self.adjust_lim(self.axes)
        self.draw()

def factorc():
    x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    y = [2.0,2.1,2.4,2.8,3.4,4.1,5.0,5.9,7.0,8.0]
    p= np.poly1d ( np.polyfit(x,y,3) )
    xnew = np.linspace(x[0],x[-1])
    return xnew, p

class FactorC(BaseGraph):
    def draw_all(self):
        self.fig.clear()
        self.axes= self.fig.add_subplot(111)
        self.plot(self.axes,factorc()[1], xrange(90))

class FactorB(BaseGraph):
    def draw_all(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        # diff in strike 0 degrees
        x = np.array([0,10,20,30,40,45,50,60,70,80,90])
        y = np.array([0.3, 0.2,0.2,0.2,0.4,0.5,0.6,0.8,0.867,0.933,1])
        self.axes.plot(x,y) 
        # diff in strike 90 degrees
        x = np.array([10,20,30,40,50,60,70,80,90])
        y = np.array([1,1,1,1,1,1,1,1,1])
        self.axes.plot(x,y) 
        # diff in strike 45 degrees
        x= np.array([10,20,30,40,45,90])
        y= np.array([0.5, 0.55, 0.6, 0.7333,0.8,1])
        self.axes.plot(x,y) 
        # diff in strike 60 degrees
        x= np.array([10, 40, 90])
        y= np.array([0.81, 0.85, 1])
        self.axes.plot(x,y) 
        # diff in strike 30 degress
        x = np.array([10, 45, 60, 70, 90])
        y = np.array([0.2, 0.6, 0.835, 0.864, 1])
        self.axes.plot(x,y) 
        
class ImgGraph(FigureCanvas):
    """ Fixed y and x axis. On running plots a line, and updates it with
    user data"""
    def __init__(self,parent=None, imagename=None,origin=(0,0),width=5,height=5,dpi=100):
        self.fig = Figure((width,height),dpi=dpi)
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

class FactorATab():
    def __init__(self, ui,db):
        self.db =db
        self.model=controllers.Model(self.db, data=None,
                colheaders =[   'mpa','backucs','factor A'],
                rowheaders= controllers.rowheaders,
                pull_keys =sqlqueries.FactorA_keys,
                select_query=sqlqueries.FactorA_select,
                insert_query=sqlqueries.FactorA_insert)

        delegate = controllers.NumDelegate()
        self.table=controllers.generictableView(self.model,delegate)
        self.ui= ui
        layout= QtGui.QHBoxLayout()
        layout.addWidget(self.table)
        self.graph= FactorA()
        layout.addWidget(self.graph)
        self.ui.FactorA.setLayout(layout)
    def load(self):
        self.model.load()

class FactorBTab():
    def __init__(self,ui,db):
        self.db=db
        self.model=controllers.Model(self.db, data=None,
                colheaders = ['FactorB'],
                rowheaders= controllers.rowheaders,
                pull_keys=sqlqueries.FactorB_keys, 
                select_query=sqlqueries.FactorB_select,
                insert_query=sqlqueries.FactorB_insert)
        delegate = controllers.NumDelegate()
        self.table=controllers.generictableView(self.model,delegate)
        self.ui=ui
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.table)
        self.ui.FactorB.setLayout(layout)
    def load(self):
        self.model.load()

class StabilityNumberTab():
    def __init__(self,ui,db):
        self.db=db
        self.model=controllers.Model(self.db, data=None,
                        colheaders = ["N'"],
                        rowheaders= [
                            'back',
                            'north',
                            'south',
                            'east',
                            'west'],
                        pull_keys=sqlqueries.StabilityNumber_keys, 
                        select_query=sqlqueries.StabilityNumber_select,
                        insert_query=sqlqueries.StabilityNumber_insert)
        delegate = controllers.NumDelegate()
        self.table=controllers.generictableView(self.model,delegate)
        self.ui=ui
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.table)
        self.ui.StabilityNumber.setLayout(layout)
    def load(self):
        self.model.load()

class CriticalJSQTab():
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db
        self.criticaljsmodel = controllers.Model(self.db, data=None,
                colheaders = ['Dip','Direction','Worst Case','Examine Face'],
                rowheaders= controllers.rowheaders,
                pull_keys=sqlqueries.criticalJS_keys,
                select_query=sqlqueries.criticalJS_select,
                insert_query=sqlqueries.criticalJS_insert)
        delegate=controllers.NumDelegate()
        self.criticaljstable= controllers.generictableView(self.criticaljsmodel,delegate)
        self.qmodel = controllers.Model(self.db, data=None,
                colheaders = ["Rock Face Q'"],
                rowheaders = controllers.rowheaders,
                pull_keys= sqlqueries.Q_keys,
                select_query=sqlqueries.Q_select,
                insert_query=sqlqueries.Q_insert)
        self.qtable = controllers.generictableView(self.qmodel, delegate)
        
        headers =["Min","Most_Likely","Max"]
        self.minimodel = controllers.Model(self,db, data=None,
                colheaders = ["Values"],
                rowheaders = headers,
                pull_keys= headers,
                select_query=None,
                insert_query=None)
        #max button
        #min button
        #most likely button
        
        self.toggletable = controllers.generictableView(self.minimodel, delegate)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.qtable, 0,0)
        layout.addWidget(self.toggletable,0,2)
        layout.addWidget(self.criticaljstable, 3,0, 2,2)
        self.ui.criticalJS.setLayout(layout)
    def load(self):
        self.criticaljsmodel.load()
        self.qmodel.load()
    def save(self):
        self.criticaljsmodel.save()
        self.qmodel.save()

class ShapeTab():
    def __init__(self,ui,db,insert_query=None,select_query=None):
        self.db= db
        self.model= controllers.Model(self.db,
                            insert_query= sqlqueries.shape_insert,
                            select_query= sqlqueries.shape_select,
                            colheaders = ['x','y','z'],
                            rowheaders= ['t1','t2','t3','t4',
                                         'b1','b2','b3','b4'],
                            pull_keys=sqlqueries.shape_keys)
        self.ui= ui
        regNumber= reg.match_one_num
        delegate= controllers.NumDelegate()
        self.table= controllers.generictableView(self.model, delegate)

        self.ui.ShapeSubmit =QtGui.QPushButton()
        self.graph = ShapeCanvas(width=4,height=4,dpi=100)
        self.graph.compute_figure({})
        self.connect(self.graph.compute_figure)

        layout= QtGui.QGridLayout()
        layout.addWidget(self.table,0,0,2,2)
        layout.addWidget(self.ui.ShapeSubmit,2,1)
        layout.addWidget(self.graph,0,3,4,4)
        self.ui.Shape.setLayout(layout)
    def connect(self,function):
        self.ui.ShapeSubmit.clicked.connect(
                    lambda: function(self.model.modeldata))
    def load(self):
        s=self.model.load()
        return s
    def save(self):
        return self.model.save()

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self,db ):
        QtGui.QMainWindow.__init__(self)
        self.ui= mining_ui.Ui_window()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.db = db
        self.ShapeTab = ShapeTab( self.ui, self.db)
        self.FactorATab = FactorATab(self.ui,self.db)
        self.FactorBTab = FactorBTab(self.ui,self.db)
        self.CriticalJSQTab = CriticalJSQTab(self.ui, self.db)
        self.StabilityNumberTab = StabilityNumberTab(self.ui,self.db)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        #self.test_dialog()
        #self.test_dialog_factorc()
        #self.test_dialog_factorb()
    def test_dialog(self):
        # a simple dialog which acts as a placeholder for our widgets to test them
        import db_template
        pointsdict = db_template.gen_cube((0,0,0))

        self.dialog = QtGui.QDialog()
        layout = QtGui.QHBoxLayout()
        stope = StopeVisualization()
        stope.compute_figure(pointsdict)
        layout.addWidget(stope)
        self.dialog.setLayout(layout)
        self.dialog.show()
    def test_dialog_factorc(self):
        self.dialog = QtGui.QDialog()
        layout = QtGui.QHBoxLayout()
        widget = FactorC()
        layout.addWidget(widget)
        self.dialog.setLayout(layout)
        self.dialog.show()
    def test_dialog_factorb(self):
        self.dialog = QtGui.QDialog()
        layout = QtGui.QHBoxLayout()
        widget = FactorB()
        layout.addWidget(widget)
        self.dialog.setLayout(layout)
        self.dialog.show()
    def load(self):
        self.ShapeTab.load()
        self.FactorATab.load()
        self.FactorBTab.load()
        self.StabilityNumberTab.load()
        self.CriticalJSQTab.load()
    def save(self):
        self.ShapeTab.save()
        self.CriticalJSQTab.save()

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
        self.query_db(sqlqueries.FactorB_schema)
        self.query_db(sqlqueries.StabilityNumber_schema)
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
            try:
                self.bind(self.query,bindings)
                boundvalues=self.query.boundValues()
                assert(len(bindings)==len(boundvalues))
                assert(len([str(key) for key in boundvalues 
                        if str(key)[1:] not in bindings])==0)
            except AssertionError:
                print 'bindings', [key for key in bindings]
                print 'bound values', [str(key) for key in boundvalues]
                print 'diff', [str(key) for key in boundvalues 
                        if str(key)[1:] not in bindings
                        ]
                return False
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
                print self.query.lastError().text(),sqlstr
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
    name = 'test'
    shutil.copyfile('tests/generateddb',name)
    qApp = None
    mkQApp()
    db =sqldb(name=name)
    db.id = 1
    aw = ApplicationWindow(db)
    aw.setWindowTitle("%s" % progname)
    aw.show()
    aw.load()
    sys.exit(qApp.exec_())
