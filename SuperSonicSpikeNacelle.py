from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.enumeration.enumeration_types import cat_limit_mode 
from pycatia.enumeration.enumeration_types import cat_prism_orientation
from pycatia.enumeration.enumeration_types import cat_constraint_type
from pycatia.enumeration.enumeration_types import cat_constraint_mode
from pycatia.enumeration.enumeration_types import cat_selection_filter

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

spike_profile = sketches.add(plane_XY)
spike_profile.name = "Spike Outer Profile"
spike2D = spike_profile.open_edition()

p1 = (0, 47)
p2 = (-103, 79)
p3 = (-110, 80)
p4 = (-124, 80)
p5 = (-148, 79)
c1 = spike2D.create_control_point(-148, 79)
c2 = spike2D.create_control_point(-182, 76)
p7 = (-205, 71)
c3 = spike2D.create_control_point(-205, 71)
p8 = (-240, 70)
c4 = spike2D.create_control_point(-240, 70)
c5 = spike2D.create_control_point(-248, 69)
p10 = (-264, 66)
c6 = spike2D.create_control_point(-264, 66)
p11 = (-310, 62)
p12 = (-340, 62)
p13 = (-340, 47)


spike2D.create_line(*p1, *p2)
spike2D.create_line(*p2, *p3)
spike2D.create_line(*p3, *p4)
spike2D.create_line(*p4, *p5)
spike2D.create_spline((c1, c2, c3))
spike2D.create_line(*p7, *p8)
spike2D.create_spline((c4, c5, c6))
spike2D.create_line(*p10, *p11)
spike2D.create_line(*p11, *p12)
spike2D.create_line(*p12, *p13)
spike2D.create_line(*p13, *p1)

spike_profile.close_edition()
document.part.update()

#Creating Geometrical Set
construction_elements = hybrid_bodies.add()
construction_elements.name = "construction_elements"

#Creating Rev axis
point1 = hsf.add_new_point_coord(10, 47, 0)
construction_elements.append_hybrid_shape(point1)
document.part.update()

point2 = hsf.add_new_point_coord(-330, 47, 0)
construction_elements.append_hybrid_shape(point2)
document.part.update()

rev_axis = hsf.add_new_line_pt_pt(point1, point2)
rev_axis.name = "revolution_axis"
construction_elements.append_hybrid_shape(rev_axis)
document.part.update()

part.in_work_object = partbody

# Create shaft
shaft1 = shpfac.add_new_shaft(spike_profile)
shaft1.revolute_axis = rev_axis
document.part.update()

#End of Spike

#start of strut
#base profile points
point3 = hsf.add_new_point_coord(-211,47,0)
construction_elements.append_hybrid_shape(point3)
document.part.update()

point4 = hsf.add_new_point_coord(-235,56,0)
construction_elements.append_hybrid_shape(point4)
document.part.update()

point5 = hsf.add_new_point_coord(-270,56,0)
construction_elements.append_hybrid_shape(point5)
document.part.update()

point6 = hsf.add_new_point_coord(-297,47,0)
construction_elements.append_hybrid_shape(point6)
document.part.update()

point7 = hsf.add_new_point_coord(-324,47,0)
construction_elements.append_hybrid_shape(point7)
document.part.update()

spline1 = hsf.add_new_spline()
spline1.add_point(point3)
spline1.add_point(point4)
spline1.add_point(point5)
spline1.add_point(point6)
construction_elements.append_hybrid_shape(spline1)
document.part.update()

mirror_line = hsf.add_new_line_pt_pt(point3, point7)
construction_elements.append_hybrid_shape(mirror_line)
document.part.update()

symmetrical_spline1 = hsf.add_new_symmetry(spline1, mirror_line)
construction_elements.append_hybrid_shape(symmetrical_spline1)
document.part.update()

strut_base_profile = hsf.add_new_join(spline1, symmetrical_spline1)
strut_base_profile.name = "Strut_Base_Profile"
construction_elements.append_hybrid_shape(strut_base_profile)
document.part.update()

#Upper Profile Points
point8 = hsf.add_new_point_coord(-231,47,43)
construction_elements.append_hybrid_shape(point8)
document.part.update()

point9 = hsf.add_new_point_coord(-265,52,43)
construction_elements.append_hybrid_shape(point9)
document.part.update()

point10 = hsf.add_new_point_coord(-287,52,43)
construction_elements.append_hybrid_shape(point10)
document.part.update()

point11 = hsf.add_new_point_coord(-317,47,43)
construction_elements.append_hybrid_shape(point11)
document.part.update()

spline2 = hsf.add_new_spline()
spline2.add_point(point8)
spline2.add_point(point9)
spline2.add_point(point10)
spline2.add_point(point11)
construction_elements.append_hybrid_shape(spline2)
document.part.update()

mirror_line2 = hsf.add_new_line_pt_pt(point8, point11)
construction_elements.append_hybrid_shape(mirror_line2)
document.part.update()

symmetrical_spline2 = hsf.add_new_symmetry(spline2, mirror_line2)
construction_elements.append_hybrid_shape(symmetrical_spline2)
document.part.update()

strut_end_profile = hsf.add_new_join(spline2, symmetrical_spline2)
strut_end_profile.name = "Strut_Base_Profile"
construction_elements.append_hybrid_shape(strut_end_profile)
document.part.update()

#add loft
strut_surface = hsf.add_new_loft()
strut_surface.add_section_to_loft(strut_base_profile,1,1)
strut_surface.add_section_to_loft(strut_end_profile,1,1)
construction_elements.append_hybrid_shape(strut_surface)
document.part.update()

#Hide the strut surface
selection.clear();
selection.add(strut_surface)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
document.part.update()

#Make the strut solid
solid_strut  = shpfac.add_new_close_surface(strut_surface)
document.part.update()

#Make pattern of the strut
#Create Reference axis
point12 = hsf.add_new_point_coord(0,47,0)
construction_elements.append_hybrid_shape(point12)
document.part.update()

point13 = hsf.add_new_point_coord(-1500,47,0)
construction_elements.append_hybrid_shape(point13)
document.part.update()

ref_axis_to_ptrn = hsf.add_new_line_pt_pt(point12, point13)
construction_elements.append_hybrid_shape(ref_axis_to_ptrn)
document.part.update() 

#Pattern
part.in_work_object = partbody
strut_pattern = shpfac.add_new_circ_pattern(solid_strut, 1, 4, 0, 90, 1, 1, ref_axis_to_ptrn, ref_axis_to_ptrn, True, 0, True)
document.part.update()

#Creating stator
#base profile
point14 = hsf.add_new_point_coord(-340, 47, 0)
construction_elements.append_hybrid_shape(point14)
document.part.update()

point15 = hsf.add_new_point_coord(-333, 50, 0)
construction_elements.append_hybrid_shape(point15)
document.part.update()

point16 = hsf.add_new_point_coord(-325, 50, 0)
construction_elements.append_hybrid_shape(point16)
document.part.update()

spline3 = hsf.add_new_spline()
spline3.add_point(point14)
spline3.add_point(point15)
spline3.add_point(point16)
construction_elements.append_hybrid_shape(spline3)
document.part.update()

mirror_line3 = hsf.add_new_line_pt_pt(point14, point16)
construction_elements.append_hybrid_shape(mirror_line3)
document.part.update()

symmetrical_spline3 = hsf.add_new_symmetry(spline3, mirror_line3)
construction_elements.append_hybrid_shape(symmetrical_spline3)
document.part.update()

stator_blade_base = hsf.add_new_join(spline3, symmetrical_spline3)
stator_blade_base.name = "stator_blade_base"
construction_elements.append_hybrid_shape(stator_blade_base)
document.part.update()

#end profile
point17 = hsf.add_new_point_coord(-340, 47, 28)
construction_elements.append_hybrid_shape(point17)
document.part.update()

point18 = hsf.add_new_point_coord(-333, 50, 28)
construction_elements.append_hybrid_shape(point18)
document.part.update()

point19 = hsf.add_new_point_coord(-325, 50, 28)
construction_elements.append_hybrid_shape(point19)
document.part.update()

spline4 = hsf.add_new_spline()
spline4.add_point(point17)
spline4.add_point(point18)
spline4.add_point(point19)
construction_elements.append_hybrid_shape(spline4)
document.part.update()

mirror_line4 = hsf.add_new_line_pt_pt(point17, point19)
construction_elements.append_hybrid_shape(mirror_line4)
document.part.update()

symmetrical_spline4 = hsf.add_new_symmetry(spline4, mirror_line4)
construction_elements.append_hybrid_shape(symmetrical_spline4)
document.part.update()

stator_blade_end = hsf.add_new_join(spline4, symmetrical_spline4)
stator_blade_end.name = "stator_blade_base"
construction_elements.append_hybrid_shape(stator_blade_end)
document.part.update()

#add loft
stator_blade_surface = hsf.add_new_loft()
stator_blade_surface.add_section_to_loft(stator_blade_base,1,1)
stator_blade_surface.add_section_to_loft(stator_blade_end,1,1)
construction_elements.append_hybrid_shape(stator_blade_surface)
document.part.update()

#Hide the stator surface
selection.clear();
selection.add(stator_blade_surface)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
document.part.update()

#Make the stator blade
solid_stator_blade = shpfac.add_new_close_surface(stator_blade_surface)
document.part.update()

#Make pattern of the stator blade
#Pattern
part.in_work_object = partbody
stator_blade_pattern = shpfac.add_new_circ_pattern(solid_stator_blade, 1, 20, 0, 18, 1, 1, ref_axis_to_ptrn, ref_axis_to_ptrn, True, 0, True)
document.part.update()

#Stator ring
point20 = hsf.add_new_point_coord(-323, 73, 0)
construction_elements.append_hybrid_shape(point20)
point21 = hsf.add_new_point_coord(-323, 77, 0)
construction_elements.append_hybrid_shape(point21)
point22 = hsf.add_new_point_coord(-342, 77, 0)
construction_elements.append_hybrid_shape(point22)
point23 = hsf.add_new_point_coord(-342, 73, 0)
construction_elements.append_hybrid_shape(point23)

ring_profile = hsf.add_new_polyline()
ring_profile.insert_element(point20, 0)
ring_profile.insert_element(point20, 1)
ring_profile.insert_element(point21, 2)
ring_profile.insert_element(point22, 3)
ring_profile.insert_element(point23, 4)
ring_profile.insert_element(point20, 5)

construction_elements.append_hybrid_shape(ring_profile)
document.part.update()

ring_revolve = hsf.add_new_revol(ring_profile, 0, 360, ref_axis_to_ptrn)
construction_elements.append_hybrid_shape(ring_revolve)
document.part.update()

#Hide the ring_surface
selection.clear();
selection.add(ring_revolve)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
document.part.update()

#Make the ring solid
solid_strut  = shpfac.add_new_close_surface(ring_revolve)
document.part.update()

#____________Inner Nacelle surface_________________________________________________
#__________________________________________________________________________________

point24 = hsf.add_new_point_coord(-100, 87, 0)
construction_elements.append_hybrid_shape(point24)
document.part.update()

point25 = hsf.add_new_point_coord(-125, 87, 0)
construction_elements.append_hybrid_shape(point25)
document.part.update()

point26 = hsf.add_new_point_coord(-145, 86, 0)
construction_elements.append_hybrid_shape(point26)
document.part.update()

spline5 = hsf.add_new_spline()
spline5.add_point(point24)
spline5.add_point(point25)
spline5.add_point(point26)
construction_elements.append_hybrid_shape(spline5)
document.part.update()

point27 = hsf.add_new_point_coord(-240, 78, 0)
construction_elements.append_hybrid_shape(point27)
document.part.update()

point28 = hsf.add_new_point_coord(-323, 77, 0)
construction_elements.append_hybrid_shape(point28)
document.part.update()

spline6 = hsf.add_new_spline()
spline6.add_point(point26)
spline6.add_point(point27)
spline6.add_point(point28)
construction_elements.append_hybrid_shape(spline6)
document.part.update()

spline_one_for_inner_curve = hsf.add_new_join(spline5, spline6)
construction_elements.append_hybrid_shape(spline_one_for_inner_curve)
document.part.update()

#______________Curve upto the rotor blade ring ends here_____________

#Engine Part
#Create Polyline

point29 = hsf.add_new_point_coord(-342, 77, 0)
construction_elements.append_hybrid_shape(point29)
document.part.update()

point30 = hsf.add_new_point_coord(-370, 77, 0)
construction_elements.append_hybrid_shape(point30)
document.part.update()

point31 = hsf.add_new_point_coord(-375, 80, 0)
construction_elements.append_hybrid_shape(point31)
document.part.update()

point32 = hsf.add_new_point_coord(-405, 80, 0)
construction_elements.append_hybrid_shape(point32)
document.part.update()

point33 = hsf.add_new_point_coord(-410, 77, 0)
construction_elements.append_hybrid_shape(point33)
document.part.update()

point34 = hsf.add_new_point_coord(-415, 77, 0)
construction_elements.append_hybrid_shape(point34)
document.part.update()

point35 = hsf.add_new_point_coord(-420, 80, 0)
construction_elements.append_hybrid_shape(point35)
document.part.update()

point36 = hsf.add_new_point_coord(-460, 80, 0)
construction_elements.append_hybrid_shape(point36)
document.part.update()

point37 = hsf.add_new_point_coord(-465, 77, 0)
construction_elements.append_hybrid_shape(point37)
document.part.update()

point38 = hsf.add_new_point_coord(-495, 77, 0)
construction_elements.append_hybrid_shape(point38)
document.part.update()

point39 = hsf.add_new_point_coord(-502, 78, 0)
construction_elements.append_hybrid_shape(point39)
document.part.update()

point40 = hsf.add_new_point_coord(-507, 78, 0)
construction_elements.append_hybrid_shape(point40)
document.part.update()

point41 = hsf.add_new_point_coord(-525, 82, 0)
construction_elements.append_hybrid_shape(point41)
document.part.update()

point42 = hsf.add_new_point_coord(-570, 82, 0)
construction_elements.append_hybrid_shape(point42)
document.part.update()

point43 = hsf.add_new_point_coord(-580, 87, 0)
construction_elements.append_hybrid_shape(point43)
document.part.update()

point44 = hsf.add_new_point_coord(-610, 87, 0)
construction_elements.append_hybrid_shape(point44)
document.part.update()

nacelle_profile_part2 = hsf.add_new_polyline()
nacelle_profile_part2.insert_element(point28, 0)
nacelle_profile_part2.insert_element(point28, 1)
nacelle_profile_part2.insert_element(point29, 2)
nacelle_profile_part2.insert_element(point30, 3)
nacelle_profile_part2.insert_element(point31, 4)
nacelle_profile_part2.insert_element(point32, 5)
nacelle_profile_part2.insert_element(point33, 6)
nacelle_profile_part2.insert_element(point34, 7)
nacelle_profile_part2.insert_element(point35, 8)
nacelle_profile_part2.insert_element(point36, 9)
nacelle_profile_part2.insert_element(point37, 10)
nacelle_profile_part2.insert_element(point38, 11)
nacelle_profile_part2.insert_element(point39, 12)
nacelle_profile_part2.insert_element(point40, 13)
nacelle_profile_part2.insert_element(point41, 14)
nacelle_profile_part2.insert_element(point42, 15)
nacelle_profile_part2.insert_element(point43, 16)
nacelle_profile_part2.insert_element(point44, 17)

construction_elements.append_hybrid_shape(nacelle_profile_part2)
document.part.update()

point45 = hsf.add_new_point_coord(-615, 87, 0)
construction_elements.append_hybrid_shape(point45)
document.part.update()

point46 = hsf.add_new_point_coord(-620, 82, 0)
construction_elements.append_hybrid_shape(point46)
document.part.update()

spline7 = hsf.add_new_spline()
spline7.add_point(point44)
spline7.add_point(point45)
spline7.add_point(point46)
construction_elements.append_hybrid_shape(spline7)
document.part.update()

curve_engine_part = hsf.add_new_join(nacelle_profile_part2, spline7)
construction_elements.append_hybrid_shape(curve_engine_part)
document.part.update()

nacelle_inner_profile_curve = hsf.add_new_join(spline_one_for_inner_curve, curve_engine_part)
construction_elements.append_hybrid_shape(nacelle_inner_profile_curve)
document.part.update()

#converging diverging nozzle
point47 = hsf.add_new_point_coord(-640, 77, 0)
construction_elements.append_hybrid_shape(point47)
document.part.update()

point48 = hsf.add_new_point_coord(-660, 82, 0)
construction_elements.append_hybrid_shape(point48)
document.part.update()

spline8 = hsf.add_new_spline()
spline8.add_point(point46)
spline8.add_point(point47)
spline8.add_point(point48)
construction_elements.append_hybrid_shape(spline8)
document.part.update()

nacelle_inner_and_nozzle = hsf.add_new_join(nacelle_inner_profile_curve, spline8)
construction_elements.append_hybrid_shape(nacelle_inner_and_nozzle)
document.part.update()

# point49 = hsf.add_new_point_coord(-700, 87, 0)
# construction_elements.append_hybrid_shape(point49)
# document.part.update()

# line_exhaust = hsf.add_new_line_pt_pt(point48, point49)
# construction_elements.append_hybrid_shape(line_exhaust)
# document.part.update()

point50 = hsf.add_new_point_coord(-240, 95, 0)
construction_elements.append_hybrid_shape(point50)
document.part.update()

point51 = hsf.add_new_point_coord(-342, 95, 0)
construction_elements.append_hybrid_shape(point51)
document.part.update()

point52 = hsf.add_new_point_coord(-460, 95, 0)
construction_elements.append_hybrid_shape(point52)
document.part.update()

point53 = hsf.add_new_point_coord(-660, 95, 0)
construction_elements.append_hybrid_shape(point53)
document.part.update()

spline9 = hsf.add_new_spline()
spline9.add_point(point24)
spline9.add_point(point50)
spline9.add_point(point51)
spline9.add_point(point52)
spline9.add_point(point53)
construction_elements.append_hybrid_shape(spline9)
document.part.update()

line_closing_nacelle_profile = hsf.add_new_line_pt_pt(point53, point48)
construction_elements.append_hybrid_shape(line_closing_nacelle_profile)
document.part.update()

nacelle_outer_curve = hsf.add_new_join(spline9, line_closing_nacelle_profile)
construction_elements.append_hybrid_shape(nacelle_outer_curve)

nacelle_profile = hsf.add_new_join(nacelle_inner_and_nozzle, nacelle_outer_curve)
construction_elements.append_hybrid_shape(nacelle_profile)
document.part.update()

##________Nacelle Profile Curve finished _________####
##_________Make Revolve_____________
nacelle_revolved_surface = hsf.add_new_revol(nacelle_profile, 0, 360, ref_axis_to_ptrn)
construction_elements.append_hybrid_shape(nacelle_revolved_surface)
document.part.update()

#Hide the ring_surface
selection.clear();
selection.add(nacelle_revolved_surface)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
document.part.update()

nacelle = shpfac.add_new_close_surface(nacelle_revolved_surface)
document.part.update()


#Create_cross_section
# pt1 = hsf.add_new_point_coord(50, 47, -150)
# construction_elements.append_hybrid_shape(pt1)
# pt2 = hsf.add_new_point_coord(-800, 47, -150)
# construction_elements.append_hybrid_shape(pt2)
# pt3 = hsf.add_new_point_coord(-800, 150, -150)
# construction_elements.append_hybrid_shape(pt3)
# pt4 = hsf.add_new_point_coord(50, 150, -150) 
# construction_elements.append_hybrid_shape(pt4)

# pocket_rect = hsf.add_new_polyline()
# pocket_rect.insert_element(pt1, 0)
# pocket_rect.insert_element(pt1, 1)
# pocket_rect.insert_element(pt2, 2)
# pocket_rect.insert_element(pt3, 3)
# pocket_rect.insert_element(pt4, 4)
# pocket_rect.insert_element(pt1, 5)
# construction_elements.append_hybrid_shape(pocket_rect)
# document.part.update()

# view = shpfac.add_new_pocket_from_ref(pocket_rect, 200)
# document.part.update()

# selection.clear()
# caa.message_box('Select a surface', buttons=1, title='Make selection')
# selection.select_element2(('BiDim',), 'Select a surface', True)
# surf_ref = selection.item2(1).value
# print(surf_ref.name)
# selection.clear()

# shell = shpfac.add_new_shell(surf_ref, 0.5, 0)
# document.part.update()