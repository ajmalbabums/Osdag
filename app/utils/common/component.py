from app.utils.common.material import Material
from app.utils.common.is800_2007 import IS800_2007
import sqlite3
from is800_2007 import IS800_2007

class Component(object):

    def __init__(self, material=Material()):
        self.material = material
        self.path_to_database = "../../databases/Intg_osdag.sqlite"


class Bolt(Component):

    def __init__(self, grade=0.0, diameter=0.0,thread_area=0, bolt_type="", length=0.0, material=Material()):
        self.grade = grade
        self.diameter = diameter
        self.shank_area = 3.14*0.25*diameter**2
        self.thread_area= thread_area
        self.bolt_type = bolt_type
        self.length = length
    #   bearing bolt
        self.shear_capacity = 0.0
        self.bearing_capacity = 0.0
        self.bolt_capacity = 0.0
    #   friction bolt
        self.is_friction_grip = True
        self.slip_resistance = 0
    #   both
        self.shear_in_bolt = 0
        self.tension_in_bolt = 0
        self.tension_capacity = 0
        self.combined_capacity_check = "safe"

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
        
        
    def calculate_thread_area(self):
        self.thread_area = 0.78*self.shank_area
    # todo thread_area database
    """Friction bolt"""
    def calculate_slip_resistance(self, n_e ,mu_f):
        self.slip_resistance = IS800_2007.cl_10_4_3_bolt_slip_resistance(self.material.fub, self.shank_area, n_e, mu_f)

    # n_e and m_uf are plate attributes
    """bearing bolt """
    def calculate_bolt_shear_capacity(self):
        self.shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(self.material.fub, self.shank_area, self.thread_area)

    def calculate_bolt_bearing_capacity(self,t,e,p):
        self.bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(self.material.fu, self.material.fub, t, self.diameter, e, p)
    # use t , e , p from bolt group class

    def calculate_bolt_capacity(self):
        if self.is_friction_grip is False:
            self.bolt_capacity = min(self.bearing_capacity, self.shear_capacity)
    """same for both"""
    def calculate_tension_capacity(self, An):

        self.tension_capacity = min(0.9*self.material.fub*An, self.material.fyb*self.shank_area*1.25/1.1 )

    def calculate_combined_capacity(self, shear_capacity_of_friction_bolt):
        if self.is_friction_grip is False:
            if ((self.shear_in_bolt/1.25)/self.shear_capacity)**2 + ((self.tension_in_bolt/1.25)/self.tension_capacity)**2 <= 1:
                self.combined_capacity_check = "safe"
            else:
                self.combined_capacity_check = "unsafe"
        elif self.is_friction_grip is True:
            if ((self.shear_in_bolt/1.25)/shear_capacity_of_friction_bolt)**2 + ((self.tension_in_bolt/1.25)/self.tension_capacity)**2 <= 1:
                self.combined_capacity_check = "safe"
            else:
                self.combined_capacity_check = "unsafe"




class BoltGroup(Component):
    
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
        super(BoltGroup, self).__init__(material)
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
        self.Ix = 0.0
        self.Iy = 0.0
        self.cx = 0.0
        self.cy = 0.0


        super(Section, self).__init__(material)

    def __repr__(self):
        repr = "Section\n"
        repr += "Designation: {}".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, table, designation):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT D, B, tw, T, R1, R2 ,Iz ,Iy FROM " + table + " WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        self.depth = row[0]
        self.flange_width = row[1]
        self.web_thickness = row[2]
        self.flange_thickness = row[3]
        self.root_radius = row[4]
        self.toe_radius = row[5]
        self.Ix = row[6]
        self.Iy = row[7]


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

    def __init__(self, type, size=0.0, length=0.0, eff_length = 0.0, material=Material()):
        self.type = type
        self.size = size
        self.length = length
        self.throat_size = size * 0.7
        self.eff_length = None
        self.shear_strength = None
        super(Weld, self).__init__(material)

    def __repr__(self):
        repr = "Weld\n"
        repr += "Type: {}\n".format(self.type)
        repr += "Size: {}\n".format(self.size)
        repr += "Length: {}".format(self.length)
        repr += "Throat_size: {}".format(self.throat_size)
        repr += "Eff_length: {}".format(self.eff_length)
        repr += "Shear_strength: {}".format(self.shear_strength)
        return repr

    def calculate_eff_length(self,available_length):
        self.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(self.size, available_length)
        return self.eff_length

    def calculate_shear_strength(self,ultimate_stresses,fabrication):
        self.shear_strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(ultimate_stresses, fabrication)
        return self.shear_strength

    def check_for_long_joints():
        #TODO:functions for cl_10_5_4_4 and cl_10_5_7_3
        pass

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

    def min_height_check(self,depth_of_beam):
        """
        Reference: Handbook
        on
        Structural
        Steel
        Detailing, INSDAG - Chapter
        5, Section
        5.2.3, Page 5.7
        """
        if self.height >= 0.6 * depth_of_beam
            return True
        else:
            return False

    def max_plate_height_check(self,db,tbf,rb1,gap,notch_height,Db,Tbf,Rb1,connectivity):
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
            True if plate height >= max_plate_height else False
        """
        notch_height = max(Tbf, tbf) + max(Rb1, rb1) + max(Tbf / 2, tbf / 2, 10)
        if connectivity == 'beam-column':
            max_plate_height = db - 2*(tbf + rb1 + gap)
        if connectivity == 'beam-beam with single notch':
            max_plate_height = db-tbf+rb1 - notch_height
        if connectivity == 'beam-beam with double notch':
            max_plate_height = min(Db, db) - 2 * notch_height
        if self.height <= max_plate_height:
            return True
        else:
            return False

    def min_plate_width_check(self,bf):
        if self.width >= bf:
            return True
        else:
            return False

    def max_plate_width_check(self,bf):
        if self.height <= bf + 25:
            return True
        else:
            return False
    def min_thickness_check(self,F,fy,hp,tw):
        """
        Args:
            F - factored shear force
            fy - yield stress
            hp - height of plate
            tw - thickness of secondary beam web
        Note:
            [Reference: N. Subramanian’s Design of Steel Structures - Chapter 5, Sec. 5.7.7 - Page 373]
        """
        if self.thickness >= max(tw, 5*F/(fy*hp)):
            return True
        else:
            return False
    def max_thickness_check(self,bolt_diameter):
        """
        Args:
            bolt_diameter
        Returns:
            tp - maximum plate thickness
        Note:
            [Reference: Handbook on Structural Steel Detailing, INSDAG - Chapter 5, Section 5.2.3, Page 5.7]
        """
        if self.thickness <= 0.5 * bolt_diameter:
            return True
        else:
            return False

class Angle(Component):

    def __init__(self, designation, material=Material()):
        self.designation = designation

        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0
        self.Iz = 0.0
        self.Iy = 0.0
        self.cz = 0
        self.cy = 0
        self.root_radius = 0.0
        self.toe_radius = 0.0


        self.connect_to_database_update_other_attributes(designation)

        self.length = 0.0
        super(Angle, self).__init__(material)

    def __repr__(self):
        repr = "Angle\n"
        repr += "Designation: {}".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, designation):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT AXB, t, R1, R2, Iz, Iy, cz, cy FROM Angles WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        axb = row[0]
        axb = axb.lower()
        self.leg_a_length = float(axb.split("x")[0])
        self.leg_b_length = float(axb.split("x")[1])
        self.thickness = row[1]
        self.root_radius = row[2]
        self.toe_radius = row[3]
        self.cz = row[4]
        self.cy = row[5]
        self.Iz = row[6]
        self.Iy = row[7]


        conn.close()
