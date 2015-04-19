

class NetInterface():
    def __init__(self, name=None, mac=None, state=None):
        self.name = name
        self.mac = mac
        self.state = state

    def create(self):
        print "Resource acquisition is initialization"

    def read(self):
        print "Reading interface %s" %(self.name)
        return self

    def update(self, attribue=None, value=None):
        print "Updating interface %s with" %(self.name)
        print " for attribute %s with value %" %(attribue, value)
        self.attribute = value

    def delete(self):
        print "Deleting interface %s under construction" %(self.name)
        '''http://stackoverflow.com/questions/6772481/how-can-one-force-deletion-of-an-object-in-python'''