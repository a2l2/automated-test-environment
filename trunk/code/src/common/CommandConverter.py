# This class converts user level commands to OS specific commands
#----------------------------------------------------------------
# Import of Python libraries
import string
import os
import sys
import logging

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
			tempObject = MapCreator()
			self.objectMap = tempObject.GetObjectMap()
			self.log = logging.getLogger( 'ATE.CommandConverter' )
			CommandConverter.__instance = self
			self.log.debug( "CommandConverter.__init__() method called." )


# Check status method
	def __checkStatus( self, status = None, errorMessage = None ):
		if( status != True ):
			self.log.error( errorMessage )
			sys.exit( -1 )


	# The CommandLookup method
	def CommandLookup( self, argumentMap ):
		self.log.debug( "CommandConverter.CommandLookup() method called." )
		counter = len( self.objectMap.keys() )

		for iterator in range( 0, counter ):
			moduleMap = {}
			moduleMap = self.objectMap[ iterator ].GetCommandMap()

			for key in moduleMap.keys():
				if( key.lower() == argumentMap[ "command" ].lower() ):
					funcCall = getattr(self.objectMap[ iterator], key)
					
					status = funcCall( argumentMap )
					if( status == False ):
						self.__checkStatus( False, "Error calling requested function " + key )
					
					if( status != True ):
						return status
			 		else:
						return True

		self.__checkStatus( False, "Could not find specified command - " + argumentMap[ "command" ] )
