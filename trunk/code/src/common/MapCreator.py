# This class creates the Configuration Map
#-----------------------------------------

# Import of user defined Python modules 
import sys
import os
import string
import logging

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
			self.objectMap = {}
			self.log = logging.getLogger( 'ATE.MapCreator' )
			MapCreator.__instance = self
			self.log.debug( "MapCreator.__init__() method called." )
			

# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )

# Locates the path to the configuration file
	def __locateFile( self, fileName = None ):
		self.log.debug( "MapCreator.__locate() method called." )
		for path in sys.path:
			if( os.path.exists( os.path.join( path, fileName ) ) ):
				return os.path.join( path, fileName )
		
	 	self.__checkStatus( False, "Could not find configuration file " + fileName )		

# Generation of the map from a file
	def __generateMapFromFile( self, fileName = None ):
		self.log.debug( "MapCreator.__generateMapFromFile() method called." )
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
					if( len(testname) == 1 or ( testname[-1].isalpha() != True and testname[-1].isdigit() != True ) ):
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
		self.log.debug( "MapCreator.__generateMapFromArgv() method called." )
		for argument in args:
			if( argument[0][0] != '-' ):
				continue
		
			argument = argument.strip( '-"' )
			list = argument.split( '=' )
			self.configMap[ list[ 0 ] ] = list[ 1 ]
		
		return True


# Generation of the object map
	def __generateObjectMap( self ):
		self.log.debug( "MapCreator.__generateObjectMap() method called." )
		counter = 0
		fileList = os.listdir( self.configMap[ "libPath" ] )
	
		for file in fileList:
			fileName = file.split( '.' )

			if( fileName[-1] != "py" or fileName[0] == "__init__" ):
				continue

			try:
				module = __import__( fileName[ 0 ] )
			except:
				self.__checkStatus( False, "Could not load module " + fileName[0] )

#TODO: There has to be a better way than this to include only those modules that will flood the objectMap
			try:
				self.objectMap[ counter ] = module.GetObject()
			except:
				continue

			counter += 1

		return True


# Processing starts here
	def Execute( self, args = None ):
		self.log.debug( "MapCreator.Execute() method called." )
		# Flood values from the ate.conf file
		self.__checkStatus( self.__generateMapFromFile( "ate.conf" ), "Could not flood config map with values from ate.conf" )

		# Flood values from the test.conf file
		self.__checkStatus( self.__generateMapFromFile( "test.conf" ), "Could not flood config map with values from test.conf" )

		# Flood values from command line arguments, if present
		if( args != None ):
			self.__checkStatus( self.__generateMapFromArgv( args ), "Could not flood config map with values from the command line" )

		# Set path to libraries
		for key in self.configMap.keys():
			if( key.lower() == "libpath" and os.path.exists( self.configMap[ key ] ) ):
				sys.path.append( self.configMap[ key ] )

		# Generate the object map from the modules present in 'common'
		self.__checkStatus( self.__generateObjectMap(), "Could not create object map" )

		# Return config map
		return ( self.GetConfigMap() )


# Returns the config map
	def GetConfigMap( self ):
		self.log.debug( "MapCreator.GetConfigMap() method called." )
		return self.configMap

# Returns the object map
	def GetObjectMap( self ):
		self.log.debug( "MapCreator.GetObjectMap() method called." )
		return self.objectMap
