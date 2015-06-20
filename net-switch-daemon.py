#!/usr/bin/env python

"""Server start

This is a template for a Python-based server daemon derived from
SocketServer.  Hack it up as needed.

This script implements both the server daemon and a command-line
client that can issue requests against it.  The template client-server
protocol is very simple: the client simply sends the command-line
arguments to the server, and the server returns output which the
client writes to its standard output.  Change the protocol as needed
for your purposes.

The template contains a few UNIXisms.  Modification may be needed for
a Windows-based server.

References:
- Source for ServerSocket.py (standard Python module)
- Source for BaseHTTPServer.py (standard Python module)
- http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731

"""

version = '1.0'

usage = """usage: %prog [options] command [arg...]

commands:
  interfaces     interface commands

Example session:
  %prog start           # starts daemon
  %prog status          # print daemon's status
  %prog interfaces       # show all interfaces
  %prog stop            # stops daemon"""


import SocketServer
import optparse
import os
import os.path
import resource
import socket
import sys
import tempfile
import time
import switch.switch_init as switch_init
import logging

#logging.debug('So should this')
#logging.warning('And this, too')

# We can use either a TCPServer or a UnixStreamServer (assuming the OS
# supports UNIX domain sockets).  We just need to define the
# appropriate ServerBase class and then customize a few things based
# upon which base we're using.

#ServerBase = SocketServer.TCPServer
ServerBase = SocketServer.UnixStreamServer
if ServerBase == SocketServer.TCPServer:
    # TODO: replace with appropriate port number
    server_address = ('', 54444)
elif ServerBase == SocketServer.UnixStreamServer:
    # TODO: replace with appropriate socket file path
    server_address = os.path.join(tempfile.gettempdir(), 'server_socket')

# Path to log file
# TODO: Change to appropriate path and name
server_log = os.path.join(tempfile.gettempdir(), 'server.log')


class RequestHandler(SocketServer.StreamRequestHandler):

    """Request handler

    An instance of this class is created for each connection made
    by a client.  The Server class invokes the instance's
    setup(), handle(), and finish() methods.

    The template implementation here simply reads a single line from
    the client, breaks that up into whitespace-delimited words, and
    then uses the first word as the name of a "command."  If there is
    a method called "do_COMMAND", where COMMAND matches the
    commmand name, then that method is invoked.  Otherwise, an error
    message is returned to the client.

    """

    def handle(self):
        """Service a newly connected client.

        The socket can be accessed as 'self.connection'.  'self.rfile'
        can be used to read from the socket using a file interface,
        and 'self.wfile' can be used to write to the socket using a
        file interface.

        When this method returns, the connection will be closed.
        """
        
        # Read a single request from the input stream and process it.
        # TODO: Change as needed for actual client-server protocol.
        request = self.rfile.readline()
        if request:
            self.server.log('request %s: %s',
                            self.connection.getpeername(), request.rstrip())
            try:
                self.process_request(request)
            except Exception, e:
                self.server.log('exception: %s' % str(e))
                self.wfile.write('Error: %s\n' % str(e))
        else:
            self.server.log('error: unable to read request')
            self.wfile.write('Error: unable to read request')


    def process_request(self, request):
        """Process a request.

        This method is called by self.handle() for each request it
        reads from the input stream.

        This implementation simply breaks the request string into
        words, and searches for a method named 'do_COMMAND',
        where COMMAND is the first word.  If found, that method is
        invoked and remaining words are passed as arguments.
        Otherwise, an error is returned to the client.
        """

        words = request.split()
        if len(words) == 0:
            self.server.log('error: empty request')
            self.wfile.write('Error: empty request\n')
            return

        command = words[0]
        args = words[1:]

        methodname = 'do_' + command
        if not hasattr(self, methodname):
            self.server.log('error: invalid command')
            self.wfile.write('Error: "%s" is not a valid command\n' % command)
            return
        method = getattr(self, methodname)
        method(*args)


    def do_stop(self, *args):
        """Process a 'stop' command"""
        self.wfile.write('Stopping server\n')
        self.server.stop()


    def do_echo(self, *args):
        """Process an 'echo' command"""
        self.wfile.write(' '.join(args) + '\n')


    def do_status(self, *args):
        """Process a 'status' command"""
        self.wfile.write('Server Version:    %s\n' % version)
        self.wfile.write('Process ID:        %d\n' % os.getpid())
        self.wfile.write('Parent Process ID: %d\n' % os.getppid())
        self.wfile.write('Server Socket:     %s\n' % str(server_address))
        self.wfile.write('Server Log:        %s\n' % server_log)


    def do_interfaces(self, *args):
        """Process an 'add' command"""
        interface_usage = """
    name     mac address
    if01     00:00:00:00:00:01
    if02     00:00:00:00:00:02
    if03     00:00:00:00:00:03
    if04     00:00:00:00:00:04"""
        self.wfile.write('\n %s \n\n' % (interface_usage))


class Server(ServerBase):

    """Server implementation

    """

    def __init__(self, server_address):
        """Constructor"""
        self.__daemonize()

        if ServerBase == SocketServer.UnixStreamServer:
            # Delete the socket file if it already exists
            if os.access(server_address, 0):
                os.remove(server_address)

        ServerBase.__init__(self, server_address, RequestHandler)


    def log(self, format, *args):
        """Write a message to the server log file"""
        try:
            message = format % args
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print "track log activities at %s" %(server_log)
            f = open(server_log, 'a+')
            f.write('%s %s\n' % (timestamp, message))
            f.close()
        except Exception, e:
            print str(e)


    def serve_until_stopped(self):
        """Serve requests until self.stop() is called.

        This is an alternative to BaseServer.serve_forever()
        """

        self.log('started')
        self.__stopped = False
        while not self.__stopped:
            self.handle_request()
        self.log('stopped')


    def stop(self):
        """Stop handling requests.

        Calling this causes the server to drop out of
        serve_until_stopped().
        """

        self.__stopped = True


    def __daemonize(self):
        """Create daemon process.

        Based upon recipe provided at
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731
        """

        UMASK = 0
        WORKDIR = '/'
        MAXFD = 1024
        if hasattr(os, 'devnull'):
            REDIRECT_TO = os.devnull
        else:
            REDIRECT_TO = '/dev/null'

        try :
            if os.fork() != 0:
                os._exit(0)

            os.setsid()

            if os.fork() != 0:
                os._exit(0)

            os.chdir(WORKDIR)
            os.umask(UMASK)
        except OSError, e:
            self.log('exception: %s %s', e.strerror, e.errno)
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
        except Exception, e:
            self.log('exception: %s', str(e))
        
        maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if maxfd == resource.RLIM_INFINITY:
            maxfd = MAXFD
        for fd in range(0, maxfd):
            try:
                os.close(fd)
            except OSError:
                pass

        os.open(REDIRECT_TO, os.O_RDWR)
        os.dup2(0, 1)
        os.dup2(0, 2)


def run_server(options, args):
    """Run a server daemon in the current process."""
    """http://stackoverflow.com/questions/17592394/how-to-make-a-python-file-run-without-py-extension"""
    print 'Server Log:        %s' % server_log
    init = switch_init.Switch_Init()
    init.read_specification()
    svr = Server(server_address)
    svr.serve_until_stopped()
    svr.server_close()


def do_request(options, args):
    """Send request to the server and process response."""
    if ServerBase == SocketServer.UnixStreamServer:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    elif ServerBase == SocketServer.TCPServer:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Send request
    # TODO: Change as needed for actual client-server protocol
    s.connect(server_address)
    s.sendall(' '.join(args) + '\n')

    # Print response
    # TODO: Change as needed for actual client-server protocol
    sfile = s.makefile('rb')
    line = sfile.readline()
    while line:
        print line,
        line = sfile.readline()


#
# MAIN
#
if __name__ == '__main__':
    optparser = optparse.OptionParser(usage=usage,
                                      version=version)
    (options, args) = optparser.parse_args()
    print __name__
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('/tmp/net-switch/run.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    #logging.basicConfig(filename='/tmp/net-switch/run.log', filemode='w', level=logging.DEBUG)
    #logger = logging.getLogger('server_logger')
    logger.info('Log file created')
    if len(args) == 0:
        optparser.print_help()
        sys.exit(-1)
 
    if args[0] == 'start':
        run_server(options, args[1:])
    else:
        do_request(options, args)