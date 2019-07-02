from app.utils.common.material import Material
from app.utils.common.is800_2007 import IS800_2007
import sqlite3
from is800_2007 import IS800_2007

class Component(object):

    def __init__(self, material=Material()):
        self.material = material
        self.path_to_database = "../../databases/Intg_osdag.sqlite"


class Bolt(Component):

    def __init__(self, grade=0.0, diameter=0.0, bolt_type="", length=0.0, material=Material()):
        self.grade = grade
        self.diameter = diameter
        self.bolt_type = bolt_type
        self.length = length
        self.shear_capacity = 0.0
        self.bearing_capacity = 0.0
        self.bolt_capacity = 0.0
        self.no_of_bolts = 0
        self.bolt_group_capacity = 0.0
        super(Bolt, self).__init__(material)

    def __repr__(self):
        repr = "Bolt\n"
        repr += "Diameter: {}\n".format(self.diameter)
        repr += "Type: {}\n".format(self.bolt_type)
        repr += "Grade: {}\n".format(self.grade)
        repr += "Length: {}".format(self.length)
        return repr

    def calculate_bolt_shear_capacity(self, bolt_diameter):
        # self.shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity()
        # TODO : Bolt shear capacity functions
        pass
        
        
class Bolt_Group(Component):
    
    def __init__(self, no_of_bolts=0.0, group_capacity=0.0, gauge=0.0, pitch=0.0, end=0.0, edge=0.0, material=Material()):
        self.no_of_bolts = no_of_bolts
        self.group_capacity = group_capacity
        self.gauge = gauge
        self.pitch = pitch
        self.end = end
        self.edge = edge
        super(Bolt, self).__init__(material)

    def __repr__(self):
        repr = "Bolt Group\n"
        repr += "no_of_bolts: {}\n".format(self.no_of_bolts)
        repr += "group_capacity {}\n".format(self.group_capacity)
        repr += "gauge {}\n".format(self.gauge)
        repr += "pitch {}\n".format(self.pitch)
        repr += "end {}\n".format(self.end)
        repr += "edge {}\n".format(self.edge)
        return repr
    
    def calculate_no_of_bolts(self,V_d,V_bolt):
        return V_d / V_bolt
    
    def min_pitch_gauge_check(self, pitch_or_gauge):
        if pitch_or_gauge >= IS800_2007.cl_10_2_2_min_spacing(pitch_or_gauge):
            return True
        else:
            return False

    def max_pitch_gauge_check(self, pitch_or_gauge,plate_thickness):
        if pitch_or_gauge =< IS800_2007.cl_10_2_3_1_max_spacing(plate_thickness)
            return True
        else:
            return False


    def max_pitch_check_2(self, pitch, plate_thickness, compression_or_tension):
        if pitch_or_gauge = < IS800_2007.cl_10_2_3_2_max_pitch_tension_compression(pitch, plate_thickness, compression_or_tension)
            return True
        else:
            return False


    def min_end_edge_check(self,end_or_edge,bolt_hole_type, edge_type):
        if end_or_edge >= IS800_2007.cl_10_2_4_2_min_edge_end_dist(end_or_edge, bolt_hole_type, edge_type):
            return True
        else:
            return False


    def max_end_edge_check(self, end_or_edge,plate_thicknesses, f_y, corrosive_influences):
        if end_or_edge <= IS800_2007.cl_10_2_4_3_max_edge_dist(plate_thicknesses, f_y, corrosive_influences):
            return True
        else:
            return False

    def check_for_long_joints():
        pass
        
class Nut(Component):

    def __init__(self, diameter=0.0, material=Material()):
        self.diameter = diameter
        super(Nut, self).__init__(material)

    def __repr__(self):
        repr = "Nut\n"
        repr += "Diameter: {}".format(self.diameter)
        return repr

class Section(Component):

    def __init__(self, designation, material=Material()):
        self.designation = designation
        self.depth = 0.0
        self.flange_width = 0.0
        self.web_thickness = 0.0
        self.flange_thickness = 0.0
        self.root_radius = 0.0
        self.toe_radius = 0.0
        super(Section, self).__init__(material)

    def __repr__(self):
        repr = "Section\n"
        repr += "Designation: {}".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, table, designation):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT D, B, tw, T, R1, R2 FROM " + table + " WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        self.depth = row[0]
        self.flange_width = row[1]
        self.web_thickness = row[2]
        self.flange_thickness = row[3]
        self.root_radius = row[4]
        self.toe_radius = row[5]

        conn.close()


class Beam(Section):

    def __init__(self, designation, material=Material()):
        super(Beam, self).__init__(designation, material)
        self.connect_to_database_update_other_attributes("Beams", designation)


class Column(Section):

    def __init__(self, designation, material=Material()):
        super(Column, self).__init__(designation, material)
        self.connect_to_database_update_other_attributes("Columns", designation)


class Weld(Component):

    def __init__(self, size=0.0, length=0.0, material=Material()):
        self.size = size
        self.length = length
        super(Weld, self).__init__(material)

    def __repr__(self):
        repr = "Weld\n"
        repr += "Size: {}\n".format(self.size)
        repr += "Length: {}".format(self.length)
        return repr


class Plate(Component):

    def __init__(self, thickness=0.0, height=0.0, width=0.0, material=Material()):
        self.thickness = thickness
        self.height = height
        self.width = width
        super(Plate, self).__init__(material)

    def __repr__(self):
        repr = "Plate\n"
        repr += "Thickness: {}".format(self.thickness)
        return repr


class Angle(Component):

    def __init__(self, designation, material=Material()):
        self.designation = designation

        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0

        self.connect_to_database_update_other_attributes(designation)

        self.length = 0.0
        super(Angle, self).__init__(material)

    def __repr__(self):
        repr = "Angle\n"
        repr += "Designation: {}".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, designation):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT AXB, t FROM Angles WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        axb = row[0]
        axb = axb.lower()
        self.leg_a_length = float(axb.split("x")[0])
        self.leg_b_length = float(axb.split("x")[1])
        self.thickness = row[1]

        conn.close()
