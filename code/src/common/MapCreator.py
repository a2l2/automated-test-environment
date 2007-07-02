# This class creates the Configuration Map
#-----------------------------------------

# Import of user defined Python modules 
import sys
import os
import string

# Import of all common user defined Python modules 
import common
from common import *

class MapCreator:
	__borg = {}
	__instance = None
# Class constructor (a Borg)
	def __init__( self ):
		# Ensuring the __dict__ is the same for every instance / object
		self.__dict__ = self.__borg

		# If its the first instance of the class
		if( MapCreator.__instance == None ):
			self.configMap = {}
			self.exceptionHandler = ExceptionHandler()
			MapCreator.__instance = self
	

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

		# Split all lines on '='
		for line in fileRef.readlines():
			element = line.split( ' = ' )

			# If not a key value pair
			if ( len( element ) < 2 ):
				if( element[ 0 ].isspace() != True ):
					# Removing the new lines
					value = element[0].split( '\n' ) 
					if( value[ 0 ].lower() == "testlist" ):
						self.configMap[ "testList" ] = {}
						continue
			
	 				# Removing the commented out test cases
			 		if( value[ 0 ][ 0 ] == '#' ):
						continue
					
			 		# Flooding configMap
					value[ 0 ] = value[ 0 ].expandtabs(1)
					testname = value[ 0 ].split( ' ' )

					# If iterations not specified, use default 1
					if( len(testname) == 1 or testname[-1].isalpha() != True ):
						testname.append( "1" )

					moduleName = testname[ 0 ].split( '.' )
					self.configMap[ "testList" ][ moduleName[ 0 ] ] = string.atoi(testname[ -1 ])
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


# Returns the config map
	def GetMap( self ):
		return self.configMap
