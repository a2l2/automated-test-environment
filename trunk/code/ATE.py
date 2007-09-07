# This is the main ATE source file
# --------------------------------

# Import of Python libraries
import os
from os.path import join

import sys

import getopt
import string
import logging
import math
import time

class ATE:
# Class constructor
    def __init__( self ):
        self.__configMap = {}
        self.__objectMap = {}
        self.log = logging.getLogger( 'ATE' )
        self.log.debug( "ATE.__init__() method called." )

# The usage function
    def __usage( self, fileName = None ):
        self.log.debug( "ATE.__usage() method called." )
		# self.log.info( "\nUsage:\n\tpython " + fileName + " \t [--help]\n\t\t\t [--testCaseID=<test case ID>]\n" )
        self.log.info( "\nUsage:\n\tpython " + fileName + " \t [--help]\n" )

# Check status method
    def __checkStatus( self, status = None, errorMessage = None ):
        if( status != True ):
            self.log.error( errorMessage )
            sys.exit( -1 )

# This method gets called when ATE completes all operation
    def TestingComplete(self, console = None, fileName = None, logFilePath = None):
            self.log.debug("ATE.__testComplete method called." )

            # Closing the console handler
            self.log.removeHandler( console )
            console.close() 

            # Defining the destinationFileName
            destinationFileName = fileName.split( "RUNNING.log" )
            destinationFileName = destinationFileName[0] + "OPERATIONS COMPLETED.log"
            
            os.rename(os.path.join(logFilePath, fileName), os.path.join(logFilePath, destinationFileName) )
            return True

		
# The Main method
    def StartFunctions( self, argv = None, logPath = None ):
        self.log.debug( "ATE.StartFunctions() method called." )
        sanityCheck = 0


#		THIS SECTION WILL BE UNCOMMENTED WHEN COMMAND LINE SWITCHES ARE IMPLEMENTED
#		# Basic parsing of command line arguments
#		if( len( argv ) < 2 ):
#			self.__usage( argv[0] )
#			self.__checkStatus( False, "Error in arguments passed.")

#		for argument in argv:
#			if( argument[0][0] != '-' ):
#				continue
			
#	 		tempValue = argument.strip('-')
#			# Functionality if help is desired
#			if( tempValue == "help" ):
#				self.log.info( "Help on usage." )	  
#				self.__usage( argv[0] )
#				sys.exit( 0 )
			
#			if( tempValue.find( "testCaseID", 0, len( tempValue ) ) != -1 and sanityCheck == 0 ):
#				sanityCheck = 1

#		# Check to see that testCaseID has been supplied
#		if( sanityCheck != 1 ):
#			self.__usage( argv[0] )
#			self.__checkStatus(False, "Error testCaseID not specified." )


		# Check if configuration files exist 
        for path in sys.path:
            if( os.path.exists( os.path.join( path, "ate.conf" ) ) and os.path.exists( os.path.join( path, "test.conf" ) ) ):
                sanityCheck = 1
                break

        if( sanityCheck != 1 ):
            self__checkStatus( False, "Error configuration files don't exist." )


		# Starting generation of the configMap
        mapCreatorObj = MapCreator()
        self.__configMap = mapCreatorObj.Execute( argv, logPath )
        self.__objectMap = mapCreatorObj.GetObjectMap()
        return True

# Executes the specified test
    def __executeTest( self, module = None, nameInMap = None ):
        self.log.debug( "ATE.__executeTest() method called." )
		
        if( module == None or nameInMap == None):
            self.__checkStatus( False, "Test execution failed - No module or className loaded." )

        returnValue = False
        argsMap = {}

		# Removing the execution sequence numbers
        key = nameInMap
        key = key.split( ":" )
        key = key[-1]

		# Create instance of class
        self.log.debug( "Instantiating object of class - " + key + ".")
        moduleObject = getattr( module, key )()

        self.log.info( "Getting test information - Calling Info() method.")
		# Calling the Info() method
        try:
            returnValue = moduleObject.Info()
        except AttributeError, errorMessage  :
            self.__checkStatus( False, "Test execution failed - Lookup on Info() method failed - " + errorMessage )
		
        self.log.info( "Beginning test - Calling Main() method." )

		# Filling all the test specific arguments to the argument map and to the log file
        self.log.debug( "Arguments for test - " + key + ".py" )
        for elements in self.__configMap[ "testList" ][ nameInMap ].keys():
            argsMap[ elements ] = self.__configMap[ "testList" ][ nameInMap ][ elements ]

		# Filling all the generic arguments to the argument map and to the log file
        for elements in self.__configMap.keys():
            if( elements == "testList" or argsMap.__contains__( elements ) ):
                continue
            argsMap[ elements ] = self.__configMap[ elements ]
        
		# Calling the Main() method 
        try:
            returnValue = moduleObject.Main( argsMap )
        except RuntimeError, errorMessage  :
            self.__checkStatus( False, "Test execution failed - Lookup on Main() method failed - " + errorMessage )
		
        return returnValue

# Test processing starts here
    def StartTesting( self ):
        self.log.debug( "ATE.StartTesting() method called." )
        counter = 0
        testsCompleted = 0
        iterations = 0
        requiredIterations = 0
        numberPassed = 0
        numberFailed = 0

        errorMessage = ""
        for key in sorted( set( self.__configMap[ "testList" ]) ):
            requiredIterations = int( math.fabs ( string.atof(self.__configMap[ "testList" ][ key ]["iterations"] ) ) ) 
            nameInMap = key
            
            # Removing the execution sequence numbers
            key = key.split( ":" )
            key = key[-1]

	        # Import test module, if in current sys.path
            try:
                module = __import__( key )
            except ImportError, errorMessage:
                self.log.debug( key + " not present in current path scope - " + errorMessage )

                # Add testPath variable (if defined) to sys.path
                if( self.__configMap.__contains__( "testPath" ) ):
                    sys.path.append( self.__configMap[ "testPath" ] )
                else:	
                    self.__checkStatus( False, "Could not find test: " + key + " in current scope." )
				
                # Import test module, if in testPath scope
                try: 
                    module = __import__( key )
                except ImportError, errorMessage:
                    self.__checkStatus( False, "Could not import test: " + key + " - " + errorMessage )

			# Starting execution of test "requiredIterations" times
            self.log.info( "Test " + key + " will have " + `requiredIterations` + " iteration(s)." )
            for counter in range( 0, requiredIterations ):
                
                # Ensuring that each test has its own process space
                pid = os.fork()
                if( pid == 0 ):
                    # In child process
                    self.__executeTest( module, nameInMap )
                elif( pid < 0 ):
                    self__checkStatus( False, "Could not fork test process." )
                else:
                    # Parent process
                    tuple = os.wait()
                
                # if test failed
                if( tuple[-1] != 0 ):
                    self.log.log(45, "Test " + key + " - iteration count - " + `counter + 1` + " -- FAILED.\n")
                    numberFailed += 1
                # else passed
                else:
                    self.log.log(25, "Test " + key + " - iteration count - " + `counter + 1` + " -- PASSED.\n")
                    numberPassed += 1
                    
                testsCompleted += 1
                iterations += 1
                
            self.log.info( "Test " + key + " completed " + `iterations` + " iterations.\n" )
            iterations = 0

        self.log.info( "Summary:" )
        self.log.info( "--------" )
        self.log.info( "Total tests executed = " + `testsCompleted`)
        self.log.info( "Number of tests passed = "  + `numberPassed`)
        self.log.info( "Number of tests failed = " + `numberFailed` + "\n")
        
        self.log.info( "Ate completed all operations." )
        return True

# The GetConfigMap method returns the configMap
    def GetConfigMap( self ):
        self.log.debug( "ATE.GetConfigMap() method called." )			  
        return self.__configMap


# Calling the main() method
if __name__ == "__main__":
    logPath = ""
    logFilePath = ""
    
    # Modifying sys.path variable
    sys.path.append( os.getcwd() )
	
	# Add src, lib, var and etc to sys.path
    for entry in os.listdir( os.getcwd() ):
        if( os.path.isdir( entry ) == True and entry[0][0] != '.' and os.path.isfile( entry ) == False ):
            sys.path.append( os.path.join( os.getcwd(), entry ) )

	# Basic grunt work
    for path in sys.path:
		# Load all common code 
        if( os.path.exists( os.path.join( path, "common" ) ) ):
            sys.path.append( os.path.join( path, "common" ) )

        import common
        from common import *

		# Add the configuration files into path
        if( os.path.exists( os.path.join( path, "configurations" ) ) ):
            sys.path.append( os.path.join( path, "configurations" ) )

		# Add the test scripts into path
        if( os.path.exists( os.path.join( path, "tests" ) ) ):
            sys.path.append( os.path.join( path, "tests" ) )
		
		# Add the log file output directory into path
        if( os.path.exists( os.path.join(path, "var" ) ) ):
            logPath = os.path.join(path, "var" )
            logFilePath = os.path.join(path, "var" )
            
		# Add the extrenal libraries default location directory into path
        if( os.path.exists( os.path.join(path, "lib" ) ) ):
            sys.path.append( os.path.join( path, "lib" ) )
		
    # Setting up the logger
    if( logPath == "" ):
        logPath = os.getcwd()
    
    # Creating the log file for ATE
    now = time.localtime(time.time())
    tempFileName = time.strftime("%Y-%m-%d : %H-%M-%S -- ", now)
            
    tempFileName = tempFileName + "ATE.py -- RUNNING.log" 
    logPath = os.path.join( logPath, tempFileName )
    
    logging.basicConfig( level = logging.DEBUG,
							   format = '%(asctime)s - %(name)-16s - [%(levelname)s]: %(message)s',
#							   datefmt = '%Y-%m-%d %H:%M:%S',
							   filename = logPath,
                    	       filemode = 'w')

	# Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

	# Set a format which is simpler for console use
    formatter = logging.Formatter( '%(name)-36s - [%(levelname)s]\t: %(message)s' )

	# Tell the handler to use this format
    console.setFormatter(formatter)

	# Add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # Adding COMPLETED level to logging module
    logging.addLevelName( 25, "PASSED" )
    logging.addLevelName( 45, "FAILED" )

    # Begin initial setup
    ATEobj = ATE()
    ATEobj.StartFunctions( sys.argv, logFilePath )
	

    # If logging levels need to be modified	
    tempMap = ATEobj.GetConfigMap()

    for key in tempMap.keys():
        if( key.lower() == "defaultoutputlogginglevel" ):
            command = "logging." + tempMap[ key ].upper()
            console.setLevel( eval(command) )

        if( key.lower() == "defaultlogfilelogginglevel" ):
            command = "logging." + tempMap[ key ].upper()
            logging.basicConfig( level = eval(command),
							  		  	format = '%(asctime)s - %(name)-36s - [%(levelname)s]: %(message)s',
#							  		  	datefmt = '%m-%d %H:%M',
							  		  	filename = logPath,
                    	  		  	    filemode = 'w')
    
    # Start testing
    ATEobj.StartTesting()
	
    # Test complete
    ATEobj.TestingComplete(console, tempFileName, logFilePath)
    sys.exit( 0 )
