# This class creates the Configuration Map
#-----------------------------------------

# Import of user defined Python modules 
import sys
import os

# Import of all common user defined Python modules 
import common
from common import *

class MapCreator:
# Class constructor
	def __init__( self ):
		self.configMap = {}
		self.exceptionHandler = ExceptionHandler()


# Locates the path to the configuration file
	def __locateFile( self, fileName = None ):
		for path in sys.path:
			if( os.path.exists( os.path.join( path, fileName ) ) ):
				return os.path.join( path, fileName )
		
	 	self.exceptionHandler.CheckStatus( False, "Could not find configuration file " + fileName )		
		

# Generation of the map from a file
	def __generateMapFromFile( self, fileName = None ):
		# Open file in read mode
		fileRef = open( self.__locateFile( fileName ), 'r' )
		counter = 0

		# Split all lines on '='
		for line in fileRef.readlines():
			element = line.split( ' = ' )

			# If not a key value pair
			if ( len( element ) < 2 ):
				if( element[ 0 ].isspace() != True ):
					# Removing the new lines
					value = element[0].split( '\n' ) 
					if( value[ 0 ].lower() == "testlist" ):
						continue

	 				# Removing the commented out test cases
			 		if( value[ 0 ][ 0 ] == '#' ):
						continue
					
			 		# Flooding configMap
			 		key = "testCase" + `counter`
					self.configMap[ key ] = value[ 0 ]
					counter += 1
				continue	
	
			# Removing the new lines
			values = element[ -1 ].split( '\n' )
			self.configMap[ element[ 0 ] ] = values[ 0 ].strip( '"' )

		fileRef.close()
		return True


# Generation of the map from command line arguments
	def __generateMapFromArgv( self, args = None ):
		for argument in args:
			if( argument[0][0] != '-' ):
				continue
		
			argument = argument.strip( '-"' )
			list = argument.split( '=' )
			self.configMap[ list[ 0 ] ] = list[ 1 ]
		
		return True


# Processing starts here
	def Execute( self, args = None ):
		# Flood values from the ate.conf file
		status = self.__generateMapFromFile( "ate.conf" )
		self.exceptionHandler.CheckStatus( status, "Could not flood config map with values from ate.conf" )

		# Flood values from the test.conf file
		status = self.__generateMapFromFile( "test.conf" )
		self.exceptionHandler.CheckStatus( status, "Could not flood config map with values from test.conf" )

		# Flood values from command line arguments, if present
		if( args != None ):
			status = self.__generateMapFromArgv( args )
			self.exceptionHandler.CheckStatus( status, "Could not flood config map with values from the command line" )
		
		# Return config map
		return self.configMap
