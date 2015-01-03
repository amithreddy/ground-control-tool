from sympy import symbols, sqrt, Matrix, mpmath,Line3D,Segment3D,Point3D
from sympy import srepr

def dist_between_points(point1, point2):
    """ Expects input as tuple(x,y)"""
    x1,x2,y1,y2= symbols("x1 x2 y1 y2")
    distance= sqrt( (x2-x1)**2 + (y2-y1)**2)

    x1,y1,z2 = point1
    x2,y2,z2 = point2
    return distance.subs( { "x1":x1,"x2":x2, "y1":y1, "y2":y2,"z1":z1,"z2":z2})

def angles_between_vecs(vec1,vec2):
    """ Expects vectors in sympy Matrix Object """
    rad=mpath.acos( (vec1.dot(vec2))/ (sqrt(vec1[0]+vec1[1])*sqrt(vec2[0]+vec2[1])))
    return mpmath.degrees(rad)
    
def vector(first,second):
    """ where first and second are points in tuple(x,y) form"""
    x1,y1= first
    x2,y2=second
    return Matrix([[x2-x1, y2-y1]])

def is_coplaner(*points):
    """ accepts many points and tests if they are co planar """
    return Point3D.is_coplaner(*points)

def length_of_vector(vec):
    return sqrt( sum(digit**2 for digit in vec) )

def perimeter(*segments): 
    return sum(seg.length for seg in segments).evalf(2)

def area_of_quadrilateral(diag,diag2):
    """ diag,diag2 where both are vectors"""
    return (0.5)*(diag.cross(diag2))
      
def strike_dip_plane(plane):
    normal= plane.normal
    dip_plane= Northing= Plane(Point3D(0,1,0),Point3D(0,1,0),Point3D(0,1,0))
    dip_vertical=dip_plane.normal
    dip_angle= angles_between_vecs(normal,dip_vertical)

    strike_plane= Plane(Point3D(0,0,0),Point3D(0,0,1),Point3D(0,0,2))
    strike_vertical=strike_plane.normal
    strike_angle= angles_between_vecs(normal,strike_vertical)
    return dip_angle, strike_angle 

