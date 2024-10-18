#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------------------------Import Modules---------------------------
#.....................................................................
from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------------------Initiate CATIA instance----------------------
#.....................................................................
caa = catia()
application = caa.application
documents = application.documents

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------Close all active documents and add a new part--------------
#.....................................................................
try:
    if documents.count > 0:
        for document in documents:
            document.close()
except Exception as e:
    print(f"An exception occured{e}")
#------------Add_New_Part-------------
documents.add('Part')

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-----------------Creating reference to main objects------------------
#.....................................................................
document: PartDocument = application.active_document
part = document.part
partbody = part.bodies[0]
sketches = partbody.sketches
hybrid_bodies = part.hybrid_bodies
hsf = part.hybrid_shape_factory
shpfac = part.shape_factory
selection = document.selection

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-----------Creating reference to main coordinate planes--------------
#.....................................................................
plane_XY = part.origin_elements.plane_xy
plane_YZ = part.origin_elements.plane_yz
plane_ZX = part.origin_elements.plane_zx

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------Creating reference to directions along x, y and z axis--------
#.....................................................................
x_dir = hsf.add_new_direction_by_coord(1, 0, 0)
y_dir = hsf.add_new_direction_by_coord(0, 1, 0)
z_dir = hsf.add_new_direction_by_coord(0, 0, 1)

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-----------------------Creating Geometrical Set----------------------
#.....................................................................
geometrical_set = hybrid_bodies.add()
geometrical_set.name = "Construction Elements"

#-----------Clearance Between Inlet Spike and Nacelle Body-----------
clearance = 5

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------Defininig Fucntions-------------------------
#.....................................................................

#Fucntion to generate points in geometrical set
def create_construction_point(x, y, z):                 
    point = hsf.add_new_point_coord(x, y, z)
    geometrical_set.append_hybrid_shape(point)
    document.part.update()
    return point

#Fucntion to generate lines in geometrical set
def create_construction_line(point1, point2):           
    line = hsf.add_new_line_pt_pt(point1, point2)
    geometrical_set.append_hybrid_shape(line)
    document.part.update()
    return line

#Fucntion to generate splines in geometrical set
def create_construction_spline(*points):                
    spline = hsf.add_new_spline()
    for point in points:
        spline.add_point(point)
    geometrical_set.append_hybrid_shape(spline)
    document.part.update()    
    return spline

#Fucntion to create revolved surface
def create_surface_revolve(curve, start_angle, end_angle, revolve_axis):             
    surfRevolution = hsf.add_new_revol(curve, start_angle, end_angle, revolve_axis)
    geometrical_set.append_hybrid_shape(surfRevolution)
    document.part.update() 
    return surfRevolution

#Fucntion to generate inlet spike
def Inlet_Spike_Generator(l):
    # l = Length of the spike from tip to root
    # w = Maximum radius of the spike
    global w
    w = l/10
    spike_profile = sketches.add(plane_XY)
    spike_profile.name = "Spike Outer Profile"
    spike2D = spike_profile.open_edition()
    spike2D.create_spline((spike2D.create_control_point(l*0, w*0), spike2D.create_control_point(-l*0.4, w), 
                           spike2D.create_control_point(-l*0.5, w*0.92), spike2D.create_control_point(-l*0.6, w*0.68), 
                           spike2D.create_control_point(-l*0.7, w*0.52), spike2D.create_control_point(-l, w*0.4)))
    spike2D.create_line(*(-l, w*0.4), *(-l, w*0))
    spike2D.create_line(*(-l, w*0), *(l*0, w*0))
    spike_profile.close_edition()
    spike_solid = shpfac.add_new_shaft(spike_profile)
    spike_solid.revolute_axis = x_dir
    document.part.update()
    return spike_solid

def nacelle_generator(offset, L):
    # T = Distance betwwen Spike Tip and Nacalle Tip
    # d = Maximum clearance with the spike inlet
    global d
    d = w+clearance
    #Construction Points
    p1 = create_construction_point(-offset, d, 0)
    p2 = create_construction_point(-(offset+(L/10)), d*(16/15), 0)
    p3 = create_construction_point(-(offset+2*(L/10)), d, 0)
    p4 = create_construction_point(-(offset+3*(L/10)), d*(14/15), 0)
    p5 = create_construction_point(-(offset+4*(L/10)), d*(14/15), 0)
    p6 = create_construction_point(-(offset+6*(L/10)), d*(29/30), 0)
    p7 = create_construction_point(-(offset+8*(L/10)), d, 0)
    p8 = create_construction_point(-(offset+8.5*(L/10)), d*(2/3), 0)
    p9 = create_construction_point(-(offset+9*(L/10)), d, 0)
    p10 = create_construction_point(-(offset+10*(L/10)), d*(4/3), 0)
    p11 = create_construction_point(-(offset+L*3/25), (d+10), 0)
    p12 = create_construction_point(-(offset+L*(11/50)), (d+12), 0)
    p13 = create_construction_point(-(offset+L*(9/10)), (d+12), 0)
    #Construction Line
    Inner_Spline_1 = create_construction_spline(p1, p2, p3, p4, p5)
    Inner_Spline_2 = create_construction_spline(p5, p6, p7)
    Inner_Spline_3 = create_construction_spline(p7, p8, p9)
    Inner_Line = create_construction_line(p9, p10)
    Outer_Line_1 = create_construction_line(p13, p10)
    Outer_Line_2 = create_construction_line(p12, p13)
    Outer_spline = create_construction_spline(p1, p11, p12)
    #Nacelle Profile Curve
    nacelle_profile_curve = hsf.add_new_join(Inner_Spline_1, Inner_Spline_2)
    geometrical_set.append_hybrid_shape(nacelle_profile_curve)
    curves = [Inner_Spline_1, Inner_Spline_2, Inner_Spline_3, Inner_Line, Outer_Line_1, Outer_Line_2, Outer_spline]
    for i in range(len(curves)-2):
        nacelle_profile_curve = hsf.add_new_join(nacelle_profile_curve, curves[i+2])
        geometrical_set.append_hybrid_shape(nacelle_profile_curve)

    document.part.update()
    return nacelle_profile_curve


#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------Creating Inlet Spike------------------------
#.....................................................................
part.in_work_object = partbody
Inlet_Spike_Generator(250)

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------------------Creating Nacelle Body------------------------
#.....................................................................

#------------Creating 2D profile-------------
offset_from_tip = 50
length_of_nacelle = 500   
nacelle_2D_profile = nacelle_generator(offset_from_tip, length_of_nacelle)

#-------------Revolved sruface---------------
nacelle_surface = create_surface_revolve(nacelle_2D_profile, 0, 360, x_dir)

#-----------------Make Solid-----------------
nacelle = shpfac.add_new_close_surface(nacelle_surface)
document.part.update()

#-----------Hide Construction Surface-------------
selection.clear();
selection.add(nacelle_surface)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
document.part.update()


#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------Creating Exhaut Nozzle with externel flaps-----------------
#.....................................................................

#------Creating the sketch to make pockets--------
point_1 = create_construction_point(-(offset_from_tip+9*(length_of_nacelle/10)), 0, 0)
point_2 = create_construction_point(-(offset_from_tip+10.1*(length_of_nacelle/10)), 0, 2)
point_3 = create_construction_point(-(offset_from_tip+10.1*(length_of_nacelle/10)), 0, -2)

flaps_pocket_triangle = hsf.add_new_polyline()
flaps_pocket_triangle.insert_element(point_1, 0)
flaps_pocket_triangle.insert_element(point_1, 1)
flaps_pocket_triangle.insert_element(point_2, 2)
flaps_pocket_triangle.insert_element(point_3, 3)
flaps_pocket_triangle.insert_element(point_1, 4)
geometrical_set.append_hybrid_shape(flaps_pocket_triangle)
document.part.update()

#-----------Creating Pocket-----------
flaps_pocket = shpfac.add_new_pocket_from_ref(flaps_pocket_triangle, 200)
document.part.update()
#-------Adding Circular Pattern-------
part.in_work_object = partbody
exhaust_nozzle = shpfac.add_new_circ_pattern(flaps_pocket, 1, 15, 0, 24, 1, 1, x_dir, x_dir, True, 0, True)
document.part.update()
   
#------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------END of CODE-----------------------------------------------------------
#________________________________________________________________________________________________________________________