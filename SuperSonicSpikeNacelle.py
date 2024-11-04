#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------------------------Import Modules---------------------------
#.....................................................................
from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
import tkinter as tk
from tkinter import Tk
from tkinter import messagebox

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------------------Initiate CATIA instance----------------------
#.....................................................................
try:
    caa = catia()
    application = caa.application
    documents = application.documents
except Exception as e:
    print(f"An exception occured{e}")

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
try:
    document: PartDocument = application.active_document
    part = document.part
    partbody = part.bodies[0]
    sketches = partbody.sketches
    hybrid_bodies = part.hybrid_bodies
    hsf = part.hybrid_shape_factory
    shpfac = part.shape_factory
    selection = document.selection
except Exception as e:
    print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-----------Creating reference to main coordinate planes--------------
#.....................................................................
try:
    plane_XY = part.origin_elements.plane_xy
    plane_YZ = part.origin_elements.plane_yz
    plane_ZX = part.origin_elements.plane_zx
except Exception as e:
    print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------Creating reference to directions along x, y and z axis--------
#.....................................................................
try:
    x_dir = hsf.add_new_direction_by_coord(1, 0, 0)
    y_dir = hsf.add_new_direction_by_coord(0, 1, 0)
    z_dir = hsf.add_new_direction_by_coord(0, 0, 1)
except Exception as e:
    print(f"An exception occured{e}")   


#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------------------Creating Geometrical Set-----------------------
#.....................................................................
try:
    geometrical_set = hybrid_bodies.add()
    geometrical_set.name = "Construction Elements"
except Exception as e:
    print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------------Take the Aircraft Length from user-------------------
#.....................................................................
def aircraft_length():
    try:    
        def get_aircraft_len_from_user():
            user_input = entry.get()
            try: 
                # Try to convert the input to a float
                value = float(user_input)
                root.destroy()
                aircraft_length.value = value
            except ValueError:
                # If a ValueError occurs, print an error message and ask for value again
                messagebox.showerror("Invalid input", "Please enter a numeric value")
                entry.delete(0, tk.END)

        root = Tk()
        root.title("Supersonic Drone Generator")
        try:
            root_width = 350
            root_height = 100
            root.geometry(f"{root_width}x{root_height}")
            root.resizable(False,False)
        except Exception as e:
            print(f"An exception occured{e}")

        label = tk.Label(root, text="Enter the length of the drone in feet: ")
        label.pack(padx=10, pady=5)

        entry = tk.Entry(root)
        entry.pack(padx=10, pady=5)

        submit_button = tk.Button(root, text="Enter", command=get_aircraft_len_from_user)
        submit_button.pack(pady=10)

        root.mainloop()

        return aircraft_length.value
    
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-----------------------Controlling Parameters------------------------
#.....................................................................
try:
    L_Aircraft = aircraft_length()*10           #Length of the aircraft fuselage from nose to tail
    W_Aircraft = L_Aircraft*(3/10)              #Span of the aircraft fuselage between two engines
    L_Nacelle = L_Aircraft/2.4                  #Length of the nacelle including exhaust nozzle
    L_Spike = L_Nacelle/2                       #Length of the spiike from tip to root
    R_Spike = L_Spike/10                        #Maximum Radius of the spike
    clearance = R_Spike/5                       #Clearance Between Inlet Spike and Nacelle Body
    R_Nacelle = (L_Nacelle/20) + clearance      #Effective Radius of the Nacalle
    offset = (L_Spike/5)                        #Distance from spike tip to nacelle edge at inlet
    l = L_Spike
    r = R_Spike
    w = offset
    L = L_Nacelle
    R = R_Nacelle                        
except Exception as e:
    print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------Defininig Fucntions-------------------------
#.....................................................................

#Fucntion to append hybrid shape in geometrical set and update te document
def append_in_geometrical_set_and_update(shape_to_append):
    geometrical_set.append_hybrid_shape(shape_to_append)
    document.part.update()

#Fucntion to generate points in geometrical set    
def create_construction_point(x, y, z):
    try:                 
        point = hsf.add_new_point_coord(x, y, z)
        append_in_geometrical_set_and_update(point)
        return point
    except Exception as e:
        print(f"An exception occured{e}")

#Fucntion to generate lines in geometrical set
def create_construction_line(point1, point2):
    try:           
        line = hsf.add_new_line_pt_pt(point1, point2)
        append_in_geometrical_set_and_update(line)
        return line
    except Exception as e:
        print(f"An exception occured{e}")

#Fucntion to generate splines in geometrical set
def create_construction_spline(*points):
    try:                
        spline = hsf.add_new_spline()
        for point in points:
            spline.add_point(point)
        append_in_geometrical_set_and_update(spline)    
        return spline
    except Exception as e:
        print(f"An exception occured{e}")

#Fucntion to generate closed curve with polyline
def create_closed_curve_with_polyline(points_list):
    try:
        polyline = hsf.add_new_polyline()
        for i in range(1, len(points_list)+2):
            if i<=len(points_list):
                polyline.insert_element(points_list[i-1], i)
            else:
                polyline.insert_element(points_list[0], len(points_list)+1)
        append_in_geometrical_set_and_update(polyline)
        return polyline
    except Exception as e:
        print(f"An exception occured{e}")

#Function to mirror construction elements
def mirror_entity(entity_to_mirror, reference):
    try:
        mirrored_geometry = hsf.add_new_symmetry(entity_to_mirror, reference)
        append_in_geometrical_set_and_update(mirrored_geometry)
        return mirrored_geometry
    except Exception as e:
        print(f"An exception occured{e}")

#Function to join lines, polylines and splines
def join_curves(curve1, curve2):
    try:
        joined_curve = hsf.add_new_join(curve1, curve2)
        append_in_geometrical_set_and_update(joined_curve)
        return joined_curve
    except Exception as e:
        print(f"An exception occured{e}")

#Fucntion to create revolved surface
def create_surface_revolve(curve, start_angle, end_angle, revolve_axis):
    try:             
        surfRevolution = hsf.add_new_revol(curve, start_angle, end_angle, revolve_axis)
        append_in_geometrical_set_and_update(surfRevolution)
        return surfRevolution
    except Exception as e:
        print(f"An exception occured{e}")

#Fucntion to create lofted surface
def create_lofted_surface(closed_profile1, closed_profile2):
    try:
        lofted_surface = hsf.add_new_loft()
        lofted_surface.add_section_to_loft(closed_profile1,1,1)
        lofted_surface.add_section_to_loft(closed_profile2,1,1)
        append_in_geometrical_set_and_update(lofted_surface)
        return lofted_surface
    except Exception as e:
        print(f"An exception occured{e}")

#Function to create extruded surface
def create_extruded_surface(reference, length_direction1, length_direction2, orientaton, symmetry):
    try:
        extruded_surface = hsf.add_new_extrude(reference, length_direction1, length_direction2, orientaton)
        extruded_surface.symmetrical_extension = symmetry
        append_in_geometrical_set_and_update(extruded_surface)
        return extruded_surface
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------------Fucntion to create Inlet Spike---------------------
#.....................................................................

def Inlet_Spike_Generator():
    try:
        part.in_work_object = partbody
        spike_profile = sketches.add(plane_XY)
        spike_profile.name = "Spike Outer Profile"
        spike2D = spike_profile.open_edition()
        spike2D.create_spline((spike2D.create_control_point(l*0, r*0), spike2D.create_control_point(-l*0.4, r), 
                                spike2D.create_control_point(-l*0.5, r*0.92), spike2D.create_control_point(-l*0.6, r*0.68), 
                                spike2D.create_control_point(-l*0.7, r*0.52), spike2D.create_control_point(-l, r*0.4)))
        spike2D.create_line(*(-l, r*0.4), *(-l, r*0))
        spike2D.create_line(*(-l, r*0), *(l*0, r*0))
        spike_profile.close_edition()
        spike_solid = shpfac.add_new_shaft(spike_profile)
        spike_solid.revolute_axis = x_dir
        document.part.update()
        return spike_solid
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------Fucntion to create spike support struts------------------
#.....................................................................
def strut_generator():
    try:
        strut_point1 = create_construction_point(-l*(7/10), 0, 0)
        strut_point2 = create_construction_point(-l*(4/5), r/25, 0)
        strut_point3 = create_construction_point(-l*(9/10), 0, 0)
        strut_base_half_profile = create_construction_spline(strut_point1, strut_point2, strut_point3)
        strut_base_half_mirrored = mirror_entity(strut_base_half_profile, x_dir)
        strut_base_profile = join_curves(strut_base_half_profile, strut_base_half_mirrored)
        strut_surface = create_extruded_surface(strut_base_profile, R_Nacelle, 0, z_dir, False)
        strut = shpfac.add_new_close_surface(strut_surface)
        document.part.update()
        part.in_work_object = partbody
        number_of_strut_in_radial_direction = 1
        number_of_strut_in_angular_direction = 4
        number_of_steps_in_radial_direction = 0
        number_of_steps_in_angular_direction = 90
        strut_to_copy_position_along_radial_dir = 1
        strut_to_copy_position_along_angular_dir = 1
        rotation_center = x_dir
        rotation_axis = x_dir
        reversed_rotation_axis = True
        rotation_angle = 0
        radius_aligned = True
        strut_pattern = shpfac.add_new_circ_pattern(strut, number_of_strut_in_radial_direction, number_of_strut_in_angular_direction, 
                                                    number_of_steps_in_radial_direction, number_of_steps_in_angular_direction, 
                                                    strut_to_copy_position_along_radial_dir, strut_to_copy_position_along_angular_dir, 
                                                    rotation_center, rotation_axis, reversed_rotation_axis, rotation_angle, radius_aligned)
        document.part.update()
        return strut_pattern
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#--------------Fucntion to create Nacelle Proffile--------------------
#.....................................................................
def nacelle_generator():
    try:
        #Construction Points
        p1 = create_construction_point(-w, R, 0)
        p2 = create_construction_point(-(w+(L/10)), R*(16/15), 0)
        p3 = create_construction_point(-(w+2*(L/10)), R, 0)
        p4 = create_construction_point(-(w+3*(L/10)), R*(14/15), 0)
        p5 = create_construction_point(-(w+4*(L/10)), R*(14/15), 0)
        p6 = create_construction_point(-(w+6*(L/10)), R*(29/30), 0)
        p7 = create_construction_point(-(w+8*(L/10)), R, 0)
        p8 = create_construction_point(-(w+8.5*(L/10)), R*(2/3), 0)
        p9 = create_construction_point(-(w+9*(L/10)), R, 0)
        p10 = create_construction_point(-(w+10*(L/10)), R*(4/3), 0)
        p11 = create_construction_point(-(w+L*3/25), (R*(4/3)), 0)
        p12 = create_construction_point(-(w+L*(11/50)), (R*(7/5)), 0)
        p13 = create_construction_point(-(w+L*(9/10)), (R*(7/5)), 0)
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
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#---------------Fucntion to create Exhaust Nozzle---------------------
#.....................................................................
def nozzle_generator():
    try:
        #------Creating the sketch to make pockets--------
        p1 = create_construction_point(-(offset+9*(L_Nacelle/10)), 0, 0)
        p2 = create_construction_point(-(offset+10.1*(L_Nacelle/10)), 0, R_Nacelle/15)
        p3 = create_construction_point(-(offset+10.1*(L_Nacelle/10)), 0, -R_Nacelle/15)
        point_list = [p1, p2, p3]
        flaps_pocket_triangle =  create_closed_curve_with_polyline(point_list)
        #-----------Creating Pocket-----------
        flaps_pocket = shpfac.add_new_pocket_from_ref(flaps_pocket_triangle, (R_Nacelle)*(20/3))
        document.part.update()
        #-------Adding Circular Pattern-------
        part.in_work_object = partbody
        number_of_pockets_in_radial_direction = 1
        number_of_pockets_in_angular_direction = 15
        number_of_steps_in_radial_direction = 0
        number_of_steps_in_angular_direction = 24
        pockets_to_copy_position_along_radial_dir = 1
        pockets_to_copy_position_along_angular_dir = 1
        rotation_center = x_dir
        rotation_axis = x_dir
        reversed_rotation_axis = True
        rotation_angle = 0
        radius_aligned = True
        exhaust_nozzle = shpfac.add_new_circ_pattern(flaps_pocket, number_of_pockets_in_radial_direction, number_of_pockets_in_angular_direction, 
                                                     number_of_steps_in_radial_direction, number_of_steps_in_angular_direction, 
                                                     pockets_to_copy_position_along_radial_dir, pockets_to_copy_position_along_angular_dir, 
                                                     rotation_center, rotation_axis, reversed_rotation_axis, rotation_angle, radius_aligned)
        document.part.update()
        return exhaust_nozzle
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#---------Fucntion to create blow in doors in nacelle-----------------
#.....................................................................
def blow_in_door_generator():
    try:
        #------Creating the sketch to make pockets--------
        p1 = create_construction_point(-(offset+8*(L_Nacelle/10)), 0, R_Nacelle/6)
        p2 = create_construction_point(-(offset+8*(L_Nacelle/10)), 0, -R_Nacelle/6)
        p3 = create_construction_point(-(offset+8*(L_Nacelle/10)-(L_Nacelle/25)), 0, -R_Nacelle/6)
        p4 = create_construction_point(-(offset+8*(L_Nacelle/10)-(L_Nacelle/25)), 0, R_Nacelle/6)
        point_list = [p1, p2, p3, p4]
        blow_in_door_shape = create_closed_curve_with_polyline(point_list)
        #-----------Creating Pocket-----------
        blow_in_door = shpfac.add_new_pocket_from_ref(blow_in_door_shape, 200)
        document.part.update()
        #-------Adding Circular Pattern-------
        part.in_work_object = partbody
        number_of_doors_in_radial_direction = 1
        number_of_doors_in_angular_direction = 10
        number_of_steps_in_radial_direction = 0
        number_of_steps_in_angular_direction = 36
        doors_to_copy_position_along_radial_dir = 1
        doors_to_copy_position_along_angular_dir = 1
        rotation_center = x_dir
        rotation_axis = x_dir
        reversed_rotation_axis = True
        rotation_angle = 0
        radius_aligned = True
        blow_in_door_ring = shpfac.add_new_circ_pattern(blow_in_door, number_of_doors_in_radial_direction, number_of_doors_in_angular_direction, 
                                                        number_of_steps_in_radial_direction, number_of_steps_in_angular_direction, 
                                                        doors_to_copy_position_along_radial_dir, doors_to_copy_position_along_angular_dir, 
                                                        rotation_center, rotation_axis, reversed_rotation_axis, rotation_angle, radius_aligned)
        document.part.update()
        return blow_in_door_ring
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-----------Fucntion to create rudder aerofoil profile----------------
#.....................................................................
def rudder_airfoil_generator(leading_edge, mid_point, traling_edge):
    try:
        half_airfoil = create_construction_spline(leading_edge, mid_point, traling_edge)
        mirror_line = create_construction_line(leading_edge, traling_edge)
        mirrored_airfoil = mirror_entity(half_airfoil, mirror_line)
        rudder_airfoil = join_curves(half_airfoil, mirrored_airfoil)
        return rudder_airfoil
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------Fucntion to create rudder-------------------------
#.....................................................................
def rudder_generator():
    try:
        #Create base airfoil profile
        b1 = create_construction_point(-(offset+0.64*L_Nacelle), 0, R_Nacelle*(4/3))                #leading edge
        b2 = create_construction_point(-(offset+0.75*L_Nacelle), R_Nacelle/15, R_Nacelle*(4/3))     #mid point
        b3 = create_construction_point(-(offset+0.86*L_Nacelle), 0, R_Nacelle*(4/3))                #trailing edge
        rudder_base_airfoil = rudder_airfoil_generator(b1, b2, b3)

        #Create intermediate airfoil profile
        i1 = create_construction_point(-(offset+0.648*L_Nacelle), 0, R_Nacelle*(5/3))               #leading edge
        i2 = create_construction_point(-(offset+0.834*L_Nacelle), R_Nacelle/15, R_Nacelle*(5/3))    #mid point
        i3 = create_construction_point(-(offset+1.02*L_Nacelle), 0, R_Nacelle*(5/3))                #trailing edge
        rudder_intermed_airfoil = rudder_airfoil_generator(i1, i2, i3)

        #Creating top airfoil Profile
        t1 = create_construction_point(-(offset+0.76*L_Nacelle), 0, R_Nacelle*(19/3))               #leading edge
        t2 = create_construction_point(-(offset+0.855*L_Nacelle), R_Nacelle/15, R_Nacelle*(19/3))   #mid point
        t3 = create_construction_point(-(offset+0.95*L_Nacelle), 0, R_Nacelle*(19/3))               #trailing edge
        rudder_top_airfoil = rudder_airfoil_generator(t1, t2, t3)

        #Lofted surfaces and solids
        rudder_base_portion_surface = create_lofted_surface(rudder_base_airfoil, rudder_intermed_airfoil)
        rudder_top_portion_surface = create_lofted_surface(rudder_intermed_airfoil, rudder_top_airfoil)
        rudder_base_potion_solid = shpfac.add_new_close_surface(rudder_base_portion_surface)
        rudderr_top_portion_solid = shpfac.add_new_close_surface(rudder_top_portion_surface)
        document.part.update()

        #Base end cut
        corner1 = create_construction_point(-(offset+0.96*L_Nacelle), R_Nacelle*(2/3), R_Nacelle*(3/2))
        corner2 = create_construction_point(-(offset+1.04*L_Nacelle), R_Nacelle*(2/3), R_Nacelle*(3/2))
        corner3 = create_construction_point(-(offset+1.04*L_Nacelle), R_Nacelle*(2/3), R_Nacelle*(5/2))
        point_list = [corner1, corner2, corner3]
        rudder_end_cut_profile = create_closed_curve_with_polyline(point_list)
        rudder_end_cut = shpfac.add_new_pocket_from_ref(rudder_end_cut_profile, R_Nacelle*(5/3))
        document.part.update()

        return rudderr_top_portion_solid, rudder_base_potion_solid, rudder_end_cut

    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------Fucntion to create wing aerofoil profile----------------
#.....................................................................
def wing_airfoil_generator(leading_edge, top_mid_point, bottom_mid_point, trailing_edge):
    try:
        top_airfoil = create_construction_spline(leading_edge, top_mid_point, trailing_edge)
        bottom_airfoil = create_construction_spline(leading_edge, bottom_mid_point, trailing_edge)
        wing_airfoil = join_curves(top_airfoil, bottom_airfoil)
        return wing_airfoil
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------------------Fucntion to create wing------------------------
#.....................................................................
def wing_generator():
    try:
        #Root Airfoil
        r1 = create_construction_point(-(offset+0.22*L_Nacelle), R_Nacelle*(4/3), 0)                    #leading edge
        r2 = create_construction_point(-(offset+0.54*L_Nacelle), R_Nacelle*(4/3), R_Nacelle*(7/30))     #top mid point
        r3 = create_construction_point(-(offset+0.9*L_Nacelle), R_Nacelle*(4/3), 0)                     #trailing edge
        r4 = create_construction_point(-(offset+0.54*L_Nacelle), R_Nacelle*(4/3), -R_Nacelle*(2/15))    #bottom mid point
        root_airfoil = wing_airfoil_generator(r1, r2, r4, r3)

        #Tip Airfoil
        t1 = create_construction_point(-(offset+0.54*L_Nacelle), R_Nacelle*(35/3), 0)                   #leading edge
        t2 = create_construction_point(-(offset+0.66*L_Nacelle), R_Nacelle*(35/3), R_Nacelle/10)        #top mid point
        t3 = create_construction_point(-(offset+0.83*L_Nacelle), R_Nacelle*(35/3), 0)                   #trailing edge
        t4 = create_construction_point(-(offset+0.66*L_Nacelle), R_Nacelle*(35/3), -R_Nacelle/30)       #bottom mid point
        tip_airfoil = wing_airfoil_generator(t1, t2, t4, t3)

        wing_surface = create_lofted_surface(root_airfoil, tip_airfoil)
        solid_wing = shpfac.add_new_close_surface(wing_surface)
        document.part.update()
        return solid_wing

    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#----------------Fucntion to create fuselage shape--------------------
#.....................................................................
def fuselage_shape_generator(leading_edge, top_mid_point1, top_mid_point2, top_mid_point3, trailing_edge, bottom_mid):
    try:
        upper_fuselage_shape = create_construction_spline(leading_edge, top_mid_point1, top_mid_point2, top_mid_point3, trailing_edge)
        lower_fuselage_shape = create_construction_spline(leading_edge, bottom_mid, trailing_edge)
        fuselage_shape = join_curves(upper_fuselage_shape, lower_fuselage_shape)
        return fuselage_shape
    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#--------------------Fucntion to create fuselage----------------------
#.....................................................................
def fuselage_generator():
    try:
        #Fuselage part adjacent to wing
        fusel_wing_lead = create_construction_point(-(L_Aircraft/12), -(R_Nacelle*(19/15)), 0)
        fusel_wing_top_1 = create_construction_point(-(L_Aircraft/6), -(R_Nacelle*(19/15)), (R_Nacelle/3))
        fusel_wing_top_2 = create_construction_point(-(L_Aircraft/4), -(R_Nacelle*(19/15)), (R_Nacelle*(2/5)))
        fusel_wing_top_3 = create_construction_point(-(L_Aircraft/3),-(R_Nacelle*(19/15)), (R_Nacelle/3))
        fusel_wing_trail = create_construction_point(-(L_Aircraft*(5/12)), -(R_Nacelle*(19/15)), 0)
        fusel_wing_bottom = create_construction_point(-(L_Aircraft/4), -(R_Nacelle*(19/15)), -(R_Nacelle/6))

        fuselage_wing_adjacent_profile = fuselage_shape_generator(fusel_wing_lead, fusel_wing_top_1, fusel_wing_top_2, 
                                                                  fusel_wing_top_3, fusel_wing_trail, fusel_wing_bottom)

        #Fuselage part in midplane
        fusel_mid_lead = create_construction_point((L_Aircraft/2), -(W_Aircraft/2), 0)
        fusel_mid_top_1 = create_construction_point((L_Aircraft/4), -(W_Aircraft/2), (L_Aircraft/40))
        fusel_mid_top_2 = create_construction_point(0, -(W_Aircraft/2), L_Aircraft*(7/240))
        fusel_mid_top_3 = create_construction_point(-(L_Aircraft/4), -(W_Aircraft/2), L_Aircraft/40)
        fusel_mid_trail = create_construction_point(-(L_Aircraft/2), -(W_Aircraft/2), 0)
        fusel_mid_bottom = create_construction_point(0, -(W_Aircraft/2), -(L_Aircraft/60))

        fuselage_midplane_profile = fuselage_shape_generator(fusel_mid_lead, fusel_mid_top_1, fusel_mid_top_2, 
                                                             fusel_mid_top_3, fusel_mid_trail, fusel_mid_bottom)

        half_fuselage_surface = create_lofted_surface(fuselage_wing_adjacent_profile, fuselage_midplane_profile)

        half_fuselage_solid = shpfac.add_new_close_surface(half_fuselage_surface)
        document.part.update()
        return half_fuselage_solid

    except Exception as e:
        print(f"An exception occured{e}")

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------------------Creating the aircraft------------------------
#.....................................................................

#_______________Generating Spike and support strut____________________
    
Inlet_Spike_Generator()
strut_generator()

#______________________Generating Nacelle Body________________________
try:
    #------------Creating 2D profile-------------
    nacelle_2D_profile = nacelle_generator()
    #-------------Revolved sruface---------------
    #curve = nacelle_2D_profile
    #start angle = 0
    #end angle = 360
    #revolve_axis = x_dir
    nacelle_surface = create_surface_revolve(nacelle_2D_profile, 0, 360, x_dir)
    #-----------------Making Solid---------------
    nacelle = shpfac.add_new_close_surface(nacelle_surface)
    document.part.update()
except Exception as e:
        print(f"An exception occured{e}")

#________________________Generating Nozzle____________________________
nozzle_generator()

#___________________Generating blow in doors__________________________
blow_in_door_generator()

#______________________Generating Rudder______________________________
rudder_generator()

#________________________Generating Wing______________________________
wing_generator()

#_____________________Generating Fuselage_____________________________
fuselage_generator()

#________________Mirror to get the entire airplane____________________

#----------Add Plane to Mirror--------------
try:
    plane_to_mirror = hsf.add_new_plane_offset(plane_ZX, -(W_Aircraft/2), False)
    append_in_geometrical_set_and_update(plane_to_mirror)
except Exception as e:
        print(f"An exception occured{e}")
#------------Mirror operation---------------
try:
    part.in_work_object = partbody
    shpfac.add_new_mirror(plane_to_mirror)
    document.part.update()
except Exception as e:
        print(f"An exception occured{e}")

#________________Hiding the construction elements____________________
try:
    selection.clear();
    selection.add(geometrical_set)
    selection.vis_properties.set_show(1) # 0: Show / 1: Hide
    selection.clear()
except Exception as e:
    print(f"An exception occured{e}")

#___________________UPDATE THE DOCUMENT_____________________       
try:
    document.part.update()
except Exception as e:
    print(f"An exception occured{e}")

#------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------END of CODE-----------------------------------------------------------
#________________________________________________________________________________________________________________________