# This is the base class from which all other classes are derived

import sys
import os
import string
import logging
import commands
import time
import random

# Import of all common user defined Python modules 
import common
from common import *

class BaseClass:
# This method defines the private member variables whenever they are needed 
    def __securityChecker( object = None ):
        if( object.lower() == "log" ):
            return logging.getLogger( 'BaseClass.py' )
        elif( object.lower() == "configmap" ):
            object = MapCreator()
            return getattr ( object, "GetConfigMap" ) () 
        elif( object.lower() == "objectmap" ):
            object = MapCreator()
            return getattr ( object, "GetObjectMap" ) () 
        elif( object.lower() == "logobjectmap" ):
            object = MapCreator()
            return getattr ( object, "GetLogObjectMap" ) () 

# Private Member Variables
    __log = __securityChecker( "log" )
    __configMap = __securityChecker( "configMap" )
    __objectMap = __securityChecker( "objectMap" )
    __logObjectMap = __securityChecker( "logObjectMap" )
    __logHandler = None
    
# This method checks the status of any method call. If fail it renames the log file and exist
    def __checkStatus( self, status, errorMessage ):
        self.__log.debug( "BaseClass.__checkStatus() method called." )

        if( status == False ):
            self.__log.error( "Test failed - " + errorMessage )
            
            # Closing the file handler
            fileName = self.__logHandler.baseFilename
            destinationFileName = ""
            self.__log.removeHandler( self.__logHandler )

            # Remove the log handler from each of the lib/ classes
            for entry in self.__logObjectMap.keys():
                self.__logObjectMap[entry].removeHandler( self.__logHandler )
                
            self.__logHandler.close() 

            # Defining the destinationFileName
            destinationFileName = fileName.split( "PROCESSING.log" )
            destinationFileName = destinationFileName[0] + " FAILED.log"
            
            # Calling the common commands class
            argsMap = {}
            argsMap[ "command" ] = "renameFile"
            argsMap[ "path" ] = self.__configMap[ "logPath" ]
            argsMap[ "sourceFileName" ] = fileName
            argsMap[ "destinationFileName" ] = destinationFileName
            
            self.BaseClassCheckStatus(self.BaseClassExecuteCommand( argsMap ), "Could not rename failed test, log file output." )

            sys.exit( 1 )
        
        return None

# This is the public method for the __checkStatus method
    def BaseClassCheckStatus( self, status = None, errorMessage = None ):
        self.__log.debug( "BaseClass.BaseClassCheckStatus() method called." )
    
        # If any of the arguments not passed by caller method
        if( status != None and errorMessage != None ):
            self.__checkStatus( status, errorMessage )
        else:
            self.__checkStatus(False, "Invalid arguments passed - \"status\" or \"errorMessage\" not provided.")

        return None

# This method gets called when the test operation completes successfully
    def __testComplete(self):
            
            # Closing the file handler
            fileName = self.__logHandler.baseFilename
            destinationFileName = ""
            self.__log.removeHandler( self.__logHandler )

            # Remove the log handler from each of the lib/ classes
            for entry in self.__logObjectMap.keys():
                self.__logObjectMap[entry].removeHandler( self.__logHandler )
                
            self.__logHandler.close() 

            # Defining the destinationFileName
            destinationFileName = fileName.split( "PROCESSING.log" )
            destinationFileName = destinationFileName[0] + "PASSED.log"
            
            # Calling the common commands class
            argsMap = {}
            argsMap[ "command" ] = "renameFile"
            argsMap[ "path" ] = self.__configMap[ "logPath" ]
            argsMap[ "sourceFileName" ] = fileName
            argsMap[ "destinationFileName" ] = destinationFileName
            
            self.BaseClassCheckStatus( self.BaseClassExecuteCommand( argsMap ), "Could not rename passed test, log file output." )

            sys.exit( 0 )

# This is the public method for the __testComplete method
    def BaseClassTestComplete(self, status = None):
        if( status == None or status == False ):
            self.BaseClassCheckStatus(False, "Test completed unsuccessfully")
        else:
            self.__testComplete()

# This method looks up the configMap and returns all arguments associated with an entryName
# Special values for entryName - 
#    "commonArguments" - returns all the common arguments of the map except those part of the TestList key
#    "testList"        - returns all arguments in the testList argument list
    def __mapLookUp( self, mapName = None, entryName = None ):
        self.__log.debug( "BaseClass.__mapLookUp() method called." )
        
        argsMap = {}
        
        # If configuration map look up is requested
        if( mapName.lower() == "configmap" ):
            mapName = self.__configMap
        # If object map look up is requested
        elif( mapName.lower() == "objectmap" ):
            mapName = self.__objectMap
        # Invalid map name provided
        else:
            self.BaseClassCheckStatus( False, mapName + " is invalid." )

        # Flooding argument map with all the generic arguments (i.e. all values except those part of the testList key)
        if( entryName.lower() == "commonarguments" ):
            for elements in mapName.keys():
                if( elements.lower() == "testlist" ):
                    continue
                argsMap[ elements ] = mapName[ elements ]
        # Flooding argument map will all agruments in the testList argument list
        elif (entryName.lower() == "testlist" ):
            argsMap = mapName[ "testList" ]
        # Flooding argument map with only those arguments that match the entryName condition
        else:
            for elements in mapName.keys():
                if( elements == entryName ):
                    argsMap[ elements ] = mapName[ elements ]

        # If argument map not forwarded correctly from private member method
        if( argsMap == {} ):
            self.BaseClassCheckStatus( False, entryName + " not found in " + mapName + "." )
        
        return argsMap

# This is the public method for         
    def BaseClassMapLookUp( self, mapName = None, entryName = None ):
        self.__log.debug( "BaseClass.BaseClassMapLookUp() method called." )            
        
        return self.__mapLookUp( mapName, entryName )

# This method gets called when it is required to dynamically call a library method
    def __executeCommand( self, argumentMap ):
        self.__log.debug( "BaseClass.__executeCommand() method called." )

        # Check parameters
        if( argumentMap == None or argumentMap.__contains__("command") != True ):
            self.BaseClassCheckStatus( False, "argument map provided is invalid." )

        status = None
        counter = len( self.__objectMap.keys() )
        
        # Iterating over each entry in the objectMap - .py files in the lib/ directory
        for iterator in range( 0, counter ):
            moduleMap = {}
            moduleMap = getattr( self.__objectMap[ iterator ], "GetCommandMap" ) ()
            
            # Iterating over each command defined in the .py file
            for key in moduleMap.keys():
                if( key.lower() == argumentMap[ "command" ].lower() ):
                    # Check to see whether required function actually exists and whether it can be called
                    try:
                        funcCall = getattr(self.__objectMap[ iterator], key)
                    except LookupError, errorMessage:
                        self.__log.debug( "Could not find " + key + " - " + errorMessage )

                    # Calling the specified method
                    try:
                        status = funcCall( argumentMap )
                        self.BaseClassCheckStatus( status, "Could not execute command - " + argumentMap[ "command" ] )
                    except SyntaxError, errorMessage:
                        self.BaseClassCheckStatus( False, "Executing method " + key + " failed - " + errorMessage )

                    return status
                else:
                    continue
                
            # If command not found in current object map
            continue
        # If execution ever reaches here, that means the command was not found.
        self.BaseClassCheckStatus( False, "Could not find specified command - " + argumentMap[ "command" ] )

# This is the public method for the __executeCommand method
    def BaseClassExecuteCommand( self, argsMap = None ):
        self.__log.debug( "BaseClass.BaseClassExecuteCommand() method called." )

        return  self.__executeCommand( argsMap )
        
# This method returns a log object based on the fileName and instance
    def __getLogObject( self, fileName = None, instance = 1 ):
        self.__log.debug( "BaseClass.__getLogObject() method called." )
        
        # Removing the .py extension, if added to the file name
        fileName = fileName.split( "." )
        fileName = fileName[0]
        
        # Creating the log file for the specific test
        now = time.localtime(time.time())
        tempFileName = time.strftime("%Y-%m-%d : %H-%M-%S -- ", now)

        tempFileName = tempFileName + fileName + ".py : Instance-" + `instance` + " -- PROCESSING.log" 
        logPath = os.path.join( self.__configMap[ "logPath" ], tempFileName )
            
        handler = logging.FileHandler( logPath )
        handler.setFormatter( logging.Formatter( '%(asctime)s - %(name)-16s - [%(levelname)s]: %(message)s' ) )
        
        handler.setLevel(logging.DEBUG)
        self.__log.addHandler( handler )
        
        # Saving handler object    
        self.__logHandler = handler

        # Remove the log handler from each of the lib/ classes
        for entry in self.__logObjectMap.keys():
            self.__logObjectMap[entry].addHandler( self.__logHandler )

        logObject = logging.getLogger( fileName + ".py" )
        self.BaseClassCheckStatus( logObject, "Log object not returned." )
        
        # Adding the new handler to the log object
        logObject.addHandler( handler )
        
        # Flushing the arguments for this test to the new log file
        commonMap = self.BaseClassMapLookUp( "configMap", "commonarguments" )
        testListMap = self.BaseClassMapLookUp( "configMap", "testList" )

        argsMap = {}
        
        self.__log.debug( "Arguments for test - " + fileName + ".py" )

       # Adding all the test specific arguments to the argsMap
        for entry in testListMap.keys():
            if( entry.__contains__( fileName ) == True ):
                argsMap = testListMap[ entry ]
        
        # Adding all the common arguments to the argsMap
        for entry in commonMap.keys():
            if( argsMap.__contains__( entry ) == True ):
                continue
            else:
                argsMap[ entry ] = commonMap[ entry ]

        # Logging all the arguments for the test
        for key in argsMap.keys():
            self.__log.debug( key + " = " + str(argsMap[key]) )

        argsMap[ "logObject" ] = logObject
        argsMap[ "handler" ] = handler 
        return argsMap
                
# This is the public method for the __getLogObect method      
    def BaseClassGetLogObject(self, fileName = None, instance = None ):
        self.__log.debug( "BaseClass.BaseClassGetLogObject() method called." )
        
        # If instance not provided, default to 1
        if( instance == None ):
            instance = 1
            
        if( fileName == None ):
            self.BaseClassCheckStatus(False, "\"fileName\" parameter provided was invalid.")

        return self.__getLogObject(fileName, instance)
    
# This method checks whether for a certain command, all the appropriate arguments are provided
    def __checkArguments( self, argsMap = None ):
        self.__log.debug( "BaseClass.__checkArguments() method called." )
        # Defining the reqArgsList
        if( argsMap.__contains__("reqArgsList") == True ):
            reqArgsList = argsMap[ "reqArgsList" ]
        else:
            self.BaseClassCheckStatus(False, "\"reqArgsList\" parameter not provided.")

        # Defining the argsMap
        if( argsMap.__contains__("argsMap") == True ):
            argsMap = argsMap[ "argsMap" ]
        else:
            self.BaseClassCheckStatus(False, "\"argsMap\" parameter not provided.")

        # Check if each entry in the reqArgsList exists in the argsMap. - reqArgsList[0] defines the command name
        for counter in range(1, len(reqArgsList) ):
            if( argsMap.__contains__( reqArgsList[counter] ) != True ):
                self.BaseClassCheckStatus(False, "Command " + reqArgsList[0] + " Failed - Argument " + reqArgsList[counter] + " not provided.")

        return True
    
# This is the interface for the __checkArguments method    
    def BaseClassCheckArguments(self, argsMap = None ):
        self.__log.debug( "BaseClass.BaseClassCheckArguments() method called." )
        if( argsMap == None ):
            self.BaseClassCheckStatus(False, "\"argsMap\" not provided.")
        
        return self.__checkArguments( argsMap )

# On a posix machine, unmounts and then mounts the iSCSI device moint point
    def __mountUnmount(self, mountPoint = None):
        self.__log.debug( "BaseClass.__mountUnmount() method called." )
        
        # Check parameters
        if( mountPoint == None ):
            self.BaseClassCheckStatus(False, "\"mountPoint\" not provided.")
                            
        # Step (a) - Obtain the current device - awk '$2 ~ /\/mnt\/cleversafe/ {print $1}' < /proc/mounts
        self.__log.info( "Step (a) - Obtain the current device" )
        commandToExecute = "awk '$2 ~ /" + string.replace( mountPoint, '/', "\/" ) + "/ {print $1}' < /proc/mounts "
        try:
            returnList = commands.getstatusoutput( commandToExecute  )
            if( returnList[0] != 0 ):
                self.CheckStatus( False, "Test failed - awk return code: " + `returnList[0]` )
        except OSError, exception:
            self.BaseClassCheckStatus( False, "Test failed - " + exception )
        
        device = returnList[-1]
            
        # Step (b) - Unmount the slice server mount point - umount self.__argsMap[ "iSCSIdrive" ]
        self.__log.info( "Step (b) - Unmount the slice server mount point" )
        commandToExecute = "umount " + mountPoint
        try:
            returnList = commands.getstatusoutput( commandToExecute  )
            if( returnList[0] != 0 ):
                self.BaseClassCheckStatus( False, "Test failed - umount return code: " + `returnList[0]`  )
        except OSError, exception:
            self.BaseClassCheckStatus( False, "Test failed - " + exception )

        # Step (c) - Re-mount the slice server mount point - mount device mountPoint
        self.__log.info( "Step (c) - Re-mount the slice server mount point" )
        commandToExecute = "mount " + device + " " + mountPoint
        try:
            returnList = commands.getstatusoutput( commandToExecute  )
            if( returnList[0] != 0 ):
                self.BaseClassCheckStatus( False, "Test failed - umount return code: " + `returnList[0]`  )
        except OSError, exception:
            self.BaseClassCheckStatus( False, "Test failed - " + exception )

        return True

# The public interface for __mountUnmount    
    def BaseClassMountUnmount(self, mountPoint = None):
        self.__log.debug( "BaseClass.BaseClassMountUnmount() method called." )

        return self.__mountUnmount( mountPoint )
        