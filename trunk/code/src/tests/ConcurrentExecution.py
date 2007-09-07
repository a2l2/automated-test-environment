# Test Name: ConcurrentExecution.py 
#----------------------------------
# Mandatory parameters
# --------------------
# testToExecute        - Name of the user defined test
# instanceCount        - The number of instances of the test

# Optional Parameters
# -------------------
# testToExecutePath    - Path at which the test is located. ( Default - look up is done only in the current test directory - ATE_ROOT/code/src/tests )

import TestTemplate
from TestTemplate import *

class ConcurrentExecution( TestTemplate ):
# Class constructor
    def __init__(self, instance = 1):
        self.__instance = instance
        self.__log = self.GetLogObject( "ConcurrentExecution", instance )
        self.__log.debug( "ConcurrentExecution.__init__() method called." )
        self.__argsMap = {}
        return None

# The mandatory Info method
    def Info(self):
        self.__log.debug( "ConcurrentExecution.Info() method called" )
        self.__log.info( "This test forks \"n\" processes which in turn executes a user defined test." )
        return True

# The mandatory Main method
    def Main( self, argsMap = None ):
        self.__log.debug( "ConcurrentExecution.Main() method called" )          
        if( argsMap != None ):
            self.__argsMap = argsMap
        else:
            self.__argsMap = self.GetArguments( "ConcurrentExecution.py" )

        if( self.StartTest() == True ):
            self.__log.info("Test ConcurrentExecution.py completed successfully.")
            self.TestComplete( True )
        else:
            self.CheckStatus( False,"Test ConcurrentExecution.py failed." )

        return None

    def __childProcess( self, module = None, className = None, instanceCount = None ):
        self.__log.debug( "ConcurrentExecution.__childProcess() method called." )
        argsMap = {}
        
        if( module == None or className == None or instanceCount == None ):
            self.CheckStatus( False, "Test failed - Test execution failed - No module loaded OR class name or instance count provided." )
        
        # Instanciating the class and calling the Info method
        try:
            moduleObject = getattr( module, className )(instanceCount)
            returnValue = moduleObject.Info()
        except AttributeError, errorMessage:
            self.CheckStatus( False, "Test execution failed - Info() method not defined. - " + errorMessage )
        
        self.__log.info( "Calling Main() method for test - " +  className )
        # Filling all the generic arguments to the argument map and to the log file
        argsMap = self.__argsMap
        
        # Calling the Main() method 
        try:
            returnValue = moduleObject.Main( argsMap )
        except RuntimeError, errorMessage  :
            self.CheckStatus( False, "Test execution failed - Lookup on Main() method failed - " + errorMessage )

        # Since status code is not false, assuming test completed successfully
        self.TestComplete( True )

# Starting test execution
    def StartTest(self):
        instanceCount = 1
        pidGroup = {}
        pid = 0
        
        if( string.atoi(self.__argsMap["instanceCount"]) <= 0 ):
            self.CheckStatus( False, "Test failed - argument \"instanceCount\" is invalid." )
        
        
        testName = self.__argsMap["testToExecute"].split(".py")
        testName = testName[0]
        
        # Import test module, if in current sys.path
        try:
            module = __import__( testName )
        except ImportError, errorMessage:
            self.__log.debug( testName + " not present in current path scope - " + errorMessage )

            # Add testPath variable (if defined) to sys.path
            if( self.__argsMap.__contains__( "testToExecutePath" ) ):
                sys.path.append( self.__argsMap[ "testToExecutePath" ] )
            else:    
                self.CheckStatus( False, "Test failed - Could not find test: " + testName + " in current scope." )
                
            # Import test module, if in testToExecutePath scope
            try: 
                module = __import__( testName )
            except ImportError, errorMessage:
                self.CheckStatus( False, "Test failed - Could not import test: " + testName + " - " + errorMessage )

        # Defining argsMap for forked test
        argsMap = self.__argsMap
        
        # Starting to fork processes
        while (True):
            pid = os.fork()
            
            # Setting group id of forked process
            os.setpgid(pid, 0)
            pidGroup[instanceCount] = pid
            
            if( pid == 0):
                # Child process
                self.__childProcess(module, testName, instanceCount )
            else:
                # Parent process
                if( instanceCount != string.atoi(self.__argsMap["instanceCount"]) ):
                    # if threshold point not reached
                    instanceCount += 1
                    continue
                else:
                    # else if threshold reached
                    tuple = os.waitpid(pid, 0)
                    # if test failed
                    if( tuple[-1] != 0 ):
                        self.__log.log(45, "Test " + testName + " - instance count - " + `instanceCount` + " -- FAILED.\n")
                        return False
                    # else passed
                    else:
                        return True