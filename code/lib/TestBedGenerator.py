# This class creates the required test bed based off the users specifications
# ---------------------------------------------------------------------------
# Import of Python libraries
import struct
import logging
import os
import random
import time
import string

# Import of all common user defined Python modules 
import common
from common import *

log = logging.getLogger( 'ATE.CommandConverter.TestBedGenerator' )

class TestBedGenerator:
    __borg = {}
    __instance = None
# Class constructor (a Borg)
    def __init__( self ):
		# Ensuring the __dict__ is the same for every instance / object
        self.__dict__ = self.__borg
        
		# If its the first instance of the class
        if( TestBedGenerator.__instance == None ):
            self.log = logging.getLogger( 'ATE.CommandConverter.TestBedGenerator' )
            TestBedGenerator.__instance = self
            self.commandMap = {}
            self.commandConverter = CommandConverter()
            self.__loadList()
            self.log.debug( "TestBedGenerator.__init__() method called." )

# Check status method
    def __checkStatus( self, status = None, errorMessage = None ):
        if( status != True ):
            self.log.error( errorMessage )
            sys.exit( -1 )
		
# Load commands to CommnadMap
    def __loadList( self ):
        self.log.debug( "TestBedGenerator.__loadList() method called." )
        self.commandMap[ "createTestBed" ] = ( "fileCount", "maxFileSize", "fileType" )

# Check provided parameters for all commands
    def __checkParameters( self, argumentMap = None ):
        self.log.debug( "TestBedGenerator: TestBedGenerator.__checkParameters() method called" )
        if( argumentMap == None ):
            self__checkStatus( False, "argumentMap is invalid." )
		
        for parameter in self.commandMap[ argumentMap[ "command" ] ]:
            if( argumentMap.__contains__( parameter ) != True ):
                self.__checkStatus( False, parameter + " not defined." )
		
        return True

# Delete and previous occurrence of a directory 
    def __deletePrevious( self, path = None, dirName = None ):
        self.log.debug( "TestBedGenerator: TestBedGenerator.__deletePrevious() method called" )
        commandMap = {}
        commandMap[ "command" ] = "deleteDirectory"
        commandMap[ "directoryName" ] = dirName
        commandMap[ "path" ] = path
        
        if( self.commandConverter.CommandLookup( commandMap ) ):
            return True
        else:
            return False

# Creates the specified directory
    def __createTestDirectory( self, path = None, dirName = None, removePrevious = None ):
        self.log.debug( "TestBedGenerator: TestBedGenerator.__createTestDirectory() method called" )
        if( os.path.exists( os.path.join( path, dirName ) ) ):
            status = self.__deletePrevious( path, dirName )
            self.__checkStatus( status, "Test failed - could not remove previously created directory " + dirName + " at " + path )	

        commandMap = {}
        commandMap[ "command" ] = "createDirectory"
        commandMap[ "path" ] = path
        commandMap[ "directoryName" ] = dirName
        commandMap[ "removePrevious" ] = removePrevious
        
        if( self.commandConverter.CommandLookup( commandMap ) ):
            return True
        else:
            return False

# Creates a user specific test bed
    def createTestBed( self, argumentMap = None ):
        self.log.info( "TestBedGenerator: TestBedGenerator.createTestBed() method called" )
        self.__checkStatus( self.__checkParameters( argumentMap ), "Required arguments not provided." )
		
        testBedPath = ""
        
        # Specifying whether the previous instance (if any) should be removed
        if( argumentMap.__contains__( "removePrevious" ) == True ):
            removePrevious = argumentMap[ "removePrevious" ]
        else:
            removePrevious = True
        
        # Defining the test directory Name
        if( argumentMap.__contains__( "testBedDirectoryName" ) == True and argumentMap[ "testBedDirectoryName" ] != None ):
            testBedName = argumentMap[ "testBedDirectoryName" ]
        else:
            testBedName = "testData"

        # Define test bed path and create test Bed directory
        if( argumentMap.__contains__( "testBedPath" ) == True and argumentMap[ "testBedPath" ] != None):
            testBedPath = os.path.join( argumentMap[ "testBedPath" ], testBedName )
            self.__createTestDirectory( argumentMap[ "testBedPath" ], testBedName, removePrevious )
        else:
            testBedPath = os.path.join( os.getcwd(), testBedName )
            self.__createTestDirectory( os.getcwd(), testBedName, removePrevious )



        testDirectory = os.getcwd()
        os.chdir( testBedPath )

        fileName = "testFile"
        random.seed( time.clock() )
        fileCount = 0
        swapFileType = argumentMap[ "fileType" ]
		
        switch = "binary"
        while fileCount != string.atoi( argumentMap[ "fileCount" ] ):
            fileDescriptor = open( fileName + `fileCount`, 'w' )
		
			# Varying file size 		
            if( ( string.atoi( argumentMap[ "fileCount" ] ) == fileCount + 1 ) or ( string.atoi( argumentMap[ "maxFileSize" ] ) == 0 ) ):
                fileSize = string.atoi( argumentMap[ "maxFileSize" ] )
            else:
                fileSize = random.choice( range( 0, string.atoi( argumentMap[ "maxFileSize" ] ) ) )

            counter = 0

            filePath = os.path.join( os.getcwd(), fileName + `fileCount` )
            while fileSize >= os.path.getsize( filePath ):
                if( swapFileType.lower() != "mixed" ):
                    if( swapFileType.lower() == "binary" ):
                            fileDescriptor.write( struct.pack( 'i', counter ) ) 
                    else:
                            fileDescriptor.write( `counter` )
                else:
                    if( switch == "binary" ):
                        fileDescriptor.write( struct.pack( 'i', counter ) ) 
                    else:
                        fileDescriptor.write( `counter` )
							
								
                counter += 1
				
            fileDescriptor.close()

            fileCount += 1
            if( switch == "binary" ):
                switch = "text"
            else:
                switch = "binary"

		# Returning to testDirectory
        os.chdir( testDirectory )
        self.log.info( "TestBedGenerator: TestBedGenerator.createTestBed() successfully completed all operations." )
        return testBedPath


# Returns to the caller the commandMap
    def GetCommandMap( self ):
        self.log.debug( "TestBedGenerator.GetCommandMap() method called" )
        return self.commandMap

# REPLACE SOON - Returns to the caller the log object
    def GetLogObject( self ):
        self.log.debug( "TestBedGenerator.GetLogObject() method called" )
        return self.log


# The GetObject method
def GetObject():
    log.debug( "TestBedGenerator.py - GetObject() method called" )		  
    moduleObject = TestBedGenerator()
    return moduleObject

# The GetLogObject method
def GetLogObject():
    log.debug( "TestBedGenerator.py - GetLogObject() method called" )          
    moduleObject = TestBedGenerator()
    return moduleObject.GetLogObject()
