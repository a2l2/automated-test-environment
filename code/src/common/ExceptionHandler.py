# This class handles razing all exceptions
# ----------------------------------------

# Import of Python libraries
import sys

class ExceptionHandler:
# Class constructor
	def __init__( self ):
		self.status = False
		self.errorMessage = None


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
