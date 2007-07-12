# This is the main ATE source file
# --------------------------------

# Import of Python libraries
import os
from os.path import join

import sys
from sys import argv

import getopt
import string
import logging


class ATE:
# Class constructor
	def __init__( self ):
		self.configMap = {}
		self.log = logging.getLogger( 'ATE' )
		self.log.debug( "ATE.__init__() method called." )


# The usage function
	def __usage( self, fileName = None ):
		self.log.debug( "ATE.__usage() method called." )
		self.log.info( "\nUsage:\n\tpython " + fileName + " \t [--help]\n\t\t\t [--testCaseID=<test case ID>]\n" )


# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )
		
# The Main method
	def StartFunctions( self, argv = None ):
		self.log.debug( "ATE.StartFunctions() method called." )
		sanityCheck = 0

		# Basic parsing of command line arguments
		if( len( argv ) < 2 ):
			self.__usage( argv[0] )
			self.__checkStatus( False, "Error in arguments passed.")

		for argument in argv:
			if( argument[0][0] != '-' ):
				continue
			
	 		tempValue = argument.strip('-')
			# Functionality if help is desired
			if( tempValue == "help" ):
				self.log.info( "Help on usage." )	  
				self.__usage( argv[0] )
				sys.exit( 0 )
			
			if( tempValue.find( "testCaseID", 0, len( tempValue ) ) != -1 and sanityCheck == 0 ):
				sanityCheck = 1

		# Check to see that testCaseID has been supplied
		if( sanityCheck != 1 ):
			self.__usage( argv[0] )
			self.__checkStatus(False, "Error testCaseID not specified." )

		# Check if configuration files exist 
		for path in sys.path:
			if( os.path.exists( os.path.join( path, "ate.conf" ) ) and os.path.exists( os.path.join( path, "test.conf" ) ) ):
				sanityCheck = 1
				break

		if( sanityCheck != 1 ):
			self__checkStatus( False, "Error configuration files don't exist." )


		# Starting generation of the configMap
		mapCreatorObj = MapCreator( )
		self.configMap = mapCreatorObj.Execute( argv )

		return True


# Executes the specified test
	def __executeTest( self, module = None ):
		self.log.debug( "ATE.__executeTest() method called." )
		if( module == None ):
			self.__checkStatus( False, "Test execution failed - No module loaded." )
		
		try:
			self.log.info( module.Info() )
		except:
			self.__checkStatus( False, "Test execution failed - Info() method not defined." )
		
		self.log.info( "Beginning test - Calling Main() method.\n" )

		self.__checkStatus( module.Main(), "Test execution failed - Main() returned unsuccessfully." )
		

# Test processing starts here
	def StartTesting( self ):
		self.log.debug( "ATE.StartTesting() method called." )
		counter = 0
		testsCompleted = 0
		iterations = 0

		for key in self.configMap[ "testList" ]:
			# Import test module, if in current sys.path
			try:
				module = __import__(  key )
			except:
				# Add testPath variable (if defined) to sys.path
				if( self.configMap.__contains__( "testPath" ) ):
					sys.path.append( self.configMap[ "testPath" ] )
				else:	
					self.__checkStatus( False, "Could not find test: " + key + " in current scope." )
				
				# Import test module, if in testPath scope
				try: 
					module = __import__( key )
				except:
					self.__checkStatus( False, "Could not find test: " + key + " in current / testPath scope." )

			self.log.info( "Test " + key + " will have " + `self.configMap[ "testList" ][ key]` + " iterations." )
			for counter in range( 0, self.configMap[ "testList" ][ key] ):
				self.__executeTest( module )
				self.log.info( "Iteration count - " + `counter + 1` + " completed successfully.\n" )
				testsCompleted += 1
				iterations += 1

			self.log.info( "Test " + key + " completed " + `iterations` + " iterations successfully.\n" )
			iterations = 0

	 	self.log.info( "Summary - " + `testsCompleted` + " test(s) completed successfully." )
		return True


# The GetConfigMap method returns the configMap
	def GetConfigMap( self ):
		self.log.debug( "ATE.GetConfigMap() method called." )			  
		return self.configMap


# Calling the main() method
if __name__ == "__main__":
	logPath = None

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
		

# Setting up the logger
	if( logPath == None ):
		logPath = os.getcwd()
	
	logPath = os.path.join( logPath, "output.log" )
	logging.basicConfig( level = logging.DEBUG,
							   format = '%(asctime)s - %(name)-36s - [%(levelname)s]: %(message)s',
							   datefmt = '%m-%d %H:%M',
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


# Begin initial setup
	ATEobj = ATE()
	ATEobj.StartFunctions( sys.argv )
	

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
							  		  	datefmt = '%m-%d %H:%M',
							  		  	filename = logPath,
                    	  		  	filemode = 'w')


	# Start testing
	ATEobj.StartTesting()
	
	sys.exit( 0 )
