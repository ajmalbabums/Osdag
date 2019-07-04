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
    
    def __init__(self, bolt, no_rows, no_columns, gauge=0.0, pitch=0.0, end=0.0, edge=0.0, material=Material()):
        self.bolt = bolt
        self.no_rows = no_rows
        self.no_columns = no_columns
        self.no_of_bolts = no_rows * no_columns
        self.group_capacity = self.no_of_bolts * self.bolt.bolt_capacity
        self.gauge = gauge
        self.pitch = pitch
        self.end = end
        self.edge = edge
        super(Bolt_Group, self).__init__(material)

    def __repr__(self):
        repr = "Bolt Group\n"
        repr += "no_of_bolts: {}\n".format(self.no_of_bolts)
        repr += "group_capacity {}\n".format(self.group_capacity)
        repr += "gauge {}\n".format(self.gauge)
        repr += "pitch {}\n".format(self.pitch)
        repr += "end {}\n".format(self.end)
        repr += "edge {}\n".format(self.edge)
        return repr
    
    def no_of_bolts_check(self, v_d, v_bolt):
        if self.no_of_bolts > v_d / v_bolt :
            return True
        if self.no_of_bolts > v_d / v_bolt :
            return False

    def min_pitch_check(self):
        if self.pitch >= IS800_2007.cl_10_2_2_min_spacing(self.pitch):
            return True
        else:
            return False

    def min_gauge_check(self):
        if self.gauge >= IS800_2007.cl_10_2_2_min_spacing(self.gauge):
            return True
        else:
            return False

    def max_pitch_check(self, plate):
        if self.pitch <= IS800_2007.cl_10_2_3_1_max_spacing(plate.thickness)
            return True
        else:
            return False


    def max_gauge_check(self, plate):
        if self.gauge <= IS800_2007.cl_10_2_3_1_max_spacing(plate.thickness)
            return True
        else:
            return False


    def max_pitch_check_2(self, plate, compression_or_tension):
        if self.pitch <= IS800_2007.cl_10_2_3_2_max_pitch_tension_compression(self.pitch, plate.thickness, compression_or_tension)
            return True
        else:
            return False

    def min_end_check(self, bolt_hole_type, edge_type):
        if self.end >= IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.end, bolt_hole_type, edge_type):
            return True
        else:
            return False

    def min_edge_check(self,bolt_hole_type, edge_type):
        if self.edge >= IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.end, bolt_hole_type, edge_type):
            return True
        else:
            return False

    def max_end_check(self, plate, f_y, corrosive_influences):
        if self.end <= IS800_2007.cl_10_2_4_3_max_edge_dist(plate.thickness, f_y, corrosive_influences):
            return True
        else:
            return False

    def max_edge_check(self, plate, f_y, corrosive_influences):
        if self.edge <= IS800_2007.cl_10_2_4_3_max_edge_dist(plate.thickness, f_y, corrosive_influences):
            return True
        else:
            return False


    def check_for_long_joints(self):
        l_j = (self.no_rows - 1) * self.pitch
        beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.diameter, l_j)
        return beta_lj
        
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

    def __init__(self, thickness, height, width, plate_type,material=Material()):
        self.thickness = thickness
        self.height = height
        self.width = width
        self.plate_type = plate_type
        super(Plate, self).__init__(material)

    def __repr__(self):
        repr = "Plate\n"
        repr += "Thickness: {}".format(self.thickness)
        repr += "Height: {}".format(self.height)
        repr += "Width: {}".format(self.width)
        repr += "Type: {}".format(self.plate_type)
        return repr

    def calculate_minimum_plate_height(self,depth_of_beam):
        """
        Reference: Handbook
        on
        Structural
        Steel
        Detailing, INSDAG - Chapter
        5, Section
        5.2.3, Page 5.7
        """
        return 0.6 * depth_of_beam

    def calculate_maximum_plate_height(self,db,tbf,rb1,gap,notch_height,Db,Tbf,Rb1,connectivity):
        """
        Args:
            db - Depth of supported beam
            tbf - Thickness of supported beam flange
            rb1 - Root radius of supported beam flange
            gap - Clearance between fin plate and supported beam flange
            notch_height - max(Tbf, tbf) + max(Rb1, rb1) + max(Tbf / 2, tbf / 2, 10)
            Db - Depth of supporting beam
            Tbf - Thickness of supporting beam flange
            Rb1 - Root radius of supporting beam flange
            connectivity - 'beam-column','beam-beam with single notch' or 'beam-beam with double notch'
        Returns:
            max_plate_height
        """
        notch_height = max(Tbf, tbf) + max(Rb1, rb1) + max(Tbf / 2, tbf / 2, 10)
        if connectivity == 'beam-column':
            max_plate_height = db − 2*(tbf + rb1 + gap)
        if connectivity == 'beam-beam with single notch':
            max_plate_height = db−tbf+rb1−notch_height
        if connectivity == 'beam-beam with double notch':
            max_plate_height = min(Db, db) − 2 ∗ notch_height
        return max_plate_height

    def calculate_minimum_plate_width(self,bf):
        return bf
    def calculate_max_plate_width(self,bf):
        return bf + 25
    def calculate_minimum_plate_thickness(self,F,fy,hp,tw):
        """
        Args:
            F - factored shear force
            fy - yield stress
            hp - height of plate
            tw - thickness of secondary beam web
        Note:
            [Reference: N. Subramanian’s Design of Steel Structures - Chapter 5, Sec. 5.7.7 - Page 373]
        """
        return max(tw, 5*F/(fy*hp))
    def calculate_max_plate_thickness(self,bolt_diameter):
        """
        Args:
            bolt_diameter
        Returns:
            tp - maximum plate thickness
        Note:
            [Reference: Handbook on Structural Steel Detailing, INSDAG - Chapter 5, Section 5.2.3, Page 5.7]
        """
        return 0.5 * bolt_diameter
    def moment_capacity_check(Mdb,F,d_bw,f_y,Z):
        #TODO
        pass
    def calculate_block_shear():
        #TODO
        pass
    def shear_yielding_check():
        pass

    def shear_rupture_check():
        pass

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
