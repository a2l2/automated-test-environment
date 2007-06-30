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

		for key in self.configMap.keys():
			print key, ":", self.configMap[ key ]

		return True


# Calling the main() method
if __name__ == "__main__":
	sys.path.append( os.path.join( os.getcwd(), "configurations" ) )
	sys.path.append( "..\\lib\\" )
	ATEobj = ATE()
	ATEobj.StartFunctions( sys.argv )
	sys.exit( 0 )

