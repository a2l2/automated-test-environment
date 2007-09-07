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
            self.logObjectMap = {}
            self.log = logging.getLogger( 'MapCreator.py' )
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

        # Only gets set when a test is commented out
        neglectArguments = False
        
        testListCounter = 0
        testName = ""		
		
        for line in fileRef.readlines():
			# Removing all the tabs from the line
            line = line.expandtabs(1)
			
			# Split all lines on '='
            element = line.split( ' = ' )

			# If not a key value pair
            if ( len( element ) < 2 ):
                if( element[ 0 ].isspace() != True ):

					# Removing the new lines
                    value = element[0].split( '\n' ) 
                    
                    # Checking if "TestList" category encountered
                    if( value[ 0 ].lower() == "testlist" ):
                        self.configMap[ "testList" ] = {}
                        continue
                    
                    # Test name encountered
                    if( value[0].__contains__(".py") == True and value[ 0 ].__contains__ ( '#' ) == True ):
                        neglectArguments = True
                        continue
                    elif( value[0].__contains__(".py") == True and value[ 0 ].__contains__ ( '#' ) == False ):
                        neglectArguments = False
                        
					# Check if a python test case or argument
                    if( value[ 0 ].__contains__( ".py" ) ):
						# Separating the file count from the file name
                        fileName = value[ 0 ].split( ' ' )

						# If iterations not specified, use default 1
                        if( len(fileName) == 1 or ( fileName[-1].isalpha() != True and fileName[-1].isdigit() != True ) ):
                            fileName.append( "1" )
				
                        moduleName = fileName[ 0 ].split( '.' )

						# In order to maintain the order of test execution all tests prepended by the count and a ":". 
						# Example- Test name = abc then Map contains 01:abc
                        moduleName[0] = `testListCounter` + ":" + moduleName[0]
                        testListCounter += 1
						
						# Creating map of arguments for the test
						# Example: Map[ [ testList ] [ <Test Name> ] ] = { args1:value1, args2:value2 ..etc }
                        self.configMap[ "testList" ][ moduleName[ 0 ].strip( '"' ) ] = {}

                        self.configMap[ "testList" ][ moduleName[ 0 ] ]["iterations"] = fileName[ -1 ].strip( '"' )
                        testName = moduleName[ 0 ]
                continue	

            # Removing the commented lines 
            if( element[ 0 ].__contains__( '#' ) or neglectArguments == True ):
                continue

			# Removing the new lines
            values = element[ -1 ].split( '\n' )
            if( testName == "" ):
                self.configMap[ element[ 0 ].strip( '"' ) ] = values[ 0 ].strip( '"' )
            else:
                self.configMap[ "testList" ][ testName ][ element[ 0 ].strip( '"' ) ] = values[ 0 ].strip( '"' )
			
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

            if( fileName[-1] != "py" or fileName[0] == "__init__" or fileName[0] == "LibraryTemplate" ):
                continue

            try:
                module = __import__( fileName[ 0 ] )
            except ImportError, errorMessage:
                self.__checkStatus( False, "Could not load module " + fileName[0] + " - " + str(errorMessage ) )

#TODO: There has to be a better way than this to include only those modules that will flood the objectMap
            try:
                self.objectMap[ counter ] = module.GetObject()
            except:
                self.__checkStatus( False, "Module " + fileName[0] + " doesn't have a GetObject() method. This is a required method." )

# THIS IS TEMP SECTION - NEEDS TO BE CHANGED SOON
            try:
                self.logObjectMap[ counter ] = module.GetLogObject()
            except:
                self.__checkStatus( False, "Module " + fileName[0] + " doesn't have a GetLogObject() method. This is a required method." )


            counter += 1

        return True

# Processing starts here
    def Execute( self, args = None, logPath = None ):
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
            
        # Adding the path to where the logs are created to the configMap
        self.configMap[ "logPath" ] = logPath

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

# MUST BE REPLACED SOON - Returns the log object map
    def GetLogObjectMap( self ):
        self.log.debug( "MapCreator.GetLogObjectMap() method called." )
        return self.logObjectMap
