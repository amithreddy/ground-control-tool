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
import matplotlib.image as mpimg 

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

class _3DMplCanvas(FigureCanvas):
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
            axes.set_xticks([])
            axes.set_yticks([])
            axes.set_zticks([])
        else:
            axes = self.fig.add_subplot(number) 
        axes.hold(True)
        return axes
    def draw_view(self,view=None):
        points= self.points
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
        axes.plot(x,y,color=color,linewidth=2.0)
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
        [axes.clear() for axes in self.fig.axes]
        self.front = self.create_subplot(221) 
        self.plan = self.create_subplot(222) 
        self.side = self.create_subplot(223)
        self.axes3d = self.create_subplot(224, _3d='True') 
 
        self.points= points
        self.draw_view(view='front')
        self.draw_view(view='side')
        self.draw_view(view='plan')
        self.draw_plot3d(self.axes3d)
        self.fig.tight_layout()
    def sizeHint(self):
        w, h =self.get_width_height()
        return QtCore.QSize(w,h)

class StaticGraph(FigureCanvas):
    """ Fixed y and x axis. On running plots a line, and updates it with
    user data"""
    def __init__(self,parent=None, imagename=None,width=5,height=5,dpi=100):
        self.fig = plt.figure(figsize=(width,height),dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Minimum)
        FigureCanvas.updateGeometry(self)
        self.axes = self.fig.add_subplot(111)
        self.setParent(parent)
        img = mpimg.imread(imagename)
        imgplot = self.axes.imshow(img)
    def submit(self):
        pass

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui= mining_ui.Ui_window()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtGui.QWidget(self)

        grid= QtGui.QGridLayout()
        grid.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
       
        l = _3DMplCanvas(self.main_widget,width=4,height=4,dpi=100)
        l.compute_figure(points)
        grid.addWidget(l,0,0)
        al = StaticGraph(self.main_widget,imagename="test.png")
        grid.addWidget(al,1,0)
        horizontal= self.ui.horizontalLayout
        horizontal.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        horizontal.addLayout(grid)
    def submit(self):
       pass 

points = [(0,0,0),(1,1,0),(2,1,0),(1,0,0),
        (0,0,1),(1,1,1),(2,1,1),(1,0,1)
        ]
qApp = QtGui.QApplication(sys.argv)
aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
