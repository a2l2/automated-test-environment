 #Test script for test ID: AT-01258 
#----------------------------------

# Import of Python libraries
import string
import os
import sys

# Import of all common user defined Python modules 
import common
from common import *


class TestCase2:
	def GetValue( self ):
		return "Running Test Case1 "

def Info():
	return "test2 does some stuff"

def Main( argsMap = None ):
    if( argsMap == None ):
        argsMap = {}
        argsMap[ "command" ] = "clientInstall"
        argsMap[ "clientRPMPath" ] = "/root"
        argsMap[ "clientRPMName" ] = "dsgrid-20070804-0.i386.rpm"
        argsMap[ "username" ] = "griduser"
        argsMap[ "password" ] = "gridpass"
        argsMap[ "vaultDescriptorPath" ] = "/root"
        argsMap[ "vaultDescriptorName" ] = "remote-local-vault-descriptor.xml"
        argsMap[ "sliceServerPath" ] = "/mnt"
        argsMap[ "sliceDirectoryName" ] = "cleversafe"

	commandConverterObj = CommandConverter()
	commandConverterObj.CommandLookup( argsMap )
	
	return True

