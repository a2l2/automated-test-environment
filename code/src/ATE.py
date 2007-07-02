# This is the main ATE source file
# --------------------------------

# Import of Python libraries
import os
from os.path import join

import sys
from sys import argv

import getopt
import string


# Import of all common user defined Python modules 
import common
from common import *


class ATE:
# Class constructor
	def __init__( self ):
		self.configMap = {}
		self.exceptionHandler = ExceptionHandler()


# The usage function
	def __usage( self, fileName = None ):
		print "Usage:"
		print "\tpython", fileName
		print	"\t\t [--help]\
				\n\t\t [--testCaseID=<test case ID>]\n"


# The Main method
	def StartFunctions( self, argv = None ):
		sanityCheck = 0

		# Basic parsing of command line arguments
		if( len( argv ) < 2 ):
			self.__usage( argv[0] )
			self.exceptionHandler.CheckStatus( False, "Error in arguments passed" )

		for argument in argv:
			if( argument[0][0] != '-' ):
				continue
			
	 		tempValue = argument.strip('-')
			# Functionality if help is desired
			if( tempValue == "help" ):
				print "[INFO] : Help on usage"
				self.__usage( argv[0] )
				sys.exit( 0 )
			
			if( tempValue.find( "testCaseID", 0, len( tempValue ) ) != -1 and sanityCheck == 0 ):
				sanityCheck = 1

		# Check to see that testCaseID has been supplied
		if( sanityCheck != 1 ):
			self.__usage( argv[0] )
			self.exceptionHandler.CheckStatus( False, "Error testCaseID not specified" )
			sanityCheck = 0

		# Check if configuration files exist 
		for path in sys.path:
			if( os.path.exists( os.path.join( path, "ate.conf" ) ) and os.path.exists( os.path.join( path, "test.conf" ) ) ):
				sanityCheck = 1
				break

		if( sanityCheck != 1 ):
			self.exceptionHandler.CheckStatus( False, "Error configuration files don't exist" )

		# Create the map
		mapCreatorObj = MapCreator( )
		self.configMap = mapCreatorObj.Execute( argv )

		return True


# Executes the specified test
	def __executeTest( self, module = None ):
		if( module == None ):
			self.exceptionHandler.CheckStatus( False, "Test execution failed - No module loaded." )
		
		try:
			print "[INFO] :", module.Info()
		except:
			self.exceptionHandler.CheckStatus( False, "Test execution failed - Info() method not defined." )
		
		print "[INFO] : Beginning test - Calling Main() method.\n"

		status = module.Main()
		self.exceptionHandler.CheckStatus( status, "Test execution failed - Main() returned unsuccessfully." )
		

# Test processing starts here
	def StartTesting( self ):
		counter = 0
		testsCompleted = 0

		for key in self.configMap[ "testList" ]:
			# Import test module, if in current sys.path
			try:
				module = __import__(  key, globals(), locals(), [], -1 )
			except:
				# Add testPath variable (if defined) to sys.path
				if( self.configMap.__contains__( "testPath" ) ):
					sys.path.append( self.configMap[ "testPath" ] )
				else:	
					self.exceptionHandler.CheckStatus( False, "Could not find test: " + key + " in current scope." )
				
				# Import test module, if in testPath scope
				try: 
					module = __import__( key, globals(), locals(), [], -1 )
				except:
					self.exceptionHandler.CheckStatus( False, "Could not find test: " + key + " in current / testPath scope." )

			print "[INFO] : Test", key, "will have", self.configMap[ "testList" ][ key], "iterations"
			for counter in range( 0, self.configMap[ "testList" ][ key] ):
				self.__executeTest( module )
				print "[INFO] : Iteration count -", counter+1, "completed successfully."
			testsCompleted += 1

			print "[INFO] : Test", key, "completed successfully.\n"

	 	print "[INFO] : Summary -", testsCompleted, "test(s) completed successfully."
		return True


# Calling the main() method
if __name__ == "__main__":
	sys.path.append( os.path.join( os.getcwd(), "configurations" ) )
	sys.path.append( os.getcwd() )
	sys.path.append( "..\\lib\\" )
	ATEobj = ATE()
	ATEobj.StartFunctions( sys.argv )
	
	ATEobj.StartTesting()
	
	sys.exit( 0 )

