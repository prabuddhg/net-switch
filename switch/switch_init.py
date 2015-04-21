

class Switch_Init():
    def __init__(self, spec=None):
        print "Start switch initialization"
        self.spec = spec

    def read_specification(self):
        print "Reading specification..."
    def parse_specification(self):
        print "Parsing specification..."
    def acquire_resources(self):
        print "Acquiring resources..."
    def store_objects(self):
        print "Storing object..."

def main():
    #switch init process
    switch_init = Switch_Init()
    switch_init.read_specification()
    switch_init.parse_specification()
    switch_init.acquire_resources()
    switch_init.store_objects()

#main()
