# This is the test template that must be inherited by each test case
import common.Interface
from common.Interface import *

class TestTemplate( Interface ):
# This method defines the private member variables whenever they are needed 
    def __securityChecker( object = None ):
        if( object.lower() == "log" ):
            return logging.getLogger( 'TestTemplate.py' )
        else:
            self.__checkStatus(False, "Security violation - Invalid object provided.")
    
# Private Member Variables    
    __log = __securityChecker( "log" )

# This method forwards the call to the InterfaceCheckStatus method
    def __checkStatus(self, status = None, errorMessage = None ):
        self.__log.debug( "TestTemplate.__checkStatus() method called." )

        # Check parameters
        if( status == None or errorMessage == None ):
            self.CheckStatus(False, "Invalid arguments passed - \"status\" or \"errorMessage\" not provided.")
        
        self.InterfaceCheckStatus( status, errorMessage )
        return None

# Public Method - Interface for __checkStatus method
    def CheckStatus( self, status = None, errorMessage = None ):
        self.__log.debug( "TestTemplate.CheckStatus() method called." )
        
        self.__checkStatus(status, errorMessage)
        return None
    
# The Info method - Design paradigm, execution should never reach here    
    def Info(self):
        self.__log.debug( "TestTemplate.Info() method called." )

        self.CheckStatus( False, "Info() method not defined in test. This is a mandatory method that needs to be implemented." )
        return None

# The Main method - Design paradigm, execution should never reach here            
    def Main(self):
        self.__log.debug( "TestTemplate.Main() method called." )

        self.CheckStatus( False, "Main() method not defined in test. This is a mandatory method that needs to be implemented." )
        return None

# This method performs all operations on the key value pairs provided (configMap and testList) and returns a map of all arguments for a certain test
    def __getArguments(self, testName = None ):
        self.__log.debug( "TestTemplate.__getArguments() method called." )

        # Check parameters
        if( testName ==  None):
            self.CheckStatus(False, "Invalid arguments passed - \"testName\" not provided.")

        # Removing the .py extension if present
        testName = testName.split( ".py" )
        testName = testName[0]
        
        commonArgsMap = None
        testListMap = None
        argsMap = None
        
        # Collecting all the common arguments
        commonArgsMap = self.InterfaceMapLookUp( "configMap", "commonArguments" )
        
        # Collecting the test list
        testListMap = self.InterfaceMapLookUp( "configMap", "testList" )

        # Adding all the test specific arguments to the argsMap
        for entry in testListMap.keys():
            if( entry.__contains__( testName ) == True ):
                argsMap = testListMap[ entry ]
        
        if( argsMap == None ):
            self.__log.debug( testName + " has no test specific arguments.")
            
        # Adding all the common arguments to the argsMap
        for entry in commonArgsMap.keys():
            if( argsMap.__contains__( entry ) == True ):
                continue
            else:
                argsMap[ entry ] = commonArgsMap[ entry ]
        
        if( argsMap == None ):
            self.CheckStatus( False, testName + " has no common / test specific arguments.")

        return argsMap       

# Public Method - Interface for __getArguments method
    def GetArguments( self, testName = None ):
        self.__log.debug( "TestTemplate.GetArguments() method called." )
        
        return self.__getArguments( testName )

# This method forwards the command map to be executed to the InterfaceExecuteCommand method
    def __executeCommand(self, argsMap = None ):
        self.__log.debug( "TestTemplate.__executeCommand() method called." )

        # Check parameters
        if( argsMap == None ):
            self.CheckStatus(False, "Invalid arguments passed - \"argsMap\" not provided.")
        
        if( argsMap.__contains__( "command" ) != True ):
            self.CheckStatus(False, "\"command\" to execute not provided.")

        # ReturnStatus collects any argument passed that was a result of the execution of the command
        status = self.InterfaceExecuteCommand( argsMap )
        self.CheckStatus( status, "Test Failed - Could not execute command - " + argsMap["command"] + "." )
        
        return status
        
# Public Method - Interface for __executeCommand method
    def ExecuteCommand(self, argsMap = None ):
        self.__log.debug( "TestTemplate.ExecuteCommand() method called." )
        
        return self.__executeCommand( argsMap )
        
# This method forwards the testName and instance to the InterfaceGetLogObject method. Also it adds the test case log object handler to the local log object
    def __getLogObject(self, testName = None, instance = None ):
        self.__log.debug( "TestTemplate.__getLogObject() method called." )        

        # Check parameters
        if( testName == None ):
            self.CheckStatus( False, "\"testName\" variable not provided." )

        # Calling interface method
        argsMap = self.InterfaceGetLogObject( testName, instance )
        self.CheckStatus( argsMap, "Test Failed - Log object not obtained for test name - " + testName + "." )
        
        # Adding log handler to local log object
        self.__log.addHandler( argsMap[ "handler" ])
        
        return argsMap[ "logObject" ]

# Public Method - Interface for __getLogObject method
    def GetLogObject( self, testName = None, instance = None ):
        self.__log.debug( "TestTemplate.GetLogObject() method called." )

        return self.__getLogObject( testName, instance )

# This method forwards the status of the test execution to to the InterfaceTestComplete method
    def __testComplete(self, status = None):
        self.__log.debug( "TestTemplate.__testComplete() method called." )        

        # Check Parameters
        if( status == None ):
            self.CheckStatus( False, "Test Failed - Test completion status not provided")
        
        self.InterfaceTestComplete( status )
        return None
        
# Public Method - Interface for __testComplete method
    def TestComplete( self, status = None ):
        self.__log.debug( "TestTemplate.TestComplete() method called." )        

        self.__testComplete( status )
        return None

# This method forwards argsMap to the InterfaceDeleteDirectory method
    def __deleteDirectory( self, argsMap = None ):
        self.__log.debug( "TestTemplate.__deleteDirectory() method called" )

        # Check parameters
        if( argsMap == None ):
            self.CheckStatus( False, "Test Failed - No arguments sent to DeleteDirectory method.")

        # Calling interface method
        status =  self.IntefaceDeleteDirectory( argsMap )
        self.CheckStatus( status, "Test Failed - Could not delete directory " + os.path.join( argsMap["path"], argsMap["directoryName"] + ".") )
        
        return status
    
# The public interface for __deleteDirectory
    def DeleteDirectory( self, argsMap = None ):
        self.__log.debug( "TestTemplate.DeleteDirectory() method called" )

        return self.__deleteDirectory( argsMap )

# Creates the specified directory
    def __createDirectory( self, argsMap = None ):
        self.__log.debug( "TestTemplate.__createDirectory() method called" )

        # Check parameters
        if( argsMap == None ):
            self.CheckStatus( False, "Test Failed - No arguments sent to CreateDirectory method.")

        # Calling interface method            
        status =  self.IntefaceCreateDirectory( argsMap )
        self.CheckStatus( status, "Test Failed - Could not create directory " + os.path.join( argsMap["path"], argsMap["directoryName"] + ".") )
        
        return status

# The public interface for __createDirectory
    def CreateDirectory( self, argsMap = None ):
        self.__log.debug( "TestTemplate.CreateDirectory() method called" )

        return self.__createDirectory( argsMap )
        
# Copies the specified file
    def __copyFile( self, argsMap = None ):
        self.__log.debug( "TestTemplate.__copyFile() method called" )
        
        # Check parameters
        if( argsMap == None ):
            self.CheckStatus( False, "Test Failed - No arguments sent to CopyFile method.")
            
        # Calling interface method            
        status =  self.IntefaceCopyFile( argsMap )
        self.CheckStatus( status, "Test Failed - Could not copy file " + os.path.join( argsMap["sourcePath"], argsMap["sourceFileName"] + ".") )
        
        return status

# The public interface for __copyFile
    def CopyFile( self, argsMap = None ):
        self.__log.debug( "TestTemplate.CopyFile() method called" )

        return self.__copyFile( argsMap )

# This method creates the required test bed
    def __generateTestBed( self, argsMap = None ):
        self.__log.debug( "TestTemplate.__generateTestBed() method called" )
        
        # Check parameters
        if( argsMap == None ):
            self.CheckStatus( False, "Test Failed - No arguments sent to GenerateTestBed method.")

        # Calling interface method            
        status =  self.IntefaceGenerateTestBed( argsMap )
        self.CheckStatus( status, "Test Failed - Could not generate test bed.")
        
        return status
      
# The public interface for __generateTestBed
    def GenerateTestBed( self, argsMap = None ):
        self.__log.debug( "TestTemplate.GenerateTestBed() method called" )

        return self.__generateTestBed( argsMap )

# Upload / Download the files to and from the slice server
    def __uploadDownload( self, argsMap = None ):          
        self.__log.debug( "TestTemplate.__uploadDownload() method called" )
        
        # Check parameters
        if( argsMap == None ):
            self.CheckStatus( False, "Test Failed - No arguments sent to UploadDownload method.")

        # Calling interface method            
        status =  self.InterfaceUploadDownload( argsMap )
        self.CheckStatus( status, "Test Failed - Could not perform upload / download on specified directories .")
        
        return status

# The public interface for __uploadDownload
    def UploadDownload( self, argsMap = None ):
        self.__log.debug( "TestTemplate.UploadDownload() method called" )

        return self.__uploadDownload( argsMap )

# Compare two directories
    def __compareDirectories( self, argsMap = None ):
        self.__log.debug( "TestTemplate.__compareDirectories() method called" )

        # Check parameters
        if( argsMap == None ):
            self.CheckStatus( False, "Test Failed - No arguments sent to compare method.")

        # Calling interface method            
        status =  self.IntefaceCompare( argsMap )
        self.CheckStatus( status, "Test Failed - Could not perform compare on specified directories .")
        
        return status

# The public interface for __compare
    def CompareDirectories( self, argsMap = None ):
        self.__log.debug( "TestTemplate.CompareDirectories() method called" )

        return self.__compare( argsMap )

# Unmounts then mounts the mount point
    def __mountUnmount(self, mountPoint = None):
        self.__log.debug( "TestTemplate.__mountUnmount() method called." )

        return self.InterfaceMountUnmount( mountPoint )

# The public interface for __mountUnmount
    def MountUnmount(self, mountPoint = None):
        self.__log.debug( "TestTemplate.MountUnmount() method called." )

        return self.__mountUnmount( mountPoint )
