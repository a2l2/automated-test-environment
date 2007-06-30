# This class handles razing all exceptions
# ----------------------------------------

# Import of Python libraries
import sys

class ExceptionHandler:
	__borg = {}
	__instance = None

# Class constructor
	def __init__( self ):
		self.__dict__ = self.__borg
		if( ExceptionHandler.__instance == None ):
			self.status = False
			self.errorMessage = None
			ExceptionHandler.__instance = self

# Raises an exception
	def __raiseException( self ):
		if( self.status == False ):
			print "[ERROR] : ", self.errorMessage
			sys.exit(-1)


# Check status
	def CheckStatus( self, status = False, errorMessage = None ):
		self.status = status
		self.errorMessage = errorMessage

		self.__raiseException()
