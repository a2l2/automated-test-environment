# Test Name: VaryBlockCount.py 
#-----------------------------
# Mandatory parameters
# --------------------
# xmlDirectory         - Path to the directory that contains the various xml files
# installScriptPath    - Path to the install script
# installScript        - Name of the install script
# testScriptPath       - Path to the test script that needs to follow the install
# testScript           - Name of the test script

import TestTemplate
from TestTemplate import *

class VaryBlockCount( TestTemplate ):
# Class constructor
    def __init__(self, instance = 1):
        self.__instance = instance
        self.__log = self.GetLogObject( "VaryBlockCount", instance )
        self.__log.debug( "VaryBlockCount.__init__() method called." )
        self.__argsMap = {}
        return None

# The mandatory Info method
    def Info(self):
        self.__log.debug( "VaryBlockCount.Info() method called" )
        self.__log.info( "This test reads in a list of remote-local-vault-descriptors. It then executes an \"installationScript\" and a \"testScript\" so as to validite the accuracy / authenticity of the xml file." )
        return True

# The mandatory Main method
    def Main( self, argsMap = None ):
        self.__log.debug( "VaryBlockCount.Main() method called" )          
        if( argsMap != None ):
            self.__argsMap = argsMap
        else:
            self.__argsMap = self.GetArguments( "VaryBlockCount.py" )

        if( self.StartTest() == True ):
            self.__log.info("Test VaryBlockCount completed successfully.")
            self.TestComplete( True )
        else:
            self.CheckStatus( False,"Test VaryBlockCount failed." )

        return None

# Executes the specified test
    def __executeTest( self, module = None, argsMap = None, className = None ):
        self.__log.debug( "VaryBlockCount.__executeTest() method called." )
        if( module == None or className == None ):
            self.__checkStatus( False, "Test execution failed - No module loaded or class name provided." )
        
        try:
            moduleObject = getattr( module, className )()
            returnValue = moduleObject.Info()
        except AttributeError, errorMessage:
            self.CheckStatus( False, "Test execution failed - Info() method not defined. - " + errorMessage )
        
        self.__log.info( "Calling Main() method for test - " +  className )
		# Filling all the generic arguments to the argument map and to the log file
        for elements in self.__argsMap.keys():
            if( argsMap.__contains__( elements ) ):
                continue
            argsMap[ elements ] = self.__argsMap[ elements ]

		# Calling the Main() method 
        try:
            returnValue = moduleObject.Main( argsMap )
        except RuntimeError, errorMessage  :
            self.CheckStatus( False, "Test execution failed - Lookup on Main() method failed - " + errorMessage )
		
        return returnValue
        
# Start executing the test 
    def StartTest( self ):
        self.__log.debug( "VaryBlockCount.__StartTest() method called" )

        # Check is stub is set to True, in which case stop test immediately
        if( self.__argsMap.__contains__("stub") == True and self.__argsMap["stub"] == True ):
            self.CheckStatus( False, "Test execution failed - Varibale \"stub\" is defined and set to True. This test will need to instal the s/w." )

        # Adding the install and test script paths to the global path if necessary & importing the modules
        self.__log.info( "Phase - I: Adding the paths of the test case & install scripts to global path - if necessary & importing the modules" )

        # Maintaining local copy of the sys.path.
        self.__originalSystemPath = sys.path
        
        if( sys.path.__contains__( self.__argsMap[ "installScriptPath" ] ) != True ):
            sys.path.append( self.__argsMap[ "installScriptPath" ] )
            
        if( sys.path.__contains__( self.__argsMap[ "testScriptPath" ] ) != True ):
            sys.path.append( self.__argsMap[ "testScriptPath" ] )

        key = self.__argsMap[ "installScript" ].split( "." )
        installModuleClassName = key[0]
        try:
            self.__installModule = __import__( key[0] )
        except OSError, exception:
            self.CheckStatus( False, "Test failed - Could not import " + key[0] + " - " + exception )    
        
        key = self.__argsMap[ "testScript" ].split( "." )
        testModuleClassName = key[0]
        try:
            self.__testModule = __import__( key[0] )
        except OSError, exception:
            self.CheckStatus( False, "Test failed - Could not import " + key[0] + " - " + exception )    

        # Read in list of xml files
        self.__log.info( "Phase - II: Read in list of all xml files" )
        xmlFileList = os.listdir( self.__argsMap[ "xmlDirectory" ] )
        
        # Call install & test script on each entry in the directory
        self.__log.info( "Phase - III: Calling the install & test script on each entry in the directory" )
        commandMap[ "command" ] = "clientInstall"
        commandMap[ "clientRPMPath" ] = "/root"
        commandMap[ "clientRPMName" ] = "dsgrid-20070804-0.i386.rpm"
        commandMap[ "username" ] = "griduser"
        commandMap[ "password" ] = "gridpass"
        commandMap[ "sliceServerPath" ] = "/mnt"
        commandMap[ "sliceDirectoryName" ] = "cleversafe"

        for xmlFile in xmlFileList:
            commandMap[ "vaultDescriptorPath" ] = self.__argsMap[ "xmlDirectory" ]
            commandMap[ "vaultDescriptorName" ] = xmlFile
            
            # Executing the installation script
            self.__log.info( "Calling the install script with vault descriptor - " + xmlFile )
            self.__executeTest( self.__installModule, commandMap, installModuleClassName )
            self.__log.info( "Installation completed successfully for vault descriptor - " + xmlFile )
            
            # Executing the test script
            self.__log.info( "Calling the test script with vault descriptor - " + xmlFile )
            self.__executeTest( self.__testModule, self.__argsMap, testModuleClassName )
            self.__log.info( "Test completed successfully for vault descriptor - " + xmlFile )
            
            self.__log.info( "Vault descriptor file " + xmlFile + " is valid." )

        return True