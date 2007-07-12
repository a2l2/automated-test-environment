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

log = logging.getLogger( 'ATE.TestCase-AT-01258' )

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
			self.log = logging.getLogger( 'ATE.TestCase-AT-01258' )
			self.commandConverter = CommandConverter()
			self.log.debug( "TestCase-AT-01258: TestOperations.__init__() method called" )

# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )


	def __checkParameters( self ):
		self.log.debug( "TestCase-AT-01258: TestOperations.__checkParameters() method called" )
		if( self.configMap.__contains__( "iSCSIdrive" ) != True or 
				os.path.exists( self.configMap[ "iSCSIdrive" ] ) != True ):
			self.__checkStatus( False, "Test failed - iSCSIdrive parameter invalid.")	

		if( self.configMap.__contains__( "testBedPath" ) != True or
				os.path.exists( self.configMap[ "testBedPath" ] ) != True ):
			self.__checkStatus( False, "Test failed - testBedPath parameter invalid.")

		if( self.configMap.__contains__( "testDirectory" ) != True or
				os.path.exists( self.configMap[ "testDirectory" ] ) != True ):
			self.__checkStatus( False, "Test failed - testDirectory parameter invalid.")	

		if( self.configMap.__contains__( "averageFileCount" ) != True ):
			self.__checkStatus( False, "Test failed - averageFileCount parameter invalid.")	
		
		return True


	def __deletePrevious( self, path = None, dirName = None ):
		self.log.debug( "TestCase-AT-01258: TestOperations.__deletePrevious() method called" )
		commandMap = {}
		commandMap[ "command" ] = "removeDirectory"
		commandMap[ "directoryName" ] = dirName
		commandMap[ "path" ] = path
		if( self.commandConverter.CommandLookup( commandMap ) ):
			return True
	 	else:
			return False


	def __createTestDirectory( self, path = None, dirName = None ):
		self.log.debug( "TestCase-AT-01258: TestOperations.__createTestDirectory() method called" )
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


	def __copyFile( self, fileName = None, sourcePath = None, destinationPath = None, destFileName = None ):
		self.log.debug( "TestCase-AT-01258: TestOperations.__copyFile() method called" )
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


	def __uploadDownload( self, sourcePath, destinationPath ):		  
		self.log.debug( "TestCase-AT-01258: TestOperations.__uploadDownload() method called" )
		# Create the test directory
		status = self.__createTestDirectory( destinationPath, "testData" )
		self.__checkStatus( status, "Test failed - could not create test directory at " + destinationPath)	

		# List all currently available test beds
		currentDir = os.getcwd()
		dirNames = os.listdir( sourcePath )

		# For each test bed perform the required operation
		testBedCounter = 0
		totalFileCount = 0
		for directory in dirNames:
			source = os.path.join( sourcePath, directory )
			try:
				os.chdir( source )
			except:
				continue
	 		os.chdir( currentDir )

			self.log.info( "Using test bed - " + directory )

			# Create current test bed directory at destination
			status = self.__createTestDirectory( os.path.join( destinationPath, "testData" ), directory )
			self.__checkStatus( status, "Test failed - could not create test bed directory at " + os.path.join( destinationPath, "testData" ) )
			destination = os.path.join( os.path.join( destinationPath, "testData" ), directory )

			# Gather list of files in current test bed
			fileList = os.listdir( source )

			# Set number of files to be copied
			if( len( fileList ) <= string.atoi( self.configMap[ "averageFileCount" ] ) ):
				counter = len( fileList )
			else:
				counter = string.atoi( self.configMap[ "averageFileCount" ]  )

			# Copy required number of files
			self.log.info( "Starting transfer of files" )
			for iterator in range(0, counter):
				status = self.__copyFile( fileList[ iterator ], source, destination )
				self.__checkStatus( status, "Test failed - could not copy file " + fileList[ iterator ] )
				
				self.log.debug( "File " + fileList[ iterator ] + " copied successfully" )
			
		 	self.log.info( `counter` + " files copied" )
		
			totalFileCount += counter
			testBedCounter += 1

		self.log.info( `totalFileCount` + " files from " + `testBedCounter` + " test beds successfully uploaded " )

		return True


	def __compare( self, sourcePath, destinationPath ):
		self.log.debug( "TestCase-AT-01258: TestOperations.__compare() method called" )
		# Since recursive directory structure
		currentDir = os.getcwd()
		dirNames = os.listdir( sourcePath )

		# For each test bed perform the required operation
		testBedCounter = 0
		for directory in dirNames:
			source = os.path.join( sourcePath, directory )
			try:
				os.chdir( source )
			except:
				continue
	 		os.chdir( currentDir )
			
			destination = os.path.join( destinationPath, directory )
			
			
			commandMap = {}
			commandMap[ "command" ] = "compareDirectory"
			commandMap[ "sourcePath" ] = source
			commandMap[ "destinationPath" ] = destination 

			if( self.commandConverter.CommandLookup( commandMap ) ):
				self.log.info( "Test bed " + directory + " comparison completed successfully" )
				testBedCounter += 1
 			else:
				return False

	 	self.log.info( "All test beds successfully compared")
	 	return True
				

	def StartTest( self ):
		self.log.debug( "TestCase-AT-01258: TestOperations.__StartTest() method called" )
		# Check map parameters
		status = self.__checkParameters()
		self.__checkStatus( status, "Test failed - required parameters not given" )	
	
		# Upload operation
		self.log.info( "Phase - I: Starting the upload operation" )
		status = self.__uploadDownload( self.configMap[ "testBedPath" ], self.configMap[ "iSCSIdrive" ] )
		self.__checkStatus( status, "Test failed - upload operation failed" )	

		# Download operation
		self.log.info( "Phase - II: Starting the download operation" )
		status = self.__uploadDownload( os.path.join( self.configMap[ "iSCSIdrive" ], "testData" ), self.configMap[ "testDirectory" ] )
		self.__checkStatus( status, "Test failed - download operation failed" )	

		# Compare operation
		self.log.info( "Phase - III: Starting compare operation" )
		status = self.__compare( os.path.join( self.configMap[ "testDirectory" ], "testData" ), self.configMap[ "testBedPath" ] )
		self.__checkStatus( status, "Test failed - upload operation failed" )

		return True


def Info():
	log.debug( "TestCase-AT-01258: Info() method called" )
	testInfo = "This test performs a UDC from the local drive to iSCSI device. The file count is varied based on the \"averageFileCount\" parameter."
	return testInfo


def Main():
	log.debug( "TestCase-AT-01258: Main() method called" )		  
	testObj = TestOperations()
	if( testObj.StartTest() ):
		log.info( "TestCase-AT-01258: completed successfully" )
		return( True )
	else:
		return( False )
