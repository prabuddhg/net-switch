import os
import yaml

class Switch_Init():
    def __init__(self, spec=None):
        print "Start switch initialization"
        self.spec = spec

    def read_specification(self):
        print "Reading specification..."
        dir = os.path.dirname(__file__)
        # hardcoded the spec
        filename =\
            os.path.join(dir, '../specification/spec.yaml')
        stream = open(filename, 'r')
        print yaml.load(stream)
    def parse_specification(self):
        print "Parsing specification..."
    def acquire_resources(self):
        print "Acquiring resources..."
    def store_objects(self):
        print "Storing object..."
