# This is the test template that must be inherited by each test case
import common.BaseClass
from common.BaseClass import *

class Interface( BaseClass ):
# This method defines the private member variables whenever they are needed 
    def __securityChecker( object = None ):
        if( object.lower() == "log" ):
            return logging.getLogger( 'Interface.py' )
        else:
            self.__checkStatus(False, "Security violation - Invalid object provided.")
    
# Private Member Variables    
    __log = __securityChecker( "log" )

# Interface for BaseClassCheckStatus
    def __checkStatus( self, status = None, errorMessage = None ):
        self.__log.debug( "Interface.__checkStatus() method called." )
        
        self.BaseClassCheckStatus( status, errorMessage )
        return None

# Public Method - Interface for __checkStatus
    def InterfaceCheckStatus( self, status = None, errorMessage = None ):
        self.__log.debug( "Interface.InterfaceCheckStatus() method called." )
        
        self.__checkStatus( status, errorMessage )
        return None

# Interface for BaseClassMapLookUp
    def __mapLookUp( self, mapName = None, entryName = None ):
        self.__log.debug( "Interface.__mapLookUp() method called." )            
        
        return self.BaseClassMapLookUp( mapName, entryName )

# Public Method - Interface for __mapLookUp
    def InterfaceMapLookUp( self, mapName = None, entryName = None ):
        self.__log.debug( "Interface.InterfaceMapLookUp() method called." )            
        
        return self.__mapLookUp( mapName, entryName )

# Interface for BassClassExecuteCommand
    def __executeCommand(self, argsMap = None ):
        self.__log.debug( "Interface.__executeCommand() method called." )

        # Return status & collects any argument passed that was a result of the execution of the command
        return self.BaseClassExecuteCommand( argsMap )

# Public Method - Interface for __executeCommand
    def InterfaceExecuteCommand(self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceExecuteCommand() method called." )

        # Return status & collects any argument passed that was a result of the execution of the command
        return self.__executeCommand( argsMap )

# Interface for BaseClassGetLogObject method
    def __getLogObject( self, testName = None, instance = None ):
        self.__log.debug( "Interface.__getLogObject() method called." )

        argsMap = self.BaseClassGetLogObject( testName, instance )

        # Adding log handler to local log object
        self.__log.addHandler( argsMap[ "handler" ])
        
        return argsMap

# Public Method - Interface for __getLogObject method
    def InterfaceGetLogObject( self, testName = None, instance = None ):
        self.__log.debug( "Interface.InterfaceGetLogObject() method called." )

        return self.__getLogObject( testName, instance )

# Interface for BaseClassTestComplete method
    def __testComplete(self, status = None):
        self.__log.debug( "Interface.__testComplete() method called." )        

        self.BaseClassTestComplete( status )
        return None
        
# Public Method - Interface for __testComplete method
    def InterfaceTestComplete( self, status = None ):
        self.__log.debug( "Interface.InterfaceTestComplete() method called." )        

        self.__testComplete( status )
        return None

# Interface for BaseClassCheckArguments
    def __checkArguments( self, argsMap = None ):
        self.__log.debug( "Interface.__checkArguments() method called." )            
        
        return self.BaseClassCheckArguments( argsMap )

# Public Method - Interface for __checkArguments
    def InterfaceCheckArguments( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceCheckArguments() method called." )            
        
        return self.__checkArguments( argsMap )

# Calls the InterfaceExecute command with command name as deleteDirectory
    def __deleteDirectory(self, argsMap = None):
        self.__log.debug( "Interface.__deleteDirectory() method called." )        

        if(argsMap == None):
            self.CheckStatus( False, "Interface Error - \"argsMap\" not provided" )

        # A list with all required parameters
        reqArgsList = []
        reqArgsList.append( "deleteDirectory" )
        reqArgsList.append( "directoryName" )
        reqArgsList.append( "path" )

        # Parameter passing map
        checkMap = {}
        checkMap[ "reqArgsList" ] = reqArgsList
        checkMap[ "argsMap" ] = argsMap

        # Check if all parameters provided for
        self.CheckStatus( self.InterfaceCheckArguments( checkMap ), "Interface Error - All arguments not provided." )
        
        # The command map that will get executed
        commandMap = {}
        commandMap[ "command" ] = "deleteDirectory"
        commandMap[ "directoryName" ] = argsMap["dirName"]
        commandMap[ "path" ] = argsMap["path"]
        
        # Calling the execute method
        status = self.InterfaceExecuteCommand( commandMap )
        self.CheckStatus( status, "Interface Error - Execution of DeleteDirectory failed." )
        
        return status

# Public Method - Interface for __deleteDirectory method
    def InterfaceDeleteDirectory( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceDeleteDirectory() method called." )        

        return self.__deleteDirectory( argsMap )

# Calls the InterfaceExecute command with command name as createDirectory
    def __createDirectory(self, argsMap = None):
        self.__log.debug( "Interface.__createDirectory() method called." )        
        
        # A list with all required parameters
        reqArgsList = []
        reqArgsList.append( "createDirectory" )
        reqArgsList.append( "path" )
        reqArgsList.append( "directoryName" )

        # Parameter passing map
        checkMap = {}
        checkMap[ "reqArgsList" ] = reqArgsList
        checkMap[ "argsMap" ] = argsMap

        # Check if all parameters provided for
        self.CheckStatus( self.InterfaceCheckArguments( checkMap ), "Test Failed - All arguments not provided." )

        # The command map that will get executed
        commandMap = {}
        commandMap[ "command" ] = "createDirectory"
        commandMap[ "path" ] = argsMap["path"]
        commandMap[ "directoryName" ] = argsMap["directoryName"]
        if( argsMap.__contains__( "removePrevious" ) == True ):
            commandMap[ "removePrevious" ] = argsMap["removePrevious"]

        # Calling the execute method
        status = self.InterfaceExecuteCommand( commandMap )
        self.CheckStatus( status, "Test Failed - Execution of CreateDirectory failed." )
        
        return status

# The public interface for __createDirectory
    def InterfaceCreateDirectory( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceCreateDirectory() method called" )

        return self.__createDirectory( argsMap )

# Calls the InterfaceExecute command with command name as copyFile        
    def __copyFile(self, argsMap = None):
        self.__log.debug( "Interface.__copyFile() method called." )        
        
        # A list with all required parameters
        reqArgsList = []
        reqArgsList.append( "copyFile" )
        reqArgsList.append( "sourcePath" )
        reqArgsList.append( "destinationPath" )
        reqArgsList.append( "sourceFileName" )

        # Parameter passing map
        checkMap = {}
        checkMap[ "reqArgsList" ] = reqArgsList
        checkMap[ "argsMap" ] = argsMap

        # Check if all parameters provided for
        self.CheckStatus( self.InterfaceCheckArguments( checkMap ), "Test Failed - All arguments not provided." )

        # The command map that will get executed
        commandMap = {}
        commandMap[ "command" ] = "copyFile"
        commandMap[ "sourcePath" ] = argsMap["sourcePath"]
        commandMap[ "destinationPath" ] = argsMap["destinationPath"]
        commandMap[ "sourceFileName" ] = argsMap["sourceFileName"]
        if( argsMap.__contains__( "destinationFileName" ) == True ):
            commandMap[ "destinationFileName" ] = argsMap["destinationFileName"]

        # Calling the execute method
        status = self.InterfaceExecuteCommand( commandMap )
        self.CheckStatus( status, "Test Failed - Execution of CopyFile failed." )
        
        return status

# The public interface for __copyFile
    def InterfaceCopyFile( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceCopyFile() method called" )

        return self.__copyFile( argsMap )

# Calls the InterfaceExecute command with command name as generateTestBed        
    def __generateTestBed(self, argsMap = None):
        self.__log.debug( "Interface.__generateTestBed() method called" )
        
        # A list with all required parameters
        reqArgsList = []
        reqArgsList.append( "createTestBed" )
        reqArgsList.append( "maxFileSize" )
        reqArgsList.append( "fileType" )
        reqArgsList.append( "fileCount" )
        
        # Parameter passing map
        checkMap = {}
        checkMap[ "reqArgsList" ] = reqArgsList
        checkMap[ "argsMap" ] = argsMap

        # Check if all parameters provided for
        self.CheckStatus( self.InterfaceCheckArguments( checkMap ), "Interface Error - All arguments not provided." )

        # The command map that will get executed
        commandMap = {}
        commandMap[ "command" ] = "createTestBed"
        commandMap[ "maxFileSize" ] = argsMap["maxFileSize"]
        commandMap[ "fileType" ] = argsMap["fileType"]
        commandMap[ "fileCount" ] = argsMap["fileCount"]

        if( argsMap.__contains__("testBedPath") == True ):
            commandMap[ "testBedPath" ] = argsMap[ "testBedPath" ]
        
        if( argsMap.__contains__("testBedDirectoryName") == True ):
            commandMap[ "testBedDirectoryName" ] = argsMap[ "testBedDirectoryName" ]
            
        if( argsMap.__contains__("removePrevious") == True ):
            commandMap[ "removePrevious" ] = argsMap[ "removePrevious" ]

        
        # Calling the execute method
        status = self.InterfaceExecuteCommand( commandMap )
        self.CheckStatus( status, "Test Failed - Execution of GenerateTestBed failed." )
        
        return status

# The public interface for __generateTestBed
    def InterfaceGenerateTestBed( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceGenerateTestBed() method called" )

        return self.__generateTestBed( argsMap )

# Performs a copy of all files to and from the slice server
    def __uploadDownload(self, argsMap = None):
        self.__log.debug( "Interface.__uploadDownload() method called" )

        # A list with all required parameters
        reqArgsList = []
        reqArgsList.append( "uploadDownload" )
        reqArgsList.append( "sourcePath" )
        reqArgsList.append( "destinationPath" )
        reqArgsList.append( "testBedPath" )
        
        # Parameter passing map
        checkMap = {}
        checkMap[ "reqArgsList" ] = reqArgsList
        checkMap[ "argsMap" ] = argsMap

        # Check if all parameters provided for
        self.CheckStatus( self.InterfaceCheckArguments( checkMap ), "Interface Error - All arguments not provided." )

        sourcePath = argsMap["sourcePath"]
        destinationPath = argsMap["destinationPath"]
        testBedPath = argsMap["testBedPath"]

        # Getting the destinationTestDirectoryName
        if( argsMap.__contains__( "destinationTestDirectoryName" ) == True ):
            destinationTestDirectoryName = argsMap[ "destinationTestDirectoryName" ]
        else:
            destinationTestDirectoryName = "TestDirectory"

        # Getting the sourceTestDirectoryName
        if( argsMap.__contains__( "sourceTestDirectoryName" ) == True ):
            sourceTestDirectoryName = argsMap[ "sourceTestDirectoryName" ]
        else:
            sourceTestDirectoryName = "TestDirectory"

        # Create the test directory on destination
        tempMap = {}
        tempMap["command"] = "createDirectory"
        tempMap["path"] = destinationPath
        tempMap["directoryName"] = destinationTestDirectoryName
        
        self.InterfaceCheckStatus( self.InterfaceCreateDirectory( tempMap ), "Interface Error - Could not create the TestDirectory" )        
        destination = os.path.join( destinationPath, destinationTestDirectoryName )

        # If copying from test bed to the slice server
        if( sourcePath == testBedPath ):
            source = sourcePath
        else:
            source = os.path.join( sourcePath, sourceTestDirectoryName )

        
        counter = 0

        # Gather list of files in current test bed
        for fileList in os.listdir( source ):
            counter += 1
            
            # Defining values in the tempMap
            tempMap = {}
            tempMap["command"] = "copyFile"
            tempMap["sourceFileName"] = fileList
            tempMap["sourcePath"] = source
            tempMap["destinationPath"] = destination
            
            # Calling execute method
            status = self.InterfaceCopyFile( tempMap )
            self.CheckStatus( status, "Test failed - could not copy file " + fileList )
            self.__log.debug(" File " + fileList + " copied from " + source + " to " + destination + " successfully." )
            
        self.__log.info( `counter` + " files copied from " + source + " to " + destination + " successfully" )
    
        return True

# The public interface for __uploadDownload
    def InterfaceUploadDownload( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceUploadDownload() method called" )

        return self.__uploadDownload( argsMap )

# Compare two directories
    def __compareDirectories( self, argsMap = None ):
        self.__log.debug( "Interface.__compareDirectories() method called" )

        # A list with all required parameters
        reqArgsList = []
        reqArgsList.append( "compareDirectories" )
        reqArgsList.append( "sourcePath" )
        reqArgsList.append( "destinationPath" )
        reqArgsList.append( "testBedPath" )
        
        # Parameter passing map
        checkMap = {}
        checkMap[ "reqArgsList" ] = reqArgsList
        checkMap[ "argsMap" ] = argsMap

        # Check if all parameters provided for
        self.CheckStatus( self.InterfaceCheckArguments( checkMap ), "Test Failed - All arguments not provided." )

        destinationPath = argsMap["destinationPath"]
        sourcePath = argsMap["sourcePath"]
        testBedPath = argsMap["testBedPath"]

        # If copying from test bed to the slice server
        if( sourcePath == testBedPath ):
            source = sourcePath
        else:
            source = os.path.join( sourcePath, testDirectoryName )

        if( destinationPath == testBedPath ):
            destination = destinationPath
        else:
            destination = os.path.join( destinationPath, testDirectoryName )

        # For each test bed perform the required operation
        for root, dirs, files in os.walk( source, topdown = False ):
            for name in files:
                commandMap = {}
                commandMap[ "command" ] = "compareFile"
                commandMap[ "sourcePath" ] = root
                commandMap[ "destinationPath" ] = destination
                commandMap[ "sourceFileName" ] = name

                self.InterfaceCheckStatus( self.InterfaceExecuteCommand( commandMap ), "Test failed - File comparison failed on file " + name + " at " + root )
                self.__log.debug( "File: " + name + " compared successfully." )

        self.__log.info( "All directories successfully compared")
        return True

# The public interface for __compareDirectories
    def InterfaceCompareDirectories( self, argsMap = None ):
        self.__log.debug( "Interface.InterfaceCompareDirectories() method called" )

        return self.__compareDirectories( argsMap )

# Unmounts then mounts the mount point
    def __mountUnmount(self, mountPoint = None):
        self.__log.debug( "Interface.__mountUnmount() method called." )

        return self.BaseClassMountUnmount( mountPoint )

# The public interface for __mountUnmount
    def InterfaceMountUnmount(self, mountPoint = None):
        self.__log.debug( "Interface.InterfaceMountUnmount() method called." )

        return self.__mountUnmount( mountPoint )

