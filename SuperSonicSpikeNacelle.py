from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.enumeration.enumeration_types import cat_limit_mode 
from pycatia.enumeration.enumeration_types import cat_prism_orientation
from pycatia.enumeration.enumeration_types import cat_constraint_type
from pycatia.enumeration.enumeration_types import cat_constraint_mode

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

point13 = hsf.add_new_point_coord(-500,47,0)
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
point17 = hsf.add_new_point_coord(-340, 47, 25)
construction_elements.append_hybrid_shape(point17)
document.part.update()

point18 = hsf.add_new_point_coord(-333, 50, 25)
construction_elements.append_hybrid_shape(point18)
document.part.update()

point19 = hsf.add_new_point_coord(-325, 50, 25)
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
p14 = hsf.add_new_point_coord(-323, 70, 0)
p15 = hsf.add_new_point_coord(-323, 74, 0)
p16 = hsf.add_new_point_coord(-342, 74, 0)
p17 = hsf.add_new_point_coord(-342, 70, 0)

ring_profile = hsf.add_new_polyline()
ring_profile.insert_element(p14, 0)
ring_profile.insert_element(p14, 1)
ring_profile.insert_element(p15, 2)
ring_profile.insert_element(p16, 3)
ring_profile.insert_element(p17, 4)
ring_profile.insert_element(p14, 5)

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
