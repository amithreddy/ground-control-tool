from sympy import symbols, sqrt, Matrix, mpmath
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
    pass
    #return Point3D.is_coplaner(*points)

def length_of_vector(vec):
    return sqrt( sum(digit**2 for digit in vec) )

def perimeter(*vectors):
    return sum(length_of_vector(vec) for vec in vectors)

def area_of_quadrilateral(diag,diag2):
    """ diag,diag2 where both are vectors"""
    expr= (0.5)* (diag.cross(diag2))

def equation_plane():
    pass

def normal_to_plane(plane):
    pass

def slope_of_plane(plane):
    pass
