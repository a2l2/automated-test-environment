class Test1:
	def GetValue( self ):
		return "Woo hoo - 1 "

def Info():
	return "This is information about the test1"

def Main():
  	print "[INFO] : Processing starts now for test1"
	objTest = Test1()
	print "[INFO] : Object returned", objTest.GetValue()
	return True
