from __future__ import unicode_literals
import sys
import os
import random
import itertools

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        FigureCanvas.updateGeometry(self)
    def sizeHint(self):
        w, h =self.get_width_height()
        return QtCore.QSize(w,h)

class _2DMplCanvas(MplCanvas):
    """Simple canvas with a sine plot."""
    def __init__(self,*args,**kwargs):
        self.points=kwargs["points"]
        self.view=kwargs["view"]
        del kwargs["points"]
        del kwargs["view"]
        MplCanvas.__init__(self,*args,**kwargs)

        self.compute_initial_figure(self.view)
    def draw_view(self,points,view=None):
        x,y,z=0,1,2
        if view=="plan":i,c=x,y
        elif view=="front":i,c=x,z
        elif view=="side":i,c=y,z
        else: 
            return "ERROR NO VIEW"
    
        p1,p2,p3,p4,p5,p6,p7,p8= [(point[i],point[c]) for point in points]
        views = {
            'top':[p5,p6,p7,p8],
            'bottom':[p1,p2,p3,p4],
            'left': [p1,p5,p6,p2],
            'right':[p7,p3, p8,p4]
            }
        def front_or_side():
            self.draw_plot(view, views['top'], color=color['top'])
            self.draw_plot(view, unpack(views['left'][:2]), color=color['left'])
            self.draw_plot(view, unpack(views['left'][2:]), color=color['left'])
            self.draw_plot(view, unpack(views['right'][:2]), color=color['right'])
            self.draw_plot(view, unpack(views['right'][2:]), color=color['right'])
            self.draw_plot(view, views['bottom'], color=color['bottom'])
        if view=="plan":
            self.draw_plot(view, views['bottom'], color=color['bottom'])
            self.draw_plot(view, views['top'], color=color['top'])
        elif view=="front":
            front_or_side()
        elif view=="side":
            front_or_side()
        self.adjust_lim()
    def draw_plot(self,view,_set, color='black'):
        self.fig.suptitle(view,fontsize=12)
        if len(_set)==4:
            x,y= self.line(_set)
        else:
            x,y= _set
        self.axes.set_autoscale_on(True)
        self.axes.grid()
        self.axes.axis('equal')
        self.axes.plot(x,y,color=color,linewidth=2.0)
    def adjust_lim(self):        
        xticks= self.axes.get_xticks()
        #shift a half a step to the left
        # x0 - (x1- x0)/ 2 = (3*x0-x1)/2
        xmin = (3*xticks[0] - xticks[1])/2
        #shift a half a tick to the right
        xmax = (3*xticks[-1] - xticks[-2])/2
        self.axes.set_xlim(xmin,xmax)

        yticks= self.axes.get_yticks()
        #shift a half a step to the left
        # y0 - (y1- y0)/ 2 = (3*y0-y1)/2
        ymin = (3*yticks[0] - yticks[1])/2
        #shift a half a tick to the right
        ymax = (3*yticks[-1] - yticks[-2])/2
        self.axes.set_ylim(ymin,ymax)
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
    def compute_initial_figure(self,view):
        self.draw_view(self.points,view=view)

class _3DMplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100,points=None):
        self.points=points
        self.fig = plt.figure(figsize=(width,height),dpi=dpi)
        self.axes = self.fig.add_subplot(111, projection='3d') 
        self.axes.hold(True)
        FigureCanvas.__init__(self, self.fig)
        self.axes.mouse_init()
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        FigureCanvas.updateGeometry(self)
        self.compute_initial_figure()
    def sizeHint(self):
        w, h =self.get_width_height()
        return QtCore.QSize(w,h)
    def draw_plot(self):
        p1,p2,p3,p4,p5,p6,p7,p8 = self.points
        views = {
                'top':[p5,p6,p7,p8,p5],
                'bottom':[p1,p2,p3,p4,p1],
                'left': [p1,p5,p6,p2],
                'right':[p7,p3, p8,p4]
                }
        #self.axes.plot3D(*unpack([p1,p2,p3,p4,p1,p5,p6,p7,p8,p5]))
        self.axes.plot3D(*unpack(views['top']))
        self.axes.plot3D(*unpack(views['left'][:2]), color=color['left'])
        self.axes.plot3D(*unpack(views['left'][2:]), color=color['left'])
        self.axes.plot3D(*unpack(views['right'][2:]), color=color['right'])
        self.axes.plot3D(*unpack(views['right'][:2]), color=color['right'])
        self.axes.plot3D(*unpack(views['bottom']), color=color['bottom'])
    def compute_initial_figure(self):
        self.draw_plot()

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui= mining_ui.Ui_window()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtGui.QWidget(self)

        grid= QtGui.QGridLayout()
        grid.setSizeConstraint(QtGui.QLayout.SetMinimumSize)

        row,column =0,0
        for index, val in enumerate(["plan","front","side"]):
            l = _2DMplCanvas(self.main_widget,view=val, points=points,
                    width=3, height=2, dpi=100)
            grid.addWidget(l,row,column)
            column+=1
            if column==2:
                column=0; row= 1
        l = _3DMplCanvas(self.main_widget,points=points,width=3,
                        height=2,dpi=100)
        grid.addWidget(l,1,1)
        horizontal= self.ui.horizontalLayout
        horizontal.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        horizontal.addLayout(grid)
        
points = [(0,0,0),(1,1,0),(2,1,0),(1,0,0),
        (0,0,1),(1,1,1),(2,1,1),(1,0,1)
        ]

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
