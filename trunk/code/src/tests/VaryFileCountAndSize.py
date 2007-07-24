# Test script for test ID: AT-01259 
#----------------------------------
# Import of Python libraries
import string
import os
import sys
import logging

# Import of all common user defined Python modules 
import common
from common import *

log = logging.getLogger( 'ATE.VaryFileCountAndSize' )

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
			self.log = logging.getLogger( 'ATE.VaryFileCountAndSize' )
			self.commandConverter = CommandConverter()
			self.log.debug( "VaryFileCountAndSize: TestOperations.__init__() method called" )
			self.__testBedPath = ""

# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )

# Check the parameters passed
	def __checkParameters( self ):
		self.log.debug( "VaryFileCountAndSize: TestOperations.__checkParameters() method called" )
		if( self.configMap.__contains__( "iSCSIdrive" ) != True or 
				os.path.exists( self.configMap[ "iSCSIdrive" ] ) != True ):
			self.__checkStatus( False, "Test failed - iSCSIdrive parameter invalid.")	

		if( self.configMap.__contains__( "testDirectory" ) != True or
				os.path.exists( self.configMap[ "testDirectory" ] ) != True ):
			self.__checkStatus( False, "Test failed - testDirectory parameter invalid.")	

		if( self.configMap.__contains__( "fileCount" ) != True ):
			self.__checkStatus( False, "Test failed - averageFileCount parameter invalid.")	

		if( self.configMap.__contains__( "maxFileSize" ) != True ):
			self.__checkStatus( False, "Test failed - maxFileSize parameter invalid.")	

		if( self.configMap.__contains__( "fileType" ) != True ):
			self.__checkStatus( False, "Test failed - fileType parameter invalid.")	

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


# Upload / Download the files to and from the slice server
	def __uploadDownload( self, sourcePath, destinationPath ):		  
		self.log.debug( "VaryFileCountAndSize: TestOperations.__uploadDownload() method called" )

		# Create the test directory on destination
		self.__checkStatus( self.__createDirectory( destinationPath, "TestDirectory" ), "Could not create the TestDirectory" )		
		destination = os.path.join( destinationPath, "TestDirectory" )

		if( sourcePath == self.__testBedPath ):
			source = sourcePath
		else:
			source = os.path.join( sourcePath, "TestDirectory" )

		counter = 0
		# Gather list of files in current test bed
		for fileList in os.listdir( source ):
			counter += 1
			status = self.__copyFile( fileList, source, destination )
			self.__checkStatus( status, "Test failed - could not copy file " + fileList )
			self.log.debug(" File " + fileList + " copied from " + source + " to " + destination + " successfully." )
			
	 	self.log.info( `counter` + " files copied from " + source + " to " + destination + " successfully" )
	
		return True


# Compare two directories
	def __compare( self, sourcePath, destinationPath ):
		self.log.debug( "VaryFileCountAndSize: TestOperations.__compare() method called" )
		# Since recursive directory structure
		if( sourcePath == self.__testBedPath ):
			source = sourcePath
		else:
			source = os.path.join( sourcePath, "TestDirectory" )

		if( destinationPath == self.__testBedPath ):
			destination = destinationPath
		else:
			destination = os.path.join( destinationPath, "TestDirectory" )

		# For each test bed perform the required operation
		for root, dirs, files in os.walk( source, topdown = False ):
			for name in files:
				commandMap = {}
				commandMap[ "command" ] = "compareFile"
				commandMap[ "sourcePath" ] = root
				commandMap[ "destinationPath" ] = destination
				commandMap[ "sourceFileName" ] = name

				self.__checkStatus( self.commandConverter.CommandLookup( commandMap ), "Test failed - File comparison failed on file " + name + " at " + root )
				self.log.debug( "File: " + name + " compared successfully." )

	 	self.log.info( "All directories successfully compared")
	 	return True


# Start executing the test 
	def StartTest( self ):
		self.log.debug( "VaryFileCountAndSize: TestOperations.__StartTest() method called" )
		# Check map parameters
		status = self.__checkParameters()
		self.__checkStatus( status, "Test failed - required parameters not given" )	

		# Create test bed
		self.log.info( "Phase - I: Generating test bed" )
		status = self.__generateTestBed( self.configMap[ "fileCount" ], self.configMap[ "maxFileSize" ], self.configMap[ "fileType" ], self.configMap[ "testDirectory" ] )
		self.__checkStatus( status, "Test failed - Test bed could not be generated successfully." )	

		# Upload operation
		self.log.info( "Phase - II: Starting the upload operation" )
		status = self.__uploadDownload( self.__testBedPath, self.configMap[ "iSCSIdrive" ] )
		self.__checkStatus( status, "Test failed - upload operation failed" )	

		# Download operation
		self.log.info( "Phase - III: Starting the download operation" )
		status = self.__uploadDownload( self.configMap[ "iSCSIdrive" ], self.configMap[ "testDirectory" ] )
		self.__checkStatus( status, "Test failed - download operation failed" )	

		# Compare operation
		self.log.info( "Phase - IV: Starting compare operation" )
		status = self.__compare( self.__testBedPath, self.configMap[ "testDirectory" ] )
		self.__checkStatus( status, "Test failed - upload operation failed" )

		return True


def Info():
	log.debug( "VaryFileCountAndSize: Info() method called" )
	testInfo = "This test performs a UDC from the local drive to iSCSI device. The file count is varied based on the \"averageFileCount\" parameter."
	return testInfo


def Main():
	log.debug( "VaryFileCountAndSize: Main() method called" )		  
	testObj = TestOperations()
	if( testObj.StartTest() ):
		log.info( "VaryFileCountAndSize: completed successfully" )
		return( True )
	else:
		return( False )
