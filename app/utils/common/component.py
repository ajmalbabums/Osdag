from app.utils.common.material import Material
from app.utils.common.is800_2007 import IS800_2007
import sqlite3


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
