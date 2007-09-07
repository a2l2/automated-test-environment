# This is the library template that must be inherited by each library
import common.BaseClass
from common.BaseClass import *

class LibraryTemplate( BaseClass ):
# This method defines the private member variables whenever they are needed 
    def __securityChecker( object = None ):
        if( object.lower() == "log" ):
            return logging.getLogger( 'LibraryTemplate' )
        else:
            self.__checkStatus(False, "Security violation - Invalid object provided.")
    
# Private Member Variables    
    __log = __securityChecker( "log" )

