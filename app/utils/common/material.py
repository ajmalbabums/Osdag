class Material(object):

    def __init__(self, fyb=0.0, fub=0.0,fu=0):
        self.fyb = fyb
        self.fub = fub
        self.fu = fu

    def __repr__(self):
        repr = "Material:\n"
        repr += "fy: {}\n".format(self.fy)
        repr += "fu: {}".format(self.fu)
        return repr
