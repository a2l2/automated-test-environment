# This class automates the installation operations based off the users specifications - Posix specific
# ----------------------------------------------------------------------------------------------------
# Import of Python libraries
import struct
import logging
import os
import commands
import time
import string
import sys
import glob


# Import of all common user defined Python modules 
import common
from common import *

log = logging.getLogger( 'ATE.CommandConverter.AutomatedInstall' )

class AutomatedInstall:
    __borg = {}
    __instance = None
# Class constructor (a Borg)
    def __init__( self ):
        # Ensuring the __dict__ is the same for every instance / object
        self.__dict__ = self.__borg

        # If its the first instance of the class
        if( AutomatedInstall.__instance == None ):
            self.log = logging.getLogger( 'ATE.CommandConverter.AutomatedInstall' )
            AutomatedInstall.__instance = self
            self.commandMap = {}
            self.commandConverter = CommandConverter()
            self.__loadList()
            self.log.debug( "AutomatedInstall.__init__() method called." )


# Check status method
    def __checkStatus( self, status = None, errorMessage = None ):
        if( status != True ):
            self.log.error( errorMessage )
            sys.exit( -1 )
        
# Load commands to CommnadMap
    def __loadList( self ):
        self.log.debug( "AutomatedInstall.__loadList() method called." )
        self.commandMap[ "clientInstall" ] = ( "clientRPMPath", "clientRPMName", "username", "password", "vaultDescriptorPath", "vaultDescriptorName", "sliceServerPath", "sliceDirectoryName" )


# Check provided parameters for all commands
    def __checkParameters( self, argumentMap = None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__checkParameters() method called" )
        if( argumentMap == None ):
            self__checkStatus( False, "argumentMap is invalid." )
        
        for parameter in self.commandMap[ argumentMap[ "command" ] ]:
            if( argumentMap.__contains__( parameter ) != True ):
                self.__checkStatus( False, parameter + " not defined." )
        
        return True


# Delete and previous occurrence of a directory 
    def __deletePrevious( self, path = None, dirName = None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__deletePrevious() method called" )
        commandMap = {}
        commandMap[ "command" ] = "deleteDirectory"
        commandMap[ "directoryName" ] = dirName
        commandMap[ "path" ] = path
        if( self.commandConverter.CommandLookup( commandMap ) ):
            return True
        else:
            return False


# Creates the specified directory
    def __createDirectory( self, path = None, dirName = None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__createDirectory() method called" )

        if( os.path.exists( os.path.join( path, dirName ) ) ):
            status = self.__deletePrevious( path, dirName )
            self.__checkStatus( status, "Test failed - could not remove previously created directory " + dirName + " at " + path )
               
        commandMap = {}
        commandMap[ "command" ] = "createDirectory"
        commandMap[ "path" ] = path
        commandMap[ "directoryName" ] = dirName
        if( self.commandConverter.CommandLookup( commandMap ) ):
            return True
        else:
            return False


# This method calls the required os function based on the args list provided
    def __executeCommand( self, commandToExecute = None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__executeCommand() method called" )
        returnList = ""
        try:
            returnList = commands.getstatusoutput( commandToExecute  )
            if( returnList[0] != 0  and returnList[-1] != ""  ):
                self.__checkStatus( False, "Test failed - " + commandToExecute + " exection returned with code: " + `returnList[0]` + " " + `returnList[1]`)
        except OSError, exception:
            self.__checkStatus( False, "Test failed - " + commandToExecute + " exection failed.\n" + exception )
        
        return returnList


# This method removes all previous installations of the rpm
    def __removePreviousInstallation(self):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__removePreviousInstallation() method called" )

        # Removing the rpm
        self.log.debug( "Calling rpm -qa | grep dsgrid " )
        commandToExecute = "rpm -qa | grep dsgrid"
        
        returnList = self.__executeCommand( commandToExecute )

        if( returnList[-1] == "" ):
            self.log.info( "No previous revision of the dsgrid s/w exists." )
        else:
            self.log.info( "Removing previous revision of the dsgrid s/w exists." )
            commandToExecute = "rpm -e dsgrid"
            returnList = self.__executeCommand( commandToExecute )
            if( returnList[-1] == "" ):
                self.log.info( "Previous revision of the dsgrid s/w removed successfully." )
            
        # Removing the /etc/dsgrid/ directory
        self.log.debug( "Calling rm -rf /etc/dsgrid " )
        commandToExecute = "rm -rf /etc/dsgrid"
 
        returnList = self.__executeCommand( commandToExecute )

        if( returnList[-1] == "" ):
            self.log.info( "/etc/dsgrid/ directory removed successfully." )

        # Removing the /var/dsgrid/ directory
        self.log.debug( "Calling rm -rf /var/dsgrid " )
        commandToExecute = "rm -rf /var/dsgrid"
        
        returnList = self.__executeCommand( commandToExecute )

        if( returnList[-1] == "" ):
            self.log.info( "/var/dsgrid/ directory removed successfully." )

        return True
        
        
# This method installs the rpm
    def __installRPM( self, rpmPath = None, rpmName= None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__installRPM() method called" )
        
        if( os.path.exists( os.path.join(rpmPath, rpmName) ) ):
            RPM = os.path.join(rpmPath, rpmName)
        else:
            self.__checkStatus( False, os.path.join(rpmPath, rpmName) + " doesn't exist." )
            
        # Installing the rpm
        self.log.debug( "Calling rpm -ivh " +  RPM )
        commandToExecute = "rpm --quiet -i " +  RPM
        
        returnList = self.__executeCommand( commandToExecute )

        if( returnList[-1] == "" ):
            self.log.info( "RPM installed successfully." )
        
        return True
    
    
# This method start all client operations
    def __clientOperations(self, username = None, password = None, vaultDescriptorPath = None, vaultDescriptorName = None, sliceServerPath = None, sliceDirectoryName = None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__clientOperations() method called" )
        
        # I. Restart the iscsi initiator
        self.log.info( "Calling /etc/init.d/iscsid restart" )
        commandToExecute = "/etc/init.d/iscsid start"
        
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[0] == 0 ):
            self.log.info( "iSCSI initiator restarted successfully." )

        
        # II. Creating an account
        self.log.info( "Calling dsgrid-create-account --username=" + username + " --password=" + password )
        commandToExecute = "dsgrid-create-account --username=" + username + " --password=" + password
        
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[-1] == "" ):
            self.log.info( "Account created successfully." )

        # III. Creating a vault
        if( os.path.exists( os.path.join(vaultDescriptorPath, vaultDescriptorName) ) != True ):
            self.__checkStatus( False, os.path.join(vaultDescriptorPath, vaultDescriptorName) + " doesn't exist." )
        
        self.log.info( "Calling dsgrid-create-vault --username=" + username + " --password=" + password + " --descriptor=" + os.path.join(vaultDescriptorPath, vaultDescriptorName) )
        commandToExecute = "dsgrid-create-vault --username=" + username + " --password=" + password + " --descriptor=" + os.path.join(vaultDescriptorPath, vaultDescriptorName)
        
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[0] == 0 ):
            self.log.info( "Vault created successfully." )
                    
        # IV. Setting the UUID variables
        self.log.debug( "Calling ls /etc/dsgrid/accounts/*.jks | cut -d/ -f5 | cut -d. -f1")
        commandToExecute = "ls /etc/dsgrid/accounts/*.jks | cut -d/ -f5 | cut -d. -f1"
        
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[-1] != "" ):
            AccountUUID = returnList[-1]
            self.log.info( "AccountUUID successfully found." )

        self.log.debug( "Calling ls /etc/dsgrid/vaults/*.xml | cut -d/ -f5 | cut -d. -f1")
        commandToExecute = "ls /etc/dsgrid/vaults/*.xml | cut -d/ -f5 | cut -d. -f1"
        
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[-1] != "" ):
            VaultUUID = returnList[-1]
            self.log.info( "VaultUUID successfully found." )

        self.log.debug( "AccountUUID: " + AccountUUID )
        self.log.debug( "VaultUUID: " + VaultUUID )

        # Modifying the /etc/dsgrid/dsgrid-iscsi.conf file
        file = open('/etc/dsgrid/dsgrid-iscsi.conf', 'r' )
        buffer = ""
        target_domain_name = ""
        
        for line in file.readlines():
            parts = line.split(" " )
            
            for counter in range ( 0, 3  ):
                if( parts[ 0 ] == "account" or parts[ 0 ] == "#account" ):
                    if( parts[-2] == "=" ): 
                        line = "account = " + AccountUUID + "\n"
                    
                elif( parts[ 0 ] == "vault" or parts[ 0 ] == "#vault" ):
                    if( parts[-2] == "=" ):
                        line = "vault = " + VaultUUID + "\n"

                elif( parts[ 0 ] == "target_domain_name" ):
                    if( parts[-2] == "=" ):
                        target_domain_name = parts[-1]

                elif( parts[ 0 ] == "target_domain_ownership_date" ):
                    if( parts[-2] == "=" ):
                        target_domain_ownership_date = parts[-1]
                    

            buffer += line       

        file.close()
        
	
        file = open('/etc/dsgrid/dsgrid-iscsi.conf', 'w' )
        file.write( buffer )
        file.close()

        self.log.info( "/etc/dsgrid/dsgrid-iscsi.conf modified successfully" )

        temp = target_domain_ownership_date.split("\n")
        target_domain_ownership_date = temp[ 0 ]
	
        temp = target_domain_name.split("\n")
        target_domain_name = temp[ 0 ]

        self.log.debug( "target_domain_ownership_date: " + target_domain_ownership_date )
        self.log.debug( "target_domain_name: " +  target_domain_name )
	
       
        # V. Starting the iscsi target
        self.log.info( "Calling /etc/init.d/dsgrid-iscsi restart" )
        commandToExecute = "/etc/init.d/dsgrid-iscsi restart"
        
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[0] == 0 ):
            self.log.info( "dsgrid iSCSI target restarted successfully." )

	    # VI. Calling the target discovery phase
        self.log.info( "Going to sleep for 10 seconds so that the target can come alive successfully" )
        time.sleep(10)
        self.log.info( "Calling iscsiadm -m discovery -t sendtargets -p 127.0.0.1" )
        commandToExecute = "iscsiadm -m discovery -t sendtargets -p 127.0.0.1"

        returnList = self.__executeCommand( commandToExecute )
        if( returnList[-1] != "" ):
            self.log.info( "dsgrid iSCSI target discovered  successfully." )
        self.log.debug( returnList[-1] )

        # VII. Loging in to the iSCSI target
        targetName = ""
        targetName = "iqn." + target_domain_ownership_date + "." + target_domain_name + ":vault-uuid-" +  VaultUUID
        self.log.info( "Calling iscsiadm --mode node --targetname " + targetName +" --portal 127.0.0.1 --login")
        commandToExecute = "iscsiadm --mode node --targetname " + targetName +" --portal 127.0.0.1 --login"
 
        returnList = self.__executeCommand( commandToExecute )
        if( returnList[0] == 0 ):
            self.log.info( "Login successful." )

        # VIII. Performing an fdisk on the new partition
        self.log.info( "Going to sleep for 10 seconds so that the device table can get updated successfully" )
        time.sleep(10)
        list = glob.glob( '/dev/sd[a-z]' )
        sys.stdin.flush()
        input = raw_input( "Fdisk will partition the device " + list[ 0 ] + ". Continue(y/n)" )
        if( input.lower() != 'y' ):
            self.__checkStatus( False, "User terminated test execution. Fdisk will not be performed." )
		
        self.log.info( "Proceeding to partition device" + list[0] )
        self.log.info( "Calling fdisk " + list[ 0 ])
        commandToExecute = "fdisk " + list[ 0 ]
        try:
            os.system( commandToExecute )
        except OSError, exception:
            self.__checkStatus( False, "Test failed - " + commandToExecute + " exection failed.\n" + exception )

        self.log.info( "Fdisk operation successful." )

        # IX. Formatting the new partition
        self.log.info( "Going to sleep for 10 seconds so that the device table can get updated successfully" )
        time.sleep(10)
        list = glob.glob( '/dev/sd[a-z][0-7]' )
        sys.stdin.flush()
        input = raw_input( "mke2fs will format the device " + list[ 0 ] + ". Continue(y/n)" )
        if( input.lower() != 'y' ):
            self.__checkStatus( False, "User terminated test execution. mke2fs will not be performed." )

        self.log.info( "Proceeding to format device.")
        self.log.info( "Calling mke2fs " + list[ 0 ])
        commandToExecute = "mke2fs " + list[ 0 ]

        returnList = self.__executeCommand( commandToExecute )
        if( returnList[0] == 0 ):
            self.log.info( "Device formatted successfully." )

        # X. Mounting the new partiotion
        # Check to see if defined mount mount already exists in /proc/mounts
        commandToExecute = "awk '$2 ~ /" + string.replace( os.path.join( sliceServerPath, sliceDirectoryName ), '/', "\/" ) + "/ {print $1}' < /proc/mounts "
        try:
            returnList = self.__executeCommand( commandToExecute )
            if( returnList[0] != 0 ):
                self.__checkStatus( False, "Test failed - awk return code: " + `returnList[0]` )
        except OSError, exception:
                self.__checkStatus( False, "Test failed - " + exception )
        
        if( returnList[-1] != "" ):
            self.log.info( "Mount point " + returnList[-1] + " previously mounted." )
            sys.stdin.flush()
            input = raw_input( "Do you want to umount this mount point " + returnList[-1] + " (y/n)? " )
            if( input.lower() != 'y' ):
                self.__checkStatus( False, "User terminated test execution. Mount point " + returnList[-1] + " already in use." )
            
            commandToExecute = "umount " + returnList[-1]
            returnList = self.__executeCommand( commandToExecute )
            if( returnList[0] == 0 ):
                self.log.info( "Umount completed successfully." )
        
        list = glob.glob( '/dev/sd[a-z][0-7]' )
        self.log.info( "Calling mount " + list[ 0 ] + " " + os.path.join( sliceServerPath, sliceDirectoryName ) )
        commandToExecute = "mount " + list[ 0 ] + " " + os.path.join( sliceServerPath, sliceDirectoryName )

        returnList = self.__executeCommand( commandToExecute )
        if( returnList[0] == 0 ):
            self.log.info( "Slice server mounted successfully." )

        return True
        
# This method facilitates the client install and login process
    def clientInstall( self, argumentMap = None ):
        self.log.debug( "AutomatedInstall: AutomatedInstall.__clientInstall() method called" )
        self.__checkStatus( self.__checkParameters( argumentMap ), "Required arguments not provided." )
        
        # Phase I - rpm install
        self.__checkStatus(self.__removePreviousInstallation(), "Could not remove previous installation" )
        
        # Phase II - install client rpm
        self.__checkStatus(self.__installRPM( argumentMap[ "clientRPMPath" ], argumentMap[ "clientRPMName" ] ), "Could not install software" )
        
        # Phase III - Start client operations
        self.__checkStatus(self.__clientOperations( argumentMap[ "username" ], argumentMap[ "password" ], argumentMap[ "vaultDescriptorPath" ], argumentMap[ "vaultDescriptorName" ], argumentMap[ "sliceServerPath" ], argumentMap[ "sliceDirectoryName" ] ), "Could perform all client operations." )
       
        return True 


# Returns to the caller the commandMap
    def GetCommandMap( self ):
        self.log.debug( "AutomatedInstall.GetCommandMap() method called" )
        return self.commandMap

# REPLACE SOON - Returns to the caller the logObject
    def GetLogObject( self ):
        self.log.debug( "AutomatedInstall.GetLogObject() method called" )
        return self.log


# The GetObject method
def GetObject():
    log.debug( "AutomatedInstall.py - GetObject() method called" )          
    moduleObject = AutomatedInstall()
    return moduleObject

# The GetObject method
def GetLogObject():
    log.debug( "AutomatedInstall.py - GetLogObject method called" )          
    moduleObject = AutomatedInstall()
    return moduleObject.GetLogObject()
