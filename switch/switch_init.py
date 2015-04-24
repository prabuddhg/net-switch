import os
import yaml
import imp
import interface.net_interface

moduleNames = ['interface']
dir = os.path.dirname(__file__)

class Switch_Init():
    def __init__(self, spec=None):
        print "Start switch initialization"
        self.spec = spec

    def read_specification(self):
        print "Reading specification..."
        # hardcoded the spec
        # /Users/prabuddh/Desktop/mountCode/net-switch/
        spec_yaml =\
            os.path.join(dir, '../specification/spec.yaml')
        stream = open(spec_yaml, 'r')
        spec_dict = yaml.load(stream)
        for module in moduleNames:
            for sub_spec in spec_dict[module]:
                self.parse_specification(module, sub_spec)

    def parse_specification(self, module=None, spec=None):
        print "Parsing specification for %s" %(spec['name'])
        module_yaml =\
            os.path.join(dir, '../module_information/switch_modules.yaml')
        stream = open(module_yaml, 'r')
        module_dict = yaml.load(stream)
        # hardcoded switch module
        class_type = spec['type']
        module_file = (module + "." +
                      module_dict[module][class_type]['module'])
        class_name = module_dict[module][class_type]['name']
        self.acquire_resources(module_file, class_name, spec)

    def acquire_resources(self, module_file = None, class_name = None, spec = None):
        print ("Acquiring resources using module_file: %s and class_name: %s"
               %(module_file, class_name))
        print module_file
        as_class = self.get_class(module_file)
        # Make this dynamic
        module_object = as_class.NetInterface(spec['name'], spec['mac'],spec['state'])
        print module_object

    def get_class(self, kls = None):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
            return m

    def store_objects(self):
        print "Storing object..."
