from __future__ import unicode_literals
import sys
import os
import random

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.path as mpath

import mining_ui
from geometry import *

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)

    def sizeHint(self):
        w, h =self.get_width_height()
        return QtCore.QSize(w, h)

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def __init__(self,*args,**kwargs):
        self.points=kwargs["points"]
        del kwargs["points"]
        MyMplCanvas.__init__(self,*args,**kwargs)
        print(dir(self))

    def draw_view(self,points,view=None):
        x,y,z=0,1,2
        if view=="plan":i,c=x,y
        elif view=="front":i,c=x,z
        elif view=="side":i,c=y,z
        else: 
            return "ERROR NO VIEW"
    
        p1,p2,p3,p4,p5,p6,p7,p8= [(point[i],point[c]) for point in points]

        if view=="plan":
            self.draw_plot([p5,p6,p7,p8],[p1,p2,p3,p4])
        elif view=="front":
            self.draw_plot([p1,p5,p8,p4],[p2,p6,p7,p3])
        elif view=="side":
            self.draw_plot([p4,p8,p7,p3],[p1,p5,p6,p2])
    
    def draw_plot(self,set1,set2):
        color1,color2= 'r','g'
        
        x,y= self.line(set1)
        self.axes.plot(x,y,color1+'s-',linewidth=2.0)

        x,y= self.line(set2)
        self.axes.plot(x,y,color2+'s-',linewidth=2.0)
        
        self.axes.grid()
        self.axes.axis('equal')
        self.axes.set_ylim(ymin=-1,ymax=2)
        
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

    def compute_initial_figure(self):
        self.draw_view(self.points,view="front")

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui= mining_ui.Ui_window()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtGui.QWidget(self)
        print(dir(self.ui))
        l = self.ui.verticalLayout
        sc = MyStaticMplCanvas(self.main_widget, points=points,width=3, height=2, dpi=100)
        l.addWidget(sc)

points = [(0,0,0),(1,1,0),(2,1,0),(1,0,0),
        (0,0,1),(1,1,1),(2,1,1),(1,0,1)
        ]

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
