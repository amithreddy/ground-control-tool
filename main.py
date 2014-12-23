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

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.figure= FigureCanvas
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

        if view=="plan":
            self.draw_plot(view,[p5,p6,p7,p8],[p1,p2,p3,p4])
        elif view=="front":
            self.draw_plot(view,[p1,p5,p8,p4],[p2,p6,p7,p3])
        elif view=="side":
            self.draw_plot(view,[p4,p8,p7,p3],[p1,p5,p6,p2])
    def draw_plot(self,view,set1,set2):
        self.fig.suptitle(view,fontsize=12)
        color1,color2= 'r','g'
        min_ =min(itertools.chain(set1,set2))       
        max_ =max(itertools.chain(set1,set2))
        x,y= self.line(set1)
        self.axes.plot(x,y,color1+'s-',linewidth=2.0)
        
        x,y= self.line(set2)
        self.axes.plot(x,y,color2+'s-',linewidth=2.0)
        
        self.axes.grid()
        self.axes.axis('equal')
        self.axes.autoscale_view(True)

        self.axes.set_xlim(xmin=min_[0]-0.5, xmax=max_[0]+0.5)
        self.axes.set_ylim(ymin=min_[1],ymax=max_[1])
    def line(self,points):
        p1,p2,p3,p4=points
        Path = mpath.Path
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
        self.figure= FigureCanvas
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        FigureCanvas.updateGeometry(self)

        self.compute_initial_figure()
    def sizeHint(self):
        w, h =self.get_width_height()
        return QtCore.QSize(w,h)
    def unpack(self,points):
        """ takes[(x,y,z),(1,1,1),(2,2,2)] and returns
            [x,1,2],[y,1,2],[z,1,2] """
        x,y,z= ([point[0] for point in points],
                [point[1] for point in points],
                [point[2] for point in points]
                )
        return x,y,z
        return self.fig.add_subplot(111, projection='3d')
    def draw_plot(self):
        p1,p2,p3,p4,p5,p6,p7,p8 = self.points
        self.axes.plot3D(*self.unpack([p1,p2,p3,p4,p1,p5,p6,p7,p8,p5]))
        self.axes.plot3D(*self.unpack([p4,p8]), color="green")
        self.axes.plot3D(*self.unpack([p2,p6]), color="blue")
        self.axes.plot3D(*self.unpack([p7,p3]), color="blue")
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
            grid.addWidget(l,0,column)
        l = _3DMplCanvas(self.main_widget,points=points,width=3,
                        height=2,dpi=100)
        grid.addWidget(l,0,4)
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
