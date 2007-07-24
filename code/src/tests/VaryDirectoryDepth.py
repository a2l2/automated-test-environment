# Test script for test ID: AT-01258 
#----------------------------------
# Import of Python libraries
import string
import os
import sys
import logging

# Import of all common user defined Python modules 
import common
from common import *

log = logging.getLogger( 'ATE.VaryDirectoryDepth' )

class TestOperations:
	__borg = {}
	__instance = None
# Class constructor (a Borg)
	def __init__( self ):
		# Ensuring the __dict__ is the same for every instance / object
		self.__dict__ = self.__borg

		# If its the first instance of the class 
		if( TestOperations.__instance == None ):
			tempObject = MapCreator()
			self.configMap = tempObject.GetConfigMap()
			self.log = logging.getLogger( 'ATE.VaryDirectoryDepth' )
			self.commandConverter = CommandConverter()
			self.log.debug( "VaryDirectoryDepth: TestOperations.__init__() method called" )
			self.__testBedPath = ""

# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )


# Check the parameters passed
	def __checkParameters( self ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__checkParameters() method called" )
		if( self.configMap.__contains__( "iSCSIdrive" ) != True or 
				os.path.exists( self.configMap[ "iSCSIdrive" ] ) != True ):
			self.__checkStatus( False, "Test failed - iSCSIdrive parameter invalid.")	

		if( self.configMap.__contains__( "testDirectory" ) != True or
				os.path.exists( self.configMap[ "testDirectory" ] ) != True ):
			self.__checkStatus( False, "Test failed - testDirectory parameter invalid.")	

		if( self.configMap.__contains__( "fileCount" ) != True ):
			self.__checkStatus( False, "Test failed - fileCount parameter invalid.")	
		
		if( self.configMap.__contains__( "maxFileSize" ) != True ):
			self.__checkStatus( False, "Test failed - maxFileSize parameter invalid.")	

		if( self.configMap.__contains__( "fileType" ) != True ):
			self.__checkStatus( False, "Test failed - fileType parameter invalid.")	

		if( self.configMap.__contains__( "directoryDepth" ) != True ):
			self.__checkStatus( False, "Test failed - directoryDepth parameter invalid.")	

		return True


# Delete previous occurrences of the directory
	def __deletePrevious( self, path = None, dirName = None ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__deletePrevious() method called" )
		commandMap = {}
		commandMap[ "command" ] = "removeDirectory"
		commandMap[ "directoryName" ] = dirName
		commandMap[ "path" ] = path
		if( self.commandConverter.CommandLookup( commandMap ) ):
			return True
	 	else:
			return False


# Create the specified directory
	def __createDirectory( self, path = None, dirName = None ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__createTestDirectory() method called" )
		if( os.path.exists( os.path.join( path, dirName ) ) ):
			status = self.__deletePrevious( path, dirName )
			self.__checkStatus( status, "Test failed - could not remove previously created directory " + dirName + " at " + path )	

		commandMap = {}
		commandMap[ "command" ] = "createDirectory"
		commandMap[ "path" ] = path
		commandMap[ "directoryName" ] = dirName
		if( self.commandConverter.CommandLookup( commandMap ) ):
			return True
		else:
			return False


# Copies the specified file
	def __copyFile( self, fileName = None, sourcePath = None, destinationPath = None, destFileName = None ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__copyFile() method called" )
		commandMap = {}
		commandMap[ "command" ] = "copyFile"
		commandMap[ "sourcePath" ] = sourcePath
		commandMap[ "destinationPath" ] = destinationPath
		commandMap[ "sourceFileName" ] = fileName
		if( destFileName != None ):
			commandMap[ "destinationFileName" ] = destFileName

		if( self.commandConverter.CommandLookup( commandMap ) ):
			return True
 		else:
			return False

# This method creates the required test bed
	def __generateTestBed( self, fileCount = None, maxFileSize = None, fileType = None, testBedPath = None ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__generateTestBed() method called" )
		commandMap = {}
		commandMap[ "command" ] = "createTestBed"
		commandMap[ "maxFileSize" ] = maxFileSize
		commandMap[ "fileType" ] = fileType
		commandMap[ "fileCount" ] = fileCount
		if( testBedPath != None ):
			commandMap[ "testBedPath" ] = testBedPath
	
		self.__testBedPath = self.commandConverter.CommandLookup( commandMap )	
		if( self.__testBedPath == False ):
			self.log.info( "Test bed created successfully" )

	 	return True


# Creates the directory structure of defined depth
	def __createDirectoryStructure( self, directoryDepth = None, destinationPath = None ):
		directoryDepth = string.atoi( directoryDepth )
		if( directoryDepth == 0 ):
			self.__checkStatus( False, "Directory depth is defined as 0" )
		
		count = 0
		currentDirectory = os.getcwd()

		self.__checkStatus( self.__createDirectory( destinationPath, "TestDirectory" ), "Could not create the TestDirectory" )
		os.chdir( os.path.join( destinationPath, "TestDirectory" ) )

		while count != directoryDepth:
			presentDirectory = os.getcwd()
			
			self.__checkStatus( self.__createDirectory( presentDirectory, `count` ), "Could not create test directory at depth " + `count` )
			os.chdir( os.path.join( presentDirectory, `count` ) )
			
			for fileName in os.listdir( self.__testBedPath ):
				self.__checkStatus( self.__copyFile( fileName, self.__testBedPath, os.getcwd() ), "Could not copy file " + fileName )
			
			count += 1

		# Returning to the working directory
		os.chdir( currentDirectory )

		return True


# Compare two directories
	def __compare( self, sourcePath, destinationPath ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__compare() method called" )
		depth = 0
		
		# For each test bed perform the required operation
		for root, dirs, files in os.walk( sourcePath, topdown = False ):
			for name in files:
				commandMap = {}
				commandMap[ "command" ] = "compareFile"
				commandMap[ "sourcePath" ] = root
				commandMap[ "destinationPath" ] = destinationPath
				commandMap[ "sourceFileName" ] = name

				self.__checkStatus( self.commandConverter.CommandLookup( commandMap ), "Test failed - File comparison failed on file " + name + " at " + root )
				self.log.debug( "All files at directory depth - " + `depth` + " successfully compared." )
				depth += 1

	 	self.log.info( "All directories successfully compared")
	 	return True


# Start processing the test from this point		
	def StartTest( self ):
		self.log.debug( "VaryDirectoryDepth: TestOperations.__StartTest() method called" )
		# Check map parameters
		self.log.debug( "VaryDirectoryDepth: TestOperations.__checkParameters() method called" )
		status = self.__checkParameters()
		self.__checkStatus( status, "Test failed - required parameters not defined" )	
		
		# Create test bed
		self.log.info( "Phase - I: Generating test bed" )
		status = self.__generateTestBed( self.configMap[ "fileCount" ], self.configMap[ "maxFileSize" ], self.configMap[ "fileType" ], self.configMap[ "testDirectory" ] )
		self.__checkStatus( status, "Test failed - Test bed could not be generated successfully." )	

		# Create remote directory structure 
		self.log.info( "Phase - II: Starting creation of remote directory structure" )
		status = self.__createDirectoryStructure( self.configMap[ "directoryDepth" ], self.configMap[ "iSCSIdrive" ] )
		self.__checkStatus( status, "Test failed - Creation of remote directory structure failed" )	

		# Create local directory structure
		self.log.info( "Phase - III: Starting creation of local directory structure" )
		status = self.__createDirectoryStructure( self.configMap[ "directoryDepth" ], self.configMap[ "testDirectory" ] )
		self.__checkStatus( status, "Test failed - Creation of local directory structure failed" )	

		# Compare operation
		self.log.info( "Phase - IV: Starting compare operation" )
		status = self.__compare( os.path.join( self.configMap[ "testDirectory" ], "TestDirectory" ), self.__testBedPath )
		self.__checkStatus( status, "Test failed - compare operation failed" )

		return True


def Info():
	log.debug( "VaryDirectoryDepth: Info() method called" )
	testInfo = "This test performs a UDC from the local drive to iSCSI device. The depth of the directory structure is varied and a set of files is placed at the root of each directory."
	return testInfo


def Main():
	log.debug( "VaryDirectoryDepth: Main() method called" )		  
	testObj = TestOperations()
	if( testObj.StartTest() ):
		log.info( "VaryDirectoryDepth: completed successfully" )
		return( True )
	else:
		return( False )
