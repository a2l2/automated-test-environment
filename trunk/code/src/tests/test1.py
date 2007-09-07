# Test Name - test1.py
#---------------------

import TestTemplate
from TestTemplate import *

class test1(TestTemplate):
    def __init__(self):
        self.__log = self.GetLogObject( "test1" )
        self.__log.debug( "test1.__init__() method called." )
    
    def Info( self ):
        self.__log.info( "test1.Info() - Tests whether the TestTemplate methods work." )
        return True

    def Main( self, argsMap = None ):
        self.__log.info( "test1.Main() method called." )
        
        # Check to see whether the GetArguments method works correctly
        self.__log.info( "Beginning test for method - GetArguments." )

        localArgsMap = {}
        localArgsMap = self.GetArguments( "test1.py" )
        if( len(argsMap) == len(localArgsMap) ):
            for entry in argsMap.keys():
                if( localArgsMap[entry] == argsMap[entry] ):
                    continue
                else:
                    self.CheckStatus( False, "Error at -", entry, " LocalArgsMap = ", localArgsMap[entry], ": ArgsMap = ", argsMap[entry] )

        self.__log.info( "Test successful for method - GetArguments." )
        
        
        # Check to see whether the ExecuteCommand method work correctly
        self.__log.info( "Beginning test for method - ExecuteCommand." )

        newArgsMap = {}
        newArgsMap[ "command" ] = "createTestBed"
        newArgsMap[ "fileCount" ] = "10"
        newArgsMap[ "maxFileSize" ] = "102400"
        newArgsMap[ "fileType" ] = "mixed"
        newArgsMap[ "testBedPath" ] = argsMap[ "testBedPath" ]

        testBedPath = self.ExecuteCommand( newArgsMap )
        self.__log.info( "Test successful for method - ExecuteCommand." )

        self.TestComplete( True )
