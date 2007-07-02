# This class converts user level commands to OS specific commands
#----------------------------------------------------------------
# Import of Python libraries
import string
import os
import sys
import shutil
import filecmp

# Import of all common user defined Python modules 
import common
from common import *

class CommandConverter:
	__borg = {}
	__instance = None
# Class constructor (a Borg)
	def __init__( self ):
		# Ensuring the __dict__ is the same for every instance / object
		self.__dict__ = self.__borg

		# If its the first instance of the class
		if( CommandConverter.__instance == None ):
			self.exceptionHandler = ExceptionHandler()
			CommandConverter.__instance = self


# The ifExists method
	def __ifExists( self, path = None ):
		if( os.path.exists( path ) != True ):
			return False


# The copyFile command definition
	def __copyFile( self, commandMap = None ):
		# Check validity of source path 
		sourcePath = os.path.join( commandMap[ "sourcePath" ], commandMap[ "sourceFileName" ] )
		status = self.__ifExists( sourcePath )
		self.exceptionHandler.CheckStatus( status, "Test failed - source path " + sourcePath + " cannot be accessed")

		# Check validity of destination path 
		if( commandMap.__contains__( "destinationFileName" ) ):
			destinationPath =  os.path.join( commandMap[ "destinationPath"], commandMap[ "destinationFileName" ] )
		else:
			destinationPath = os.path.join( commandMap[ "destinationPath"], commandMap[ "sourceFileName" ] )
		
		status = self.__ifExists( commandMap[ "destinationPath"]  )
		self.exceptionHandler.CheckStatus( status, "Test failed - destination path " + commandMap[ "destinationPath"] + " cannot be accessed")

		
		# Calling the built-in copy2() command"
		try:
			shutil.copy2( sourcePath, destinationPath )
		except:
			self.exceptionHandler.CheckStatus( False, "Test failed - shutil.copy2() command failed to execute successfully")

		print "[INFO] : copyFile() successfully completed all operations"
		return True


# The createDirectory command definition
	def __createDirectory( self, commandMap = None ):
		# Check validity of path
		status = self.__ifExists( os.path.join( commandMap[ "path" ], commandMap[ "directoryName" ] ) )
		if( status == True ):
			self.exceptionHandler.CheckStatus( False, "Test failed - could not create directory " + commandMap[ "directoryName" ] + " at " + commandMap[ "path" ] )

		# Calling the built-in mkdir() command
		try:
			os.mkdir( os.path.join( commandMap[ "path" ], commandMap[ "directoryName" ] ) )
		except:
			self.exceptionHandler.CheckStatus( False, "Test failed - os.mkdir() command failed to execute successfully")

		print "[INFO] : createDirectory() successfully completed all operations"
		return True


# The removeDirectory command definition
	def __removeDirectory( self, commandMap = None ):
		# Check validity of path
		status = self.__ifExists( os.path.join( commandMap[ "path" ], commandMap[ "directoryName" ] ) )
		self.exceptionHandler.CheckStatus( status, "Test failed - could not remove directory " + commandMap[ "directoryName" ] + " at " + commandMap[ "path" ] )

		# Calling the built-in mkdir() command
		directory = os.path.join( commandMap[ "path" ], commandMap[ "directoryName" ] )

		for root, dirs, files in os.walk( directory, topdown = False ):
			for name in files:
				try:
					os.remove( os.path.join( root, name ) )
				except:
					self.exceptionHandler.CheckStatus( False, "Test failed - could not remove file " + os.path.join( root, name ) )
    		
			for name in dirs:
				try:
					os.rmdir( os.path.join( root, name ) )
				except:
					self.exceptionHandler.CheckStatus( False, "Test failed - could not remove directory " + os.path.join( root, name ) )
		
		try:
			os.rmdir( directory )
		except:
			self.exceptionHandler.CheckStatus( False, "Test failed - os.rmdir() command failed to execute successfully")

		print "[INFO] : removeDirectory() successfully completed all operations"
		return True


# The compareFile command definition
	def __compareFile( self, commandMap = None ):
		# Check validity of source path 
		sourcePath = os.path.join( commandMap[ "sourcePath" ], commandMap[ "sourceFileName" ] )
		status = self.__ifExists( sourcePath )
		self.exceptionHandler.CheckStatus( status, "Test failed - source path " + sourcePath + " cannot be accessed")

		# Check validity of destination path 
		if( commandMap.__contains__( "destinationFileName" ) ):
			destinationPath =  os.path.join( commandMap[ "destinationPath"], commandMap[ "destinationFileName" ] )
		else:
			destinationPath = os.path.join( commandMap[ "destinationPath"], commandMap[ "sourceFileName" ] )
		
		status = self.__ifExists( commandMap[ "destinationPath"]  )
		self.exceptionHandler.CheckStatus( status, "Test failed - destination path " + commandMap[ "destinationPath"] + " cannot be accessed")


		# Calling the built-in filecmp.cmp() command
		if( filecmp.cmp( sourcePath, destinationPath ) ):
			print "[INFO] :", sourcePath, "=", destinationPath 
			return True
 		else:
			print "[INFO] :", sourcePath, "!=", destinationPath
			return False


# The compareDirectory commmand definition
	def __compareDirectory( self, commandMap = None ):
		# Check validity of source path
		status = self.__ifExists( commandMap[ "sourcePath" ] )
		self.exceptionHandler.CheckStatus( status, "Test failed - could not find directory " + commandMap[ "sourcePath" ] )
	
		# Check validity of destination path
		status = self.__ifExists( commandMap[ "destinationPath" ] )
		self.exceptionHandler.CheckStatus( status, "Test failed - could not find directory " + commandMap[ "destinationPath" ] )

		for file in os.listdir( commandMap[ "sourcePath" ] ):
			localCommandMap = {}
			localCommandMap[ "command" ] = "compareFiles"
			localCommandMap[ "sourcePath" ] = commandMap[ "sourcePath" ]
			localCommandMap[ "destinationPath" ] = commandMap[ "destinationPath" ]
			localCommandMap[ "sourceFileName" ] = file
			status = self.__compareFile( localCommandMap )
			self.exceptionHandler.CheckStatus( status, "Test failed - compareFile() failed on file " + file )

		print "[INFO] : compareDirectories() successfully completed all operations"
		return True
		
# The lookup method
	def CommandLookup( self, commandMap = None ):
		processed = False
		status = False

		# Check to see the command parameter exists in map
		if( commandMap.__contains__( "command" ) != True ):
			self.exceptionHandler.CheckStatus( False, "Test failed - 'command' parameter not defined" )
		
		# Locate desired command
		if( commandMap[ "command" ].lower() == "copyfile" ):
			# Check supplied parameters
			if( commandMap.__contains__( "sourcePath" ) != True or
				 commandMap.__contains__( "destinationPath" ) != True or
				 commandMap.__contains__( "sourceFileName" ) != True ):
				self.exceptionHandler.CheckStatus( False, "Test failed - Incomplete parameters supplied for " + commandMap[ "command" ]  )

			print "[INFO] : copyFile() command being invoked"
			status = self.__copyFile( commandMap )
			self.exceptionHandler.CheckStatus( status, "Test failed - copyFile() failed to execute successfully" )

		elif( commandMap[ "command" ].lower() == "comparefile" ) :
			# Check supplied parameters
			if( commandMap.__contains__( "sourcePath" ) != True or
				 commandMap.__contains__( "destinationPath" ) != True or
				 commandMap.__contains__( "sourceFileName" ) != True ):
				self.exceptionHandler.CheckStatus( False, "Test failed - Incomplete parameters supplied for " + commandMap[ "command" ]  )

			print "[INFO] : compareFile() command being invoked"
			status = self.__compareFile( commandMap )
			self.exceptionHandler.CheckStatus( status, "Test failed - compareFile() failed to execute successfully" )

		elif( commandMap[ "command" ].lower() == "comparedirectory" ):
			# Check supplied parameters
			if( commandMap.__contains__( "sourcePath" ) != True or
				 commandMap.__contains__( "destinationPath" ) != True ):
				self.exceptionHandler.CheckStatus( False, "Test failed - Incomplete parameters supplied for " + commandMap[ "command" ]  )
			
			print "[INFO] : compareDirectory() command being invoked"
			status = self.__compareDirectory( commandMap )
			self.exceptionHandler.CheckStatus( status, "Test failed - compareDirectory() failed to execute successfully" )

	 	elif( commandMap[ "command" ].lower() == "removedirectory"):
			# Check supplied parameters
			if( commandMap.__contains__( "directoryName" ) != True or
				 commandMap.__contains__( "path" ) != True ):
				self.exceptionHandler.CheckStatus( False, "Test failed - Incomplete parameters supplied for " + commandMap[ "command" ]  )

			print "[INFO] : removeDirectory() command being invoked"
			status = self.__removeDirectory( commandMap )
			self.exceptionHandler.CheckStatus( status, "Test failed - removeDirectory() failed to execute successfully" )

	 	elif( commandMap[ "command" ].lower() == "createdirectory" ):
			# Check supplied parameters
			if( commandMap.__contains__( "directoryName" ) != True or
				 commandMap.__contains__( "path" ) != True ):
				self.exceptionHandler.CheckStatus( False, "Test failed - Incomplete parameters supplied for " + commandMap[ "command" ]  )

			print "[INFO] : createDirectory() command being invoked"
			status = self.__createDirectory( commandMap )
			self.exceptionHandler.CheckStatus( status, "Test failed - createDirectory() failed to execute successfully" )

		else:
			self.exceptionHandler.CheckStatus( False, "Test failed - Unsupported parameter encountered" )

		return True
