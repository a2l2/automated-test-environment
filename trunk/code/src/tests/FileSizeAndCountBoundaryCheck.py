# Test Name: FileSizeAndCountBoundaryCheck.py
#--------------------------------------------
# Mandatory parameters
# --------------------
# iSCSIdrive           - The path to the slice servers (destination)
# testDirectory        - The directory where the test bed will be created
# maxFileCount         - The maximum number of files that will be created
# maxFileSize          - The maximum file size that will be created
# fileType             - The type of test file that needs to be generated ( Text / Binary )
#
# Optional Parameters
# -------------------
# stub                 - Binary variable - If True - Doesn't mount or unmount any partition   
# fileSizeIterator     - Steps in which the file size will be incremented
# fileCountIterator    - Steps in which the file count will be incremented
# minFileSize          - The smallest file size the test will start with
# minFileCount         - The smallest file count the test will start with
# existingTestBedPath  - If new test bed is not needed, then the path of an existing bed must be provided 
# testDirectoryName    - This defines the name of the directory on the slice server and the local directory name to where files are copied back from the slice server
# testBedDirectoryName - Defines the name of the test bed directory

import TestTemplate
from TestTemplate import *

class FileSizeAndCountBoundaryCheck( TestTemplate ):
# Class constructor
    def __init__(self, instance = 1):
        self.__instance = instance
        self.__log = self.GetLogObject( "FileSizeAndCountBoundaryCheck", instance )
        self.__log.debug( "FileSizeAndCountBoundaryCheck.__init__() method called." )
        self.__testBedPath = ""
        self.__argsMap = {}
        return None

# The mandatory Info method
    def Info(self):
        self.__log.debug( "FileCountAndSizeBoundaryCheck.Info() method called" )
        self.__log.info( "This test performs a UDC from the local drive to iSCSI device. The file count and file size is varied until the system crashes or until the celing is reached." )
        return True

# The mandatory Main method
    def Main( self, argsMap = None ):
        self.__log.debug( "FileCountAndSizeBoundaryCheck.Main() method called" )          
        if( argsMap != None ):
            self.__argsMap = argsMap
        else:
            self.__argsMap = self.GetArguments( "FileCountAndSizeBoundaryCheck.py" )
            
        self.CheckStatus( self.StartTest(), "FileCountAndSizeBoundaryCheck: failed to completed successfully" )
        self.TestComplete( True )

# This method creates the required test bed
    def __generateTestBed( self, fileCount = None, maxFileSize = None, fileType = None, testBedPath = None, testBedDirectoryName = None ):
        self.__log.debug( "FileSizeAndCountBoundaryCheck.__generateTestBed() method called" )
        
        # Defining the command map
        commandMap = {}
        commandMap[ "command" ] = "createTestBed"
        commandMap[ "maxFileSize" ] = maxFileSize
        commandMap[ "fileType" ] = fileType
        commandMap[ "fileCount" ] = fileCount

        if( testBedDirectoryName != None ):
            commandMap[ "testBedDirectoryName" ] = testBedDirectoryName

        if( testBedPath != None ):
            commandMap[ "testBedPath" ] = testBedPath
    
        # Executing the command and returning the result
        return self.ExecuteCommand( commandMap )    

# Upload / Download the files to and from the slice server
    def __uploadDownload( self, sourcePath = None, destinationPath = None, destinationTestDirectoryName = None, sourceTestDirectoryName = None ):          
        self.__log.debug( "FileSizeAndCountBoundaryCheck.__uploadDownload() method called" )

        # Defining the command map
        commandMap = {}
        commandMap["command"] = "uploadDownload"
        commandMap["sourcePath"] = sourcePath
        commandMap["destinationPath"] = destinationPath
        commandMap["testBedPath"] = self.__testBedPath
        
        if(sourceTestDirectoryName != None):
            commandMap["sourceTestDirectoryName"] = sourceTestDirectoryName

        if(destinationTestDirectoryName != None):
            commandMap["destinationTestDirectoryName"] = destinationTestDirectoryName

        # Executing the command and returning the result        
        return self.UploadDownload(commandMap)


# Compare two directories
    def __compare( self, sourcePath, destinationPath ):
        self.__log.debug( "FileSizeAndCountBoundaryCheck.__compare() method called" )

        # Defining the command map
        commandMap = {}
        commandMap["command"] = "compareDirectories"
        commandMap["sourcePath"] = sourcePath
        commandMap["destinationPath"] = destinationPath
        commandMap["testBedPath"] = self.__testBedPath
        

        # Executing the command and returning the result        
        return self.ExecuteCommand(commandMap)

# Start executing the test 
    def StartTest( self ):
        self.__log.debug( "FileSizeAndCountBoundaryCheck.__StartTest() method called" )
        testDirectoryName = ""
        
        # Setting default values to all variables
        executionCount = 0
        
        curFileCount = 1
        fileCountIterator = 1
        
        curFileSize = 0
        fileSizeIterator = 1024

        iteration = 0
        
        if( self.__argsMap.__contains__( "minFileSize" ) ):
            curFileSize = string.atoi( self.__argsMap[ "minFileSize" ] )
        
        if( self.__argsMap.__contains__( "minFileCount" ) ):
            curFileCount = string.atoi( self.__argsMap[ "minFileCount" ] )

        if( self.__argsMap.__contains__( "fileSizeIterator" ) ):
            fileSizeIterator = string.atoi( self.__argsMap[ "fileSizeIterator" ] )
            
        if( self.__argsMap.__contains__( "fileCountIterator" ) ):
            fileCountIterator = string.atoi( self.__argsMap[ "fileCountIterator" ] )
            
        while( curFileCount <= string.atoi( self.__argsMap[ "maxFileCount" ] ) or  curFileSize <= string.atoi( self.__argsMap[ "maxFileSize" ] ) ):
        # Iterate through all the phases until maxFileCount and maxFileSize has been reached       

            self.__log.info( "Phase - I: Generating test bed" )
            self.__testBedPath = False
            # if - Create new test bed
            if( self.__argsMap.__contains__("existingTestBedPath") != True ):
                
                if( self.__argsMap.__contains__("testBedDirectoryName") == True ):
                    testBedDirectoryName = self.__argsMap["testBedDirectoryName"]
                else:
                    testBedDirectoryName = "FileSizeAndCountBoundaryCheck-" + `self.__instance` + " -- testBed"

                if( self.__argsMap.__contains__("testBedPath") == True ):
                    testBedPath = self.__argsMap["testBedPath"]
                else:
                    testBedPath = None

                self.__testBedPath = self.__generateTestBed( `curFileCount`, `curFileSize`, self.__argsMap[ "fileType" ], testBedPath, testBedDirectoryName )
            # else - Provide path to existing test bed
            else:
                self.__testBedPath = self.__argsMap[ "existingTestBedPath" ]
            
            self.CheckStatus( self.__testBedPath, "Test failed - Test bed could not be generated / located successfully." )                        

            # Upload operation
            self.__log.info( "Phase - II: Starting the upload operation" )
            if( self.__argsMap.__contains__("testDirectoryName") == True ):
                sliceServerTestDirectoryName = self.__argsMap["testDirectoryName"]
            else:
                # Creating the log file for the specific test
                sliceServerTestDirectoryName = "FileSizeAndCountBoundaryCheck-" + `self.__instance` + " -- Slice Server - TestDirectory"
                
            status = self.__uploadDownload( self.__testBedPath, self.__argsMap[ "iSCSIdrive" ],  sliceServerTestDirectoryName, None )
            self.CheckStatus( status, "Test failed - upload operation failed" )    
            
            # Unmount / Mount the Slice Server mount point
            if( os.name == "posix" and ( ( self.__argsMap.__contains__( "stub" ) == True and self.__argsMap[ "stub" ].lower() == "false" ) or  self.__argsMap.__contains__( "stub" ) == False ) ) :
                self.CheckStatus( self.MountUnmount(self.__argsMap[ "iSCSIdrive" ]), "Test Failed - error unmounting and mounting iSCSI device.")
            else:
                self.__log.info( "Phase - III: Skipping Phase III (Linux / Mac) specific" )
            
            # Download operation
            self.__log.info( "Phase - IV: Starting the download operation" )
            if( self.__argsMap.__contains__("testDirectoryName") == True ):
                localTestDirectoryName = self.__argsMap["testDirectoryName"]
            else:
                # Creating the log file for the specific test
                localTestDirectoryName = "FileSizeAndCountBoundaryCheck-" + `self.__instance` + " -- Local - TestDirectory"

            status = self.__uploadDownload( self.__argsMap[ "iSCSIdrive" ], self.__argsMap[ "testDirectory" ], localTestDirectoryName, sliceServerTestDirectoryName )
            self.CheckStatus( status, "Test failed - download operation failed" )    

            # Compare operation
            self.__log.info( "Phase - V: Starting compare operation" )
            status = self.__compare( self.__testBedPath, self.__argsMap[ "testDirectory" ] )
            self.CheckStatus( status, "Test failed - upload operation failed" )

            # Incrementing file size and file count
            self.__log.info( "Successfully completed iteration " + `iteration` + " with a max file size of " + `curFileSize` + " bytes and a file count of " + `curFileCount` )
            
            if( curFileCount <= string.atoi( self.__argsMap[ "maxFileCount" ] ) ):
                curFileCount += fileCountIterator
            else:
                curFileCount = string.atoi( self.__argsMap[ "maxFileCount" ] )
                
            if( curFileSize <= string.atoi( self.__argsMap[ "maxFileSize" ] ) ):
                curFileSize += fileSizeIterator
            else:
                curFileSize = string.atoi( self.__argsMap[ "maxFileSize" ] ) + 1
                    
            iteration += 1
             
        return True