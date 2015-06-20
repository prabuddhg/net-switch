import os
import yaml
import imp
import interface.net_interface
from kazoo.client import KazooClient
from kazoo.client import KazooState
import json
import logging
#logger = logging.getLogger(__name__)

#zk = KazooClient(hosts='127.0.0.1:5001')
#zk = KazooClient(hosts='127.0.0.1:5001', read_only=True)
#zk.stop()
#zk.start()


#logging.basicConfig()
from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
_retry = KazooRetry(max_tries=1000, delay=0.5, backoff=2)
zk = KazooClient(hosts="127.0.0.1:2181", logger=logging, read_only=True, timeout=30, connection_retry=_retry)
zk.start()

def my_listener(state):
    if (state == KazooState.LOST):
        print "Register somewhere that the session was lost"
    elif (state == KazooState.SUSPENDED):
        print "Handle being disconnected from Zookeeper"
    else:
        print "Handle being connected/reconnected to Zookeeper"

moduleNames = ['interface']
dir = os.path.dirname(__file__)

class Switch_Init():
    def __init__(self, spec=None):
        logging.info("Start switch initialization")
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
        zk.stop()
        #zk.add_listener(my_listener)

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
        self.acquire_resources(module, module_file, class_name, spec)

    def acquire_resources(self, module=None, module_file=None, class_name=None, spec =None):
        print ("Acquiring resources using module_file: %s and class_name: %s"
               %(module_file, class_name))
        #print module_file
        as_class = self.get_class(module_file)
        # Make this dynamic
        module_object = as_class.NetInterface(spec['name'], spec['mac'],spec['state'])
        #print module_object
        self.store_objects(module, spec['name'], module_object)

    def get_class(self, kls=None):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
            return m

    def store_objects(self, module=None, name=None, object=None):
        print "Storing object..."
        path = "/net-switch/%s/%s" %(module,name)
        zk.ensure_path(path)
        if zk.exists(path):
             print "path exists: %s" %(path)
        print "Store object at %s" %(path)
        #zk.create(path, object)
        byte_string = json.dumps(object.__dict__)
        #zk.set(path, object.__dict__)
        zk.set(path, byte_string)
        data, stat = zk.get(path)
        #zoo_data = pickle.loads(data)
        print "Data from zookeeper"
        print json.loads(data)
