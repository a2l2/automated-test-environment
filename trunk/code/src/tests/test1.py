# Test script for test ID: AT-01258 
#----------------------------------

# Import of Python libraries
import string
import os
import sys

# Import of all common user defined Python modules 
import common
from common import *


class TestCase1:
	def GetValue( self ):
		return "Running Test Case1 "

def Info():
	return "test1 does some stuff"

def Main():
	argsMap = {}
	argsMap[ "command" ] = "createTestBed"
	argsMap[ "fileCount" ] = 10
	argsMap[ "maxFileSize" ] = 102400
	argsMap[ "fileType" ] = "binary"

	commandConverterObj = CommandConverter()
	commandConverterObj.CommandLookup( argsMap )

	return True
