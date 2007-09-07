 #Test Name - InstallSoftware.py
#-------------------------------
# Mandatory parameters
# --------------------
# clientRPMPath        - The path to the client rpm
# clientRPMName        - The name of the client RPM 
# username             - The username for creating an account / vault 
# password             - The password for creating an account / vault 
# vaultDescriptorPath  - The path to the vault descriptor (.xml) file
# vaultDescriptorName  - The name of the vault descriptor (.xml) file  
# sliceServerPath      - The path to where the slice server will be mounted
# sliceDirectoryName   - The name of the directory to where the slice server will be mounted


import TestTemplate
from TestTemplate import *


class InstallSoftware( TestTemplate ):
# Class constructor (a Borg)
    def __init__( self, instance = 1 ):
        self.__log = self.GetLogObject( "InstallSoftware", instance )
        self.__log.debug( "InstallSoftware.__init__() method called." )

# Install client software
    def __installClientSoftware( self, argsMap = None ):    
        self.__log.info( "InstallSoftware.Main() method called." )
        
        argumentMap = {}
        argumentMap[ "command" ] = "clientInstall"
        argumentMap[ "clientRPMPath" ] = argsMap[ "clientRPMPath" ] 
        argumentMap[ "clientRPMName" ] = argsMap[ "clientRPMName" ] 
        argumentMap[ "username" ] = argsMap[ "username" ] 
        argumentMap[ "password" ] = "gridpass"
        argumentMap[ "vaultDescriptorPath" ] = argsMap[ "vaultDescriptorPath" ] 
        argumentMap[ "vaultDescriptorName" ] = argsMap[ "vaultDescriptorName" ] 
        argumentMap[ "sliceServerPath" ] = argsMap[ "sliceServerPath" ] 
        argumentMap[ "sliceDirectoryName" ] = argsMap[ "sliceDirectoryName" ] 

        status = self.ExecuteCommand( argumentMap )
        self.__log.info( "Client software successfully installed." )
        return status
        
    def Info(self):
        self.__log.info( "This test installs the grid server & client software based on the parameters supplied" )
        return True

    def Main(self, argsMap = None):
        self.__log.info( "InstallSoftware.Main() method called." )
        
        # Installing Client softwares
        self.CheckStatus( self.__installClientSoftware(argsMap), "Client software installation failed." )
        
        self.TestComplete( True )
