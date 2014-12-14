#!/usr/bin/env python

# Import Section
import os                   # Base package
import sys                  # Low level system IO
import BaseHTTPServer       # Implements a simple web server
import CGIHTTPServer        # Used to run CGI scripts
import commands             # Used for running commands in terminal

# Global Variables
gPort   = 4294              # Port at which HTTP Server listens.

#===============================================================================
# Class         : CCGIRequestHandler
# Description   : Empty HTTP CGI Server class
#===============================================================================
class CCGIRequestHandler( CGIHTTPServer.CGIHTTPRequestHandler ):
    pass

#===============================================================================
# Class         : NullDevice
# Description   : Simulates a NULL device - /dev/null
#===============================================================================
class NullDevice:
    def write( self, aData ):
        pass

#===============================================================================
# Subroutine    : StartServer
# Arguments     : -NA-
# Return        : -NA-
# Description   : This subroutine starts the HTTP Server.
#===============================================================================
def StartServer():
    '''    if os.fork():
        sys.stderr.flush()
        sys.stdout.flush()    
        os._exit( 0 )

    # Create session leader
    os.setsid()
    os.umask( 0 )
    sys.stdin.close()
    sys.stdout = NullDevice()
    sys.stderr = NullDevice()
    if os.fork():
        sys.exit( 0 )
    '''    
    serverAddress   = ( '', gPort )
    httpServer      = BaseHTTPServer.HTTPServer( serverAddress, CCGIRequestHandler )
    ret, hostName   = commands.getstatusoutput( 'hostname' )
    pid             = os.getpid() 

    #print '[I] Server Succesfully Started. Serving at port : ', gPort, ' from ', hostName
    #print '[I] Access url : http://' + hostName + '.ca1.paypal.com:' + str( gPort )
    #print '[I] Server PID :', pid
    httpServer.serve_forever()

#===============================================================================
# Subroutine    : main
# Arguments     : -NA-
# Return        : -NA-
# Description   : Main Entry Ponit
#===============================================================================
if __name__ == '__main__':
    ret, out = commands.getstatusoutput( 'hostname' )
    StartServer()
else:
    print '[E] This script is not intended for importing\n';
