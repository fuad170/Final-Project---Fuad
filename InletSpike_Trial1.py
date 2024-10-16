from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument

caa = catia()
application = caa.application
documents = application.documents

try:
    if documents.count > 0:
        for document in documents:
            document.close()
except Exception as e:
    print(f"An exception occured{e}")

documents.add('Part')

document: PartDocument = application.active_document
part = document.part
partbody = part.bodies[0]
sketches = partbody.sketches
hybrid_bodies = part.hybrid_bodies
hsf = part.hybrid_shape_factory
shpfac = part.shape_factory
selection = document.selection

plane_XY = part.origin_elements.plane_xy
plane_YZ = part.origin_elements.plane_yz
plane_ZX = part.origin_elements.plane_zx

part.in_work_object = partbody

geometrical_set = hybrid_bodies.add()
geometrical_set.name = "construction_geometry"

#Direction
x_dir = hsf.add_new_direction_by_coord(1, 0, 0)
y_dir = hsf.add_new_direction_by_coord(0, 1, 0)
z_dir = hsf.add_new_direction_by_coord(0, 0, 1)

def create_point_for_geometrical_set(x, y, z):
    point = hsf.add_new_point_coord(x, y, z)
    geometrical_set.append_hybrid_shape(point)
    document.part.update()
    return point

def create_line_for_geometrical_set(point1, point2):
    line = hsf.add_new_line_pt_pt(point1, point2)
    geometrical_set.append_hybrid_shape(line)
    document.part.update()
    return line

def create_spline_for_geometrical_set(*points):
    spline = hsf.add_new_spline()
    for point in points:
        spline.add_point(point)
    geometrical_set.append_hybrid_shape(spline)
    document.part.update()    
    return spline

def create_surace_revolve(curve, start_angle, end_angle, revolve_axis):
    surfRevolution = hsf.add_new_revol(curve, start_angle, end_angle, revolve_axis)
    geometrical_set.append_hybrid_shape(surfRevolution)
    document.part.update() 
    return surfRevolution

#Create Spike_______________________________________________
#___________________________________________________________
origin = create_point_for_geometrical_set(0, 0, 0)
p2 = create_point_for_geometrical_set(-100, 0, 25)
p5 = create_point_for_geometrical_set(-175, 0, 13)
p6 = create_point_for_geometrical_set(-250, 0, 10)
p1 = create_point_for_geometrical_set(-125, 0, 23)
p3 = create_point_for_geometrical_set(-150, 0, 17)
line1 = create_line_for_geometrical_set(origin, p2)
spline1 = create_spline_for_geometrical_set(p2, p1, p3, p5)
line2 = create_line_for_geometrical_set(p5,p6)

surfRevolution = hsf.add_new_revol(line1, 0, 360, x_dir)
geometrical_set.append_hybrid_shape(surfRevolution)

surfRevolution2 = hsf.add_new_revol(spline1, 0, 360, x_dir)
geometrical_set.append_hybrid_shape(surfRevolution2)

surfRevolution3 = hsf.add_new_revol(line2, 0, 360, x_dir)
geometrical_set.append_hybrid_shape(surfRevolution3)

# Update the document
document.part.update()


#Create Struts______________________________________________
#___________________________________________________________

p7 = hsf.add_new_point_coord(-170, 0, 0)
p7.name = "Point 7"
geometrical_set.append_hybrid_shape(p7)
document.part.update()

p8 = hsf.add_new_point_coord(-190, 2, 0)
p8.name = "Point 8"
geometrical_set.append_hybrid_shape(p8)
document.part.update()

p9 = hsf.add_new_point_coord(-190, -2, 0)
p9.name = "Point 9"
geometrical_set.append_hybrid_shape(p9)
document.part.update()

p10 = hsf.add_new_point_coord(-250, 0, 0)
p10.name = "Point 10"
geometrical_set.append_hybrid_shape(p10)
document.part.update()

spline2 = hsf.add_new_spline()
spline2.add_point(p7)
spline2.add_point(p8)
spline2.add_point(p10)
geometrical_set.append_hybrid_shape(spline2)
document.part.update()

spline3 = hsf.add_new_spline()
spline3.add_point(p7)
spline3.add_point(p9)
spline3.add_point(p10)
geometrical_set.append_hybrid_shape(spline3)
document.part.update()

surfExtrusion = hsf.add_new_extrude(spline2, 33, 0, z_dir)
surfExtrusion.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion)
document.part.update()

surfExtrusion2 = hsf.add_new_extrude(spline3, 33, 0, z_dir)
surfExtrusion2.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion2)
document.part.update()

surfExtrusion = hsf.add_new_extrude(spline2, -33, 0, z_dir)
surfExtrusion.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion)
document.part.update()

surfExtrusion2 = hsf.add_new_extrude(spline3, -33, 0, z_dir)
surfExtrusion2.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion2)
document.part.update()

p11 = hsf.add_new_point_coord(-190, 0, 2)
p11.name = "Point 11"
geometrical_set.append_hybrid_shape(p11)
document.part.update()

p12 = hsf.add_new_point_coord(-190, 0, -2)
p12.name = "Point 12"
geometrical_set.append_hybrid_shape(p12)
document.part.update()

spline4 = hsf.add_new_spline()
spline4.add_point(p7)
spline4.add_point(p11)
spline4.add_point(p10)
geometrical_set.append_hybrid_shape(spline4)
document.part.update()

spline5 = hsf.add_new_spline()
spline5.add_point(p7)
spline5.add_point(p12)
spline5.add_point(p10)
geometrical_set.append_hybrid_shape(spline5)
document.part.update()

surfExtrusion3 = hsf.add_new_extrude(spline4, 33, 0, y_dir)
surfExtrusion3.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion3)
document.part.update()

surfExtrusion4 = hsf.add_new_extrude(spline5, 33, 0, y_dir)
surfExtrusion4.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion4)
document.part.update()

surfExtrusion3 = hsf.add_new_extrude(spline4, -33, 0, y_dir)
surfExtrusion3.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion3)
document.part.update()

surfExtrusion4 = hsf.add_new_extrude(spline5, -33, 0, y_dir)
surfExtrusion4.symmetrical_extension = False
geometrical_set.append_hybrid_shape(surfExtrusion4)
document.part.update()

#__Create Nocelle Profile_________________________________
#_________________________________________________________
p13 = hsf.add_new_point_coord(-170, 0, 33)
p13.name = "Point 13"
geometrical_set.append_hybrid_shape(p13)
document.part.update()

p14 = hsf.add_new_point_coord(-100, 0, 30)
p14.name = "Point 14"
geometrical_set.append_hybrid_shape(p14)
document.part.update()

p15 = hsf.add_new_point_coord(-60, 0, 25)
p15.name = "Point 14"
geometrical_set.append_hybrid_shape(p15)
document.part.update()

spline6 = hsf.add_new_spline()
spline6.add_point(p15)
spline6.add_point(p14)
spline6.add_point(p13)
geometrical_set.append_hybrid_shape(spline6)
document.part.update()

surfRevolution5 = hsf.add_new_revol(spline6, 0, 360, x_dir)
geometrical_set.append_hybrid_shape(surfRevolution5)
document.part.update()

p16 = hsf.add_new_point_coord(-250, 0, 33)
p16.name = "Point 16"
geometrical_set.append_hybrid_shape(p16)
document.part.update()

line3 = hsf.add_new_line_pt_pt(p13,p16)
line3.name = "Line 3"
geometrical_set.append_hybrid_shape(line3)
document.part.update()

surfRevolution6 = hsf.add_new_revol(line3, 0, 360, x_dir)
geometrical_set.append_hybrid_shape(surfRevolution6)
document.part.update()