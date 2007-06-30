# This class converts user level commands to OS specific commands
#----------------------------------------------------------------

# Import of all common user defined Python modules 
import common
from common import *

class CommandConverter:
# Class constructor
	def __init__( self ):
		self.exceptionHandler = ExceptionHandler()


# The lookup method
	def ProcessCommandMap( self, commandMap = None ):
		processed = False
		status = False
		if ( commandMap[ "command" ] == "copyFile" ):

		elif:


		else:
			# command not recognizable 
