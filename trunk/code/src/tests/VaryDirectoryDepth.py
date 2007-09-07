# Test Name: VaryDirectoryDepth.py 
#---------------------------------
# Mandatory parameters
# --------------------
# iSCSIdrive           - The path to the slice servers (destination)
# testDirectory        - The directory where the test bed will be created
# maxFileCount         - The maximum number of files that will be created
# maxFileSize          - The maximum file size that will be created
# fileType             - The type of test file that needs to be generated ( Text / Binary )
# directoryDepth       - The maximum depth of the directory structure

# Optional Parameters
# -------------------
# stub                 - Binary variable - If True - Doesn't mount or unmount any partition   
# testBedPath          - If new test bed is not needed, then the path of an existing bed must be provided 
# testDirectoryName    - This defines the name of the directory on the slice server and the local directory name to where files are copied back from the slice server
# existingTestBedPath  - If new test bed is not needed, then the path of an existing bed must be provided 
# testBedDirectoryName - Defines the name of the test bed directory

import TestTemplate
from TestTemplate import *

class VaryDirectoryDepth( TestTemplate ):
# Class constructor
    def __init__(self, instance = 1):
        self.__instance = instance
        self.__log = self.GetLogObject( "VaryDirectoryDepth", instance )
        self.__log.debug( "VaryDirectoryDepth.__init__() method called." )
        self.__testBedPath = ""
        self.__argsMap = {}
        return None

# The mandatory Info method
    def Info(self):
        self.__log.debug( "VaryDirectoryDepth.Info() method called" )
        self.__log.info( "This test performs a UDC from the local drive to iSCSI device. The depth of the directory structure is varied and a set of files is placed at the root of each directory." )
        return True

# The mandatory Main method
    def Main( self, argsMap = None ):
        self.__log.debug( "VaryDirectoryDepth.Main() method called" )          
        if( argsMap != None ):
            self.__argsMap = argsMap
        else:
            self.__argsMap = self.GetArguments( "VaryDirectoryDepth.py" )

        if( self.StartTest() == True ):
            self.__log.info("Test VaryDirectoryDepth completed successfully.")
            self.TestComplete( True )
        else:
            self.CheckStatus( False,"Test VaryDirectoryDepth failed." )

        return None

# This method creates the required test bed
    def __generateTestBed( self, fileCount = None, maxFileSize = None, fileType = None, testBedPath = None, testBedDirectoryName = None ):
        self.__log.debug( "VaryDirectoryDepth.__generateTestBed() method called" )

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

# Creates the directory structure of defined depth
    def __createDirectoryStructure( self, directoryDepth = None, destinationPath = None, testDirectoryName = None ):
        self.__log.debug( "VaryDirectoryDepth.__createDirectoryStructure() method called" )
        
        directoryDepth = string.atoi( directoryDepth )
        if( directoryDepth <= 0 ):
            self.__checkStatus( False, "Directory depth invalid" )
		
        count = 0
        currentDirectory = os.getcwd()

        commandMap = {}
        commandMap["command"] = "createDirectory"
        commandMap["path"] = destinationPath
        commandMap["directoryName"] = testDirectoryName
        

        self.CheckStatus( self.ExecuteCommand( commandMap ), "Test Failed - Could not create the TestDirectory" )
        os.chdir( os.path.join( destinationPath, testDirectoryName ) )

        while count != directoryDepth:
            presentDirectory = os.getcwd()
            
            commandMap = {}
            commandMap["command"] = "createDirectory"
            commandMap["path"] = presentDirectory
            commandMap["directoryName"] = `count`

            self.CheckStatus( self.ExecuteCommand( commandMap ), "Test Failed - Could not create test directory at depth " + `count` )
            os.chdir( os.path.join( presentDirectory, `count` ) )
			
            for fileName in os.listdir( self.__testBedPath ):
                commandMap = {}
                commandMap["command"] = "copyFile"
                commandMap["sourcePath"] = self.__testBedPath
                commandMap["sourceFileName"] = fileName
                commandMap["destinationPath"] = os.getcwd()
                
                self.CheckStatus( self.ExecuteCommand( commandMap ), "Test Failed - Could not copy file " + fileName )
			
            count += 1

		# Returning to the working directory
        os.chdir( currentDirectory )

        return True

# Compare two directories
    def __compare( self, sourcePath, destinationPath ):
        self.__log.debug( "VaryDirectoryDepth.__compare() method called" )
        depth = 0
		
		# For each test bed perform the required operation
        for root, dirs, files in os.walk( sourcePath, topdown = False ):
            for name in files:
                commandMap = {}
                commandMap[ "command" ] = "compareFile"
                commandMap[ "sourcePath" ] = root
                commandMap[ "destinationPath" ] = destinationPath
                commandMap[ "sourceFileName" ] = name

                self.CheckStatus( self.ExecuteCommand( commandMap ), "Test failed - File comparison failed on file " + name + " at " + root )
            self.__log.debug( "All files at directory depth - " + `depth` + " successfully compared." )
            depth += 1

        self.__log.info( "All directories successfully compared")
        return True

# Start processing the test from this point		
    def StartTest( self ):
        self.__log.debug( "VaryDirectoryDepth.__StartTest() method called" )

        self.__log.info( "Phase - I: Generating test bed" )
        self.__testBedPath = False
        # if - Create new test bed
        if( self.__argsMap.__contains__("existingTestBedPath") != True ):
                
            if( self.__argsMap.__contains__("testBedDirectoryName") == True ):
                testBedDirectoryName = self.__argsMap["testBedDirectoryName"]
            else:
                testBedDirectoryName = "VaryDirectoryDepth-" + `self.__instance` + " -- testBed"

            if( self.__argsMap.__contains__("testBedPath") == True ):
                testBedPath = self.__argsMap["testBedPath"]
            else:
                testBedPath = None

            self.__testBedPath = self.__generateTestBed( self.__argsMap[ "maxFileCount" ], self.__argsMap[ "maxFileSize" ], self.__argsMap[ "fileType" ], testBedPath, testBedDirectoryName )
        # else - Provide path to existing test bed
        else:
            self.__testBedPath = self.__argsMap[ "existingTestBedPath" ]
            
        self.CheckStatus( self.__testBedPath, "Test failed - Test bed could not be generated / located successfully." )                        

		# Create remote directory structure 
        self.__log.info( "Phase - II: Starting creation of remote directory structure" )
        if( self.__argsMap.__contains__("testDirectoryName") == True ):
            sliceServerTestDirectoryName = self.__argsMap["testDirectoryName"]
        else:
            # Creating the log file for the specific test
            sliceServerTestDirectoryName = "VaryDirectoryDepth-" + `self.__instance` + " -- SliceServer - TestDirectory"

        status = self.__createDirectoryStructure( self.__argsMap[ "directoryDepth" ], self.__argsMap[ "iSCSIdrive" ], sliceServerTestDirectoryName )
        self.CheckStatus( status, "Test failed - Creation of remote directory structure failed" )	

        # Unmount / Mount the Slice Server mount point
        if( os.name == "posix" and ( ( self.__argsMap.__contains__( "stub" ) == True and self.__argsMap[ "stub" ].lower() == "false" ) or  self.__argsMap.__contains__( "stub" ) == False ) ) :
            self.CheckStatus( self.MountUnmount(self.__argsMap[ "iSCSIdrive" ]), "Test Failed - error unmounting and mounting iSCSI device.")
        else:
            self.__log.info( "Phase - III: Skipping Phase III (Linux / Mac) specific" )
			
		# Create local directory structure
        self.__log.info( "Phase - IV: Starting creation of local directory structure" )
        if( self.__argsMap.__contains__("testDirectoryName") == True ):
            localTestDirectoryName = self.__argsMap["testDirectoryName"]
        else:
            # Creating the log file for the specific test
            now = time.localtime(time.time())
            tempFileName = time.strftime("%Y-%m-%d : %H-%M-%S -- ", now)
            localTestDirectoryName = "VaryDirectoryDepth-" + `self.__instance` + " -- Local - TestDirectory"

        status = self.__createDirectoryStructure( self.__argsMap[ "directoryDepth" ], self.__argsMap[ "testDirectory" ], localTestDirectoryName)
        self.CheckStatus( status, "Test failed - Creation of local directory structure failed" )	

        # Compare operation
        self.__log.info( "Phase - V: Starting compare operation" )
        status = self.__compare( os.path.join( self.__argsMap[ "testDirectory" ], localTestDirectoryName ), self.__testBedPath )
        self.CheckStatus( status, "Test failed - compare operation failed" )

        return True