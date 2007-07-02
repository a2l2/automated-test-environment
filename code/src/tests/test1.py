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
		return "Woo hoo - 1 "

def Info():
	return "This is information about the test1"

def Main():
  	print "[INFO] : Processing starts now for test1"
	objTest = TestCase1()
	print "[INFO] : Object returned", objTest.GetValue()
	return True
