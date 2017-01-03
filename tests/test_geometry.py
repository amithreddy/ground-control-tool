"""
print "strike dip"
#west fa
aplane = make_plane( (0, 0, 0), (0, 100, 0 ), (0, 100, 100))
print strike_dip_plane(aplane)

#east face
aplane = make_plane( (100,0,0), (100, 100, 0 ), (100,100,100))
print strike_dip_plane(aplane)

#north face
aplane = make_plane( (0, 100, 0), (0,100, 100), (100,100,100))
print strike_dip_plane(aplane)

#south face
aplane = make_plane( (0, 0, 0), (0, 0, 100), (100, 0,100))
print strike_dip_plane(aplane)
"""
