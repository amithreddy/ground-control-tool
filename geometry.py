from sympy import symbols, sqrt, Matrix, mpmath, Line3D, Segment3D, Point3D, Plane
from sympy import srepr

def dist_between_points(point1, point2):
    """ Expects input as tuple(x,y)"""
    x1,x2,y1,y2= symbols("x1 x2 y1 y2")
    distance= sqrt( (x2-x1)**2 + (y2-y1)**2)

    x1,y1,z2 = point1
    x2,y2,z2 = point2
    return distance.subs( { "x1":x1,"x2":x2, "y1":y1, "y2":y2,"z1":z1,"z2":z2})

def vector_angles(vec1,vec2):
    """ Expects vectors in sympy Matrix Object """
    #need magnitude of vector 1 and 2
    vec1_mag = magnitude(vec1)
    vec2_mag = magnitude(vec2)
    rad=mpmath.acos( (vec1.dot(vec2))/ (vec1_mag * vec2_mag))
    return mpmath.degrees(rad)
    
def vector(first,second):
    """ where first and second are points in tuple(x,y) form"""
    x1,y1= first
    x2,y2=second
    return Matrix([[x2-x1, y2-y1]])

def is_coplaner(*points):
    """ accepts many points and tests if they are co planar """
    return Point3D.is_coplaner(*points)

def magnitude(vec):
    """ Expects vectors in sympy Matrix Object """
    return sqrt( sum(digit**2 for digit in vec) )

def perimeter(*segments): 
    return sum(seg.length for seg in segments).evalf(2)

def area_of_quadrilateral(diag,diag2):
    """ diag,diag2 where both are vectors"""
    return (0.5)*(diag.cross(diag2))
      
def strike_dip(plane):
    """
    strike is measured against the vertical plane 
    dip is measured by the angle between horizontal plane
    """
    normal= Matrix ( list(plane.normal_vector))

    horizontal= Plane( Point3D(0,0,0),Point3D(0,1,0),Point3D(1,1,0))
    vertical= make_plane((0,0,0), (0,0,1), (0,1,1))
    dip_vec = Matrix(list(horizontal.normal_vector))
    strike_vec = Matrix(list(vertical.normal_vector))

    dip_angle= vector_angles(dip_vec, normal)
    strike_angle= vector_angles(strike_vec, normal) 
    return  strike_angle, dip_angle

def make_plane(*args):
    assert( len(args) == 3)
    return Plane( *[Point3D(tuple_) for tuple_ in args])

def calculate_dip_strike(points):
    # makes sure it takes three non-coliner lines?
    # what happens if they input junk?
    faces = sort_faces(points)
    adict = {}
    for key, face in faces.items():
        plane = make_plane(*face[:3]) 
        strike, dip = strike_dip(plane)
        adict[key+"dip"] = dip
        adict[key+"direction"] = strike
    return adict

def sort_faces(points):
    # returns msc faces
    p1,p2,p3,p4,p5,p6,p7,p8 = points
    faces = {
    "one" :[p5,p6,p7,p8],
    "two" : [p5, p6, p1, p2],
    "three" : [p6, p7, p3, p2],
    "four" : [p7, p8, p4, p3],
    "five" : [p5, p8, p1, p4]}
    return faces

def orientation(faces):
    # you just need to check one face 
    # to get the orientation of all the other faces
    vertical= make_plane((0,0,0), (0,0,1), (0,1,1))
    plane = make_plane(faces[0][:3])
    angle = vector_angles(plane.normal_vector, vertical.normal_vector)
    if angle == 90:
        return ["back", "north", "east", "south", "west"]
    else:
        return ["back", "northeast", "southeast", "southwest", "northwest"]


