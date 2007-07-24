# This class converts user level commands to OS specific commands
#----------------------------------------------------------------
# Import of Python libraries
import string
import os
import sys
import shutil
import filecmp
import logging

# Import of all common user defined Python modules 
import common
from common import *

log = logging.getLogger( 'ATE.CommandConverter.CommonCommands' )

class CommonCommands:
	__borg = {}
	__instance = None
# Class constructor (a Borg)
	def __init__( self ):
		# Ensuring the __dict__ is the same for every instance / object
		self.__dict__ = self.__borg

		# If its the first instance of the class
		if( CommonCommands.__instance == None ):
			self.log = logging.getLogger( 'ATE.CommandConverter.CommonCommands' )
			CommonCommands.__instance = self
			self.commandMap = {}
			self.__loadList()
			self.log.debug( "CommonCommands.__init__() method called." )


# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )
		

# Load commands to CommnadMap
	def __loadList( self ):
		self.log.debug( "CommonCommands.__loadList() method called." )
		self.commandMap[ "copyFile" ] = ( "sourcePath", "destinationPath", "fileName" )
		self.commandMap[ "createDirectory" ] = ( "path", "directoryName" )
		self.commandMap[ "removeDirectory" ] = ( "path", "directoryName" )
		self.commandMap[ "compareFile" ] = ( "sourcePath", "destinationPath", "sourceFileName" )
		self.commandMap[ "compareDirectory" ] = ( "sourcePath", "destinationPath" )
		

# The ifExists method
	def __ifExists( self, path = None ):
		self.log.debug( "CommonCommands.__ifExists() method called." )
		if( os.path.exists( path ) == True ):
			return True
		else:
			return False


# The copyFile command definition
	def copyFile( self, argumentMap = None ):
		self.log.info( "CommonCommands.copyFile() method called." )

		# Check validity of source path 
		if( argumentMap.__contains__( "sourcePath" ) == True and argumentMap.__contains__( "sourceFileName" ) == True ):
			sourcePath = os.path.join( argumentMap[ "sourcePath" ], argumentMap[ "sourceFileName" ] )
			self.__checkStatus( self.__ifExists( sourcePath ), "Test failed - source path " + sourcePath + " cannot be accessed" )
		else:
			self.__checkStatus( False, "Test failed - sourcePath and/or sourceFileName arguments not defined" )

		# Check validity of destination path
		if( argumentMap.__contains__( "destinationPath" ) == True ):
			if( argumentMap.__contains__( "destinationFileName" ) ):
				destinationPath =  os.path.join( argumentMap[ "destinationPath"], argumentMap[ "destinationFileName" ] )
			else:
				destinationPath = os.path.join( argumentMap[ "destinationPath"], argumentMap[ "sourceFileName" ] )
		else:
			self.__checkStatus( False, "Test failed - destinationPath argument not defined" )

		self.__checkStatus( self.__ifExists( argumentMap[ "destinationPath"]  ), "Test failed - destination path " + argumentMap[ "destinationPath"] + " cannot be accessed")

		# Calling the built-in copy2() command"
		try:
			shutil.copy2( sourcePath, destinationPath )
		except:
			self.__checkStatus( False, "Test failed - shutil.copy2() command failed to execute successfully" )

		self.log.info( "CommonCommands.copyFile() successfully completed all operations" )

		return True


# The createDirectory command definition
	def createDirectory( self, argumentMap = None ):
		self.log.info( "CommonCommands.createDirectory() method called" )

		# Check validity of path
		if( argumentMap.__contains__( "directoryName" ) != True or
			 argumentMap.__contains__( "path" ) != True ):
			self.__checkStatus( False, "Test failed - Incomplete parameters supplied for " + argumentMap[ "command" ]  )

		if( self.__ifExists( os.path.join( argumentMap[ "path" ], argumentMap[ "directoryName" ] ) ) ):
			self.__checkStatus( False, "Test failed - could not create directory " + argumentMap[ "directoryName" ] + " at " + argumentMap[ "path" ] )

		# Calling the built-in mkdir() command
		try:
			os.mkdir( os.path.join( argumentMap[ "path" ], argumentMap[ "directoryName" ] ) )
		except:
			self.__checkStatus( False, "Test failed - os.mkdir() command failed to execute successfully" )

		self.log.info( "CommonCommands.createDirectory() successfully completed all operations" )

		return True


# The removeDirectory command definition
	def removeDirectory( self, argumentMap = None ):
		self.log.info( "CommonCommands.removeDirectory() method called" )

		# Check validity of path
		if( argumentMap.__contains__( "directoryName" ) != True or
			 argumentMap.__contains__( "path" ) != True ):
			self.__checkStatus( False, "Test failed - Incomplete parameters supplied for " + argumentMap[ "command" ]  )

		
		self.__checkStatus( self.__ifExists( os.path.join( argumentMap[ "path" ], argumentMap[ "directoryName" ] ) ), "Test failed - could not remove directory " + argumentMap[ "directoryName" ] + " at " + argumentMap[ "path" ] )

		# Calling the built-in mkdir() command
		directory = os.path.join( argumentMap[ "path" ], argumentMap[ "directoryName" ] )

		for root, dirs, files in os.walk( directory, topdown = False ):
			for name in files:
				try:
					os.remove( os.path.join( root, name ) )
				except:
					self.__checkStatus( False, "Test failed - could not remove file " + os.path.join( root, name ) )
    		
			for name in dirs:
				try:
					os.rmdir( os.path.join( root, name ) )
				except:
					self.__checkStatus( False, "Test failed - could not remove directory " + os.path.join( root, name ) )
		
		try:
			os.rmdir( directory )
		except:
			self.__checkStatus( False, "Test failed - os.rmdir() command failed to execute successfully")

		self.log.info( "CommonCommands.removeDirectory() successfully completed all operations" )

		return True


# The compareFile command definition
	def compareFile( self, argumentMap = None ):
		self.log.info( "CommonCommands.compareFile() method called" )

		# Check supplied parameters
		if( argumentMap.__contains__( "sourcePath" ) != True or
			 argumentMap.__contains__( "destinationPath" ) != True or
			 argumentMap.__contains__( "sourceFileName" ) != True ):
			self.__checkStatus( False, "Test failed - Incomplete parameters supplied for " + argumentMap[ "command" ]  )
			  
		# Check validity of source path 
		sourcePath = os.path.join( argumentMap[ "sourcePath" ], argumentMap[ "sourceFileName" ] )
		self.__checkStatus( self.__ifExists( sourcePath ), "Test failed - source path " + sourcePath + " cannot be accessed")

		# Check validity of destination path 
		if( argumentMap.__contains__( "destinationFileName" ) ):
			destinationPath =  os.path.join( argumentMap[ "destinationPath"], argumentMap[ "destinationFileName" ] )
		else:
			destinationPath = os.path.join( argumentMap[ "destinationPath"], argumentMap[ "sourceFileName" ] )
		
		self.__checkStatus( self.__ifExists( argumentMap[ "destinationPath"]  ), "Test failed - destination path " + argumentMap[ "destinationPath"] + " cannot be accessed")


		# Calling the built-in filecmp.cmp() command
		if( filecmp.cmp( sourcePath, destinationPath ) ):
			self.log.debug( sourcePath + " = " + destinationPath )
			self.log.info( "Source and destination file were identical" )
			return True
 		else:
			self.log.debug( sourcePath + " != " + destinationPath )
			self.log.info( "Source and destination file were NOT identical" )
			return False


# The compareDirectory commmand definition
	def compareDirectory( self, argumentMap = None ):
		self.log.info( "CommonCommands.compareDirectory() method called" )

		# Check supplied parameters
		if( argumentMap.__contains__( "sourcePath" ) != True or
			 argumentMap.__contains__( "destinationPath" ) != True ):
			self.__checkStatus( False, "Test failed - Incomplete parameters supplied for " + argumentMap[ "command" ]  )

		# Check validity of source path
		self.__checkStatus( self.__ifExists( argumentMap[ "sourcePath" ] ), "Test failed - could not find directory " + argumentMap[ "sourcePath" ] )
	
		# Check validity of destination path
		self.__checkStatus( self.__ifExists( argumentMap[ "destinationPath" ] ), "Test failed - could not find directory " + argumentMap[ "destinationPath" ] )

		for file in os.listdir( argumentMap[ "sourcePath" ] ):
			if( os.path.isfile( file ) ):
				localCommandMap = {}
				localCommandMap[ "command" ] = "compareFile"
				localCommandMap[ "sourcePath" ] = argumentMap[ "sourcePath" ]
				localCommandMap[ "destinationPath" ] = argumentMap[ "destinationPath" ]
				localCommandMap[ "sourceFileName" ] = file
				self.__checkStatus( self.compareFile( localCommandMap ), "Test failed - compareFile() failed on file " + file )
		
		self.log.info( "CommonCommands.compareDirectories() successfully completed all operations" )
		return True

# Returns to the caller the commandMap
	def GetCommandMap( self ):
		self.log.debug( "CommonCommands.GetCommandMap() method called" )
		return self.commandMap

# The GetObject method
def GetObject():
	log.debug( "CommonCommands.py - GetObject() method called" )		  
	moduleObject = CommonCommands()
	return moduleObject
